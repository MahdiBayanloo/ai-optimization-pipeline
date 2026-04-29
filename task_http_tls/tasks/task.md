# Task: De-block httpServerEstablishSecureConnection

## Target File
libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h

## Target Function
httpServerEstablishSecureConnection(HttpConnection *connection)

## Problem
This function performs a full synchronous TLS handshake via CycloneTCP.
It blocks the Reflex/seve cooperative event loop for the entire handshake duration
(multiple network round-trips + crypto operations).

## Required Transformation
Apply the 3-pattern hybrid:
1. State Machine — decompose handshake into discrete states that yield control
2. Adapter Layer — wrap CycloneTCP behind a non-blocking interface  
3. Callback Wrapper — turn the blocking call into start() + progress() + done()

## Constraints
- Minimal changes to CycloneTCP internals (vendor code)
- Must be compatible with seve::eventflow activity model
- Existing HttpConnState infrastructure should be reused
