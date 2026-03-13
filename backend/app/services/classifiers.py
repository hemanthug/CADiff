from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RegionDelta:
    region_id: str
    added_volume: float
    removed_volume: float
    centroid: tuple[float, float, float]


class BaseClassifier:
    change_type = "generic_region_change"

    def classify(self, region: RegionDelta) -> dict | None:
        magnitude = max(region.added_volume, region.removed_volume)
        if magnitude <= 0:
            return None

        severity = "low"
        if magnitude > 1000:
            severity = "high"
        elif magnitude > 100:
            severity = "medium"

        return {
            "change_type": self.change_type,
            "title": f"Local geometry changed (region {region.region_id})",
            "description": "Detected material addition/removal in a localized region.",
            "location": {"centroid": region.centroid},
            "reference_faces_or_features": [],
            "values": {
                "old_value": region.removed_volume,
                "new_value": region.added_volume,
                "delta": region.added_volume - region.removed_volume,
                "units": "mm^3",
            },
            "severity": severity,
            "confidence": 0.6,
            "affected_region_geometry": {"region_id": region.region_id},
        }


class ClassifierPipeline:
    def __init__(self) -> None:
        self.classifiers = [BaseClassifier()]

    def run(self, regions: list[RegionDelta]) -> list[dict]:
        changes: list[dict] = []
        for idx, region in enumerate(regions, start=1):
            for classifier in self.classifiers:
                item = classifier.classify(region)
                if item:
                    item["change_id"] = f"CHG-{idx:03d}"
                    changes.append(item)
                    break
        return changes
