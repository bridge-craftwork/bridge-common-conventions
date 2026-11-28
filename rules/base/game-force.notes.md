# game-force: when the auction forces to game

Rick, 2026-09-30: "we should have a state 'in game force' that 2/1
triggers, or 4th suit forcing, or xyz 2d, etc. there are also some
standard bidding scenarios - i'm not sure there is 100% agreement, but
like a 3rd bid by responder at the 3 level or higher is usually
considered a GF. Also 1x - 1y - 2NT, anything but pass is usually a GF.
There is a convention where 3C there is to stop in part score (Wolff?)."

The state is `we.forcing = game` (it existed). What was missing is what
creates it:

| trigger | where | status |
|---|---|---|
| a call whose meaning forces (2/1 on a 2/1 card, strong jump shift, reverse ...) | the rule's `sets forcing=game` | 2/1 built 2026-09-30 (responses.notes.md) |
| fourth suit forcing, game-forcing variant | fourth-suit-forcing.bid, the card's `fourth_suit_forcing.game_force` | built 2026-09-30 |
| XYZ 2D | a new module | not built |
| responder's third bid at the three level, below game (3C-3S), uncontested | `force game` here | built |
| after 1x-1y-2NT, anything but pass (Wolff's 3C excepted) | `force game` here | built |

`force game` (engine 0.4.0, LANGUAGE.md §3) is a declaration, not a rule:
it applies whichever rule made or explains the call, because these forces
belong to the shape of the auction.

## Measured (2026-09-30)

Random deals (20,000 Pavlicek, 21GF both sides) +23, corpus +7 IMPs vs
BBA, double-dummy par as the yardstick; no new "no rule" or broken-force
boards. Small because few auctions reach these shapes without a rule that
already forces; the declarations matter for the rules written against
`we.forcing = game` (control bids, the keycard ask, fast arrival).

## Open

- "Usually considered a GF": exceptions some partnerships make
  (responder's third-bid preference to opener's minor at the three
  level) are not carved out; say if they should be.

## Forces from the shape, and game when nothing else applies (2026-11-27)

Ruling: Rick, 2026-11-27 (after Thorvald's mail of 2026-11-25 on Brill daily 2026-11-24 MP-strong b6): "after a 1M-1N-2N, any bid should be GF. so we shouldn't stop in a GF sequence. We could add a rule not to pass after partner's unknown bid, but this could generate an auction to 7NT if both sides take that view."

- `force game after 1M (P) 1N (P) 2N (P) when !call = P`: the existing
  declaration's `1y` is a suit, so the forcing 1NT was left out. A
  declaration holds for a call no rule reads (checked: Brill's
  artificial 3H shows `[GF]` in `explain-auction`), so the force does
  not depend on understanding the call.
- The game catch-all (`when we.gf, !game_reached, !they.bid`, priority
  -70 to -77, below every other rule): with the force on and no rule left, the engine used to
  pass anyway (docs/CONTRACT.md, "No rule"). Now: a known fit's game,
  else 3NT, else game in my own five-card suit, a four-card major, then
  any game. Each is game, so it ends the force: this is the bounded form
  of "don't pass partner's unknown call" that Rick's 7NT worry asks
  for. Brill 2026-11-24 MP-strong b5 (2C P 2D P 3C P 4C P, passed with
  25 HCP) now bids 5C.
- Round forces are not caught: a round-forcing call no rule answers
  still passes. None of the nine Brill boards needed it.

## Sources

- Rick's rulings, 2026-09-30 (quoted above).
- Responder's third bid at the three level and the 2NT-rebid game force:
  standard practice, not yet cited.
- Rick's ruling of 2026-11-27 quoted above; Thorvald Aagaard's mail
  "Bidding misunderstanding" (2026-11-25); the round-3 "No rule applies"
  list in rusty-bidding-bot docs/reviews/2026-11-27-brill-gaps.md, (d).
