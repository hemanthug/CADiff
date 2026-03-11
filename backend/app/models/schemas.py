from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class MassProperties(BaseModel):
    volume: float
    surface_area: float
    center_of_mass: tuple[float, float, float]
    bbox_min: tuple[float, float, float]
    bbox_max: tuple[float, float, float]


class AlignmentTransform(BaseModel):
    matrix: list[list[float]]
    method: str
    residual_error: float | None = None


class ValueDelta(BaseModel):
    old_value: float | None = None
    new_value: float | None = None
    delta: float | None = None
    units: str | None = None


class ChangeItem(BaseModel):
    change_id: str
    change_type: str
    title: str
    description: str
    location: dict[str, Any] = Field(default_factory=dict)
    reference_faces_or_features: list[str] = Field(default_factory=list)
    values: ValueDelta = Field(default_factory=ValueDelta)
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    confidence: float = Field(ge=0, le=1, default=0.5)
    affected_region_geometry: dict[str, Any] = Field(default_factory=dict)


class ComparisonSummary(BaseModel):
    total_changes: int
    added_volume: float
    removed_volume: float
    volume_delta: float
    surface_area_delta: float


class ComparisonReport(BaseModel):
    summary: ComparisonSummary
    mass_properties_a: MassProperties
    mass_properties_b: MassProperties
    alignment: AlignmentTransform
    changes: list[ChangeItem]


class CompareResponse(BaseModel):
    status: Literal["ok", "error"]
    report: ComparisonReport | None = None
    error: str | None = None
