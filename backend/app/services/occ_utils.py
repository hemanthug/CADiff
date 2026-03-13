"""OCC import helpers.

Geometry operations in this service layer are intentionally isolated so the API
can fail gracefully with a clear message if pythonocc-core is not installed.
"""

from __future__ import annotations


class OCCUnavailableError(RuntimeError):
    pass


def require_occ() -> None:
    try:
        import OCC.Core  # noqa: F401
    except Exception as exc:  # pragma: no cover - environment dependent
        raise OCCUnavailableError(
            "Open Cascade bindings (pythonocc-core) are required for STEP parsing and geometric diff."
        ) from exc
