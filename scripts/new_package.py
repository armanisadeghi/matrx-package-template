#!/usr/bin/env python3
"""Instantiate the Matrx package template. Stdlib only.

Usage:
    python new_package.py matrx-files "Matrx Files" \
        --desc "All things files: cloud storage, media, conversion, sharing." \
        --dest /path/to/repo/packages

Placeholders replaced everywhere (file contents AND paths):
    __PKG_DIST__        matrx-files          (distribution name)
    __PKG_MODULE__      matrx_files          (import name)
    __PKG_TITLE__       Matrx Files          (human name)
    __PKG_SLUG__        files                (route prefix segment)
    __PKG_DESC__        --desc value

There is deliberately NO per-package env-var prefix placeholder. A package takes
ONE required connection through matrx_orm.register_platform_db() (SUPABASE_MATRIX_*)
and never a package-named connection variable — INDEPENDENCE.md law #4 and
/Users/armanisadeghi/code/common-docs/policies/package-vs-implementation.md.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
ROOT_DOCS = ["INDEPENDENCE.md"]  # copied from the template repo root into each package


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dist_name", help="e.g. matrx-files")
    ap.add_argument("title", help='e.g. "Matrx Files"')
    ap.add_argument("--desc", required=True)
    ap.add_argument("--dest", required=True, type=Path, help="parent dir (e.g. <repo>/packages)")
    args = ap.parse_args()

    dist = args.dist_name.lower()
    if not dist.startswith("matrx-"):
        print("Matrx packages are named matrx-<thing>.")
        return 1
    module = dist.replace("-", "_")
    slug = dist.removeprefix("matrx-")

    mapping = {
        "__PKG_DIST__": dist,
        "__PKG_MODULE__": module,
        "__PKG_TITLE__": args.title,
        "__PKG_SLUG__": slug,
        "__PKG_DESC__": args.desc,
    }

    target = args.dest / dist
    if target.exists():
        print(f"refusing to overwrite existing {target}")
        return 1

    for src in sorted(TEMPLATE.rglob("*")):
        rel = str(src.relative_to(TEMPLATE))
        for k, v in mapping.items():
            rel = rel.replace(k, v)
        dst = target / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text()
        for k, v in mapping.items():
            text = text.replace(k, v)
        dst.write_text(text)

    for doc in ROOT_DOCS:
        shutil.copy(TEMPLATE.parent / doc, target / doc)
    (target / "README.md").write_text(
        f"# {args.title}\n\n{args.desc}\n\nContract: [INDEPENDENCE.md](INDEPENDENCE.md).\n"
    )

    print(f"✅ created {target}")
    print("Next: wire the independence gate into the host repo's CI/release script:")
    print(f"  independence_gate.sh {target} <declared local sibling dirs...>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
