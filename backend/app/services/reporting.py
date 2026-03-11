from __future__ import annotations

from app.models.schemas import AlignmentTransform, ComparisonReport, ComparisonSummary, MassProperties


def build_report(
    mass_a: dict,
    mass_b: dict,
    alignment_matrix: list[list[float]],
    alignment_method: str,
    alignment_residual: float | None,
    added_volume: float,
    removed_volume: float,
    changes: list[dict],
) -> ComparisonReport:
    summary = ComparisonSummary(
        total_changes=len(changes),
        added_volume=added_volume,
        removed_volume=removed_volume,
        volume_delta=mass_b["volume"] - mass_a["volume"],
        surface_area_delta=mass_b["surface_area"] - mass_a["surface_area"],
    )

    return ComparisonReport(
        summary=summary,
        mass_properties_a=MassProperties(**mass_a),
        mass_properties_b=MassProperties(**mass_b),
        alignment=AlignmentTransform(
            matrix=alignment_matrix,
            method=alignment_method,
            residual_error=alignment_residual,
        ),
        changes=changes,
    )
