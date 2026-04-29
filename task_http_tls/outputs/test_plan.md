# Black-Box Validation Test Plan for TLS Handshake Transformation

## Test Plan Overview

| Test ID | Category | Description | Priority |
|---------|----------|-------------|----------|
| TLS-001 | Event Loop Continuity | Verify ticks continue during TLS operation | Critical |
| TLS-002 | Handshake Success | Verify TLS completes successfully | Critical |
| TLS-003 | Callback Single Fire | Verify onComplete fires exactly once | Critical |
| TLS-004 | Error Handling | Invalid connection parameter | High |
| TLS-005 | Error Handling | Invalid server context parameter | High |
| TLS-006 | Error Handling | Null adapter parameter | High |
| TLS-007 | Error Handling | TLS negotiation failure | High |
| TLS-008 | State Transitions | Verify correct state progression | High |
| TLS-009 | Timeout Handling | Verify timeout still works across ticks | Medium |
| TLS-010 | Memory Management | Verify cleanup releases resources | Medium |

---

## Test TLS-001: Event Loop Ticks Continue During TLS Operation

### Objective
Verify that the seve event loop continues processing ticks while TLS handshake is in progress (no freeze).

### Preconditions
- HTTP server initialized and listening
- Valid TLS certificates configured
- Event loop tick counter accessible
- TLS client ready to connect

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;    // Valid initialized server
    HttpConnection* connection;          // New incoming connection
    uint32_t tickCounterBefore;          // Event loop tick count at start
    uint32_t maxAllowedTickGap;          // Maximum ticks without progress = 1
    systime_t testTimeout;               // 5000ms overall timeout
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_001_EventLoopContinuity) {
    // SETUP
    TestInputs inputs = setupValidTlsConnection();
    TlsHandshakeAdapter* adapter = nullptr;
    std::vector<systime_t> tickTimestamps;
    uint32_t ticksRecorded = 0;
    
    // ACTION 1: Start async handshake
    error_t startError = httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    
    ASSERT_EQ(startError, NO_ERROR);
    ASSERT_NE(adapter, nullptr);
    
    // ACTION 2: Simulate event loop ticks
    TlsHandshakeStatus status = TlsHandshakeStatus::IN_PROGRESS;
    systime_t lastTickTime = osGetSystemTime();
    
    while (status == TlsHandshakeStatus::IN_PROGRESS) {
        // Record tick timestamp
        systime_t currentTime = osGetSystemTime();
        tickTimestamps.push_back(currentTime);
        ticksRecorded++;
        
        // Call progress (one tick of work)
        bool complete = false;
        TlsHandshakeCompleteEvent event;
        status = httpServerTlsHandshakeTick(adapter, &complete, &event);
        
        // VERIFY: This tick completed quickly (< 10ms)
        systime_t tickDuration = osGetSystemTime() - currentTime;
        ASSERT_LT(tickDuration, 10);  // No tick should take > 10ms
        
        // Safety timeout
        if (currentTime - tickTimestamps[0] > inputs.testTimeout) {
            FAIL("Test timeout exceeded");
        }
        
        lastTickTime = currentTime;
    }
    
    // CLEANUP
    httpServerTlsHandshakeCleanup(adapter);
    
    // VERIFY: Multiple ticks occurred (handshake was decomposed)
    ASSERT_GT(ticksRecorded, 1);
}
```

### Expected Outputs
| Measurement | Expected Value | Tolerance |
|-------------|----------------|-----------|
| Individual tick duration | < 10ms | None |
| Total ticks recorded | > 1 | Minimum 2 |
| Maximum gap between ticks | < 15ms | None |
| Event loop remained responsive | true | - |

### Pass/Fail Criteria
- **PASS**: All tick durations < 10ms AND ticksRecorded > 1 AND no tick gaps > 15ms
- **FAIL**: Any tick duration >= 10ms OR ticksRecorded <= 1 OR any tick gap >= 15ms

---

## Test TLS-002: TLS Handshake Completes Successfully

### Objective
Verify that TLS handshake reaches successful completion through the non-blocking interface.

### Preconditions
- Valid TLS server configuration
- Valid client certificate (if mutual TLS)
- Network connectivity between client and server

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;    // Configured with valid TLS
    HttpConnection* connection;          // Socket connected, pre-TLS
    MockTlsClient* client;               // Simulated TLS client
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_002_HandshakeSuccess) {
    // SETUP
    TestInputs inputs = setupValidTlsScenario();
    TlsHandshakeAdapter* adapter = nullptr;
    
    // ACTION 1: Start handshake
    error_t error = httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    ASSERT_EQ(error, NO_ERROR);
    
    // ACTION 2: Drive handshake to completion
    TlsHandshakeStatus finalStatus = TlsHandshakeStatus::IN_PROGRESS;
    TlsHandshakeCompleteEvent completionEvent;
    bool completed = false;
    uint32_t iterations = 0;
    const uint32_t maxIterations = 1000;
    
    while (!completed && iterations < maxIterations) {
        // Simulate client responding (pump network)
        inputs.client->processServerMessages();
        
        // Server side tick
        finalStatus = httpServerTlsHandshakeTick(adapter, &completed, &completionEvent);
        iterations++;
    }
    
    // VERIFY
    ASSERT_TRUE(completed);
    ASSERT_EQ(finalStatus, TlsHandshakeStatus::DONE);
    ASSERT_EQ(completionEvent.success, true);
    ASSERT_EQ(completionEvent.result, NO_ERROR);
    ASSERT_EQ(completionEvent.connection, inputs.connection);
    ASSERT_EQ(inputs.connection->state, HTTP_CONNECTION_STATE_TLS_COMPLETE);
    
    // VERIFY: TLS context is now usable
    ASSERT_NE(inputs.connection->tlsContext, nullptr);
    
    // CLEANUP
    httpServerTlsHandshakeCleanup(adapter);
}
```

