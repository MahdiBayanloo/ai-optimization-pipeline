# Transformation Playbook

## Step 1 — Identify the blocking call
Find the exact CycloneTCP function causing the block.
For TLS: httpServerEstablishSecureConnection → calls tlsConnect() internally.

## Step 2 — Create the Adapter class
File: ConnectionHelper_Adapter.h
Class: TlsHandshakeAdapter
Methods: start(HttpConnection*), progress() -> HandshakeStatus, setOnComplete(callback)

## Step 3 — Extend the state machine
Add to HttpConnState:
  HTTP_CONNECTION_STATE_TLS_STARTING
  HTTP_CONNECTION_STATE_TLS_IN_PROGRESS  
  HTTP_CONNECTION_STATE_TLS_COMPLETE

## Step 4 — Wire into event loop
In the activity that handles HTTP connections:
- On new connection: call adapter.start(), set state to TLS_STARTING, return
- On each tick: call adapter.progress(), if DONE fire onComplete event, return

## Step 5 — Validate
- Ticks must continue printing while TLS is in progress
- No tick gaps > 1 event loop cycle during handshake
- TLS must still complete successfully end-to-end
