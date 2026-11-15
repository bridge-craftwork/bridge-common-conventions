#!/usr/bin/env python3
"""Check that the restructured pack lost nothing (Phase 3).

Rebuilds card schema 2's field list from the pack (definitions, settings,
functions and migrations/2-to-3.toml) and compares it, attribute by
attribute, with convention-card's spec/fields.toml at the tag the content
came from. Also compares every definition's own keys with its file at the
tag, and every rule file's text with rusty-bidding-bot's.

    python3 scripts/roundtrip.py

Exit status 0 when the only differences are the ones listed in EXPECTED,
each of which says where that information now lives.
"""
import json
import pathlib
import re
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent

# Attributes of schema 2 fields that the pack holds in another form. None:
# migrations/2-to-3.toml records the few there were under `was`.
EXPECTED = {}


# Rule files rewritten to read a function (`defence_to_1nt.strong`, `opening.2d`) by the ID of the
# convention that fills it, where they compared schema 2's option words.
# Their text is not compared; the rule tests and the bidding comparison
# (before/README.md) are what hold them.
BY_FUNCTION = {"dont.bid", "meckwell.bid", "suction.bid", "cappelletti.bid", "preempts.bid",
               "multi-landy.bid", "vs-1nt.bid", "overcalls.bid"}

# Corrections: text that differs from the tag on purpose (Phase 5).
CORRECTED = {
    ("two_level.reverse_flannery.play", "desc"):
        "Reverse Flannery is responder's jump over one of a minor, not an opening (Rick, 2026-11-14)",
    ("bidding_conventions/reverse_flannery", "summary"): "the same",
    ("bidding_conventions/reverse_flannery", "desc"): "the same",
    ("bidding_conventions/reverse_flannery", "contexts"): "the same",
    ("two_level.reverse_flannery.two_d", "retired"):
        "#69: left from the 2♦ opening Reverse Flannery never was (Rick, 2026-11-14)",
}

# Rule files whose bidding was corrected on purpose (Phase 5), and why.
# Their text is no longer the tag's; the rule tests and the reviewed
# differences are what hold them.
CORRECTED_RULES = {
    "weak-jump-shifts.bid": "#74: the not-in-competition box counts; follow-ups only after a real jump",
    "after-interference.bid": "#67: a jump shift after an overcall is weak unless the card says strong",
    "weak-jump-shifts.test": "#74: cases added", "soloway.bid": "#74",
    "bergen.test": "#33: the Reverse Bergen card switches Bergen on",
    "reverse-flannery.notes.md": "#69: its open question is answered",
    "reverse-flannery.bid": "#69: a jump it takes is not also a strong jump shift",
    "reverse-flannery.test": "#69: case added",
    "stayman.bid": "#73: on for a silent card", "jacoby-transfers.bid": "#73: on for a silent card", "responses.bid": "#74, #69", "rebids.bid": "#74", "responder-rebids.bid": "#74",
}

# Files that did not stay in the pack, and where they went.
ELSEWHERE = {
    "stock-cards.test": "rusty-bidding-bot's cards/: it tests the engine's stock cards, which the pack does not hold",
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode()


def renamed(text):
    """Robert S. Todd's site is named as it is today: at the tag our files
    called it by its old name (Rick, 2026-11-14)."""
    return text.replace("Advancing" + " in Bridge", "Adventures in Bridge")


def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])


