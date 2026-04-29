# System Summary — periCORE-SDK (Perinet GmbH)

## Runtime model
- Event-driven, single-threaded, non-preemptive (Reflex OS)
- Run-to-completion handlers — no handler may block
- Cooperative scheduling — event loop is the only execution driver
- Target: ARM microcontrollers, cross-compiled with gcc-arm-none-eabi

## Codebase structure
- seve/         — Reflex runtime core
- libperiCORE/  — peripheral and protocol libraries
- applications/ — application-level components

## The problem
A purchased third-party TLS/networking stack was integrated via a single
interface call. During TLS handshake and crypto key generation this call
blocks the event loop for up to ~500ms, breaking scheduling and violating
the run-to-completion contract.

## Goal
Replace the blocking TLS integration with a non-blocking design using:
- State Machine (explicit handshake states)
- Adapter Layer (isolate vendor code behind a clean interface)
- Callback Wrapper (convert blocking call to start/progress/done)

## Hard constraints
- Minimal changes to the purchased TLS stack (vendor owns security patches)
- No threads introduced
- No busy waiting
- Event loop structure preserved
- Every patch must be reviewable, localized, and explainable
