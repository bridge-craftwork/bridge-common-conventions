# Styles: one switch per bot

`general.style` (settings/general.toml) picks a set of treatments at once:
unset is our default; `standard` the textbook treatment where our default
is modern; `bba` and `gib` play as those bots do, for comparison runs
(`rbb compare --set general.style=bba`, `gib_tree.py agreed --set
general.style=gib`). A style changes only the items listed here; every
other rule plays the default.

**Rick (2026-11-26):** a style reaches further than conventions: the
strength a call needs is a partnership agreement too. Eventually every
item becomes a card setting of its own, so people can practise with
their own card. For now they are grouped by bot, one switch each. This
file is the map of what must later be configurable one by one: each item
with our default, the bot's value, the source, and the setting name it
would get (proposed; none exists yet).

## gib

GIB's own 2/1 card, as BBO's `gibrest` bidding tree states it (the
archive in rusty-bidding-bot's `.rbb-cache/gib-tree/xml/`; the
comparison is `probes/tools/gib_tree.py agreed`, docs/BIDDING-MODEL.md
section 4 there).

| item | our default | GIB | source | setting (proposed) | rules |
|---|---|---|---|---|---|
| Third-seat 1♥/1♠ on a good four-card suit, 10-11 HCP | allowed (Rick 2026-11-25: normal) | 5+ in every seat, 11-21 HCP | tree `P-P`: "Major suit opening -- 5+ !S; 11-21 HCP; 12-22 total points" | `major_openings.light_4_card_3rd` (bool) | base.bid, `when opening, seat=3, style is not gib` |
| Weak two: side four-card suit | a side four-card major without the jack or better is allowed; read 1-4 in each side suit | no side four-card suit but clubs: 2♦ ♣1-4 ♥♠1-3; 2♥ ♣1-4 ♦♠1-3; 2♠ ♣1-4 ♦♥1-3 | tree `_` and `P`: "Weak two bid -- 1-4 !C; 1-3 !D; 6+ !H; 1-3 !S; 10- HCP; 7+ total points" | `preempts.weak_two.side_four` (enum: `any`, `minor_only`, `none`; GIB `clubs_only` is narrower still) | preempts.bid, the `style is gib` block |

Listed, not changed:

| item | our default | GIB | source | setting (proposed) |
|---|---|---|---|---|
| Power double, the doubler's own suit | 18+ total points (or 17+ HCP) | 18+ total points: the same | tree `1D-D-P-1H-P` 1♠ and 2♣ "18+ total points"; `1H-D-P-2C-P` 2♦/2♠ "18-21" (Rick had expected 17+) | `doubles.takeout.power_suit_min` (int) |
| Power double, notrump | 19-21 balanced, a stopper | 19-21 HCP, a stopper | tree `1D-D-P-1H-P` 1NT | follows `nt_overcalls.direct.range_max` |
| Doubler's raise of advancer's suit | 2-level 17-19, 3-level 20-21 | 2-level 14-18, 3-level 17-19 | tree `1D-D-P-1H-P` 2♥, 3♥ | `doubles.takeout.raise_ranges` |
| Weak two strength | 4-10 HCP | 10- HCP, 7+ total points | tree `_` | `preempts.weak_two.hcp_min` / `hcp_max` |
| One-level opening floor | 10+ HCP with 12 HCP + length | 11-21 HCP, 12-22 total points | tree `_` 1♠ | `general.min_hcp_open` exists (12 total); an HCP floor would be new |

Measured (2026-11-26; `gib_tree.py agreed`, the top 20,000 positions of
the 100,000 random deals, 21GF-GIB, tags `gibstyle-off` and
`gibstyle-on`): call-boards with any range difference on agreed calls
fell from 225,477 to 214,315 (-11,162), and differences counted by kind
from 356,363 to 339,348. The five rules the two items touch (the
third-seat 1♥/1♠ and the three weak twos, 10,763 call-boards) leave the
difference list; nothing else moved by more than 110. By kind: "len
max-wide" 50,698 to 39,904, "len min-wide" 59,195 to 52,505. Our readings
only: the positions are our default engine's auctions.

## bba

What BBA does, from probes and the corpus (each module's notes say
more). Modules with `style is bba` rules, and what they change:

| item | where | notes |
|---|---|---|
| Valuation: counts tens, no length points at notrump | engine (`Valuation::for_card`) | docs/DESIGN.md "Treatments" in rusty-bidding-bot |
| One-level openings and the ten-count with a six-card suit | base.bid (`style is not standard` shares the default) | preempts.notes.md |
| Weak twos to 10 HCP; a side major with the jack or better stops it | preempts.bid (shared with the default) | preempts.notes.md |
| Weak-two responses | weak-two-responses.bid | weak-two-responses.notes.md |
| Responses and raises of a major | responses.bid | responses.notes.md |
| Opener's rebids | rebids.bid | rebids.notes.md |
| Responder's rebids | responder-rebids.bid | responder-rebids.notes.md |
| Strong openings | strong-openings.bid | |
| 1NT and 2NT responses, minor transfers | one-nt.bid, two-nt-responses.bid, minor-transfers.bid | one-nt.notes.md, two-nt-responses.notes.md |
| Stayman, Smolen, Jacoby transfers | conventions/bidding_conventions/ | stayman.notes.md, jacoby-transfers.notes.md |
| Gerber, Exclusion Blackwood | conventions/bidding_conventions/ | |

Setting names for these are not proposed yet: each module's notes hold
the details.

## Other bots

Brill's treatments test `general.system = brill` (the stock card
`Brill`), not a style, until `general.style` gains a `brill` value.
Known Brill items: the weak two is 5-10 HCP with no five-card side
major (a four-card one allowed; preempts.bid).
