import numpy as np

from app.services.alignment import alignment_from_bboxes, compute_origin_alignment


def test_origin_alignment_translation():
    t = compute_origin_alignment((10, 0, -2), (7, 1, 3))
    assert np.allclose(t[:3, 3], [3, -1, -5])


def test_bbox_alignment_translation():
    t = alignment_from_bboxes(((0, 0, 0), (10, 10, 10)), ((10, 10, 10), (20, 20, 20)))
    assert np.allclose(t[:3, 3], [-10, -10, -10])
