# CAD Diff MVP

CAD Diff is a production-minded MVP web application for comparing two STEP part revisions and producing an engineer-friendly geometric change report.

## Stack

- **Backend**: FastAPI + pythonocc-core (Open Cascade bindings) + NumPy/SciPy
- **Frontend**: React + TypeScript + Vite + Three.js
- **Diff strategy**: STEP parsing, mass properties, automatic alignment, boolean add/remove volume extraction, and pluggable change classification.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI expects backend at `http://localhost:8000` by default.

## Architecture

See `docs/architecture.md` and `docs/roadmap.md`.

## Notes

- MVP focuses on single-part STEP comparisons.
- Geometry operations require OCC runtime. The backend returns clear diagnostics if OCC is unavailable.

## Folder structure

```text
backend/
  app/
    main.py
    models/
    services/
  tests/
frontend/
  src/
    components/
    api/
docs/
samples/
```
