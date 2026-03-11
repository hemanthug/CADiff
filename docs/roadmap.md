# Roadmap

## MVP (single-part STEP)
- Upload two STEP files.
- Parse and validate solids.
- Auto align.
- Compute mass property deltas.
- Compute bidirectional boolean differences.
- Build structured change report.
- Show interactive list + highlighted regions.

## Next: richer feature inference
- Improve hole/boss/slot/pocket/fillet/chamfer classifiers.
- Add robust correspondence graph between faces/features.
- Confidence scoring per classifier and aggregate certainty.

## Next: exports + collaboration
- CSV + PDF exports.
- Saved comparisons and report versioning.
- API auth and audit trail.

## Beyond MVP
- Assembly support with component matching and BOM-aware diff.
- Native CAD ingestion pipeline (Parasolid, CATPart, Creo, NX) via translators.
- Cloud/offline hybrid execution for sensitive environments.
