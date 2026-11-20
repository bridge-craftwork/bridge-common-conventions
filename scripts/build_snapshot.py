#!/usr/bin/env python3
"""Build the published snapshot of the pack (docs/CONTRACT.md, section 10).

Writes two files to --out:

- pack.json: everything in the pack as one JSON document, for readers that
  cannot list a directory or parse TOML (a web page). Rule, test and notes
  files are carried as their source text, keyed by path.
- manifest.json: each source file's hash and the date it last changed, the
  commit it was built from, the pack's format numbers, the rules number and
  the engine the rules were checked with.

    python3 scripts/build_snapshot.py --out DIR [--engine "rbb 0.16.0"]

The pack is checked first (scripts/check.py); a pack that fails is not
built. Standard library only (Python 3.11+, for tomllib).

The publish workflow (.github/workflows/publish.yml) runs this after the
engine has checked the rules and run their tests, and pushes the result to
the `published` branch.

The rules number is the count of commits on the first-parent history of the
commit built from that changed a source file of the pack (SOURCES), leaving
out the files that cannot change a bid: notes (`.notes.md`) and tests
(`.test`). It only increases while that history is not rewritten, and two
snapshots with the same number bid the same. Nothing in either file depends
on when the build ran, so the same commit always gives the same bytes.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent
TEXT = (".bid", ".test", ".notes.md", ".dlr")
# What a pack is made of. A commit that touches none of these does not
# change the snapshot.
SOURCES = ["bridge-pack.toml", "conventions", "skills", "rules", "settings", "contexts.toml",
           "functions.toml", "levels.toml", "alerts.toml", "announced-names.toml", "deals.toml",
           "migrations"]
# Source files that cannot change a bid. A commit that changes only these
# changes the snapshot but not the rules number.
NOT_RULES = [":(exclude,glob)**/*.notes.md", ":(exclude,glob)**/*.test"]


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def history(root):
    """The commit built from, the rules number, and each file's last change."""
    commit = git(root, "rev-parse", "HEAD").strip()
    number = int(git(root, "rev-list", "--count", "--first-parent", "HEAD", "--",
                     *SOURCES, *NOT_RULES).strip())
    changed = {}
    log = git(root, "log", "--format=%x00%cI", "--name-only", "--", *SOURCES)
    for block in log.split("\x00")[1:]:
        date, *names = [line for line in block.split("\n") if line]
        for name in names:
            changed.setdefault(name, date)
    return commit, number, changed


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
    skills = {}
    for f in sorted((root / "skills").glob("*/*/skill.toml")):
        d = read(f)
        skills[d["id"]] = d
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
        "skills": dict(sorted(skills.items())),
        "settings": {f.stem: read(f) for f in sorted((root / "settings").glob("*.toml"))},
        "contexts": read(root / "contexts.toml"),
        "functions": read(root / "functions.toml"),
        "levels": read(root / "levels.toml"),
        "alerts": read(root / "alerts.toml"),
        # Optional: an engine that does not read it ignores the key.
        "announced_names": read(root / "announced-names.toml") if (root / "announced-names.toml").is_file() else {},
        "deals": read(root / "deals.toml") if (root / "deals.toml").is_file() else {},
        "migrations": {f.stem: read(f) for f in sorted((root / "migrations").glob("*.toml"))},
        "files": files,
    }
    return pack, sources


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--root", type=pathlib.Path, default=HERE)
    ap.add_argument("--no-check", action="store_true", help="build without checking the pack first")
    ap.add_argument("--engine", help="the engine the rules were checked and tested with (`rbb -V`)")
    args = ap.parse_args()

    if not args.no_check:
        check = subprocess.run([sys.executable, str(HERE / "scripts" / "check.py")],
                               capture_output=True, text=True)
        if check.returncode:
            sys.exit("The pack does not pass its check; nothing was built.\n" + check.stdout + check.stderr)

    pack, sources = build(args.root)
    try:
        commit, number, changed = history(args.root)
        dirty = bool(git(args.root, "status", "--porcelain", "--", *SOURCES).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit, number, changed, dirty = None, None, {}, False
    names = [s.relative_to(args.root).as_posix() for s in sorted(sources)]
    manifest = {
        "schema": "pack-manifest/v1",
        "source_commit": commit,
        **({"uncommitted_changes": True} if dirty else {}),
        "rules_number": number,
        **{k: v for k, v in pack["pack"].items() if k.endswith("_version") or k == "name"},
        **({"checked_with": args.engine} if args.engine else {}),
        "files": {n: {"sha256": hashlib.sha256((args.root / n).read_bytes()).hexdigest(),
                      "changed": changed.get(n)} for n in names},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(pack, ensure_ascii=False, indent=1) + "\n"
    (args.out / "pack.json").write_text(text)
    manifest["pack_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"rules number {number} from {commit}: {len(pack['conventions'])} definitions, {sum(len(s) for s in pack['settings'].values())} settings, "
          f"{len(pack['files'])} rule, test and notes files: {len(text) // 1024} KB")


if __name__ == "__main__":
    main()
