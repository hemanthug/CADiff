from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import CompareResponse
from app.services.alignment import compute_origin_alignment, transform_to_list
from app.services.diff_engine import classify_diff_regions, compute_boolean_diff
from app.services.occ_utils import OCCUnavailableError, require_occ
from app.services.reporting import build_report
from app.services.step_parser import parse_step_file

app = FastAPI(title="CAD Diff API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    try:
        require_occ()
        occ_ready = True
    except OCCUnavailableError:
        occ_ready = False
    return {"status": "ok", "occ_ready": occ_ready}


def _validate_step(file: UploadFile) -> None:
    if not file.filename:
        raise ValueError("Uploaded file is missing a filename.")
    if not file.filename.lower().endswith((".step", ".stp")):
        raise ValueError(f"{file.filename} is not a STEP file.")


@app.post("/compare", response_model=CompareResponse)
async def compare(
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    tolerance: float = Form(0.01),
) -> CompareResponse:
    try:
        _validate_step(file_a)
        _validate_step(file_b)

        with NamedTemporaryFile(suffix=".step", delete=False) as temp_a, NamedTemporaryFile(
            suffix=".step", delete=False
        ) as temp_b:
            temp_a.write(await file_a.read())
            temp_b.write(await file_b.read())
            path_a = Path(temp_a.name)
            path_b = Path(temp_b.name)

        model_a = parse_step_file(path_a)
        model_b = parse_step_file(path_b)

        transform = compute_origin_alignment(
            model_a.mass_properties["center_of_mass"],
            model_b.mass_properties["center_of_mass"],
        )

        # Apply transform to model B shape
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        from OCC.Core.gp import gp_Trsf, gp_Vec

        trsf = gp_Trsf()
        tvec = transform[:3, 3]
        trsf.SetTranslation(gp_Vec(float(tvec[0]), float(tvec[1]), float(tvec[2])))
        transformed = BRepBuilderAPI_Transform(model_b.shape, trsf, True)
        shape_b_aligned = transformed.Shape()

        diff_result = compute_boolean_diff(model_a.shape, shape_b_aligned, tolerance=tolerance)
        changes = classify_diff_regions(diff_result)

        report = build_report(
            mass_a=model_a.mass_properties,
            mass_b=model_b.mass_properties,
            alignment_matrix=transform_to_list(transform),
            alignment_method="center_of_mass_translation",
            alignment_residual=None,
            added_volume=diff_result.added_volume,
            removed_volume=diff_result.removed_volume,
            changes=changes,
        )
        return CompareResponse(status="ok", report=report)
    except (ValueError, OCCUnavailableError) as exc:
        return CompareResponse(status="error", error=str(exc))
    except Exception as exc:  # pragma: no cover - safety net for API robustness
        return CompareResponse(status="error", error=f"Unexpected failure during comparison: {exc}")
