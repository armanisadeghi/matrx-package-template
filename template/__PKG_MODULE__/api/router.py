"""The package's own API layer — mounted identically by host and standalone app.

Routers here are the package's public HTTP surface. Rules:
- Routers do NO work (thin: validate → call package service functions).
- Bare prefixes (host may strip a public /api/ itself).
- Every router added here must be mounted in standalone/app.py in the same
  change — a router that only exists in host mode violates INDEPENDENCE.md.
"""

from __future__ import annotations

from fastapi import APIRouter

from __PKG_MODULE__._config import get_config

router = APIRouter(prefix="/__PKG_SLUG__", tags=["__PKG_SLUG__"])


@router.get("/health")
async def health() -> dict[str, str]:
    get_config()  # proves the seam is wired; screams if not
    return {"status": "ok", "package": "__PKG_DIST__"}
