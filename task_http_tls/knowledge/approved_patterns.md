# Approved Transformation Patterns

## Pattern 1: State Machine
- Add states to existing HttpConnState enum
- Each state does ONE small unit of work and returns
- Next tick: check state, advance, return again
- Example states: TLS_INIT, TLS_CLIENT_HELLO, TLS_WAITING, TLS_KEY_EXCHANGE, TLS_DONE

## Pattern 2: Adapter Layer
- Create class TlsHandshakeAdapter
- Public interface: start(connection), progress() -> Status, onComplete(callback)
- Internally calls CycloneTCP — hidden behind this boundary
- seve code never calls CycloneTCP directly

## Pattern 3: Callback Wrapper
- start() kicks off the operation and returns immediately
- progress() called each event loop tick — does one small step
- Returns: IN_PROGRESS, DONE, or ERROR
- onDone callback fires when complete, delivers result via event channel
