#!/usr/bin/env python3
"""Compare two captures made by scripts/capture.py.

    python3 scripts/compare.py BEFORE AFTER [--ignore-rule] [--report FILE]

Exit status 0 when nothing differs, 1 otherwise. Phase 3 must end with
status 0; phases 5 and 6 end with a report that has been reviewed.

Compared: every file under cards/ and coverage/, and, where both sides have
full/, every board's auction and every call's alert, meaning, what it shows
and the rule that chose it. --ignore-rule leaves the rule out, for a
comparison across a move of the rule files.
"""
import argparse
import collections
import json
import pathlib
import sys


def flat(v, prefix=""):
    if isinstance(v, dict):
        out = {}
        for k, x in v.items():
            out.update(flat(x, f"{prefix}{k}."))
        return out
    return {prefix.rstrip("."): json.dumps(v, sort_keys=True, ensure_ascii=False)}


def diff_file(a, b):
    """Lines describing how two captured files differ."""
    ta, tb = a.read_text(), b.read_text()
    if ta == tb:
        return []
    if a.suffix == ".json":
        fa, fb = flat(json.loads(ta)), flat(json.loads(tb))
        out = []
        for k in sorted(set(fa) | set(fb)):
            if fa.get(k) != fb.get(k):
                out.append(f"    {k}: {fa.get(k, '(absent)')} -> {fb.get(k, '(absent)')}")
        return out
    la, lb = ta.split("\n"), tb.split("\n")
    gone = [x for x in la if x not in set(lb)]
    new = [x for x in lb if x not in set(la)]
    return [f"    - {x}" for x in gone] + [f"    + {x}" for x in new]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("before", type=pathlib.Path)
    ap.add_argument("after", type=pathlib.Path)
    ap.add_argument("--ignore-rule", action="store_true")
    ap.add_argument("--report", type=pathlib.Path)
    ap.add_argument("--examples", type=int, default=5,
                    help="how many differing boards to show per card")
    args = ap.parse_args()

    lines = []
    counts = collections.Counter()

    for folder in ("cards", "coverage"):
        fa = {p.relative_to(args.before): p for p in (args.before / folder).rglob("*") if p.is_file()}
        fb = {p.relative_to(args.after): p for p in (args.after / folder).rglob("*") if p.is_file()}
        for rel in sorted(set(fa) | set(fb)):
            if rel not in fa or rel not in fb:
                counts[f"{folder}: files on one side only"] += 1
                lines.append(f"{rel}: only in {'before' if rel in fa else 'after'}")
                continue
            d = diff_file(fa[rel], fb[rel])
            if d:
                counts[f"{folder}: files that differ"] += 1
                lines.append(f"{rel}: {len(d)} differences")
                lines.extend(d[:40])
                if len(d) > 40:
                    lines.append(f"    ... and {len(d) - 40} more")

    fa, fb = args.before / "full", args.after / "full"
    if fa.is_dir() and fb.is_dir():
        keys = ["call", "alert", "meaning", "shown"] + ([] if args.ignore_rule else ["rule"])
        for name in sorted({p.name for p in fa.glob("*.jsonl")} | {p.name for p in fb.glob("*.jsonl")}):
            if not (fa / name).exists() or not (fb / name).exists():
                counts["bidding: cards on one side only"] += 1
                lines.append(f"full/{name}: only on one side")
                continue
            shown = 0
            with open(fa / name) as xa, open(fb / name) as xb:
                rows_a, rows_b = xa.read().split("\n"), xb.read().split("\n")
            if len(rows_a) != len(rows_b):
                counts["bidding: cards with a different number of boards"] += 1
                lines.append(f"full/{name}: {len(rows_a)} boards against {len(rows_b)}")
                continue
            for ra, rb in zip(rows_a, rows_b):
                counts["bidding: boards compared"] += 1
                if ra == rb or not ra:
                    continue
                a, b = json.loads(ra), json.loads(rb)
                if a["auction"] != b["auction"]:
                    kind = "auctions"
                    detail = f"{' '.join(a['auction'])}  ->  {' '.join(b['auction'])}"
                else:
                    what = sorted({k for ca, cb in zip(a["calls"], b["calls"])
                                   for k in keys if ca.get(k) != cb.get(k)})
                    if not what:
                        continue
                    kind = "explanations (" + ", ".join(what) + ")"
                    ca, cb = next((x, y) for x, y in zip(a["calls"], b["calls"])
                                  if any(x.get(k) != y.get(k) for k in keys))
                    detail = (f"{' '.join(a['auction'])}: {ca['call']} "
                              + "; ".join(f"{k}: {ca.get(k)!r} -> {cb.get(k)!r}" for k in what
                                          if ca.get(k) != cb.get(k)))
                counts[f"bidding: boards with different {kind}"] += 1
                if shown < args.examples:
                    shown += 1
                    lines.append(f"full/{name} board {a['board']} {a['deal']}")
                    lines.append(f"    {detail}")
    else:
        lines.append("bidding not compared: full/ is missing on one side "
                     "(run scripts/capture.py with --rbb)")
        ma = json.loads((args.before / "MANIFEST.json").read_text())["cards"]
        mb = json.loads((args.after / "MANIFEST.json").read_text())["cards"]
        for name in sorted(set(ma) & set(mb)):
            if ma[name].get("bidding") != mb[name].get("bidding"):
                counts["bidding: cards whose digest differs"] += 1
                lines.append(f"{name}: bidding digest differs")

    differing = {k: v for k, v in counts.items() if k != "bidding: boards compared"}
    head = [f"Compared {args.before} with {args.after}",
            f"Boards compared: {counts['bidding: boards compared']}", ""]
    head += [f"{v:8}  {k}" for k, v in sorted(differing.items())] or ["No differences."]
    report = "\n".join(head + [""] + lines) + "\n"
    if args.report:
        args.report.write_text(report)
        print("\n".join(head))
    else:
        print(report)
    sys.exit(1 if differing else 0)


if __name__ == "__main__":
    main()
