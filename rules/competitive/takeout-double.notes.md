# Takeout doubles (`takeout-double.bid`): notes

The direct double of a one-level opening, advancer's replies, and the
doubler's rebid. Cases: `takeout-double.test`.

## Guidance (Rick, 2026-09-22)

- **12 total points with three or more cards in every unbid suit.**
- **18+ total points doubles whatever the shape**, including with a long
  strong suit: too strong to overcall is double first, then bid the suit.
  That is why the double's second branch starts one point above the
  overcall maximum (`overcalls.one_level_max` + 1).
- **Advancer answers on the standard ladder**: the cheapest suit is 0-8,
  a jump 9-11, and the cue bid of their suit 12+ and forcing to game.
  (BBA's own ladder is 0-10 / 7-12 / 10+, which we did not copy.)
- Advancer bids his longest suit, majors first, and the cheaper of two
  equal suits.
- **The doubler passes a minimum** and shows his extra values afterwards:
  18-19 raises one level, 20-21 two, 22+ bids the major game, and a
  five-card suit of his own is bid at the cheapest level.

## Evidence

From `bba-cli --all-meanings` on the two Basic scenarios:

- **(1x) X** — "takeout double", 12-37 total points, 3+ in each unbid
  suit and at most four of theirs. The hands were 10-18 HCP, median 13,
  and typically 4-4-3 or 4-3-3 in the unbid suits.
- **(1x) X (P)** — advancer: a minimum suit bid 0-10 total points with
  4+; a jump 7-12; the cue bid "strength cue bid", 10+.

The double is what BBA does with most 12-17 balanced-ish hands short in
their suit: it is the single largest divergence in these two scenarios
(424 of the 1,000 boards diverged at call 2 with BBA doubling and us
passing). Adding it took call-2 agreement from 46.6% to 87.5%.

## Accepted differences from BBA

- Our ladder starts the jump at 9 and the cue bid at 12; BBA's bands
  overlap (7-12 for a jump, 10+ for the cue bid), so boundary hands
  differ.
- BBA doubles some 10-11 HCP hands with shape that we pass, and passes
  some 12-counts with a five-card suit that we double.
- We require three cards in every unbid suit; BBA's meaning allows a
  doubleton in an unbid minor on stronger hands.

Advancer when RHO does not pass is written too: a free bid needs 6+ at
the one level and 8+ higher, the cue bid is still 12+, and over a
redouble advancer names his cheapest four-card suit however weak. That
alone took Basic_Takeout_Double from 71.3% to 72.5% of calls and its
contracts from 5.6% to 7.4%.

## Gaps and open questions

- **Responsive doubles** are in `responsive-doubles.bid`, switched on by
  `doubles.responsive.play` — the 21GF cards play them, Basic-Bridge does
  not, so on this card a double by advancer over their raise still has no
  rule.
- The **penalty pass** of a takeout double with length in their suit.
- Doubles of anything but a one-level suit opening: weak twos, preempts,
  1NT, and the **balancing double**.
- Advancer's rebid after the cue bid (the cue sets `forcing=game`, so the
  base rule bids game in the agreed suit or 3NT).

## Advancer, probed (2026-09-25, `probes/advance-1S-X.toml`)

2,000 random advancer hands after 1S X P (Basic-Bridge). Agreement
before: 45%; after: 55%. Corpus: -162,699 -> -162,394 (+305).
- **3NT with 12+ and their suit stopped** (no four-card unbid major),
  where we cue-bid. Worth +72 alone. **For Rick:** this overrides "the
  cue bid is 12+" for hands with a stopper. Test 19 now expects 3NT.
- **No four-card suit to name** (four of their suit, say): BBA bids the
  cheapest three-card suit. We had no call.
- **1NT is 7-10 HCP** with a stopper. Total points put 5-3-3-2 hands
  with nine or ten out of range, leaving them no call.
- **Jumps:** BBA does not jump with four cards and 9 HCP. It jumps with
  five from about 8, or four with 10-11. Four cards and 9 now bid at the
  cheapest level.

