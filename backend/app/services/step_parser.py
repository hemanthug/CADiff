from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .occ_utils import require_occ


@dataclass
class ParsedModel:
    shape: object
    mass_properties: dict
    topology_counts: dict


def parse_step_file(path: Path) -> ParsedModel:
    """Parse a STEP file into an OCC solid and extract topology + mass properties."""
    require_occ()

    from OCC.Core.BRep import BRep_Builder
    from OCC.Core.BRepBndLib import brepbndlib_Add
    from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_VolumeProperties
    from OCC.Core.BRepTools import breptools_UVBounds
    from OCC.Core.Bnd import Bnd_Box
    from OCC.Core.GProp import GProp_GProps
    from OCC.Core.IFSelect import IFSelect_RetDone
    from OCC.Core.STEPControl import STEPControl_Reader
    from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_VERTEX
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopoDS import TopoDS_Compound

    reader = STEPControl_Reader()
    status = reader.ReadFile(str(path))
    if status != IFSelect_RetDone:
        raise ValueError(f"Failed to read STEP file: {path.name}")

    ok = reader.TransferRoots()
    if ok == 0:
        raise ValueError(f"STEP transfer failed for file: {path.name}")

    shape = reader.OneShape()

    volume_props = GProp_GProps()
    surface_props = GProp_GProps()
    brepgprop_VolumeProperties(shape, volume_props)
    brepgprop_SurfaceProperties(shape, surface_props)

    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

    def count_topology(kind: int) -> int:
        explorer = TopExp_Explorer(shape, kind)
        count = 0
        while explorer.More():
            count += 1
            explorer.Next()
        return count

    return ParsedModel(
        shape=shape,
        mass_properties={
            "volume": volume_props.Mass(),
            "surface_area": surface_props.Mass(),
            "center_of_mass": tuple(volume_props.CentreOfMass().Coord()),
            "bbox_min": (xmin, ymin, zmin),
            "bbox_max": (xmax, ymax, zmax),
        },
        topology_counts={
            "solids": count_topology(TopAbs_SOLID),
            "faces": count_topology(TopAbs_FACE),
            "edges": count_topology(TopAbs_EDGE),
            "vertices": count_topology(TopAbs_VERTEX),
        },
    )
