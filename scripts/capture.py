#!/usr/bin/env python3
"""Capture how the tools behave today (Phase 2), so later phases can be
compared against it.

For every card in the corpus (before/corpus.toml):

- what convention-card makes of it: the card as loaded, the .bbsa, BBO and
  Bridgodex exports, the values in both ACBL PDFs, the editor's rows
  (scripts/capture-cards.mjs);
- what rusty-bidding-bot does with it: the auction, rule, alert and meaning
  of every call over a fixed set of deals, and which settings its rules read.

    python3 scripts/capture.py --rbb PATH/TO/rbb --rules PATH/TO/conventions

A change that cannot alter a bid can be checked on a sample,
--boards-per-file N: the first N boards of every scenario, numbered as in
the full set, so scripts/compare.py sets a sample beside a full capture
board for board. Cards are exported and bid side by side (--jobs), which
shortens a sample; a full run is bound by the bidding itself, which
already uses every core for one card.

Output goes to before/ (or --out). The card captures and the digests of the
bidding are small and are committed; the bidding itself goes to <out>/full/,
which git ignores, and is rebuilt by running this again.

Cards that are people's own data (saved in Bridge Classroom) never go in
this repo. Capture them with --cards DIR --out DIR, both outside the repo.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

HERE = pathlib.Path(__file__).resolve().parent.parent
TAGS = ("Event", "Board", "Dealer", "Vulnerable", "Deal")


def git(repo, *args, text=True):
    out = subprocess.check_output(["git", "-C", str(repo), *args])
    return out.decode() if text else out


def files_at(repo, ref, pattern):
    folder, _, glob = pattern.rpartition("/")
    names = git(repo, "ls-tree", "--name-only", ref, folder + "/").split("\n")
    return sorted(n for n in names if n and pathlib.PurePath(n).match(glob))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build_deals(repo, spec, sample=None):
    """The first N boards of each PBN file, cut down to the tags a bidder needs.

    With `sample`, only the first `sample` of those in each file, each keeping
    the number it has in the full set.
    """
    games, index = [], []
    number = 0
    for name in files_at(repo, spec["ref"], spec["glob"]):
        text = git(repo, "show", f"{spec['ref']}:{name}")
        chunks = re.split(r"(?m)^(?=\[Event )", text)[1:]
        kept = 0
        for chunk in chunks[: spec["boards_per_file"]]:
            tags = dict(re.findall(r'(?m)^\[(\w+) "(.*)"\]', chunk))
            if "Deal" not in tags:
                continue
            # Board numbers repeat from file to file; number the set afresh.
            number += 1
            kept += 1
            if sample is not None and kept > sample:
                continue
            tags["Event"] = pathlib.PurePath(name).stem
            index.append(f"{number}\t{tags['Event']}\t{tags.get('Board', '')}")
            tags["Board"] = str(number)
            games.append("".join(f'[{k} "{tags[k]}"]\n' for k in TAGS if k in tags))
    return "\n".join(games), "\n".join(index) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=pathlib.Path, default=HERE / "before")
    ap.add_argument("--corpus", type=pathlib.Path, default=HERE / "before" / "corpus.toml")
    ap.add_argument("--cards", type=pathlib.Path,
                    help="capture the cards in this directory instead of the corpus's")
    ap.add_argument("--siblings", type=pathlib.Path, default=HERE.parent,
                    help="where the other repos are checked out")
    ap.add_argument("--convention-card", type=pathlib.Path,
                    help="the convention-card checkout to capture with (default: the sibling)")
    ap.add_argument("--rbb", type=pathlib.Path, help="the rbb binary to bid with")
    ap.add_argument("--rules", type=pathlib.Path, help="the directory of .bid files")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1,
                    help="how many cards to export and to bid at once (default: one per "
                         "processor core). The bidder uses every core for one card's full "
                         "set, so this shortens a sample and the exports, not a full run")
    ap.add_argument("--boards-per-file", type=int, metavar="N",
                    help="bid a sample: the first N boards of every scenario, not the corpus's "
                         "full set. For a change that cannot alter a bid")
    ap.add_argument("--only", metavar="NAMES",
                    help="of the cards, only these: file names without their ending, "
                         "comma-separated, or @FILE with one a line (test-cards/fast.txt)")
    ap.add_argument("--no-check-tags", action="store_true",
                    help="capture from tools that are not at the corpus's tags (the 'after' side)")
    args = ap.parse_args()

    corpus = tomllib.loads(args.corpus.read_text())
    cc = args.convention_card or args.siblings / "convention-card"
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"tools": {}, "cards": {}}

    cc_at = git(cc, "describe", "--tags", "--always").strip()
    manifest["tools"]["convention-card"] = cc_at
    if not args.no_check_tags and cc_at != corpus["tools"]["convention_card"]:
        sys.exit(f"convention-card is at {cc_at}, not {corpus['tools']['convention_card']}; "
                 "check out the tag, or pass --no-check-tags")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        cards = tmp / "cards"
        cards.mkdir()
        if args.cards:
            for f in sorted(args.cards.iterdir()):
                if f.suffix in (".bbsa", ".json"):
                    shutil.copy(f, cards / f.name)
            manifest["corpus"] = "a directory of cards outside the corpus"
        else:
            manifest["corpus"] = corpus["cards"]
            for src in corpus["cards"]:
                repo = args.siblings / src["repo"]
                for name in files_at(repo, src["ref"], src["glob"]):
                    target = cards / pathlib.PurePath(name).name
                    if target.exists():
                        sys.exit(f"two corpus cards are named {target.name}")
                    target.write_bytes(git(repo, "show", f"{src['ref']}:{name}", text=False))
        if args.only:
            only = (pathlib.Path(args.only[1:]).read_text().split("\n") if args.only.startswith("@")
                    else args.only.split(","))
            only = {n.strip() for n in only if n.strip() and not n.strip().startswith("#")}
            for f in list(cards.iterdir()):
                if f.stem not in only:
                    f.unlink()
            missing = only - {f.stem for f in cards.iterdir()}
            if missing:
                sys.exit(f"--only names cards that are not there: {', '.join(sorted(missing))}")
        names = sorted(f.name for f in cards.iterdir())

        # --- convention-card ---
        card_out = out / "cards"
        if card_out.exists():
            shutil.rmtree(card_out)
        # The exports are one thread of work a card file: several node
        # processes, each with its share of the files, writing to one folder.
        shares = [names[i::max(1, min(args.jobs, len(names)))]
                  for i in range(max(1, min(args.jobs, len(names))))]

        def export(n, share):
            mine = tmp / f"cards-{n}"
            mine.mkdir()
            for name in share:
                shutil.copy(cards / name, mine / name)
            return subprocess.run(["node", str(HERE / "scripts" / "capture-cards.mjs"), str(cc),
                                   str(mine), str(card_out)], check=True, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(shares)) as pool:
            listing = "".join(pool.map(export, range(len(shares)), shares))
        source = dict(line.split("\t") for line in listing.splitlines() if "\t" in line)
        # One capture per card; a file can hold several (a BBO export).
        # `bid_with` is the file the bidder is given: the card as it came,
        # when the bidder reads that format itself, else the card as
        # convention-card imported it.
        bid_with = {}
        for stem, name in sorted(source.items()):
            folder = card_out / stem
            files = sorted(folder.iterdir())
            errors = [f.name for f in files if "capture_error" in f.read_text()]
            read = json.loads((folder / "import.json").read_text())
            manifest["cards"][stem] = {"source": name, "sha256": sha((cards / name).read_bytes()),
                                       "exports": len(files)}
            if errors:
                manifest["cards"][stem]["export_errors"] = errors
            if read.get("format") in ("card", "bbsa"):
                bid_with[stem] = cards / name
            else:
                manifest["cards"][stem]["bid_as_imported"] = read.get("format")
                bid_with[stem] = folder / "card.json"

        # --- rusty-bidding-bot ---
        if args.rbb:
            version = subprocess.check_output([str(args.rbb), "-V"]).decode().strip()
            manifest["tools"]["rbb"] = version
            if args.rules:
                top = git(args.rules, "rev-parse", "--show-toplevel").strip()
                manifest["tools"]["rules"] = git(top, "describe", "--tags", "--always", "--dirty").strip()
                want = corpus["tools"]["rusty_bidding_bot"]
                if not args.no_check_tags and manifest["tools"]["rules"] != want:
                    sys.exit(f"the rules are at {manifest['tools']['rules']}, not {want}")
            deals, index = build_deals(args.siblings / corpus["deals"]["repo"], corpus["deals"],
                                       args.boards_per_file)
            (tmp / "deals.pbn").write_text(deals)
            manifest["deals"] = dict(corpus["deals"], count=deals.count("[Deal "),
                                     sha256=sha(deals.encode()))
            if args.boards_per_file is not None:
                manifest["deals"]["sample_boards_per_file"] = args.boards_per_file
            full = out / "full"
            full.mkdir(exist_ok=True)
            (full / "deals.tsv").write_text("board\tscenario\tits board\n" + index)
            cov_out = out / "coverage"
            if cov_out.exists():
                shutil.rmtree(cov_out)
            cov_out.mkdir()
            rules = ["--rules", str(args.rules)] if args.rules else []
            def bid(stem, card):
                """One card: its bidding digest (or the error) and its coverage."""
                target = full / f"{stem}.jsonl"
                r = subprocess.run([str(args.rbb), "bid-pbn", "-i", str(tmp / "deals.pbn"),
                                    "-o", str(target), "--ns-card", str(card),
                                    "--json", "--all-meanings", *rules],
                                   capture_output=True, text=True)
                if r.returncode:
                    return {"bidding_error": r.stderr.strip()[-400:]}, None, 0
                # Rules are named by their path inside the rules directory, so
                # the capture does not depend on where that directory is.
                text = target.read_text()
                if args.rules:
                    text = text.replace(json.dumps(str(args.rules.resolve()) + "/")[1:-1], "")
                    target.write_text(text)
                auctions = []
                for line in text.split("\n"):
                    if line:
                        b = json.loads(line)
                        auctions.append(" ".join(c["call"] if isinstance(c, dict) else str(c)
                                                 for c in b.get("auction", [])))
                digest = {"bidding": {
                    "boards": len(auctions),
                    "sha256": sha(target.read_bytes()),
                    "auctions_sha256": sha("\n".join(auctions).encode()),
                }}
                c = subprocess.run([str(args.rbb), "card", "coverage", "-v", *rules,
                                    str(card)], capture_output=True, text=True)
                return digest, (c.stdout if not c.returncode else c.stderr), len(auctions)

            # Each card is its own processes and its own files; the manifest
            # is filled in here, so its content does not depend on the order
            # the cards finish in.
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
                jobs = {pool.submit(bid, stem, card): stem for stem, card in bid_with.items()}
                for job in concurrent.futures.as_completed(jobs):
                    stem = jobs[job]
                    digest, coverage, boards = job.result()
                    manifest["cards"][stem].update(digest)
                    if coverage is not None:
                        (cov_out / f"{stem}.txt").write_text(coverage)
                        print(stem, boards, "boards", flush=True)

    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
