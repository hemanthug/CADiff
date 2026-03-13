# CAD Diff MVP Architecture

## 1. High-level system architecture

```text
React UI (upload + results + viewer)
   -> FastAPI REST API
      -> STEP Parser (OCC)
      -> Alignment Engine (PCA + registration)
      -> Diff Engine (boolean add/remove + topology heuristics)
      -> Change Classifier Pipeline (pluggable)
      -> Report Builder (JSON + CSV/PDF hooks)
```

## 2. Backend modules

- `app/services/step_parser.py`: Loads STEP solids, extracts topology and mass properties.
- `app/services/alignment.py`: Computes transformation from model B into model A frame using origin, principal axes, and optional ICP-like refinement hooks.
- `app/services/diff_engine.py`: Computes boolean A-B and B-A, segments changed regions, and invokes classifiers.
- `app/services/classifiers.py`: Rule-based classifiers for holes/bosses/fillets/chamfers etc. (initial subset implemented, extensible design).
- `app/services/reporting.py`: Builds engineer-friendly structured output.
- `app/main.py`: API endpoints for upload, compare, and report export.

## 3. Frontend modules

- `src/App.tsx`: Main workflow layout.
- `src/components/UploadPanel.tsx`: Two-file upload cards + status.
- `src/components/ComparisonSettings.tsx`: Tolerance and options.
- `src/components/SummaryCards.tsx`: Global comparison metrics.
- `src/components/ChangeList.tsx`: Interactive list with zoom callbacks.
- `src/components/DiffViewer.tsx`: Three.js-based visual overlay for added/removed regions (MVP: mesh payload support with fallback placeholder).

## 4. Data model

`ChangeItem` carries:
- id, type, title, description
- location + reference features
- old/new/delta values + units
- severity + confidence
- region mesh/id

## 5. Error handling

- Non-STEP uploads rejected with actionable message.
- Parse/alignment/diff failures return stage-specific diagnostics.
- OCC dependency failures explicitly communicated.

## 6. Extensibility

- Add new feature classifiers by implementing `ChangeClassifier` protocol.
- Add assemblies by introducing `AssemblyGraph` preprocessor and per-part pairing.
- Add native CAD by plugging converters/parsers before OCC shape normalization.
