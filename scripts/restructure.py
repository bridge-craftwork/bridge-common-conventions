#!/usr/bin/env python3
"""Phase 3, step 1: put the moved files into the contract's layout.

Run once, on the tree as the two history merges left it (definitions under
conventions/, the field list at settings/fields.toml, rule files under
rules/). Driven by the inventory, so nothing is placed by hand. It is kept
for the record and for review; it refuses to run on a tree it has already
restructured.

What it does:

- definitions gain `contexts`, `implements`, `label`, `desc`,
  `taught_under` and their `[treatments.*]`, taken from the card fields
  that were their group; the seven new IDs get a definition;
- settings/fields.toml is split into settings/<section>.toml, holding the
  fields that stay settings, line for line;
- functions.toml, contexts.toml and bridge-pack.toml are written;
- alerts.toml names conventions and treatments by address;
- rule modules that take the `convention` header move beside their
  definition (their text is converted to rule language 2 in a later step);
- migrations/2-to-3.toml is generated.

Nothing else about the content changes. scripts/roundtrip.py checks that.
"""
import collections
import csv
import json
import pathlib
import re
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent
INV = HERE / "inventory"

CONTEXTS = [
    ("notrump_openings", "Notrump openings"),
    ("major_openings", "Major openings"),
    ("minor_openings", "Minor openings"),
    ("preemptive_openings", "Two-level and preemptive openings"),
    ("responses_rebids", "Responses and rebids"),
    ("slam", "Slam bidding"),
    ("overcalls", "Our overcalls"),
    ("doubles", "Our doubles"),
    ("after_interference", "After they interfere"),
    ("vs_notrump", "Defence to their notrump"),
    ("vs_openings", "Defence to their other openings"),
    ("leads", "Leads"),
    ("signals", "Signals"),
    ("general", "General approach"),
]

# Attributes a treatment keeps as the field had them, in this order.
TREATMENT_KEYS = ["kind", "label", "desc", "options", "min", "max", "default", "level",
                  "context", "value_aliases", "requires", "choice", "bid", "note",
                  "explains", "implies", "many", "heading", "about", "taught_under"]


