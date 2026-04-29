# Validation Rules

## Architecture Reviewer Must Check
- [ ] No blocking calls present in transformed code
- [ ] All state stored in member variables (not stack)
- [ ] Adapter Layer present and CycloneTCP calls isolated inside it
- [ ] State machine states added correctly
- [ ] No threading primitives used

## Behavior Reviewer Must Check  
- [ ] start() returns immediately (no waiting)
- [ ] progress() advances state each call
- [ ] onComplete fires exactly once when handshake done
- [ ] Error states are handled and propagated
- [ ] Existing HTTP connection flow is not broken

## Test Validator Must Check
- [ ] Event loop ticks continue during TLS handshake
- [ ] TLS handshake still completes successfully
- [ ] No regression in HTTP request handling
