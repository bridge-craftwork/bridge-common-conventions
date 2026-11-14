#!/usr/bin/env python3
"""Name the settings on a rule test's `card` lines by address (Phase 3).

A `.test` file sets its card with `card <name> <path>=<value> ...`. The
paths were card schema 2's; this rewrites each to the address the pack gives
it (migrations/2-to-3.toml): a convention's ID, `<id>:<treatment>`, or a
function's part with the ID of the convention that fills it.

    python3 scripts/convert_tests.py          # rewrite the files
    python3 scripts/convert_tests.py --check  # exit 1 if any would change

A setting that stays a setting keeps its path. Run once; kept for the record.
"""
import pathlib
import re
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent


def main():
    mig = tomllib.loads((HERE / "migrations" / "2-to-3.toml").read_text())
    address = dict(mig["convention"])
    address.update(mig["treatment"])
    for place in mig["place"]:
        for path, t in place["switches"].items():
            address[path] = f"{place['convention']}:{t}"
    address.update(mig["alias"])
    functions = {}
    for f in mig["function"]:
        for part, path in f["settings"].items():
            functions[path] = (f"{f['function']}.{part}", f["options"])

    def token(tok):
        path, eq, value = tok.partition("=")
        if not eq:
            return tok
        if path in functions:
            name, options = functions[path]
            # `natural` and `other` named no convention.
            return f"{name}={options.get(value, 'none')}"
        return f"{address.get(path, path)}={value}"

    changed = 0
    files = subprocess.check_output(["git", "-C", str(HERE), "ls-files", "*.test"], text=True).split()
    for name in files:
        f = HERE / name
        out = []
        for line in f.read_text().split("\n"):
            m = re.match(r"(\s*card\s+\S+)(.*)", line)
            if m and "=" in m.group(2):
                rest = re.sub(r"\S+", lambda t: token(t.group(0)), m.group(2))
                line = m.group(1) + rest
            out.append(line)
        text = "\n".join(out)
        if text != f.read_text():
            changed += 1
            if "--check" not in sys.argv:
                f.write_text(text)
    print(f"{changed} of {len(files)} test files {'would change' if '--check' in sys.argv else 'changed'}")
    sys.exit(1 if changed and "--check" in sys.argv else 0)


if __name__ == "__main__":
    main()
