# System Summary — periCORE-SDK / Reflex (seve)

## Architecture
- Cooperative event-based OS called seve (the Reflex implementation)
- Activities run to completion — NO blocking allowed, ever
- Single stack shared across all activities
- Event channels (seve::eventflow::Queue, Sink) connect components
- Schedulers: FIFO (default), Fixed Priority, EDF — all in seve/scheduling/

## The Vendor Library
- CycloneTCP / CycloneSSL by Oryx Embedded
- Purchased — minimal changes allowed to preserve vendor support
- Currently integrated via synchronous blocking calls
- Key blocking entry points: httpServerEstablishSecureConnection, mqttClientStateConnect

## The Problem
TLS handshake and crypto operations in CycloneTCP block the seve event loop.
This violates the cooperative model and freezes the system for 200-500ms.

## Approved Solution Patterns
1. State Machine — decompose long operations into discrete yield points
2. Adapter Layer — boundary between seve and CycloneTCP
3. Callback Wrapper — start() / progress() / onDone() interface