def main():
    dec = tomllib.loads((HERE / "inventory" / "decisions.toml").read_text())
    cc = HERE.parent / "convention-card"
    rbb = HERE.parent / "rusty-bidding-bot"
    cc_tag, rbb_tag = dec["sources"]["convention_card"], dec["sources"]["rusty_bidding_bot"]
    doc = tomllib.loads(git(cc, "show", f"{cc_tag}:spec/fields.toml"))
    want = {f"{s}.{k}": v for s, fs in doc.items() for k, v in fs.items()}

    mig = tomllib.loads((HERE / "migrations" / "2-to-3.toml").read_text())
    defs = {}
    for f in (HERE / "conventions").glob("*/*/convention.toml"):
        d = tomllib.loads(f.read_text())
        defs[d["id"]] = d
    functions = tomllib.loads((HERE / "functions.toml").read_text())

    # address -> schema 2 path
    back = {v: k for k, v in mig["convention"].items()}
    back.update({v: k for k, v in mig["treatment"].items()})
    for place in mig["place"]:
        for path, t in place["switches"].items():
            back[f"{place['convention']}:{t}"] = path

    def path_of(cid, a):
        return back.get(a) or back.get(f"{cid}:{a}") or a

    got = {}
    for fname, fn in functions.items():
        for part, was in fn.get("was", {}).items():
            back[f"{fname}.{part}"] = was["setting"]
    # settings
    for f in (HERE / "settings").glob("*.toml"):
        for k, v in tomllib.loads(f.read_text()).items():
            v = dict(v)
            for a in ("explains", "requires"):
                if a in v:
                    v[a] = back.get(v[a], v[a])
            if "implies" in v:
                v["implies"] = {i: back.get(p, p) for i, p in v["implies"].items()}
            got[f"{f.stem}.{k}"] = v
    # the settings that became entries through a function
    for fname, fn in functions.items():
        for part, was in fn.get("was", {}).items():
            got[was["setting"]] = {"kind": "enum", **{k: x for k, x in was.items() if k != "setting"}}
            back[f"{fname}.{part}"] = was["setting"]
    # switches and treatments
    places = {p: (pl["convention"], t) for pl in mig["place"] for p, t in pl["switches"].items()}
    for path, cid in mig["convention"].items():
        d = defs[cid]
        new = cid in mig.get("new_ids", [])
        v = {"kind": "bool", "label": d.get("label", d["name"]), "level": d["level"]}
        if "desc" in d:
            v["desc"] = d["desc"]
        skill = ([] if new else [cid]) + d.get("taught_under", [])
        if skill:
            v["skill"] = skill
        got[path] = v
    for cid, d in defs.items():
        single = [p for p, c in mig["convention"].items() if c == cid]
        base = as_list(want[single[0]].get("skill")) if single else [cid]
        for t, a in d.get("treatments", {}).items():
            path = back[f"{cid}:{t}"]
            v = dict(a)
            is_place = path in places
            if is_place:
                if v.get("default") is True:
                    del v["default"]
                v.pop("context", None)
            v.pop("implements", None)
            v.pop("independent", None)
            v.pop("brief", None)
            skill = v.pop("skill", None)
            also = v.pop("taught_under", None)
            if skill is None:
                v["skill"] = base + (also or [])
            elif skill is not False:
                v["skill"] = as_list(skill)
            if not v.get("skill"):
                v.pop("skill", None)
            for k in ("explains", "requires"):
                if k in v:
                    v[k] = path_of(cid, v[k])
            if "implies" in v:
                v["implies"] = {i: path_of(cid, p) for i, p in v["implies"].items()}
            got[path] = v
    aliases = {}
    for old, target in mig["alias"].items():
        aliases.setdefault(back.get(target, target), []).append(old)
    for path, olds in aliases.items():
        got[path]["aliases"] = sorted(olds)

    for path, attrs in mig.get("was", {}).items():
        got[path].update(attrs)
    if list(want) != [p for p in mig.get("order", []) if p in want]:
        got["(order)"] = {}

    problems, expected, corrected = [], [], []
    for path in sorted(set(want) | set(got)):
        if path not in got:
            problems.append(f"{path}: not in the pack")
            continue
        if path not in want:
            problems.append(f"{path}: in the pack, not at {cc_tag}")
            continue
        w, g = dict(want[path]), dict(got[path])
        for x in (w, g):
            if "skill" in x:
                x["skill"] = as_list(x["skill"])
        if "aliases" in w:
            w["aliases"] = sorted(w["aliases"])
        for k in sorted(set(w) | set(g)):
            if w.get(k) != g.get(k):
                if (path, k) in CORRECTED:
                    corrected.append(f"{path} {k}: {CORRECTED[(path, k)]}")
                elif (path, k) in EXPECTED:
                    expected.append(f"{path} {k}: {EXPECTED[(path, k)]}")
                else:
                    problems.append(f"{path} {k}: {w.get(k)!r} at the tag, {g.get(k)!r} from the pack")

    # definitions: every key the file had at the tag is unchanged
    names = git(cc, "ls-tree", "-r", "--name-only", cc_tag, "spec/conventions").split()
    seen = 0
    for name in names:
        if name.count("/") != 3 or not name.endswith(".toml"):
            continue
        old = tomllib.loads(git(cc, "show", f"{cc_tag}:{name}"))
        if "id" not in old:
            continue
        seen += 1
        new = defs.get(old["id"])
        if new is None:
            problems.append(f"{old['id']}: definition missing")
            continue
        for k, v in old.items():
            # Sources may be added (scripts/find_references.py); none is dropped.
            if k == "see" and all(json.loads(renamed(json.dumps(e, ensure_ascii=False))) in new.get("see", []) for e in v):
                continue
            if new.get(k) != v:
                if (old["id"], k) in CORRECTED:
                    corrected.append(f"{old['id']} {k}: {CORRECTED[(old['id'], k)]}")
                else:
                    problems.append(f"{old['id']} {k}: changed")

    # rule files: the same bytes, wherever they sit now
    here = {f.name: f for f in HERE.rglob("*") if f.suffix in (".bid", ".test") or f.name.endswith(".notes.md")}
    rules = converted = by_function = 0
    for name in git(rbb, "ls-tree", "-r", "--name-only", rbb_tag, "conventions").split("\n"):
        base = name.rsplit("/", 1)[-1]
        if not (base.endswith((".bid", ".test", ".notes.md"))):
            continue
        rules += 1
        if base in ELSEWHERE:
            continue
        if base not in here:
            problems.append(f"{name}: not in the pack")
        elif here[base].read_text() != renamed(git(rbb, "show", f"{rbb_tag}:{name}")):
            # A .bid file's header is converted to rule language 2
            # (scripts/convert_rules.py); everything below it is unchanged.
            old = renamed(git(rbb, "show", f"{rbb_tag}:{name}")).split("\n")
            new = here[base].read_text().split("\n")
            # A .test file's `card` lines name settings by address
            # (scripts/convert_tests.py). The rules that read the defence to
            # 1NT compare the function with an ID, in their conditions too.
            # A comment cannot change a bid, so comment lines are not held
            # to the tag either (a source's URL added to a header).
            body = lambda ls: [l for l in ls if not re.match(r"\s*(card|param|convention)\s|\s*#", l)]
            if base in BY_FUNCTION or base in CORRECTED_RULES:
                by_function += 1
            elif not base.endswith((".bid", ".test")) or body(old) != body(new):
                problems.append(f"{name}: text differs from {here[base].relative_to(HERE)}")
            else:
                converted += 1

    print(f"{len(want)} card fields, {seen} definitions and {rules} rule files compared "
          f"with convention-card {cc_tag} and rusty-bidding-bot {rbb_tag}.")
    print(f"{converted} rule and test files differ from the tag only in their card, param and convention lines; "
          f"{by_function} read a function or were corrected; {len(ELSEWHERE)} moved out.")
    print(f"\nHeld in another form ({len(expected)}):")
    for e in expected:
        print("  " + e)
    print(f"\nCorrected on purpose ({len(corrected)}):")
    for c in corrected:
        print("  " + c)
    print(f"\nProblems ({len(problems)}):")
    for p in problems[:60]:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
