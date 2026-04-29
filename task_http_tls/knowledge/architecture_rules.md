# Architecture Rules — Must Be Followed

1. NO blocking calls inside any seve Activity handler
2. NO sleep(), usleep(), delay(), or any busy-wait loop
3. NO synchronous socket calls that wait for network response
4. All long operations MUST be split across multiple event loop ticks
5. State must be stored in member variables, NOT on the call stack between ticks
6. CycloneTCP internals must NOT be rewritten — only wrapped
7. The Adapter Layer is the ONLY place CycloneTCP is called from
8. Callbacks/completions MUST be delivered via seve event channels
9. Every new class must have a clear single responsibility
10. Existing HttpConnState enum must be reused or extended, not replaced
