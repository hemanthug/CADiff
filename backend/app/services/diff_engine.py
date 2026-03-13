from __future__ import annotations

from dataclasses import dataclass

from .classifiers import ClassifierPipeline, RegionDelta
from .occ_utils import require_occ


@dataclass
class DiffResult:
    added_volume: float
    removed_volume: float
    regions: list[RegionDelta]


def compute_boolean_diff(shape_a: object, shape_b_aligned: object, tolerance: float) -> DiffResult:
    """Compute bidirectional boolean material differences.

    `shape_a - shape_b` => removed from B relative to A.
    `shape_b - shape_a` => added in B relative to A.
    """
    require_occ()
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps

    cut_removed = BRepAlgoAPI_Cut(shape_a, shape_b_aligned)
    cut_removed.SetFuzzyValue(tolerance)
    cut_removed.Build()

    cut_added = BRepAlgoAPI_Cut(shape_b_aligned, shape_a)
    cut_added.SetFuzzyValue(tolerance)
    cut_added.Build()

    removed_props = GProp_GProps()
    added_props = GProp_GProps()
    brepgprop_VolumeProperties(cut_removed.Shape(), removed_props)
    brepgprop_VolumeProperties(cut_added.Shape(), added_props)

    removed_volume = max(0.0, removed_props.Mass())
    added_volume = max(0.0, added_props.Mass())

    # MVP region strategy: start with aggregate regions; can be replaced with
    # connected-component segmentation of resulting solids.
    regions = [
        RegionDelta("R-ADD", added_volume, 0.0, tuple(added_props.CentreOfMass().Coord())),
        RegionDelta("R-REM", 0.0, removed_volume, tuple(removed_props.CentreOfMass().Coord())),
    ]
    return DiffResult(added_volume=added_volume, removed_volume=removed_volume, regions=regions)


def classify_diff_regions(diff_result: DiffResult) -> list[dict]:
    pipeline = ClassifierPipeline()
    return pipeline.run(diff_result.regions)
