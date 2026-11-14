#!/usr/bin/env python3
"""Build the published snapshot of the pack (docs/CONTRACT.md, section 10).

Writes two files to --out:

- pack.json: everything in the pack as one JSON document, for readers that
  cannot list a directory or parse TOML (a web page). Rule, test and notes
  files are carried as their source text, keyed by path.
- manifest.json: each source file's hash, the commit it was built from and
  the pack's format numbers.

    python3 scripts/build_snapshot.py --out DIR

The pack is checked first (scripts/check.py); a pack that fails is not
built. Standard library only (Python 3.11+, for tomllib).

The publish pipeline (Phase 4) runs this and pushes the result to the
`published` branch. The rules number and each file's last-changed date are
settled there and are not in the manifest yet.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent
TEXT = (".bid", ".test", ".notes.md")


def toml(path):
    return tomllib.loads(path.read_text())


def build(root):
    """The snapshot of the pack at `root`, and the source files it was built from."""
    sources = []

    def read(path):
        sources.append(path)
        return toml(path)

    conventions = {}
    for f in sorted((root / "conventions").glob("*/*/convention.toml")):
        d = read(f)
        conventions[d["id"]] = d
    files = {}
    for folder in ("conventions", "rules"):
        for f in sorted((root / folder).rglob("*")):
            if f.is_file() and f.name.endswith(TEXT):
                sources.append(f)
                files[f.relative_to(root).as_posix()] = f.read_text()
    pack = {
        "schema": "pack/v1",
        "pack": read(root / "bridge-pack.toml"),
        "categories": read(root / "conventions" / "categories.toml"),
        "conventions": dict(sorted(conventions.items())),
        "settings": {f.stem: read(f) for f in sorted((root / "settings").glob("*.toml"))},
        "contexts": read(root / "contexts.toml"),
        "functions": read(root / "functions.toml"),
        "levels": read(root / "levels.toml"),
        "alerts": read(root / "alerts.toml"),
        "migrations": {f.stem: read(f) for f in sorted((root / "migrations").glob("*.toml"))},
        "files": files,
    }
    return pack, sources


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--root", type=pathlib.Path, default=HERE)
    ap.add_argument("--no-check", action="store_true", help="build without checking the pack first")
    args = ap.parse_args()

    if not args.no_check:
        check = subprocess.run([sys.executable, str(HERE / "scripts" / "check.py")],
                               capture_output=True, text=True)
        if check.returncode:
            sys.exit("The pack does not pass its check; nothing was built.\n" + check.stdout + check.stderr)

    pack, sources = build(args.root)
    try:
        commit = subprocess.check_output(["git", "-C", str(args.root), "rev-parse", "HEAD"],
                                         text=True).strip()
        dirty = bool(subprocess.check_output(["git", "-C", str(args.root), "status", "--porcelain",
                                              "--", *[str(s) for s in sources]], text=True).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit, dirty = None, False
    manifest = {
        "schema": "pack-manifest/v1",
        "source_commit": commit,
        **({"uncommitted_changes": True} if dirty else {}),
        **{k: v for k, v in pack["pack"].items() if k.endswith("_version") or k == "name"},
        "files": {s.relative_to(args.root).as_posix(): hashlib.sha256(s.read_bytes()).hexdigest()
                  for s in sorted(sources)},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(pack, ensure_ascii=False, indent=1) + "\n"
    (args.out / "pack.json").write_text(text)
    manifest["pack_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"{len(pack['conventions'])} definitions, {sum(len(s) for s in pack['settings'].values())} settings, "
          f"{len(pack['files'])} rule, test and notes files: {len(text) // 1024} KB")


if __name__ == "__main__":
    main()
