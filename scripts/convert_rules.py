#!/usr/bin/env python3
"""Phase 3, step 2: convert the rule files' headers to rule language 2.

Run once, after scripts/restructure.py. Only `card` and `param` lines in a
module's header change; no rule does.

- A card field's schema 2 path becomes its address (the inventory's):
  `slam.rkcb.play` is `bidding_conventions/roman_keycard`, and
  `slam.rkcb.style` is `bidding_conventions/roman_keycard:style`.
- In a module that sits beside its definition, `card <its switch>` becomes
  `convention <id>`, and its own treatments are written by bare name.
- A module switched by a place (`notrump.lebensohl.play`) gets
  `convention <id>` and `card <the place's treatment>`.

Not converted yet: the two defence-to-1NT settings
(`competitive.vs_1nt_strong.system`), which the rules still read as schema 2
option words. The engine keeps them readable; reading the function
(`defence_to_1nt.strong`) as an ID waits for the rule language to compare
IDs. The modules that would then take a `convention` header (DONT,
Meckwell, Suction) have none until then.
"""
import csv
import pathlib
import re
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent


def main():
    manifest = HERE / "bridge-pack.toml"
    if "rule_language_version = 2" in manifest.read_text():
        sys.exit("the rule files are already in rule language 2")
    dec = tomllib.loads((HERE / "inventory" / "decisions.toml").read_text())
    fields = {r["field"]: r for r in csv.DictReader(open(HERE / "inventory" / "fields.csv"))}
    modules = {r["module"]: r for r in csv.DictReader(open(HERE / "inventory" / "modules.csv"))}
    keep = {p for fn in dec["functions"].values() for p in fn.get("settings", {}).values()}
    places = {p: (cid, a["treatment"]) for cid, sw in dec["places"].items() for p, a in sw.items()}

    changed = lines_changed = headers = 0
    for f in sorted(HERE.rglob("*.bid")):
        text = f.read_text()
        m = re.search(r"(?m)^module\s+(\S+)", text)
        mod = modules[m.group(1)]
        own = mod["convention"] if mod["switched_by"].startswith("card") else ""
        out, in_header, touched = [], False, False

        def address(path):
            if path in keep or path not in fields:
                return path
            a = fields[path]["address"]
            if own and a.startswith(own + ":"):
                return a.split(":", 1)[1]
            return a

        for line in text.split("\n"):
            if line.startswith("module "):
                in_header = True
                out.append(line)
                continue
            if in_header and line and not line[0].isspace() and not line.startswith("#"):
                in_header = False
            if not in_header:
                out.append(line)
                continue
            c = re.match(r"^(\s+)card(\s+)(\S+)(.*)$", line)
            p = re.match(r"^(\s+param\s+\w+\s*=\s*)(\S+)(.*)$", line)
            new = line
            if c:
                indent, gap, path, rest = c.groups()
                r = fields.get(path)
                if own and r and r["becomes"] == "convention" and r["convention"] == own:
                    new = f"{indent}convention  {own}{rest}"
                    headers += 1
                elif own and path in places and places[path][0] == own:
                    new = f"{indent}convention  {own}\n{indent}card{gap}{places[path][1]}{rest}"
                    headers += 1
                else:
                    new = f"{indent}card{gap}{address(path)}{rest}"
            elif p:
                head, path, rest = p.groups()
                new = f"{head}{address(path)}{rest}"
            if new != line:
                lines_changed += 1
                touched = True
            out.append(new)
        if touched:
            # `convention` comes before every `card` and `param` line.
            f.write_text("\n".join(out))
            changed += 1
    manifest.write_text(re.sub(r"# The rule files are still.*\n# next step.*\n", "", manifest.read_text())
                        .replace("rule_language_version = 1", "rule_language_version = 2"))
    print(f"{changed} rule files, {lines_changed} header lines, {headers} `convention` headers")


if __name__ == "__main__":
    main()