Not done: BBA's penalty pass with long strong trumps; the rest of the
disagreement is mostly the level with 9-11 (2S cue vs 3H...).
- **Their suit is not an unbid major** (2026-09-25). The advances in a
  minor said S<=3, H<=3, meant to prefer an unbid major. That left four
  of their suit (spades over 1S) with no call: 177 corpus boards. The
  guards now read `S<=3 | x is S`. The heart advance says the same about
  spades. Corpus: -162,394 -> -162,157.

## The double itself, probed over 1S (2026-09-25, `probes/tod-1S.toml`)

2,500 hands with three or fewer spades and 9-19 HCP over 1S: 80%
agreement. BBA's threshold is HCP by shortness. With a singleton in
their suit it doubles from 10-11 HCP (and prefers the double to a
two-level minor overcall at 11-14). With a doubleton it doubles from
12 HCP; 11 with a five-card suit passes, where our total points double.
Tried against par:

| Change | IMPs |
|---|---|
| 12 HCP, or 10 with a singleton | -314 |
| Our 12 total points, plus 10 HCP with a singleton | -380 |
| Two-level overcalls on three of the top five honours instead of four | -285 |

Ours stays in all three.

## The power double in HCP (2026-09-27)

Step a of the Law of Total Tricks work (Basic_Takeout_Double 193). The
double's second meaning was "18+ total points, any shape". Length
points can add nine to an unknown hand, so no HCP limit could ever rule
the power hand out, and the double never collapsed to "three or more
in the unbid suits". BBA (`probes/tools/takeout_shape.py` and a scan
of 913 auctions where the doubler, free to pass, then bids a new suit
or notrump): its power double steps up at 17 **HCP** (12-14: 103
hands, the competitive minimum; 15: 9; 16: 5; 17: 129; 18: 268), and
counted as HCP plus length the same hands show no step. Rick: treat it
as a likelihood, accepting the rare distributional power double below
17 that the inference will misread.

| power branch | full corpus (par / side) | Basic_* competitive |
|---|---|---|
| 18+ HCP, overcall to 17 | -937 / -2,176 | -3 / -26 |
| 17+ HCP, overcall to 17 (overlap) | +13 / -171 | -11 / -11 |
| 17+ HCP, overcall to 16 | +1 / +154 | -11 / -11 |

Kept: 17+ HCP with the overcall to 16 (`one_level_max` default 16),
neutral on its own; its value is the inferences it allows. **For
Rick:** this lowers the overcall ceiling from 17 to 16 HCP; the
fallback is the overlap version (overcall to 17), -171 by side.

## Step c: the doubler's pass denies the power double (2026-09-27)

For the double to collapse to its shape, a pass must deny 17+ HCP.

- The doubler's rebids after an advance: the "minimum" pass is now 16
  HCP or less (was 17 total points); the strong actions are "18 total
  points, or 17 HCP". Moving the ladder wholly to HCP lost (-38 by par
  distance, -327 by side: 15-16 counts with a long suit stopped bidding
  it); the mixed version is neutral (+1 / -58).
