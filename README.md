# matrx-package-template

The canonical template for every Matrx Python package — **extremely opinionated,
fully independent**. A package built from this template installs alone, boots alone,
serves its own API alone, and ships its own database truth, while accepting the
host's implementations through `configure_*()` seams.

The contract is [INDEPENDENCE.md](INDEPENDENCE.md). Read it before anything else —
it is copied into every instantiated package and is mechanically enforced.

## Create a new package

```bash
python scripts/new_package.py matrx-things "Matrx Things" \
    --desc "One-line description." \
    --dest /Users/armanisadeghi/code/aidream/packages
```

You get: pyproject (deps = the whole allowed import universe) · `configure()` seam
that screams all-errors-at-once · `db/` manifest + own-models/migrations slots ·
`api/` routers · `standalone/app.py` microservice factory · Dockerfile ·
bare-venv smoke tests · INDEPENDENCE.md.

## Enforce (wire BOTH into the host repo's CI/release)

```bash
# 1. Instant AST gate — forbidden host imports, undeclared siblings
python scripts/check_imports.py <package_dir>

# 2. Proof by execution — fresh venv, install package only, boot, smoke test
scripts/independence_gate.sh <package_dir> <declared local sibling dirs…>
```

## Recreate an existing package onto this template

See [checklist/RECREATE_EXISTING_PACKAGE.md](checklist/RECREATE_EXISTING_PACKAGE.md).

First real instance: **matrx-files** (aidream `packages/matrx-files`).
