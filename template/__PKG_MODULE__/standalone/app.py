"""Standalone microservice entry — the SAME package running as its own app.

This factory is what the independence gate boots in CI, and what production
runs on the dedicated host. It builds PackageConfig from explicit environment
variables (each named here, validated all-at-once by configure()) and mounts
the exact routers the host mounts. No aidream, no host anything.

DATABASE — there is exactly ONE connection, and it is REQUIRED.
    A package that needs Postgres calls ``matrx_orm.register_platform_db()``,
    which resolves the ONE deployment-level set of variables:
        SUPABASE_MATRIX_HOST / _PORT / _DATABASE_NAME / _USER / _PASSWORD
        (+ SUPABASE_MATRIX_SSL — TLS is a deployment input, never hardcoded)
    and RAISES if they are incomplete. Never add a package-named connection
    variable and never chain (`<PKG>_DATABASE_URL` → `DATABASE_URL` → …):
    pointing this package at a customer's own Postgres, a local instance, or
    Supabase is a change of VALUES, never of variable NAMES. The prefix is a
    historical name and says nothing about who owns the database.
    Why this is absolute: /Users/armanisadeghi/code/common-docs/policies/package-vs-implementation.md
    Inside a host, this never runs — the host aliases the package's config name
    onto its already-open pool, so there is one physical connection.

Run locally:
    uvicorn __PKG_MODULE__.standalone.app:create_app --factory --port 8080
"""

from __future__ import annotations

from fastapi import FastAPI

from __PKG_MODULE__._config import configure
from __PKG_MODULE__.api.router import router


def _env_config() -> dict[str, object]:
    """Map explicit env vars → configure() kwargs. EVERY var consumed by the
    standalone app is named here — this function is the complete registry.
    Missing required values are reported by configure()'s banner, all at once.

    Connection values do NOT belong here — see the module docstring. Anything
    named after this package (`__PKG_TITLE__`-specific hosts, URLs, passwords)
    is the fragmentation failure mode, not configuration.
    """
    cfg: dict[str, object] = {}
    # Example (an opinionated input this package owns, not a connection):
    # if bucket := os.environ.get("EXAMPLE_BUCKET"):
    #     cfg["example_bucket"] = bucket
    return cfg


def _register_db() -> None:
    """Standalone DB boot: bind this package's matrx-orm config name to the ONE
    database. Delete this function if the package has no Postgres schema.

    Raises (never degrades) when the five variables are not fully set.
    """
    # from matrx_orm import register_platform_db
    #
    # register_platform_db(
    #     "__PKG_MODULE__",            # matrx-orm CONFIG name, not a database
    #     additional_schemas=[],       # e.g. ["__PKG_SLUG__"] — schemas this package owns
    #     package="__PKG_DIST__",      # names this package in the crash message
    # )


def create_app() -> FastAPI:
    _register_db()                   # crashes loud if the ONE connection is absent
    configure(**_env_config())       # crashes loud (IndependenceConfigError) if wrong
    app = FastAPI(title="__PKG_TITLE__", version="0.1.0")
    app.include_router(router)
    return app
