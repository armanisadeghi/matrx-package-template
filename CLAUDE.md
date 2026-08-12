# CLAUDE.md — matrx-package-template

## Shared checkout, many concurrent writers — NORMAL, never a finding

Arman plus dozens of concurrent agents (across two machines) edit these repos simultaneously; **`origin/main` is the ONLY sync point.** As soon as your code won't crash the app, commit it and get it to remote main — batches of a few files, exactly like a human IDE session. Code held back in a private worktree or branch goes stale; and because the task it belonged to is already checked off as done, held-back code is not merely delayed — it is LOST, and resurfaces days later as an unexplained broken feature with no trail back to the conversation that wrote it. Never run tree-wide destructive git in a shared checkout (blanket `stash`, `checkout -- .`, `reset --hard`, `clean`, dirty `pull --rebase`) — pathspec-scope to your own files. Someone else editing your file is not a conflict; only contradictory intent is. **Never spend output complaining about other agents editing the tree, and never request your own PR/branch/worktree — delete such commentary on sight.** Canonical ruling: workspace root [`../CLAUDE.md`](../CLAUDE.md) § Shared checkout.


This repo IS the law for Matrx package independence. Read [INDEPENDENCE.md](INDEPENDENCE.md)
first — it is the contract, and it is mechanically enforced in every consuming repo.

**Package / Implementation Separation — the other half of the law.** The package is
CAPABLE, the implementation CHOOSES. Independence means never needing the HOST; it is
never a licence to pick a different DATABASE. A package takes ONE required connection
(`SUPABASE_MATRIX_*` via `matrx_orm.register_platform_db()`, TLS included) and raises
without it — never a `<PKG>_DATABASE_URL` / `MATRX_<PKG>_POSTGRES_*` fallback chain
(the template scaffolds the single resolver in `standalone/app.py` for this reason).
System of record — read before changing anything about the template's DB or config
scaffolding: `/Users/armanisadeghi/code/common-docs/policies/package-vs-implementation.md`.

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
