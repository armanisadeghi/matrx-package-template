#!/usr/bin/env bash
# Independence gate — PROOF BY EXECUTION.
#
# Installs the package into a FRESH venv from its own pyproject (plus its
# declared local matrx-* siblings, passed explicitly), then boots the
# standalone app's smoke tests. No host repo, no workspace, no excuses.
# If this passes, the package is independent as a matter of demonstrated fact.
#
# Usage:
#   independence_gate.sh <package_dir> [local_sibling_dir ...]
# Example (from the aidream repo root):
#   independence_gate.sh packages/matrx-files \
#       packages/matrx-utils packages/matrx-orm packages/matrx-connect
set -euo pipefail

PKG_DIR="$(cd "$1" && pwd)"; shift
SIBLINGS=()
for s in "$@"; do SIBLINGS+=("$(cd "$s" && pwd)"); done

RED=$'\033[91m'; GREEN=$'\033[92m'; RESET=$'\033[0m'
WORK="$(mktemp -d "${TMPDIR:-/tmp}/independence-gate-XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

fail() {
  echo "${RED}==============================================================================="
  echo "🚨 INDEPENDENCE GATE FAILED for ${PKG_DIR}"
  echo "===============================================================================${RESET}"
  echo "$1"
  echo "The package cannot run outside its host. Fix the package — never this gate."
  echo "Contract: INDEPENDENCE.md"
  exit 1
}

echo "▶ independence gate: ${PKG_DIR}"
echo "  fresh venv at ${WORK}/venv"
uv venv "$WORK/venv" --python 3.13 >/dev/null

# Install declared local siblings first (leaf-order as passed), then the package.
for s in "${SIBLINGS[@]+"${SIBLINGS[@]}"}"; do
  echo "  installing declared sibling: $s"
  VIRTUAL_ENV="$WORK/venv" uv pip install --quiet "$s" || fail "sibling install failed: $s"
done
echo "  installing package (with [standalone] extra) from its own pyproject"
VIRTUAL_ENV="$WORK/venv" uv pip install --quiet "${PKG_DIR}[standalone]" \
  || fail "bare install failed — the pyproject does not describe a self-sufficient package"

# The package's own declared dev group carries dependencies needed only to run
# its tests. Read the package pyproject from the fresh interpreter so malformed
# TOML fails closed. Install only that group into this same bare environment;
# packages without a dev group keep the historical minimal test-tool fallback.
DEV_GROUP_STATE="$("$WORK/venv/bin/python" - "$PKG_DIR/pyproject.toml" <<'PY'
import sys
import tomllib
from pathlib import Path

project = tomllib.loads(Path(sys.argv[1]).read_text())
groups = project.get("dependency-groups", {})
if not isinstance(groups, dict):
    raise TypeError("[dependency-groups] must be a table")
print("declared" if "dev" in groups else "absent")
PY
)" || fail "could not read the package's dependency groups"
if [[ "$DEV_GROUP_STATE" == "declared" ]]; then
  echo "  installing the package's declared dev group from its own pyproject"
  uv pip install --quiet --python "$WORK/venv/bin/python" --group "$PKG_DIR/pyproject.toml:dev" \
    || fail "declared dev dependency group install failed"
elif [[ "$DEV_GROUP_STATE" == "absent" ]]; then
  echo "  package has no dev group; installing the minimal pytest fallback"
  VIRTUAL_ENV="$WORK/venv" uv pip install --quiet pytest pytest-asyncio httpx >/dev/null
else
  fail "unexpected dependency-group inspection result: $DEV_GROUP_STATE"
fi

# Run the smoke tests from an EMPTY cwd so the source tree can't leak in via sys.path.
cp -R "$PKG_DIR/tests" "$WORK/tests"
cp "$PKG_DIR/pyproject.toml" "$WORK/pyproject.toml"  # pytest config (asyncio_mode etc.) travels with the package
cd "$WORK"
echo "  booting standalone app + smoke tests (bare venv, empty cwd)"
"$WORK/venv/bin/python" -m pytest tests -q || fail "standalone boot / smoke tests failed in the bare venv"

echo "${GREEN}✅ INDEPENDENCE PROVEN: ${PKG_DIR} installs, boots, and serves with zero host code.${RESET}"
