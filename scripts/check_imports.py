#!/usr/bin/env python3
"""Independence import gate — AST-level, zero dependencies.

Scans a package directory and FAILS (exit 1, screaming banner) on any import
that could not resolve from the package's own pyproject dependencies:

  * host application modules (``aidream`` or any name in --forbid)
  * matrx-* siblings not declared in [project.dependencies] / optional-deps

Usage:
    python check_imports.py <package_dir> [--forbid aidream,workflows,scraper]

The allowed set is DERIVED from pyproject.toml — never hand-maintained.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
import tomllib
from pathlib import Path

DEFAULT_FORBIDDEN = {"aidream"}
RED = "\033[91m"
RESET = "\033[0m"


def declared_deps(pkg_dir: Path) -> set[str]:
    data = tomllib.loads((pkg_dir / "pyproject.toml").read_text())
    names: set[str] = set()
    deps: list[str] = list(data["project"].get("dependencies", []))
    for extra in data["project"].get("optional-dependencies", {}).values():
        deps.extend(extra)
    for group in data.get("dependency-groups", {}).values():
        deps.extend(d for d in group if isinstance(d, str))
    for spec in deps:
        name = re.split(r"[\[<>=!~; ]", spec.strip(), maxsplit=1)[0]
        names.add(name.lower().replace("-", "_"))
    return names


def own_module(pkg_dir: Path) -> str:
    data = tomllib.loads((pkg_dir / "pyproject.toml").read_text())
    wheel = data.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
    pkgs = wheel.get("packages")
    if pkgs:
        return Path(pkgs[0]).name
    return data["project"]["name"].lower().replace("-", "_")


def scan(pkg_dir: Path, forbidden: set[str]) -> list[str]:
    allowed = declared_deps(pkg_dir)
    own = own_module(pkg_dir)
    violations: list[str] = []
    for py in sorted(pkg_dir.rglob("*.py")):
        if "__pycache__" in py.parts or ".venv" in py.parts:
            continue
        try:
            tree = ast.parse(py.read_text(), filename=str(py))
        except SyntaxError as exc:
            violations.append(f"{py}: SYNTAX ERROR — {exc}")
            continue
        for node in ast.walk(tree):
            roots: list[tuple[int, str]] = []
            if isinstance(node, ast.Import):
                roots = [(node.lineno, a.name.split(".")[0]) for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [(node.lineno, node.module.split(".")[0])]
            for lineno, root in roots:
                if root in forbidden:
                    violations.append(f"{py}:{lineno}: forbidden HOST import '{root}'")
                elif root.startswith("matrx_") and root != own and root not in allowed:
                    violations.append(
                        f"{py}:{lineno}: undeclared sibling '{root}' — add it to pyproject dependencies or remove the import"
                    )
    return violations


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package_dir", type=Path)
    ap.add_argument("--forbid", default="", help="comma-separated extra forbidden root modules")
    args = ap.parse_args()
    forbidden = DEFAULT_FORBIDDEN | {f.strip() for f in args.forbid.split(",") if f.strip()}

    violations = scan(args.package_dir.resolve(), forbidden)
    if violations:
        print(f"\n{RED}{'=' * 78}")
        print(f"🚨 INDEPENDENCE VIOLATION — {args.package_dir.name} imports what it must not.")
        print(f"{'=' * 78}{RESET}")
        for v in violations:
            print(f"  ✗ {v}")
        print(
            "\nThe fix is NEVER to weaken this gate. Inject the capability via "
            "configure_*() with a standalone fallback, or declare a real dependency.\n"
            "Contract: INDEPENDENCE.md\n"
        )
        return 1
    print(f"✅ {args.package_dir.name}: independence import gate clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
