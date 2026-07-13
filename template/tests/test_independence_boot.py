"""Smoke tests run by the independence gate inside the bare venv.

These are the executable proof of INDEPENDENCE.md: the package imports, boots
its standalone app, and serves its own routes with zero host code present.
Add package-specific smoke tests here as real capability lands — every major
feature earns at least one bare-venv smoke test.
"""

from __future__ import annotations

import pytest


def test_package_imports_without_host() -> None:
    import __PKG_MODULE__  # noqa: F401


def test_unconfigured_access_screams() -> None:
    from __PKG_MODULE__._config import IndependenceConfigError, get_config, is_configured

    if is_configured():  # a prior test configured; the law still holds
        return
    with pytest.raises(IndependenceConfigError):
        get_config()


def test_standalone_app_boots_and_serves() -> None:
    from fastapi.testclient import TestClient

    from __PKG_MODULE__.standalone.app import create_app

    app = create_app()
    with TestClient(app) as client:
        resp = client.get("/__PKG_SLUG__/health")
        assert resp.status_code == 200
        assert resp.json()["package"] == "__PKG_DIST__"
