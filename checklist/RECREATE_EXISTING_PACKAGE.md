# Recreating an existing Matrx package onto the template

The migration vehicle for bringing a rotted package back to true independence.
Work top-to-bottom; every step ends with both gates green.

1. **Instantiate fresh.** `new_package.py` into a scratch dir — this is the target
   anatomy, not a place to copy old sins into.
2. **Inventory the rot.** Run `check_imports.py` against the CURRENT package with the
   host forbidden. Every violation is either (a) a capability to inject via
   `configure_*()` with a standalone fallback, or (b) a dependency to declare.
   No third bucket.
3. **Move code, keep the anatomy.** Source modules land under the package module dir;
   HTTP surface consolidates under `api/`; DB models/managers under `db/` with the
   `db_requirements.py` manifest describing host mode and the package's own
   models/migrations covering standalone mode.
4. **Build the standalone app.** `standalone/app.py` mounts every router the host
   mounts. Anything that can't run standalone reveals a missing seam — add the
   `configure()` kwarg + fallback, don't carve out the feature.
5. **Wire the host.** Host startup calls `configure(...)`; host DB wiring resolves the
   manifest (aidream: `python db/generate.py` → `_generated/package_db_wiring.py`);
   host mounts `api/` routers.
6. **Enforce forever.** Add both gates to the host CI/release script for this package.
   A package is only "on the template" once the independence gate runs on every build.
7. **Smoke tests are the ratchet.** Every subsequent feature adds at least one
   bare-venv smoke test. Feature works in host mode but not in the gate → the feature
   is not done.
