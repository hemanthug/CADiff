from __future__ import annotations

import numpy as np


def compute_origin_alignment(center_a: tuple[float, float, float], center_b: tuple[float, float, float]) -> np.ndarray:
    """Build a rigid transform translating B's COM to A's COM.

    Returns 4x4 homogeneous transform.
    """
    transform = np.eye(4)
    transform[:3, 3] = np.array(center_a) - np.array(center_b)
    return transform


def alignment_from_bboxes(
    bbox_a: tuple[tuple[float, float, float], tuple[float, float, float]],
    bbox_b: tuple[tuple[float, float, float], tuple[float, float, float]],
) -> np.ndarray:
    """Fallback alignment based on bounding box centers.

    This provides a robust baseline when feature correspondence is unavailable.
    """
    center_a = (np.array(bbox_a[0]) + np.array(bbox_a[1])) / 2.0
    center_b = (np.array(bbox_b[0]) + np.array(bbox_b[1])) / 2.0
    t = np.eye(4)
    t[:3, 3] = center_a - center_b
    return t


def transform_to_list(transform: np.ndarray) -> list[list[float]]:
    return transform.round(9).tolist()
