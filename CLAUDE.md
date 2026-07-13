# CLAUDE.md — matrx-package-template

This repo IS the law for Matrx package independence. Read [INDEPENDENCE.md](INDEPENDENCE.md)
first — it is the contract, and it is mechanically enforced in every consuming repo.

- `template/` — the instantiable skeleton (placeholders `__PKG_*__`). Every file in it
  is deliberate; changing the template changes the standard for ALL future packages.
- `scripts/new_package.py` — instantiator (stdlib only, keep it that way).
- `scripts/check_imports.py` — AST gate: forbidden host imports + undeclared siblings,
  allowed set DERIVED from pyproject (never hand-maintained).
- `scripts/independence_gate.sh` — proof by execution: bare venv, install the package
  alone, boot the standalone app, run smoke tests from an empty cwd.
- `checklist/RECREATE_EXISTING_PACKAGE.md` — migration vehicle for existing packages.

Rules for edits here:
- **Never weaken a gate.** Gates get stricter or stay; a change that makes a failing
  package pass without fixing the package is forbidden.
- The template must always instantiate + pass its own gates: after ANY template change run
  `python scripts/new_package.py matrx-selftest "Matrx Selftest" --desc t --dest /tmp/x`
  then both gates against the result.
- This is cross-repo truth — consuming repos keep pointer lines only, never copies
  (see the `cross-repo-docs` doctrine in the workspace).
