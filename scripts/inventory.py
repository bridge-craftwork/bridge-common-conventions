#!/usr/bin/env python3
"""Build the Phase 1 inventory: every card field, convention and rule module,
and what each becomes.

Reads convention-card and rusty-bidding-bot at the tags named in
inventory/decisions.toml (through git, so the working trees do not matter),
plus the hand decisions in that file. Writes inventory/*.csv and
inventory/SUMMARY.md. Run again after any change to decisions.toml:

    python3 scripts/inventory.py [--convention-card PATH] [--rusty-bidding-bot PATH]
"""
import argparse
import collections
import csv
import pathlib
import re
import subprocess
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT = HERE / "inventory"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode()


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_fields(repo, tag):
    doc = tomllib.loads(git(repo, "show", f"{tag}:spec/fields.toml"))
    fields = {}
    for section, entries in doc.items():
        if not isinstance(entries, dict):
            continue
        for key, attrs in entries.items():
            if isinstance(attrs, dict) and "kind" in attrs:
                fields[f"{section}.{key}"] = attrs
    return fields


def load_definitions(repo, tag):
    defs = {}
    names = git(repo, "ls-tree", "-r", "--name-only", tag, "spec/conventions").split()
    for name in names:
        if not name.endswith(".toml") or name.count("/") != 3:
            continue
        doc = tomllib.loads(git(repo, "show", f"{tag}:{name}"))
        if "id" in doc:
            defs[doc["id"]] = doc
    return defs


