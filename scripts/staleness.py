#!/usr/bin/env python3
"""Is the published snapshot behind `main`?

Compares the commit the snapshot on the `published` branch was built from
(its manifest's `source_commit`) with the head of `main`. The snapshot is
behind when `main` has a later commit that changes a source file of the
pack; a commit that touches only docs or scripts does not count.

    python3 scripts/staleness.py [--remote origin]

Exit status 0 when the snapshot is current, 1 when it is behind or missing.
A reader of the snapshot can make the same check from the two branches'
heads; the publish workflow runs this on a schedule, because the usual cause
is that the workflow stopped running (Actions disabled on a copy of the
repository, or a failing check nobody saw).
"""
import argparse
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_snapshot import HERE, SOURCES  # noqa: E402


def git(*args):
    return subprocess.run(["git", "-C", str(HERE), *args], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--no-fetch", action="store_true", help="compare the branches as already fetched")
    args = ap.parse_args()
    main_ref, published = f"{args.remote}/main", f"{args.remote}/published"
    if not args.no_fetch:
        git("fetch", "--quiet", args.remote, "main", "published")
    shown = git("show", f"{published}:manifest.json")
    if shown.returncode:
        sys.exit(f"There is no published snapshot on {published}: check that Actions are enabled "
                 "and the publish workflow has run.")
    manifest = json.loads(shown.stdout)
    built = manifest.get("source_commit")
    behind = git("rev-list", "--first-parent", f"{built}..{main_ref}", "--", *SOURCES)
    if behind.returncode:
        sys.exit(f"The published snapshot was built from {built}, which is not in {main_ref}'s history.")
    commits = behind.stdout.split()
    if commits:
        sys.exit(f"Published rules are behind: {len(commits)} change(s) on main since {built[:12]} "
                 f"(rules number {manifest.get('rules_number')}). Check that Actions are enabled "
                 "and that the publish workflow's last run passed.")
    print(f"Published rules are current: rules number {manifest.get('rules_number')}, built from {built[:12]}.")


if __name__ == "__main__":
    main()