def toml(v):
    """A TOML value on one line."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(toml(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{key(k)} = {toml(x)}" for k, x in v.items()) + " }"
    raise TypeError(type(v))


def key(k):
    return k if re.fullmatch(r"[A-Za-z0-9_-]+", k) else json.dumps(k, ensure_ascii=False)


def git(*args):
    subprocess.check_call(["git", "-C", str(HERE), *args])


def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])


def main():
    fields_file = HERE / "settings" / "fields.toml"
    if not fields_file.exists():
        sys.exit("settings/fields.toml is gone: this tree has already been restructured")

    dec = tomllib.loads((INV / "decisions.toml").read_text())
    inv_fields = {r["field"]: r for r in csv.DictReader(open(INV / "fields.csv"))}
    inv_convs = {r["id"]: r for r in csv.DictReader(open(INV / "conventions.csv"))}
    inv_mods = list(csv.DictReader(open(INV / "modules.csv")))

    raw = fields_file.read_text()
    doc = tomllib.loads(raw)
    fields = {f"{s}.{k}": v for s, fs in doc.items() for k, v in fs.items()}
    if set(fields) != set(inv_fields):
        sys.exit("settings/fields.toml and inventory/fields.csv list different fields; "
                 "run scripts/inventory.py")

    address = {p: r["address"] for p, r in inv_fields.items()}
    place_of = {p: (cid, a) for cid, sw in dec["places"].items() for p, a in sw.items()}

    def address_in(cid, path):
        """A field's address as written inside convention `cid`'s definition."""
        a = address.get(path, path)
        return a.split(":", 1)[1] if a.startswith(cid + ":") else a

    # ------------------------------------------------------------------
    # Definitions
    # ------------------------------------------------------------------
    by_conv = collections.defaultdict(list)       # id -> treatment field paths
    switch_of = collections.defaultdict(list)     # id -> switch paths
    for p, r in inv_fields.items():
        if r["becomes"] in ("treatment", "treatment (place)"):
            by_conv[r["convention"]].append(p)
        if r["becomes"] in ("convention", "treatment (place)"):
            switch_of[r["convention"]].append(p)
    order = {p: i for i, p in enumerate(fields)}   # the field list's own order
    alias_moves = {}                               # old alias path -> address

    for cid, r in sorted(inv_convs.items()):
        path = HERE / "conventions" / cid / "convention.toml"
        switches = switch_of.get(cid, [])
        single = switches[0] if len(switches) == 1 and switches[0] not in place_of else None
        sw = fields[single] if single else {}
        if path.exists():
            text = path.read_text()
            name = tomllib.loads(text)["name"]
        else:
            name = dec["new_ids"][cid]
            level = sw.get("level") or min(fields[s]["level"] for s in switches
                                           if place_of.get(s, (0, {}))[1].get("main"))
            text = f'id = {toml(cid)}\nname = {toml(name)}\nsource = "proposed"\nlevel = {level}\n'
            path.parent.mkdir(parents=True, exist_ok=True)

        head = []
        if sw.get("label") and sw["label"] != name:
            head.append(f"label = {toml(sw['label'])}")
        if sw.get("desc"):
            head.append(f"desc = {toml(sw['desc'])}")
        tail = []
        if r["contexts"]:
            tail.append(f"contexts = {toml(r['contexts'].split())}")
        if r["implements"]:
            tail.append(f"implements = {toml(r['implements'].split())}")
        also = [s for s in as_list(sw.get("skill")) if s != cid]
        if also:
            tail.append(f"taught_under = {toml(also)}")
        if single:
            for a in sw.get("aliases", []):
                alias_moves[a] = cid

        lines = text.rstrip("\n").split("\n")
        out = []
        placed_tail = False
        anchor = "level" if re.search(r"(?m)^level = ", text) else "source"
        for line in lines:
            out.append(line)
            if line.startswith("name = "):
                out.extend(head)
            if line.startswith(anchor + " = ") and not placed_tail:
                out.extend(tail)
                placed_tail = True
        if not placed_tail:
            out.extend(tail)

        for p in sorted(by_conv.get(cid, []), key=order.get):
            f = dict(fields[p])
            t = inv_fields[p]["treatment"]
            if p in place_of:
                attrs = place_of[p][1]
                if attrs.get("main"):
                    f["default"] = True
                if attrs.get("context"):
                    f["context"] = attrs["context"]
            for a in f.pop("aliases", []):
                alias_moves[a] = f"{cid}:{t}"
            own = set(as_list(sw.get("skill"))) | {cid}
            also = [s for s in as_list(f.pop("skill", None)) if s not in own]
            if also:
                f["taught_under"] = also
            if "requires" in f:
                if f["requires"] in switches:
                    del f["requires"]            # a treatment always needs its convention
                else:
                    f["requires"] = address_in(cid, f["requires"])
            if "explains" in f:
                f["explains"] = address_in(cid, f["explains"])
            if "implies" in f:
                f["implies"] = {k: address_in(cid, v) for k, v in f["implies"].items()}
            unknown = set(f) - set(TREATMENT_KEYS)
            if unknown:
                sys.exit(f"{p}: attribute(s) {sorted(unknown)} have no place in a treatment")
            out.append("")
            out.append(f"[treatments.{t}]")
            out.extend(f"{k} = {toml(f[k])}" for k in TREATMENT_KEYS if k in f)
        path.write_text("\n".join(out) + "\n")

    # ------------------------------------------------------------------
    # Settings: the field list, split by section, line for line
    # ------------------------------------------------------------------
    fn_settings = {path: (fname, part) for fname, fn in dec["functions"].items()
                   for part, path in fn.get("settings", {}).items()}
    header, sections, current = [], collections.OrderedDict(), None
    for line in raw.split("\n"):
        m = re.fullmatch(r"\[(\w+)\]", line)
        if m:
            current = m.group(1)
            sections[current] = []
            continue
        if current is None:
            header.append(line)
            continue
        fm = re.match(r'"([^"]+)"\s*=', line)
        if not fm:
            sections[current].append(line)   # comments and blank lines stay
            continue
        p = f"{current}.{fm.group(1)}"
        if inv_fields[p]["becomes"] in ("setting", "setting (parked)"):
            # Point at what moved: explains, requires and implies name fields.
            def fix(mo):
                return f'{mo.group(1)}"{address.get(mo.group(2), mo.group(2))}"'
            line = re.sub(r'((?:explains|requires) = )"([^"]+)"', fix, line)
            im = re.search(r"implies = \{([^}]*)\}", line)
            if im:
                body = re.sub(r'(= )"([^"]+)"', fix, im.group(1))
                line = line[:im.start(1)] + body + line[im.end(1):]
            sections[current].append(line)
    for section, lines in sections.items():
        while lines and not lines[-1].strip():
            lines.pop()
        while lines and not lines[0].strip():
            lines.pop(0)
        if not any(re.match(r'"', x) for x in lines):
            continue
        text = (f"# Card settings: {section}. A setting's name is `{section}.<key>`.\n"
                "# The attributes are described in settings/README.md.\n\n"
                + "\n".join(lines) + "\n")
        (HERE / "settings" / f"{section}.toml").write_text(text)
    readme = ["# Settings", "",
              "The agreements a card holds that are not conventions, one file per",
              "section. A setting's name is `<section>.<key>`",
              "(`notrump.one_nt.range_min`). See [the contract](../docs/CONTRACT.md),",
              "section 5.", "",
              "The notes below came with the field list from `convention-card`",
              "(`spec/fields.toml`, v0.44.0) and describe the attributes as they were",
              "there. Where they speak of conventions as groups with a `play` switch,",
              "the contract's definitions and treatments have replaced that.", "",
              "```"]
    readme += [re.sub(r"^# ?", "", x) for x in header if x.startswith("#")]
    readme += ["```", ""]
    (HERE / "settings" / "README.md").write_text("\n".join(readme))
    git("rm", "-q", "settings/fields.toml")

    # ------------------------------------------------------------------
    # functions.toml, contexts.toml, bridge-pack.toml
    # ------------------------------------------------------------------
    out = ["# The jobs that one convention at a time can do (docs/CONTRACT.md, section 6).",
           "# A convention says which it fills with `implements`; two conventions a card",
           "# plays for the same part are in conflict.", ""]
    for fname, fn in dec["functions"].items():
        out.append(f"[{fname}]")
        out.append(f"name = {toml(fn['name'])}")
        if "parts" in fn:
            out.append(f"parts = {toml(fn['parts'])}")
        for part, path in fn.get("settings", {}).items():
            f = fields[path]
            out.append("")
            out.append(f"# What `{path}` held in card schema 2: its label, and the")
            out.append("# words other tools write for each choice. `natural` and `other` name no")
            out.append("# convention, so a card that held them has no entry for this part.")
            out.append(f"[{fname}.was.{part}]")
            out.append(f"setting = {toml(path)}")
            out.append(f"label = {toml(f['label'])}")
            out.append(f"options = {toml(f['options'])}")
            if "value_aliases" in f:
                out.append(f"value_aliases = {toml(f['value_aliases'])}")
            also = [s for s in as_list(f.get("skill")) if s not in fn["options"].values()]
            if also:
                out.append(f"taught_under = {toml(also)}")
            for a in f.get("aliases", []):
                alias_moves[a] = path
        if "options" in fn:
            out.append("")
            out.append(f"[{fname}.option]")
            out.extend(f"{key(k)} = {toml(v)}" for k, v in fn["options"].items())
        out.append("")
    (HERE / "functions.toml").write_text("\n".join(out))

    out = ["# Where a convention applies (docs/CONTRACT.md, section 6), in display order.",
           "# A key never changes; a name may.", ""]
    for k, name in CONTEXTS:
        out += [f"[{k}]", f"name = {toml(name)}", ""]
    (HERE / "contexts.toml").write_text("\n".join(out))

    (HERE / "bridge-pack.toml").write_text(
        'name = "bridge-common-conventions"\n'
        'description = "bridge-craftwork\'s conventions, card settings and bidding rules"\n'
        "pack_format_version = 1\n"
        "card_schema_version = 3\n"
        "# The rule files are still in rule language 1; they are converted in the\n"
        "# next step of Phase 3.\n"
        "rule_language_version = 1\n")

    # ------------------------------------------------------------------
    # alerts.toml: name conventions and treatments by address
    # ------------------------------------------------------------------
    alerts = (HERE / "alerts.toml").read_text()

    def alert_fields(mo):
        names = re.findall(r'"([^"]+)"', mo.group(1))
        missing = [n for n in names if n not in address]
        if missing:
            sys.exit(f"alerts.toml names {missing}, not a card field")
        return "fields = " + toml([address[n] for n in names])
    alerts = re.sub(r"(?m)^fields = (\[.*\])$", alert_fields, alerts)
    (HERE / "alerts.toml").write_text(alerts)

    # ------------------------------------------------------------------
    # Rule modules beside their definitions
    # ------------------------------------------------------------------
    for m in inv_mods:
        if not m["convention"]:
            continue
        src = pathlib.PurePath("rules") / pathlib.PurePath(m["today"]).relative_to("conventions")
        dst = pathlib.PurePath(m["place"]).parent
        stem = src.name[:-len(".bid")]
        for ext in (".bid", ".test", ".notes.md"):
            f = src.with_name(stem + ext)
            if (HERE / f).exists():
                git("mv", str(f), str(dst / f.name))

    # ------------------------------------------------------------------
    # migrations/2-to-3.toml
    # ------------------------------------------------------------------
    out = [
        "# Card schema 2.0 -> 3.0: conventions are entries keyed by ID",
        "# (docs/CONTRACT.md, section 8; issue #3).",
        "#",
        "# Generated from the Phase 1 inventory (inventory/, scripts/restructure.py).",
        "# Permanent once published: it is how cards, files and PDFs already in",
        "# people's hands keep loading.",
        "#",
        "# A schema 2 card is nested `card_data`; every path below is a full dotted",
        "# path into it. A schema 3 card has `conventions`, keyed by ID, and",
        "# `settings`, the nested form of every path not named here.",
        "#",
        "# [convention]  \"switch path\" = \"ID\". The switch is the entry's `play`:",
        "#               true -> an entry (`play` left out); false -> `play = false`.",
        "#               Unset: an entry, played, when any of the convention's",
        "#               treatments below is on or filled in; otherwise no entry",
        "#               (Rick Wilson, 2026-11-13).",
        "# [treatment]   \"field path\" = \"ID:treatment\". The value moves into that",
        "#               entry under the treatment's name.",
        "# [[place]]     One convention played in several places, each a yes/no",
        "#               switch in schema 2. The entry is played when any place is",
        "#               on; every place is written, true or false, so the entry",
        "#               never falls back on a default. All false or unset with no",
        "#               treatment on: `play = false` when any was false, else no",
        "#               entry.",
        "# [[function]]  A setting whose value named a convention. The option's",
        "#               convention gets an entry. Where the function has parts",
        "#               (`strong`, `weak`), an entry chosen for only some of them",
        "#               lists them in `for`. Options with no convention (`natural`,",
        "#               `other`) leave no entry. `unless_chosen` names a switch",
        "#               that turned its convention on only while the setting was",
        "#               unset or `other`: schema 2's precedence, kept.",
        "# [alias]       \"older path\" = \"address\": spellings schema 2 still read.",
        "# Everything else moves to `settings` at the same path.",
        "",
        'from = "2.0"',
        'to = "3.0"',
        "",
        "[convention]",
    ]
    unless = {"competitive.dont.play"}
    for p, r in inv_fields.items():
        if r["becomes"] == "convention":
            out.append(f"{toml(p)} = {toml(r['convention'])}")
    out += ["", "[treatment]"]
    for p, r in inv_fields.items():
        if r["becomes"] == "treatment":
            out.append(f"{toml(p)} = {toml(r['address'])}")
    for cid, sw in dec["places"].items():
        out += ["", "[[place]]", f"convention = {toml(cid)}"]
        out.append("switches = " + toml({p: a["treatment"] for p, a in sw.items()}))
    for fname, fn in dec["functions"].items():
        if "settings" not in fn:
            continue
        out += ["", "[[function]]", f"function = {toml(fname)}",
                f"settings = {toml(fn['settings'])}",
                f"options = {toml(fn['options'])}",
                'no_entry = ["natural", "other"]',
                f"unless_chosen = {toml(sorted(unless))}"]
    out += ["", "[alias]"]
    for a, target in sorted(alias_moves.items()):
        out.append(f"{toml(a)} = {toml(target)}")
    (HERE / "migrations" / "2-to-3.toml").write_text("\n".join(out) + "\n")

    git("rm", "-q", "rules/conventions.toml")
    print("restructured:", len(inv_convs), "definitions,", len(sections), "sections,",
          sum(1 for m in inv_mods if m["convention"]), "modules moved,",
          len(alias_moves), "aliases")


if __name__ == "__main__":
    main()
