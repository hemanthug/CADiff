# Test harness strategy

Because production CAD revisions are domain-specific and often proprietary, this repo includes a harness strategy instead of embedded geometry assets:

1. Generate synthetic STEP fixtures in CI using pythonocc (box, box-with-hole, pocketed plate).
2. Store expected report assertions (volume delta, change count bounds).
3. Add regression folders in secure/internal deployment with anonymized parts.

Suggested fixture cases:
- Hole diameter increase
- Hole center translation
- Boss height increase
- Pocket depth decrease
- Fillet radius change
