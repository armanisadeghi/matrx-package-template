# INDEPENDENCE.md — the contract every Matrx package signs

> **A Matrx package is extremely opinionated, yet fully independent.** It may expect an
> exact Postgres structure, exact AWS buckets, exact conventions — but everything it
> expects is **handed to it** through `configure_*()`, or it provisions its **own exact
> duplicate copy**. It NEVER reaches into a host application.
>
> — This is Arman's standing order. Agents have repeatedly destroyed package
> independence by importing "just one thing" from the host. That is why this file and
> its enforcement gates exist. If you are an AI agent reading this: the rules below are
> not style preferences. They are mechanically enforced, and a violation FAILS the build.

## The three laws

1. **No host imports, ever.** Nothing under the package may import `aidream`, any
   host-repo root module, or an undeclared sibling. If the package needs a host
   capability, it grows a `configure_*()` kwarg with a standalone fallback.
   *Test: would this import resolve in a fresh project that contains ONLY this package
   and its declared dependencies? No → forbidden.*

2. **Opinionated inputs, validated loudly, never defaulted silently.** Required config
   is validated **all-errors-at-once at configure/boot time** with a screaming banner
   that names every missing value and how to supply it. A missing value must be
   impossible to miss — crash, never fall back to a legacy path. Optional seams get a
   real standalone fallback (the package's own duplicate copy), never a stub that
   pretends to work.

3. **The package ships its own truth.** Its database schema (models + migrations), its
   API layer (FastAPI routers), and its standalone app entry live INSIDE the package.
   Installing the package gives a customer the entire structure that drives it.
   - **Host mode:** the host resolves the package's `db/db_requirements.py` manifest
     and calls `configure_db(...)`; the host mounts the package's routers.
   - **Standalone mode:** `standalone/app.py` boots the same routers as a real
     microservice against the same (or a fresh) database, using the package's own
     migrations.
   The two modes run the SAME code. A feature that only works in host mode is a defect.

## Enforcement — the layers that SCREAM

Each layer is sufficient alone; each screams when it fires (per the extinction doctrine):

| Layer | What | When |
|---|---|---|
| `scripts/check_imports.py` | AST scan — forbidden host/undeclared-sibling imports | pre-commit / CI, instant |
| **Standalone-boot gate** `scripts/independence_gate.sh` | Fresh venv, install the package from its OWN pyproject (+ declared local siblings only), **boot the standalone app, run smoke tests** | CI + release. Proof by execution — the gate no agent can rationalize past |
| Boot validation | `configure()`/app factory raises `IndependenceConfigError` listing ALL missing config with a red banner | every process start |
| Host boundary ratchet | the host repo's `check_package_boundaries.py` | host CI |

**Never weaken a gate to make a build pass.** If a gate fires, the code is wrong, not
the gate. Deleting, skipping, baselining-up, or `# noqa`-ing an independence gate is
itself a defect — file it and fix the import instead.

## What "opinionated" licenses — and what it does not

✅ Allowed: expecting exact table names/schemas, exact bucket layouts, exact envelope
shapes, exact conventions — **received via configure() or shipped as the package's own
schema/migrations**.

❌ Not licensed: reading the host's env vars, assuming the host's filesystem layout,
importing the host's settings object, "temporarily" importing a host helper, or a
fallback that silently no-ops instead of either working or crashing.
