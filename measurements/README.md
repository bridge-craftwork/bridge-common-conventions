# Measurements

What each change did to the bidding: one small file a change, committed with
it. A rule is judged by bidding the same cards over the same deals before
and after, and by setting our auctions beside another bidder's. The
conclusions go in a module's `.notes.md`; the numbers they rest on go here,
so a later reader can see what was measured, with what, and repeat it.

Nothing here is run by CI. Whoever makes the change runs the measurement
and commits the record. How much to run depends on the change
(docs/PLAN.md, Phase 7, decision 6):

| The change | What to run |
|---|---|
| Text only: a name, a brief, notes, references | Nothing, and no record |
| Tools or layout, where no rule changes | The sample: `scripts/capture.py --boards-per-file 1` on every card |
| One convention's rules | Its `.test` lines, and the fast designed cards (`test-cards/fast.txt`) or deals from its own scenario |
| Rules many auctions pass through, a migration, a default | Every card over the full deal set |
| A convention another bidder also plays, when the question is which is right | The same deals bid by that bidder, in a `[[reference]]` |

## Making a record

    python3 scripts/capture.py --rbb RBB --rules . --out /tmp/after ...
    python3 scripts/measure.py BEFORE AFTER --name "what changed" \
        --change "One sentence on the change" --pr 125

`BEFORE` and `AFTER` are captures (`scripts/capture.py`). Several pairs go in
one record with `--and BEFORE AFTER`, one for each set of cards. A sample is
set beside a full capture board for board.

## What a record holds

`<date>-<name>.toml`:

| Key | |
|---|---|
| `date`, `change`, `pull_request` | When, what, and where it was reviewed |
| `boards_compared`, `boards_bid_differently` | The totals over every set |
| `note` | What a reader needs to make sense of the numbers |
| `[[set]]` | One set of cards: the `bidder` and its version on each side, the rules on each side, the card tools, the deal set by its `deals_sha256`, whether it was a `sample`, and its own totals |
| `[set.by_card]` | For the corpus only: each card with a difference, as `[boards compared, boards bid differently]` |
| `[[reference]]` | Optional, written by hand: another `bidder` and its version, the `deals`, the `boards`, and how many of our auctions agreed with it `agree_before` and `agree_after` |

- **Every record names its bidder.** These are what one engine did. Another
  engine's runs sit beside Rusty's, told apart by `bidder`.
- **Only the corpus's cards are named.** Cards captured from a folder
  outside the repo are people's own: a record counts them.
- **The auctions are not kept.** A capture is rebuilt by running
  `scripts/capture.py` with the tools the record names, on the deal set its
  hash identifies.
- **A record is never edited to match a later run.** A new measurement is a
  new file.
