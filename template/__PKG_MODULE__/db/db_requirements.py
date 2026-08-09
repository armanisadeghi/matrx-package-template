# Declarative manifest of the host DB artifacts this package needs — DATA ONLY.
# Imports nothing, names no host module paths. Consumed by matrx-orm's
# package_wiring generator in the host (python db/generate.py), which resolves
# every schema/table against the host inventory and emits the host-side wiring
# module that calls this package's configure_db(...).
#
# INDEPENDENCE.md law #3: this manifest covers HOST mode. STANDALONE mode uses
# the package's own generated models (db/models.py) + migrations (db/migrations/)
# against the same schema — the two must describe the SAME structure.
#
# INDEPENDENCE.md law #4: in HOST mode the package resolves NO connection at all
# — the host aliases this package's matrx-orm config name onto its already-open
# pool. In STANDALONE mode `standalone/app.py` calls register_platform_db(),
# which reads the ONE required SUPABASE_MATRIX_* set. Never a package-named
# connection variable, never a fallback chain:
# /Users/armanisadeghi/code/common-docs/policies/package-vs-implementation.md

DB_REQUIREMENTS = {
    "target": {
        "configure_import": "__PKG_MODULE__",
        "configure_call": "configure_db",
        "models_kwarg": "models",
    },
    "schemas": [],  # e.g. ["files"]
}