def load_modules(repo, tag):
    """Every .bid file's header: module, kind, card, skill and param lines."""
    mods = []
    names = git(repo, "ls-tree", "-r", "--name-only", tag, "conventions").split("\n")
    for name in sorted(n for n in names if n.endswith(".bid")):
        text = git(repo, "show", f"{tag}:{name}")
        m = {"path": name, "name": "", "title": "", "kind": "", "card": [],
             "skill": [], "params": [], "text": text}
        for line in text.split("\n"):
            if line.startswith("#"):
                continue
            w = line.split()
            if not w:
                continue
            if w[0] == "module" and not m["name"]:
                m["name"] = w[1]
                t = re.search(r'"(.*)"', line)
                m["title"] = t.group(1) if t else ""
            elif not line.startswith(" "):
                if m["name"]:
                    break  # the header ends at the first unindented line
            elif w[0] == "kind":
                m["kind"] = w[1]
            elif w[0] == "card":
                m["card"].append(w[1])
            elif w[0] == "skill":
                m["skill"].append(w[1])
            elif w[0] == "param" and "=" in w:
                m["params"].append((w[1], w[w.index("=") + 1]))
        mods.append(m)
    return mods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--convention-card", default=HERE.parent / "convention-card")
    ap.add_argument("--rusty-bidding-bot", default=HERE.parent / "rusty-bidding-bot")
    args = ap.parse_args()

    dec = tomllib.loads((OUT / "decisions.toml").read_text())
    cc_tag = dec["sources"]["convention_card"]
    rbb_tag = dec["sources"]["rusty_bidding_bot"]
    fields = load_fields(args.convention_card, cc_tag)
    defs = load_definitions(args.convention_card, cc_tag)
    modules = load_modules(args.rusty_bidding_bot, rbb_tag)

    stay = dec["stay_settings"]["groups"]
    place_of = {}   # switch path -> (id, treatment attrs)
    for cid, switches in dec["places"].items():
        for path, attrs in switches.items():
            place_of[path] = (cid, attrs)
    fn_setting = {}  # setting path -> (function, part)
    fn_option_id = {}
    for fname, fn in dec["functions"].items():
        for part, path in fn.get("settings", {}).items():
            fn_setting[path] = (fname, part)
            fn_option_id[path] = fn["options"]
    implements = collections.defaultdict(list)
    for fname, fn in dec["functions"].items():
        for cid in list(fn.get("options", {}).values()) + fn.get("implements", []):
            implements[cid].append(fname)

    # --- switches -> conventions -------------------------------------
    switches = sorted(p for p in fields if p.endswith(".play"))
    switch_conv = {}   # switch path -> id, for switches that become a convention
    problems = []
    for p in switches:
        group = p[:-5]
        if group in stay or p in place_of:
            continue
        cid = dec["switch_id"].get(p)
        if cid is None:
            skills = as_list(fields[p].get("skill"))
            if len(skills) != 1:
                problems.append(f"{p}: {len(skills)} skills and no switch_id")
                continue
            cid = skills[0]
        switch_conv[p] = cid
    group_conv = {p[:-5]: cid for p, cid in switch_conv.items()}
    for p, (cid, _) in place_of.items():
        group_conv[p[:-5]] = cid

    conv = {}  # id -> record

    def conv_rec(cid):
        if cid not in conv:
            conv[cid] = {"id": cid, "switches": [], "treatments": [], "origin": ""}
        return conv[cid]

    for p, cid in switch_conv.items():
        conv_rec(cid)["switches"].append(p)
    for p, (cid, attrs) in place_of.items():
        r = conv_rec(cid)
        r["switches"].append(p)
        r["treatments"].append(attrs["treatment"])
    for cid, count in collections.Counter(switch_conv.values()).items():
        if count > 1:
            problems.append(f"{cid}: {count} switches map to it")

    # --- every field ---------------------------------------------------
    def group_of(path):
        parts = path.split(".")
        for i in range(len(parts) - 1, 1, -1):
            g = ".".join(parts[:i])
            if g + ".play" in fields:
                return g
        return None

    rows = []
    counts = collections.Counter()
    for path in sorted(fields):
        a = fields[path]
        skills = as_list(a.get("skill"))
        row = {"field": path, "kind": a["kind"], "label": a.get("label", ""),
               "becomes": "", "convention": "", "treatment": "", "address": "",
               "note": ""}
        g = group_of(path)
        if path in switch_conv:
            cid = switch_conv[path]
            row.update(becomes="convention", convention=cid, address=cid)
            if cid in dec["new_ids"]:
                row["note"] = "new ID"
        elif path in place_of:
            cid, attrs = place_of[path]
            row.update(becomes="treatment (place)", convention=cid,
                       treatment=attrs["treatment"],
                       address=f"{cid}:{attrs['treatment']}",
                       note="main place, default true" if attrs.get("main") else "default false")
        elif g and g in stay:
            row.update(becomes="setting", address=path,
                       note="stays a setting until Phase 6 (Jordan, issue #3)")
        elif g and g in group_conv and path != g + ".play":
            cid = group_conv[g]
            name = path[len(g) + 1:].replace(".", "_")
            row.update(becomes="treatment", convention=cid, treatment=name,
                       address=f"{cid}:{name}")
            conv_rec(cid)["treatments"].append(name)
            other = [s for s in skills if s != cid and s not in as_list(fields[g + ".play"].get("skill"))]
            if other:
                row["note"] = "names another convention: " + ", ".join(other)
        elif path in fn_setting:
            fname, part = fn_setting[path]
            row.update(becomes="convention entries (function)",
                       address=f"{fname}.{part}",
                       note="each option with an ID becomes that convention's entry; natural and other leave none")
        elif a["kind"] == "bool" and skills:
            row.update(becomes="setting (parked)", address=path,
                       note="lone yes/no naming " + ", ".join(skills) + "; placed in Phase 6")
        else:
            row.update(becomes="setting", address=path)
        counts[row["becomes"]] += 1
        rows.append(row)

    for cid, r in conv.items():
        names = r["treatments"]
        for n, c in collections.Counter(names).items():
            if c > 1:
                problems.append(f"{cid}: treatment name {n} used {c} times")
            if n in ("play", "text", "from", "for"):
                problems.append(f"{cid}: treatment named {n} is reserved")

    with open(OUT / "fields.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    # --- conventions -----------------------------------------------------
    for fname, fn in dec["functions"].items():
        for cid in fn.get("options", {}).values():
            if cid not in conv:
                conv_rec(cid)["origin"] = "an option of a setting today"
    for cid in defs:
        if cid not in conv:
            conv_rec(cid)["origin"] = "no switch today"

    section_ctx = dec["context"]["section"]
    conv_ctx = dec["context"]["convention"]

    def contexts(r):
        if r["id"] in conv_ctx:
            return conv_ctx[r["id"]]
        if r["switches"]:
            return section_ctx.get(r["switches"][0].split(".")[0], [])
        return []

    # --- rule modules ------------------------------------------------------
    mod_rows = []
    place_counts = collections.Counter()
    conv_modules = collections.defaultdict(list)
    for m in modules:
        folder = m["path"].split("/")[1] if m["path"].count("/") > 1 else ""
        fname = m["path"].rsplit("/", 1)[1]
        reads_play = sorted({p for _, p in m["params"] if p.endswith(".play")})
        reads_fn = sorted({p for _, p in m["params"] if p in fn_setting})
        reads_other = sorted({p for _, p in m["params"]
                              if p in fields and not p.endswith(".play") and p not in fn_setting})
        unknown = sorted({p for _, p in m["params"] if p not in fields} |
                         {p for p in m["card"] if p not in fields})
        cid, why = "", ""
        if len(m["card"]) == 1 and m["card"][0] in switch_conv:
            cid = switch_conv[m["card"][0]]
            switched = "card: its convention's switch"
        elif len(m["card"]) == 1 and m["card"][0] in place_of:
            cid = place_of[m["card"][0]][0]
            switched = "card: a place treatment of its convention"
        elif m["card"]:
            switched = "card: " + ", ".join(m["card"])
            why = "switched by a treatment, a setting or several lines"
        elif reads_fn:
            opts = set()
            for name, p in m["params"]:
                if p in fn_setting:
                    opts |= set(re.findall(rf"\b{name} is (\w+)", m["text"]))
            ids = sorted({fn_option_id[reads_fn[0]][o] for o in opts
                          if o in fn_option_id[reads_fn[0]]})
            own = [i for i in ids if i in m["skill"]]
            if len(ids) == 1 and own:
                cid = ids[0]
                switched = "function: " + fn_setting[reads_fn[0]][0]
            else:
                switched = "function: " + fn_setting[reads_fn[0]][0]
                why = ("covers " + ", ".join(ids)) if len(ids) > 1 else "reads which defence is played"
        elif reads_play:
            switched = "param: " + ", ".join(reads_play)
            why = "reads a switch through a param; rules outside it may apply"
        elif reads_other:
            switched = "param: settings or treatments only"
            why = "no switch"
        else:
            switched = "nothing: always on with its system"
            why = "no switch"
        # What Phase 5 or 6 could do with a convention module that has no
        # header yet (issue #11). A proposal for review, not a decision.
        later = ""
        if not cid and m["kind"] == "convention":
            own = sorted({switch_conv.get(p) or place_of.get(p, ("",))[0] for p in reads_play})
            own = [i for i in own if i and (i in m["skill"] or i.split("/")[1].replace("_", "-") in m["name"]
                                            or m["name"].replace("-", "_") in i)]
            parked = [p for p in reads_other + m["card"]
                      if p in fields and fields[p]["kind"] == "bool" and not group_of(p)
                      and as_list(fields[p].get("skill"))]
            treat = [p for p in m["card"] if group_of(p)]
            if len(own) == 1:
                later = f"Phase 5: a convention with a switch ({own[0]}); takes the header once its rules stop firing without it"
            elif len(own) > 1:
                later = "stays whole: the rules for " + ", ".join(own)
            elif treat:
                later = "Phase 5: switched by a treatment of a convention (" + ", ".join(sorted({group_conv[group_of(p)] for p in treat if group_of(p) in group_conv})) + "); beside it once the treatment rule is enforced"
            elif parked:
                later = "Phase 6: switched by a lone yes/no (" + ", ".join(parked) + "); a convention once that is placed"
            elif reads_fn:
                later = "stays whole: " + why
            else:
                later = "no switch of its own: reads " + (", ".join(reads_other[:4]) or "nothing") + "; to classify by hand"
        later = dec.get("module_later", {}).get(m["name"], later)
        if cid:
            place = f"conventions/{cid}/{fname}"
            place_counts["beside its definition"] += 1
            conv_modules[cid].append(m["name"])
        else:
            place = f"rules/{folder}/{fname}"
            place_counts["rules/"] += 1
        mod_rows.append({
            "module": m["name"], "kind": m["kind"], "today": m["path"],
            "switched_by": switched, "convention": cid, "place": place,
            "why_not_beside": why,
            "later": later,
            "reads": " ".join(reads_play + reads_fn + reads_other),
            "unknown_paths": " ".join(unknown),
        })
    with open(OUT / "modules.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(mod_rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(mod_rows)

    conv_rows = []
    for cid in sorted(conv):
        r = conv[cid]
        d = defs.get(cid, {})
        origin = r["origin"] or ("card switch" if r["switches"] else "")
        conv_rows.append({
            "id": cid,
            "name": d.get("name") or dec["new_ids"].get(cid, ""),
            "origin": origin,
            "new_id": "yes" if cid in dec["new_ids"] else "",
            "contexts": " ".join(contexts(r)),
            "switches_today": " ".join(r["switches"]),
            "treatments": len(r["treatments"]),
            "implements": " ".join(implements.get(cid, [])),
            "modules": " ".join(conv_modules.get(cid, [])),
        })
        if cid not in defs and cid not in dec["new_ids"]:
            problems.append(f"{cid}: no definition at {cc_tag} and not listed in new_ids")
    with open(OUT / "conventions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(conv_rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(conv_rows)

    # --- summary -------------------------------------------------------------
    from_switch = [r for r in conv_rows if r["origin"] == "card switch"]
    no_ctx = [r for r in conv_rows if not r["contexts"]]
    no_ctx_card = [r for r in no_ctx if r["origin"] != "no switch today"]
    variants = [r for r in rows if r["note"].startswith("names another")]
    kinds = collections.Counter(m["kind"] for m in modules)
    conv_mods = [r for r in mod_rows if r["kind"] == "convention"]
    no_card = [r for r in conv_mods if not r["switched_by"].startswith("card")]
    by_switch = collections.Counter(r["switched_by"].split(":")[0] for r in no_card)
    ctx_count = collections.Counter(r["contexts"].split()[0] for r in conv_rows if r["contexts"])

    L = []
    L.append("# Inventory summary\n")
    L.append(f"Generated by `scripts/inventory.py` from `convention-card` {cc_tag} and "
             f"`rusty-bidding-bot` {rbb_tag}, with the hand decisions in "
             "`decisions.toml`. Do not edit; change `decisions.toml` and run the script.\n")
    L.append("## Card fields (`fields.csv`)\n")
    L.append("| Becomes | Fields |\n|---|---|")
    for k in ["convention", "treatment (place)", "treatment", "convention entries (function)",
              "setting (parked)", "setting"]:
        L.append(f"| {k} | {counts[k]} |")
    L.append(f"| **Total** | **{len(rows)}** |\n")
    L.append(f"- {len(switches)} switches at the tag become {len(from_switch)} conventions.")
    L.append(f"- {len(variants)} treatments name a different convention from their group: the nine "
             "yes/no variants of issue #6, and Multi's `strong_option`, an enum one of whose "
             "values is Lars Multi.")
    L.append("")
    L.append("## Conventions (`conventions.csv`)\n")
    L.append("| Origin | IDs |\n|---|---|")
    for k, v in collections.Counter(r["origin"] for r in conv_rows).most_common():
        L.append(f"| {k} | {v} |")
    L.append(f"| **Total** | **{len(conv_rows)}** |\n")
    L.append(f"- New IDs: {sum(1 for r in conv_rows if r['new_id'])}.")
    L.append(f"- With a context: {len(conv_rows) - len(no_ctx)}. Without: {len(no_ctx)}, "
             f"of which {len(no_ctx_card)} can be a card entry from a migrated card.")
    L.append("")
    L.append("| Main context | Conventions |\n|---|---|")
    for k, v in sorted(ctx_count.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {v} |")
    L.append("")
    L.append("## Rule modules (`modules.csv`)\n")
    L.append("| Kind | Modules |\n|---|---|")
    for k, v in kinds.most_common():
        L.append(f"| {k} | {v} |")
    L.append(f"| **Total** | **{len(modules)}** |\n")
    L.append("| Place | Modules |\n|---|---|")
    for k, v in place_counts.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append(f"Convention modules with no `card` line: {len(no_card)}.\n")
    L.append("| Switched by | Modules |\n|---|---|")
    for k, v in by_switch.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("What becomes of the convention modules that get no header in Phase 3 (a proposal, issue #11):\n")
    L.append("| Proposal | Modules |\n|---|---|")
    for k, v in collections.Counter(re.split(r"[:(]", r["later"])[0].strip() + (": " + r["later"].split(": ")[1].split(" (")[0].split(";")[0] if ": " in r["later"] and r["later"].startswith("Phase") else "")
                                    for r in mod_rows if r["later"]).most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Problems the script found\n")
    L.extend(f"- {p}" for p in problems) if problems else L.append("None.")
    unknown = [r for r in mod_rows if r["unknown_paths"]]
    if unknown:
        L.append("\nRule modules reading a path that is not a card field at the tag:\n")
        L.extend(f"- `{r['module']}`: {r['unknown_paths']}" for r in unknown)
    L.append("")
    (OUT / "SUMMARY.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
