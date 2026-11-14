# How the tools behave before the move

Phase 2 of [the plan](../docs/PLAN.md). A record of what `convention-card`
v0.44.0 and `rusty-bidding-bot` v0.15.3 do with a fixed set of cards, taken
before any content moves, so that Phase 3 can show it changed nothing and
Phases 5 and 6 can list exactly what they changed.

| Here | What it is |
|---|---|
| [corpus.toml](corpus.toml) | The cards, the deals and the tool versions, each pinned to a git ref |
| [MANIFEST.json](MANIFEST.json) | What was captured: every card with its digests, the tools' versions, the deal set's digest |
| `cards/<card>/` | What `convention-card` makes of the card: `card.json` (as loaded and upgraded), `import.json` (what the import reported), the `.bbsa`, BBO and Bridgodex exports, the values written into both ACBL PDFs, and `editor.json` (the rows the editor ticks and the values it shows) |
| `coverage/<card>.txt` | Which of the card's settings Rusty's rules read, and which they ignore |
| `full/` | Rusty's bidding: for every card and deal, the auction and each call's rule, alert, meaning and what it shows. About 300 MB, so git ignores it; `MANIFEST.json` holds its digests |

## The corpus

- **22 public cards**: the 18 BBA system files of Practice-Bidding-Scenarios
  and the 4 JSON cards shipped with `rusty-bidding-bot`.
- **5,565 deals**: the first 20 boards of each of the 279 scenario files of
  Practice-Bidding-Scenarios, so every convention's own auctions are among
  them. Each card bids all four seats.

Cards saved in Bridge Classroom are its users' data. They are not here, and
nothing captured from them may be. To include them in a comparison, capture
them to a directory outside this repo:

    python3 scripts/capture.py --cards ~/private/cards --out ~/private/before --rbb ... --rules ...

## Capturing and comparing

    # "before": convention-card checked out at its tag, rbb built at its tag
    python3 scripts/capture.py --rbb PATH/rbb --rules PATH/conventions

    # "after": the tools under test, to another directory
    python3 scripts/capture.py --no-check-tags --out /tmp/after --rbb NEW/rbb --rules NEW/rules

    python3 scripts/compare.py before /tmp/after --report /tmp/differences.txt

`compare.py` exits 0 only when nothing differs. `--ignore-rule` leaves out
which rule file and line chose each call, for comparing across a move of the
rule files.

## What is not captured

- The editor is not driven in a browser. `editor.json` is computed from the
  same catalogue and functions the editor's components call, which covers the
  rows and values but not layout.
- The PDFs' appearance. Only the values of their form fields are recorded.
- Rick's own Bridgodex, BBO and editor cards are not in this repo: they name
  other people. They are captured to a folder outside it with `--cards`, and
  only counts from that comparison are reported. A file holding several cards
  (a BBO export) gives one capture per card, and a card the bidder cannot
  read as it came is bid as `convention-card` imported it.
