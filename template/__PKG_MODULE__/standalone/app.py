"""Standalone microservice entry — the SAME package running as its own app.

This factory is what the independence gate boots in CI, and what production
runs on the dedicated host. It builds PackageConfig from explicit environment
variables (each named here, validated all-at-once by configure()) and mounts
the exact routers the host mounts. No aidream, no host anything.

Run locally:
    uvicorn __PKG_MODULE__.standalone.app:create_app --factory --port 8080
"""

from __future__ import annotations

import os

from fastapi import FastAPI

from __PKG_MODULE__._config import configure
from __PKG_MODULE__.api.router import router


def _env_config() -> dict[str, object]:
    """Map explicit env vars → configure() kwargs. EVERY var consumed by the
    standalone app is named here — this function is the complete registry.
    Missing required values are reported by configure()'s banner, all at once.
    """
    cfg: dict[str, object] = {}
    # Example:
    # if url := os.environ.get("__PKG_ENV_PREFIX___DATABASE_URL"):
    #     cfg["example_database_url"] = url
    return cfg


def create_app() -> FastAPI:
    configure(**_env_config())  # crashes loud (IndependenceConfigError) if wrong
    app = FastAPI(title="__PKG_TITLE__", version="0.1.0")
    app.include_router(router)
    return app
