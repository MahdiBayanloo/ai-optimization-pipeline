```json
{
  "target_function": "httpServerEstablishSecureConnection",
  "blocking_type": "TLS handshake",
  "patterns_to_apply": ["State Machine", "Adapter Layer", "Callback Wrapper"],
  "new_classes_needed": [
    "TlsHandshakeAdapter: Wraps CycloneTCP TLS handshake behind non-blocking start/progress/onComplete interface",
    "TlsHandshakeStatus: Enum representing IN_PROGRESS, DONE, ERROR states for handshake progress"
  ],
  "state_additions": [
    "HTTP_CONNECTION_STATE_TLS_STARTING: Initial state when TLS handshake begins, adapter.start() called",
    "HTTP_CONNECTION_STATE_TLS_IN_PROGRESS: Handshake ongoing, adapter.progress() called each tick",
    "HTTP_CONNECTION_STATE_TLS_COMPLETE: Handshake finished successfully, ready for HTTP traffic",
    "HTTP_CONNECTION_STATE_TLS_ERROR: Handshake failed, connection should be closed"
  ],
  "transformation_steps": [
    "Create TlsHandshakeStatus enum with values: IN_PROGRESS, DONE, ERROR in new header TlsHandshakeAdapter.h",
    "Create TlsHandshakeAdapter class with member variables to store HttpConnection*, TlsContext*, current sub-state, and error_t result",
    "Implement TlsHandshakeAdapter::start(HttpConnection*) that initializes TLS context via existing httpServerOpenSecureConnection and returns immediately",
    "Implement TlsHandshakeAdapter::progress() that calls tlsConnect() in non-blocking mode or advances internal sub-state, returns TlsHandshakeStatus",
    "Implement TlsHandshakeAdapter::setOnComplete(callback) to register completion callback for event channel delivery",
    "Implement TlsHandshakeAdapter::getError() to retrieve error_t when status is ERROR",
    "Extend HttpConnState enum in CycloneTCP http_server.h wrapper or local extension with new TLS states",
    "Modify httpServerEstablishSecureConnection to become a facade that creates/returns TlsHandshakeAdapter instance instead of blocking",
    "Create new non-blocking entry point httpServerEstablishSecureConnectionAsync that returns adapter pointer",
    "In HTTP connection Activity handler: on new secure connection, call adapter.start(), set state to TLS_STARTING, return immediately",
    "In HTTP connection Activity tick handler: check if state is TLS_IN_PROGRESS, call adapter.progress(), handle status transitions",
    "On adapter returning DONE: set state to TLS_COMPLETE, fire onComplete callback via seve event channel",
    "On adapter returning ERROR: set state to TLS_ERROR, propagate error via event channel, close connection",
    "Store TlsHandshakeAdapter instance pointer in HttpConnection user data or dedicated member to persist across ticks"
  ],
  "risk_notes": [
    "CycloneTCP tlsConnect() may not natively support non-blocking mode - verify TLS_FLAG_NON_BLOCKING_SOCKET behavior",
    "TLS sub-state machine within adapter must handle partial reads/writes and WANT_READ/WANT_WRITE conditions",
    "Memory ownership of TlsHandshakeAdapter instance must be clear - suggest connection owns adapter lifetime",
    "Existing code paths calling httpServerEstablishSecureConnection synchronously must be audited and migrated",
    "Certificate verification callback httpServerUserCertificateCallback may also block - verify it completes quickly",
    "Socket must be set to non-blocking mode before TLS handshake starts",
    "Error propagation must preserve original CycloneTCP error_t codes for debugging",
    "Timeout handling via httpServerCheckTimeout must still work across multiple ticks"
  ]
}
```