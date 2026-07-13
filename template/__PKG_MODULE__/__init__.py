"""__PKG_TITLE__ — an independent, opinionated Matrx package.

Contract: INDEPENDENCE.md at the package root. Two run modes, one code path:

- HOST mode: the host calls ``configure(...)`` (and ``configure_db(...)`` via the
  db_requirements manifest) at startup, then mounts ``api.router``.
- STANDALONE mode: ``standalone/app.py`` builds config from explicit env/args,
  calls the SAME ``configure(...)``, mounts the SAME routers, and serves them.
"""

from __PKG_MODULE__._config import (
    IndependenceConfigError,
    PackageConfig,
    configure,
    get_config,
    is_configured,
)

__all__ = [
    "IndependenceConfigError",
    "PackageConfig",
    "configure",
    "get_config",
    "is_configured",
]