- After advancer's cue bid and opener's rebid (1♥ (X) P (2♥) 3♥, board
  193) there was no rule. Now: double with 17+; pass with 16 or less
  (BBA's forcing pass, and ours where the force allows it); where the
  game force rules the pass out, a four-card suit or notrump. The suit
  bids rank **below** the pass, so a pass denies only the power hand:
  ranked above it, the pass also denied every four-card suit and read
  South as exactly 3-4-3-3. Full corpus +100 / +139, Basic_*
  competitive +17 / +24.

On board 193, North now reads South's pass as 0-16 HCP with three or
more spades, diamonds and clubs.

## The second double, (1x) X (2x) P (P) X (2026-09-27)

Ticket basic-takeout-double-b89: our West raised 1♠–X–2♠ at once
(BBA passed and bid 2♠ a round later), and Rick asked whether that shut
North–South out of their club fit. It did not in BBA's hands: given
`1S X 2S`, bba-cli goes on `P P X P 3C`, the same +130 as its own
auction. What shut us out was our doubler's pass. The second double
(12+, short in their suit) had been left out on 2026-09-25 as costing
~1,500 IMPs against par, but advancer had no rule after it and left
every one in for penalty. With takeout answers (longest unbid suit, a
major first; pass with five trumps and 5+):

| doubler shows | full corpus (par / side) | boards |
|---|---|---|
| **x<=1, 12+ (kept)** | **+169 / +377** | 212 |
| x<=2, 12+ | +159 / +515 | 372 |
| x<=1, 14+ | +136 / +244 | 124 |

Both yardsticks agree on all three; the singleton version is best by
par. Advancer with 4-4 in the minors bids 3♦ (3♣ measured 6 IMPs
worse on both, noise). Board 89 now goes `1S X 2S P P X P 3D`, +110
against BBA's +130.

## Wasted honours in their suit (2026-09-27)

Ticket basic-takeout-double-b60: South doubled 1♠ with
QT.J95.KJ95.KQT2 (12 HCP, NS vulnerable), BBA passed. Rick asked how
BBA values such hands: his instinct was that the QT is not worth two
points, that the tens and nines should help, and that a shape double
wants 13+ dummy points.

`probes/td-1S-shape.toml`: 500 hands, 10-15 HCP, a doubleton spade and
three or more in the other suits, over 1♠, all four vulnerabilities.
Without a five-card minor:

| spade holding | 12 HCP | 13 HCP |
|---|---|---|
| no honour | X 12 | X 13 |
| A or K (with or without J) | X 10 | X 13 |
| Q or J alone | **P 10** | X 7 |

So BBA marks a lone queen or jack in a doubleton of their suit down by
about a point, and the same at every vulnerability. It gives no
visible credit for tens and nines here (QT passes like Q2), and a 12
count with a doubleton and nothing wasted doubles: it does not ask for
13 dummy points.

Played at every vulnerability the discount splits the yardsticks: +418
par, −218 side IMPs (360 boards). By the doubler's vulnerability:

| doubler / opponents | boards | side | par |
|---|---|---|---|
| nv / nv | 82 | −78 | +94 |
| nv / vul | 83 | −104 | +137 |
| **vul / nv** | 96 | **+3** | **+101** |
| vul / vul | 99 | −39 | +86 |

Only at unfavourable do both agree, which is where Rick's "especially
vulnerable" pointed. Kept there: +103 par, +23 side (108 boards).
Elsewhere the light double wins by side IMPs (it gets us into the
auction). Board 60 now passes 1♠ as BBA does.

## After the redouble (2026-09-27)

Ticket basic-takeout-double-b197: `1S X XX P P P`, −520. Two holes:

- Advancer's rules after the redouble kept `S<=3, H<=3` on the minor
  suits, meant to send four-card majors to the major but also blocking
  a minor when the four spades were *their* suit. North,
  J975.JT.KQ972.87, had to pass; BBA bids 2♦ (`rbb probe`, prefix
  `1S X XX`). Now `S<=3 | x is S`, like the other advance rules.
- The doubler had no rule after `(1x) X (XX) P (P)` and sat in the
  redouble. Advancer's pass there says no four-card suit to name, so
  the doubler now runs to his cheapest four-card suit (partner
  corrects), and leaves it in only with four of their suit.

Full corpus: +2,567 par, +4,771 side IMPs (604 boards).

## Game in a known fit; minors up the line (2026-09-27)

Ticket basic-takeout-double-b455: `1H X P 2H 3H 4D P`, and North, with
five spades opposite a double that promised three, had no rule in a
game force. The game-force fallback in base.bid knew only the agreed
suit and 3NT; it now also bids game in an eight-card fit that has been
shown but not agreed (a major ahead of 3NT, a minor after it). The
doubler shows four-card minors up the line (clubs with 4-4).
Full corpus: +1,392 par, +1,698 side IMPs (1,049 boards). One test
changed: 2C 2D 2H with three hearts and 8 HCP now bids 4♥, not the
fallback 3NT.

## The strong balanced double when they raise (2026-10-05)

`(1x) X (P) 1y (2x)`: the doubler with 18-19 balanced and their suit
stopped bids 2NT, as without their raise (BBA bids it: We_Overcall_1N
board 343). Found by the Raptor self A/B (raptor.notes.md), where the
strong balanced hands double instead of overcalling 1NT; before, the
doubler passed.

## The double is read as the unbid suits (Rick, GIB tree, 2026-11-25)

The takeout double of a one-level opening ("the unbid suits and 12+,
or any 17+") narrowed no length: a range cannot hold the "or". It is
now read as the normal double, 3-4 in an unbid major, 3-5 in an unbid
minor, 12+ total points (GIB's tree: 3-4 / 3-5, 2- in theirs). The
power double still makes the call and shows itself by bidding again;
until then partner counts on the unbid suits (Rick's 3.6: freaks and
strong hands borrow a normal call). Lengths min-wide on agreed paths:
6,214 call-boards, now none (the maxima were added after that run).

Test changed: QJ32.K84.T54.932 after 1♥ X 2♥ now competes 2♠
(total-tricks.bid, eight trumps known), where the test said pass. GIB's
tree bids it: 2♠ there is 4+ spades, 6-12 total points.

Open for Rick: the power doubler's next bid is read on top of the
double (after 1♦ X P 1♠ P 2♣ the doubler reads ♠3-5, ♥3-4), which is
wrong when the power hand is short in a suit.

How it is written: a second rule for the same call, never chosen
(`when bare(C), !bare(C)`: no hand meets it, and a reader cannot judge
it, so it stays possible when the call is read), one priority above the
rule that bids. Partner reads the call by the higher rule alone
(docs/LANGUAGE.md section 8), so the description narrows and no call
changes (BIDDING-MODEL 3.6; the idiom of rkcb-1430.bid). The cost: these
calls count in compare's "calls read as a higher rule than chose them".

**Short in their suit** (2026-11-26, the top 20,000 positions): the
description now also says two or fewer in their suit (GIB 2-; ours read
0-4, 6,214 call-boards "max-wide" on the twelve direct doubles of one
of a suit). The licence is unchanged: a 4-3-3-3 with three of theirs
and 12-14 still doubles, and partner plans on the normal shape (3.6).
The reopening double (balancing.bid) was checked too: ours reads 3-4 in
an unbid major and 3-5 in a minor where GIB says 3+, narrower, and its
6-7 HCP floor against GIB's 9 is the licence's 8 total points (Rick,
2026-09-22), so it is left. Measured (top 20,000): 6,214 call-boards wide in their suit -> 6.

## The power double converts (Rick, 2026-11-25)

A double is read as takeout. When the doubler then shows a suit of his
own or bids notrump, it converts to a power double: the takeout double's
shape and strength no longer hold, and the hand shows what an overcall of
that suit (or a 1NT overcall) would, with more strength: 18+ for a suit
(GIB may say 17+), and 19-21 for notrump, since our 1NT overcall is 15-18
(`hcp>nt_max, hcp<=nt_max+3`, from the card's 1NT overcall range). Every
suit and notrump rebid of the doubler carries `converts X` (engine
0.20.0), so partner reads the seat again without the double's meaning;
what the double denied stays. Raises of advancer's suit and cue bids do
not convert: the takeout shape still holds.

- `takeout-double.test`: the 2NT case after 1♣ X P 1♥ 2♣ now holds 19
  (K73.A5.AQ87.AQJ2); with 18 and clubs stopped the hand overcalls 1NT.
- The reopening double's notrump rebid uses the same range for now; a
  balancing 1NT's range differs, which may want its own band.

## The reopening double has its own advances (Rick, 2026-11-26)

The contexts here no longer carry the balancing spelling `(1x) P (P) X
(P)` for advancer and the doubler's rebid: partner subtracts the king
the reopening doubler borrowed, so those ranges are three points up for
advancer and three down for the doubler, in balancing.bid
(balancing.notes.md, "Borrowing a king"). The contexts where RHO bids
or redoubles over the reopening double still carry it.

## The doubler in the pass-out seat after their new suit (Rick, 2026-11-27)

Brill daily 2026-11-26, board 1, dealer North, none vul: P (1♣) X (2♥,
announced "6+ H, 6-9 hcp") P (P), and Rusty, South, passed with
QJ86.QJ.AKQJ5.K9 (19 HCP). Rick: "we have 20 total points and don't bid
again after LHO's weak bid. we should X here to show the other two
suits." No rule covered the seat: the rebid contexts after their new
suit were written for opener bidding again (`!rho.last=P`), so the
doubler passed by advances.bid's catch-all, and a double there was read
as penalty (penalty-doubles.bid).

Now `(1x) X (1y) P (P)`, `(1x) X (2y) P (P)` and `(1x) X (3y) P (P)`,
y a new suit:

| call | shows | why |
|---|---|---|
| X | 4+ in both unbid suits, 3- of theirs, 17+ total points, or 15+ with a singleton of theirs (5-5 or 6-4) | partner has passed, and the double takes the auction a level up: extras, more than GIB's 17+ only with the shape |
| cheapest suit | five or more, 18+ (17 HCP), converts X | the power double's suit, as when opener bids again |
| cheapest NT | balanced, 19-21 (`nt_max`+1..+3), responder's suit stopped, converts X; priority over X | the power double's notrump; the opening lead comes through responder's suit, so that stopper is the one asked |
| P | 17 or less | the rest |

Over their jump to three, `(1x) X (3y) P (P)`, every action is two
points higher: X 19+ (17+ with the singleton), a suit 20+ with five or
18+ with six, pass 19 or less; notrump stays 19-21 (it is 3NT).

X ranks first, so 5-4 in the two unbid suits doubles rather than bid the
five (partner may hold the other). Advancer answers the second double:
pass with five of responder's suit (penalty), else the longer unbid suit
(a major on a tie), a jump with 8+ total points.

No cue bid: partner has passed twice, so a huge hand doubles or bids its
suit, and a cue would need answers we have not written.

GIB's tree (`gib_tree.py show P-1C-D-2H-P-P`, archived): X 4 ♠, 4-5 ♦,
3-4 ♥, 2- ♣, 17+ total points; P 12-17; 2♠ 5+, 18+; 3♦ 6+, 18-20; 2NT
21-23 balanced, clubs and hearts stopped. Ours after the change: X ♠4
♥3 ♦4-5 ♣1-2, 17+ declarer points (the ♥3 is the first double's 3-4
with the new 3-); P 17 or less; 2♠ 5+ 18+; 3♦ five cards (GIB six);
2NT 19-21 (GIB 21-23: ours is the power double's range, Rick
2026-11-25). Our hand has two hearts, so the first double was already
the least lie (BIDDING-MODEL 3.6); the reading assumes three.

Our own engine never reaches the seat: our responder's jump after a
double is fit-showing (forcing) and a non-jump new suit is forcing, so
opener always bids again. BBA reaches it on 7 of the 17,155 tripwire
boards and 84 of 100,000 random deals; ours on none. To make it arise
in self-play, `vs_to_double.jump_shift = weak` (after-interference.bid,
new) gives the opponents weak jump shifts over a double.

Open (engine): with Brill's meanings (`--meanings '["","3+ clubs","","6+ H,
6-9 hcp"]'` on 21GF-GIB) our reading of their 2♥ stays the fit-showing
jump, narrowed by the text: 6-9 HCP and six hearts, but still four or
more clubs, `trump ♣` and F1 for their side. The text does not
contradict the rule arithmetically (the rule's floor is 10 total
points, which 6-9 HCP with six hearts can reach), so the engine
narrows instead of replacing, and the club length the text never
mentions stays. The doubler's call is X either way.

**Measured (2026-11-27, engine `freak-patterns`, 21GF-DEFAULT against
21GF-GIB):**

- `bid test`, whole pack: 3,413 cases, 3,408 pass; the 5 failures are
  the known serious-3nt ones.
- Tripwire, `compare --limit 50` (17,155 boards): no auction of ours
  changed. In replay one call changed, on Minor_Suit_Opener 1 (1♦ X 2♥
  P P with Q97.KQ4.AT.AQ754): 3♣ now, as BBA bids.
- 100,000 random deals as dealt: no board changed (we never reach the
  seat); in replay 32 more calls agree with BBA (853,378 to 853,410).
- With `--set vs_to_double.jump_shift=weak` (both pairs), 127 of the
  100,000 boards reach the seat; against the same run without these
  rebids (weak jumps on in both), 23 boards changed. The acting side's
  contract errors: -35 IMPs (halves -40 / +5, they differ: noise);
  distance from par +31, doubling errors of the acting side +33. The
  second double over a two-level jump gained (+11 on 3 boards);
  single-board losses on 3NT, 4♦ and 3♥ over a three-level jump. A
  first version with the two-level floors at three as well lost -58 on
  30 boards with the halves agreeing, which is why the three-level
  block asks for two points more.
- The weak jump shifts themselves (`vs_to_double.jump_shift=weak` on
  both pairs, against fit-showing jumps on the same deals): 369 boards
  changed, the acting side's contract errors -295 (halves agree), the
  jumps 1♠ X 3♣ / 1♥ X 3♦ / 1♠ X 3♥ losing most. Not a verdict on the
  convention (its own notes), only on our three-level weak jumps over
  a double, which want seven cards or a lower top: open question.

## The doubler again: minors over their raise, game opposite the jump (Brill gaps, 2026-11-27)

- `(1x) X (2x) P (P)`: the minors at the three level, five with 17+ or six
  with 16+ (1♥ X 2♥ P P with KJ3.QT.AKQ8432.Q: 3♦; with AQ6.T84.AJ.AKJT6:
  3♣). Only the majors were written (16+ and five).
- `(1x) X (P) 2y (P)` after the jump advance (`partner.jumped`): game in a
  six-card major with 18+ total points (1♣ X P 2♦ P with A.AKQ98765.K.J87:
  4♥; we bid 2♥, field 4♥).

## Sources

- **Rick's rulings:** the double (12 total points and three cards in
  every unbid suit, or 18+ any shape), advancer's standard ladder (0-8,
  9-11, cue bid 12+), the doubler's rebids (2026-09-22); the power double
  as a likelihood from 17 HCP (2026-09-27). Tickets
  basic-takeout-double-b89 (the second double) and -b60 (wasted honours
  in their suit, "especially vulnerable"), 2026-09-27.
- **Book practice:** the advancer ladder is the "standard ladder" in
  Rick's words, as opposed to BBA's 0-10 / 7-12 / 10+. Standard practice,
  not yet cited to a book or article.
- **BBA evidence:** `bba-cli --all-meanings` on the two Basic scenarios;
  the scan of 913 auctions with `probes/tools/takeout_shape.py`.
- **BBA probes:** `probes/advance-1S-X.toml` and `probes/tod-1S.toml`
  (2026-09-25), `probes/td-1S-shape.toml` (2026-09-27), and `rbb probe`
  after the redouble.
- **Corpus measurements:** the power-branch table and the later steps,
  judged by par distance and by side IMPs.
- **Where we differ:** our ladder bands against BBA's overlapping ones;
  boundary doubles; three cards in every unbid suit ("Accepted
  differences from BBA"). The overcall ceiling moved from 17 to 16 HCP,
  pending Rick.
- GIB's bidding tree (BBO's `gibrest`, archived in rusty-bidding-bot `.rbb-cache/gib-tree/xml/`), agreed-path comparison on 21GF-GIB (top 5,000 positions of 100,000 random deals), Rick 2026-11-25 (BIDDING-MODEL 3.6 and 4.3): the description rules and floors in the section of that date above.
- GIB's tree, the top 20,000 positions (2026-11-26; Rick 2026-11-25, BIDDING-MODEL 3.6): the double's description short in their suit.
- Rick, 2026-11-25: the power double converts when the doubler shows his own suit or notrump; 18+ for a suit (GIB 17+), 19-21 for notrump.
- Rick, 2026-11-27 (Brill daily 2026-11-26 board 1): the doubler doubles again in the pass-out seat to show the other two suits. GIB's tree, P-1C-D-2H-P-P (archived), for the ranges. Advancer's answers and the notrump stopper rule: standard practice, not yet cited.
- Brill daily problem boards, 2026-10-08..11-26 (rusty-bidding-bot `docs/reviews/2026-11-27-brill-gaps.md`, patterns F2/F3/F4): the field's calls at each position, scored at double dummy; GIB's tree at the same positions as a check (`gib_tree.py show`).