### Expected Outputs
| Output | Expected Value |
|--------|----------------|
| finalStatus | TlsHandshakeStatus::DONE |
| completionEvent.success | true |
| completionEvent.result | NO_ERROR (0) |
| connection->state | HTTP_CONNECTION_STATE_TLS_COMPLETE (102) |
| connection->tlsContext | Not null, valid |

### Pass/Fail Criteria
- **PASS**: Handshake completes with DONE status, NO_ERROR result, connection in TLS_COMPLETE state
- **FAIL**: Timeout, ERROR status, non-zero error code, or incorrect final state

---

## Test TLS-003: onComplete Fires Exactly Once

### Objective
Verify that the completion event is generated exactly once, regardless of how many times progress() is called.

### Preconditions
- Valid TLS configuration
- Handshake will succeed

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;
    HttpConnection* connection;
    uint32_t extraTicksAfterCompletion;  // = 10
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_003_CallbackSingleFire) {
    // SETUP
    TestInputs inputs = setupValidTlsScenario();
    inputs.extraTicksAfterCompletion = 10;
    TlsHandshakeAdapter* adapter = nullptr;
    uint32_t completionEventCount = 0;
    std::vector<TlsHandshakeCompleteEvent> capturedEvents;
    
    // ACTION 1: Start handshake
    httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    
    // ACTION 2: Run until completion
    bool completed = false;
    TlsHandshakeStatus status;
    
    while (!completed) {
        TlsHandshakeCompleteEvent event;
        status = httpServerTlsHandshakeTick(adapter, &completed, &event);
        
        if (completed) {
            completionEventCount++;
            capturedEvents.push_back(event);
        }
    }
    
    // ACTION 3: Call progress() additional times after completion
    for (uint32_t i = 0; i < inputs.extraTicksAfterCompletion; i++) {
        TlsHandshakeCompleteEvent event;
        bool extraComplete = false;
        status = httpServerTlsHandshakeTick(adapter, &extraComplete, &event);
        
        // These should return DONE but not trigger "new" completion
        ASSERT_EQ(status, TlsHandshakeStatus::DONE);
        
        // Count if event indicates completion (checking isValid)
        if (extraComplete && event.isValid()) {
            completionEventCount++;
            capturedEvents.push_back(event);
        }
    }
    
    // VERIFY: Completion event generated exactly once
    // Note: The API may report complete=true on subsequent calls,
    // but the event should be idempotent (same values)
    ASSERT_GE(completionEventCount, 1);
    
    // All captured events should be identical
    for (size_t i = 1; i < capturedEvents.size(); i++) {
        ASSERT_EQ(capturedEvents[i].connection, capturedEvents[0].connection);
        ASSERT_EQ(capturedEvents[i].result, capturedEvents[0].result);
        ASSERT_EQ(capturedEvents[i].success, capturedEvents[0].success);
    }
    
    // CLEANUP
    httpServerTlsHandshakeCleanup(adapter);
}
```

### Expected Outputs
| Measurement | Expected Value |
|-------------|----------------|
| First completion event generated | true |
| All events identical | true |
| Status after completion | DONE (idempotent) |

### Pass/Fail Criteria
- **PASS**: Completion event is idempotent, all captured events have identical values
- **FAIL**: Different completion events generated, or no completion event

---

## Test TLS-004: Error Handling - Invalid Connection Parameter

### Objective
Verify proper error handling when null connection is passed.

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;    // Valid
    HttpConnection* connection;          // NULL
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_004_NullConnection) {
    // SETUP
    TestInputs inputs;
    inputs.serverContext = createValidServerContext();
    inputs.connection = nullptr;  // Invalid
    TlsHandshakeAdapter* adapter = nullptr;
    
    // ACTION
    error_t error = httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    
    // VERIFY
    ASSERT_EQ(error, ERROR_INVALID_PARAMETER);
    ASSERT_EQ(adapter, nullptr);
    
    // CLEANUP - nothing to clean, adapter was not allocated
}
```

