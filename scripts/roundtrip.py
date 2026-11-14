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
import pathlib
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent

# Attributes of schema 2 fields that the pack holds in another form.
EXPECTED = {
    ("major_openings.bergen_raises.play", "choice"):
        "Bergen or Reverse Bergen was a choice between the switch and a treatment; "
        "in schema 3 the entry is played either way and `reverse` says which",
    ("slam.blackwood.play", "choice"): "the `ace_ask` function",
    ("slam.rkcb.play", "choice"): "the `ace_ask` function",
    ("competitive.leaping_michaels.play", "choice"): "the `michaels_vs_preempts` function",
    ("competitive.non_leaping_michaels.play", "choice"): "the `michaels_vs_preempts` function",
    ("two_level.parrish_bust.relay", "requires"):
        "it required its own convention's switch, which a treatment always does",
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode()


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
            v = {"kind": "enum", "label": was["label"], "options": was["options"]}
            if "value_aliases" in was:
                v["value_aliases"] = was["value_aliases"]
            for k in ("desc", "level", "skill"):
                if k in was:
                    v[k] = was[k]
            got[was["setting"]] = v
            back[f"{fname}.{part}"] = was["setting"]
    # switches and treatments
    places = {p: (pl["convention"], t) for pl in mig["place"] for p, t in pl["switches"].items()}
    for path, cid in mig["convention"].items():
        d = defs[cid]
        new = cid in dec["new_ids"]
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

    problems, expected = [], []
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
                if (path, k) in EXPECTED:
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
            if new.get(k) != v:
                problems.append(f"{old['id']} {k}: changed")

    # rule files: the same bytes, wherever they sit now
    here = {f.name: f for f in HERE.rglob("*") if f.suffix in (".bid", ".test") or f.name.endswith(".notes.md")}
    rules = 0
    for name in git(rbb, "ls-tree", "-r", "--name-only", rbb_tag, "conventions").split("\n"):
        base = name.rsplit("/", 1)[-1]
        if not (base.endswith((".bid", ".test", ".notes.md"))):
            continue
        rules += 1
        if base not in here:
            problems.append(f"{name}: not in the pack")
        elif here[base].read_text() != git(rbb, "show", f"{rbb_tag}:{name}"):
            problems.append(f"{name}: text differs from {here[base].relative_to(HERE)}")

    print(f"{len(want)} card fields, {seen} definitions and {rules} rule files compared "
          f"with convention-card {cc_tag} and rusty-bidding-bot {rbb_tag}.")
    print(f"\nHeld in another form ({len(expected)}):")
    for e in expected:
        print("  " + e)
    print(f"\nProblems ({len(problems)}):")
    for p in problems[:60]:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
