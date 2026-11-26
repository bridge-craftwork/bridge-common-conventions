# game-tries (`game-tries.bid`): notes

Game tries after 1M-2M, uncontested. Cases: `game-tries.test`.

## What the card says

| Field | `.bbsa` key | Meaning here |
|---|---|---|
| `other_conventions.two_way_game_tries.play` | `Two way game tries` | GIB's two-way tries |
| `other_conventions.help_suit_game_tries.play` | none | a new suit is a help-suit try |

21GF-GIB (the EW card of nearly every scenario) and 21GF-PolishTwoSuiters
set `Two way game tries`, so the tries fire across the corpus.

## The structure (2026-10-05)

- Range 17-18 support points with 14+ HCP: the 3M invitation's range in
  rebids.bid. BBA passes 15 HCP with a singleton opposite a raise
  (Two-Way_Game_Try), and a singleton honour counts twice in tp.
- Two-way: the step (1♥-2♥-2♠, 1♠-2♠-2NT) shows a void or a small
  singleton (not K, Q or J) in a side suit. Responder declines (3M) with
  6 or less, accepts with 10, and asks with the next step otherwise;
  opener names the short suit, or bids 3M when it is a step suit (spades
  over 1♥, clubs over 1♠); responder bids game without a K, Q or J
  there. Any other suit below 3M is a long-suit try: three or more with
  an honour (GIB: "at least a 3-card suit with some honors"); over 1♥,
  2NT is the spade try and needs four spades with the ace or K-Q. BBA
  bids 2NT with such spades ahead of the short-suit try (AK62.KJT42.KT4.2,
  AJ98.AQT82.AT3.6) and the short-suit try with QJ86 or KT32.
- Help-suit (without two-way): a new suit below 3M with three or more
  cards and two or three losers.
- Responder accepts a long- or help-suit try with at most one loser in
  the suit or four of them, or the top of the raise (10), or 8+ with the
  ace or king there.
- Priorities 13-15, above the control bids (slam/control-bids.bid, 12):
  over a single raise a new suit is a game try and partner must read it
  so. The other way round, opener with 20+ who makes a control bid in the
  step suit (2♠ over 1♥-2♥) is read as the short-suit try (Benjamin_2D
  49): rare, left.
- base/game-force.bid: responder's third bid at the three level forced
  to game; three of the agreed suit is now excluded (the sign-off after
  the shortness exchange, 1♠-2♠-2NT-3♣-3♦-3♠).

## BBA

In Two-Way_Game_Try and Help_Suit_Game_Try (21GF-GIB both sides) BBA
always asks after the short-suit try, and invites only from 16 HCP. It
tries less often than we do with 17-18 support points and a singleton.

## The long hand counts its own points (Rick, 2026-11-25)

Rick (2026-11-25): support points (HCP plus shortness) belong to the hand with the shorter trumps, the one raising; the hand with the long trumps counts its own points, HCP plus length (`hcp+length_points`, the engine's "decl"). The long trump hand counting support points "isn't normally done" (engine repo docs/BIDDING-MODEL.md, 3.3).

`try_values` is now 16-17 HCP plus length (was 17-18 support points),
the invitational band of rebids.bid's ladder after 1M-2M (GIB: 16-17
for 3M and the tries, 17-18 for its shortness try). Tests moved: AK62.
KJT42.KT4.2 (14 HCP, a singleton) passes 1♥-2♥ instead of 2NT;
AQT65.KQ76.K.Q72 tries 3♣ instead of bidding 4♠; AQJ74.KQ5.K83.Q2 and
AQJ74.AK5.983.K2 (17 HCP, 18) bid 4♠, and 16-HCP versions of them keep
testing the help-suit try. KQJ96.Q62.AT95.K now tries 3♦, not 3♥: both
long-suit tries qualify and the count change moved a descriptiveness tie
between them (open question: should the cheaper or the weaker suit be
preferred explicitly?).

## Sources

- BBO, "GIB system notes", Two-way Game Try,
  https://www.bridgebase.com/doc/gib_system_notes.php#Two-way_Game_Try
  (the step, the ask, "bids his major if the short suit is one of the
  step suits", long-suit tries, 3M general).
- Bridge Bum, "Help Suit Game Try",
  https://www.bridgebum.com/help_suit_game_try.php.
- Responder's thresholds (6 / 10, wasted K-Q-J): standard practice, not
  yet cited.
- **Rick, 2026-11-25**: the long-trump hand counts HCP plus length, never support points (engine repo docs/BIDDING-MODEL.md 3.3); GIB's bidding tree (`probes/tools/gib_tree.py show`, engine repo) for the ranges it states.