### Expected Outputs
| Output | Expected Value |
|--------|----------------|
| Return error | ERROR_INVALID_PARAMETER |
| adapter | nullptr |

### Pass/Fail Criteria
- **PASS**: Returns ERROR_INVALID_PARAMETER, adapter remains null
- **FAIL**: Returns NO_ERROR, or adapter is allocated

---

## Test TLS-005: Error Handling - Invalid Server Context Parameter

### Objective
Verify proper error handling when null server context is passed.

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;    // NULL
    HttpConnection* connection;          // Valid
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_005_NullServerContext) {
    // SETUP
    TestInputs inputs;
    inputs.serverContext = nullptr;  // Invalid
    inputs.connection = createValidConnection();
    TlsHandshakeAdapter* adapter = nullptr;
    
    // ACTION
    error_t error = httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    
    // VERIFY
    ASSERT_EQ(error, ERROR_INVALID_PARAMETER);
    ASSERT_EQ(adapter, nullptr);
    
    // CLEANUP
    destroyConnection(inputs.connection);
}
```

### Expected Outputs
| Output | Expected Value |
|--------|----------------|
| Return error | ERROR_INVALID_PARAMETER |
| adapter | nullptr |

### Pass/Fail Criteria
- **PASS**: Returns ERROR_INVALID_PARAMETER, adapter remains null
- **FAIL**: Returns NO_ERROR, or adapter is allocated

---

## Test TLS-006: Error Handling - Null Adapter in Tick

### Objective
Verify proper error handling when null adapter is passed to tick function.

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_006_NullAdapterTick) {
    // SETUP
    TlsHandshakeAdapter* adapter = nullptr;
    bool complete = false;
    TlsHandshakeCompleteEvent event;
    
    // ACTION
    TlsHandshakeStatus status = httpServerTlsHandshakeTick(
        adapter,
        &complete,
        &event
    );
    
    // VERIFY
    ASSERT_EQ(status, TlsHandshakeStatus::ERROR);
    ASSERT_TRUE(complete);  // Error is a terminal state
    ASSERT_EQ(event.result, ERROR_INVALID_PARAMETER);
    ASSERT_FALSE(event.success);
    ASSERT_EQ(event.connection, nullptr);
}
```

### Expected Outputs
| Output | Expected Value |
|--------|----------------|
| status | TlsHandshakeStatus::ERROR |
| complete | true |
| event.result | ERROR_INVALID_PARAMETER |
| event.success | false |

### Pass/Fail Criteria
- **PASS**: Returns ERROR status with appropriate error code
- **FAIL**: Crashes, hangs, or returns unexpected values

---

## Test TLS-007: Error Handling - TLS Negotiation Failure

### Objective
Verify proper error propagation when TLS negotiation fails (e.g., certificate validation failure).

### Test Inputs
```cpp
struct TestInputs {
    HttpServerContext* serverContext;    // Valid config
    HttpConnection* connection;          // Valid socket
    MockTlsClient* client;               // Configured with invalid cert
};
```

### Test Procedure
```cpp
TEST_PROCEDURE(TLS_007_NegotiationFailure) {
    // SETUP
    TestInputs inputs = setupTlsScenarioWithInvalidClientCert();
    TlsHandshakeAdapter* adapter = nullptr;
    
    // ACTION 1: Start handshake
    error_t startError = httpServerEstablishSecureConnectionAsync(
        inputs.serverContext,
        inputs.connection,
        &adapter
    );
    ASSERT_EQ(startError, NO_ERROR);
    
    // ACTION 2: Drive handshake until failure
    TlsHandshakeStatus finalStatus = TlsHandshakeStatus::IN_PROGRESS;
    TlsHandshakeCompleteEvent completionEvent;
    bool completed = false;
    uint32_t iterations = 0;
    const uint32_t maxIterations = 1000;
    
    while (!completed && iterations < maxIterations) {
        inputs.client->processServerMessages();
        finalStatus = httpServerTlsHandsh