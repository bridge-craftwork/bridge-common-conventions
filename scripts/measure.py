#!/usr/bin/env python3
"""Write the record of a measurement: what a change did to the bidding.

A rule change is judged by bidding the same cards over the same deals before
and after. This turns two captures (scripts/capture.py) into the small file
that is committed with the change, in measurements/.

    python3 scripts/measure.py BEFORE AFTER --name two-exclusions \\
        --change "Lebensohl and Rubensohl fill one function" [--pr 125]

It may be given several pairs, one for each set of cards:

    python3 scripts/measure.py B1 A1 --and B2 A2 --name ...

The record names its bidder and its version, the rules on each side, the
deal set by its hash, and for every card how many boards were bid
differently. A card from the corpus is named. Cards captured from a folder
outside the repo are people's own and are counted, never named.

The auctions themselves stay out of git: a capture is rebuilt by running
scripts/capture.py again with the tools the record names.
"""
import argparse
import collections
import datetime
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent


def auctions(path):
    """{board: (deal, auction)} from a capture's full/<card>.jsonl."""
    out = {}
    for line in path.read_text().split("\n"):
        if line:
            b = json.loads(line)
            calls = [c["call"] if isinstance(c, dict) else str(c) for c in b.get("auction", [])]
            out[b["board"]] = (b.get("deal"), " ".join(calls))
    return out


def compare(before, after):
    """One pair of captures: its header facts and a line for each card."""
    ma = json.loads((before / "MANIFEST.json").read_text())
    mb = json.loads((after / "MANIFEST.json").read_text())
    public = isinstance(mb.get("corpus"), list)
    cards, compared, changed = [], 0, 0
    names = sorted({p.stem for p in (before / "full").glob("*.jsonl")} & {p.stem for p in (after / "full").glob("*.jsonl")})
    for name in names:
        a, b = auctions(before / "full" / f"{name}.jsonl"), auctions(after / "full" / f"{name}.jsonl")
        # A sample keeps the full set's board numbers: the boards both hold.
        both = [k for k in a if k in b and a[k][0] == b[k][0]]
        differ = sum(1 for k in both if a[k][1] != b[k][1])
        compared += len(both)
        changed += differ
        cards.append((name, len(both), differ))
    return {
        "public": public,
        "before": ma, "after": mb,
        "cards": cards, "compared": compared, "changed": changed,
        "only_one_side": len({p.stem for p in (before / "full").glob("*.jsonl")} ^ {p.stem for p in (after / "full").glob("*.jsonl")}),
    }


def q(s):
    return json.dumps(str(s), ensure_ascii=False)


def tools(m):
    t = m.get("tools", {})
    rules = t.get("rules", "the rules compiled into the bidder")
    return t.get("rbb", "unknown"), rules, t.get("convention-card", "unknown")


def render(args, sets):
    lines = [
        "# A measurement: what one change did to the bidding (measurements/README.md).",
        "# Written by scripts/measure.py; the summary line is the author's.",
        "",
        f"date = {args.date}",
        f"change = {q(args.change)}",
    ]
    if args.pr:
        lines.append(f"pull_request = {args.pr}")
    total = sum(s["compared"] for s in sets)
    changed = sum(s["changed"] for s in sets)
    lines += [f"boards_compared = {total}", f"boards_bid_differently = {changed}"]
    if args.note:
        lines.append(f"note = {q(args.note)}")
    for s in sets:
        (rbb_a, rules_a, cc_a), (rbb_b, rules_b, cc_b) = tools(s["before"]), tools(s["after"])
        deals = s["after"].get("deals", {})
        lines += [
            "",
            "[[set]]",
            f"cards = {q('the corpus (before/corpus.toml)' if s['public'] else 'hand-made cards kept outside this repo, counted and not named')}",
            f"card_count = {len(s['cards'])}",
            f"bidder = {q(rbb_b)}",
            f"bidder_before = {q(rbb_a)}",
            f"rules_before = {q(rules_a)}",
            f"rules_after = {q(rules_b)}",
            f"card_tools_before = {q(cc_a)}",
            f"card_tools_after = {q(cc_b)}",
            f"deals = {q(deals.get('repo', '') + ' ' + deals.get('glob', '') + ' at ' + str(deals.get('ref', ''))[:12])}",
            f"deals_sha256 = {q(deals.get('sha256', ''))}",
            f"boards_a_card = {deals.get('count', 0)}",
            f"sample = {'true' if 'sample_boards_per_file' in deals or s['before'].get('deals', {}).get('count') != deals.get('count') else 'false'}",
            f"boards_compared = {s['compared']}",
            f"boards_bid_differently = {s['changed']}",
            f"cards_with_a_difference = {sum(1 for _, _, d in s['cards'] if d)}",
        ]
        if s["only_one_side"]:
            lines.append(f"cards_on_one_side_only = {s['only_one_side']}")
        if s["public"]:
            differing = [(n, c, d) for n, c, d in s["cards"] if d]
            if differing:
                lines.append("# card = [boards compared, boards bid differently]")
                lines.append("[set.by_card]")
                lines += [f"{q(n)} = [{c}, {d}]" for n, c, d in differing]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("before", type=pathlib.Path)
    ap.add_argument("after", type=pathlib.Path)
    ap.add_argument("--and", dest="more", nargs=2, action="append", default=[], type=pathlib.Path,
                    metavar=("BEFORE", "AFTER"), help="another pair of captures (repeatable)")
    ap.add_argument("--name", required=True, help="a few words for the file name")
    ap.add_argument("--change", required=True, help="what was changed, in a sentence")
    ap.add_argument("--pr", type=int, help="the pull request it belongs to")
    ap.add_argument("--note", help="anything a reader needs to make sense of the numbers")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "measurements")
    args = ap.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    if not slug:
        sys.exit("--name needs a letter or a digit")
    sets = [compare(b, a) for b, a in [(args.before, args.after), *args.more]]
    if not any(s["compared"] for s in sets):
        sys.exit("no board is in both captures: they hold different deals or different cards")
    target = args.out / f"{args.date}-{slug}.toml"
    target.write_text(render(args, sets))
    total, changed = sum(s["compared"] for s in sets), sum(s["changed"] for s in sets)
    print(f"{target.relative_to(HERE) if target.is_relative_to(HERE) else target}: {total} boards compared, {changed} bid differently")


if __name__ == "__main__":
    main()
