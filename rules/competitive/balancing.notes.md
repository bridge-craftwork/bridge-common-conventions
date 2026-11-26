# The balancing seat (`balancing.bid`): notes

They opened, partner passed, RHO passed; or they found a fit and stopped at the two level. Cases: `balancing.test`.

## Guidance (Rick, 2026-09-22)

Follow BBA's meanings, which are the usual lighter balancing ranges:

- **reopening double** 8+ total points with three or more cards in every
  unbid suit (or 18+ with any shape, as in the direct seat; 16+ since
  2026-11-26, "Borrowing a king");
- **a suit at the one level** 8-15 total points with five cards, **at the
  two level** 10-15;
- **1NT** 12-15 balanced with a stopper — `nt_overcalls.balance.range_min`
  and `_max`, not the 15-18 of the direct seat — and **2NT** 19-21.

A balanced 16+ is too strong for the balancing notrump and doubles first.

## Evidence

`bba-cli --all-meanings` on the `Balancing` scenario (21GF cards, 5,197
calls). Grouped by the opening they reopened over:

| call | BBA's meaning |
|---|---|
| X | "reopening double", 8-37 total points, 3+ in each unbid suit |
| 1NT | "NT style", 12-15 total points, 2-5 in every suit |
| 2NT | "NT style", 19-21 |
| suit, one level | "bidable suit", 8-15, 5+ |
| suit, two level | "bidable suit", 10-15, 5+ |
| cue bid | Michaels (not on our card) |

Advancer over the reopening **double** needs no new rules: those
contexts in `takeout-double.bid` carry the balancing spelling of their
patterns (`(1x) P (P) X (P)` beside `(1x) X (P)`), and the notrump
modules carry `(1x) P (P) 1N (P)`, so systems are on over the balancing
notrump too.

Advancer over the reopening **suit bid** now has its own block in
`advances.bid` (2026-09-23): partner is 8-15 rather than 8-17, so the
raise is 9-11 rather than 7-11, 1NT is 10-11, 2NT 13-15, a new suit at
the one level 7+ and at the two level 11+, and the cue bid 13+. Those
are BBA's own `Balancing` meanings. The direct-seat block no longer
carries the `(1x) P (P) 1y (P)` spelling. Effect over the three
balancing scenarios: calls +5, contracts 11.7% → 12.1%, par +98 IMPs,
identical auctions 8.7% → 8.1%.

A two-level overcall in the balancing seat is left to the bare pass rule
in `advances.bid`: BBA's advancer passed 32 of the 33 in the corpus.

Effect: the `Balancing` scenario gained 6.7 points of call agreement,
11.0 of identical auctions and 13.4 of contracts; Too_Strong_for_Overcall4th
+4.1 calls; Trap_Pass_Opener +1.9 calls and +6.2 auctions. Summed over
the 46 scenarios that moved: calls +29.8, contracts +11.0, auctions -6.8
(a handful of weak-notrump scenarios where BBA passes the hand out).

## Gaps and open questions

- **Jump overcalls in the balancing seat** are not written: a jump there
  is natural and intermediate, not the weak jump of the direct seat.
- Reopening over a **two-level or preemptive opening**, and the balancing
  double of 1NT.
- Michaels and the unusual notrump in balancing after (1x) P (P) (the
  direct-seat ones are in `two-suited-overcalls.bid`, 2026-09-28;
  Basic-Bridge plays neither). Over their fit, 2NT is written (below).
- **Over their fit, not written:** stops after a preference or a
  rebid (1x P 1N P 2x, 1x P 1y P 2x), three-level stops (1M P 3M), a
  passed partner who doubled or bid first, the cue bid of their suit,
  vulnerability (the three-level suit is the same vulnerable), and the
  balancer's second call (he passes whatever advancer does).
- **The balancing suit's floor** (8, Rick 2026-09-22) is not three below
  the direct overcall's 8: for Rick.

## The reopening double is read as the unbid suits (Rick, GIB tree, 2026-11-25)

As the direct double (takeout-double.notes.md): read as 3+ in each
unbid suit (majors 3-4, minors 3-5) and 8+ total points (GIB: 3+ in
each, 9+ HCP). Lengths min-wide: 1,527 call-boards, now none; GIB's
9 HCP against our 5 is left (our 8 total points is Rick's and BBA's).

How it is written: a second rule for the same call, never chosen
(`when bare(C), !bare(C)`: no hand meets it, and a reader cannot judge
it, so it stays possible when the call is read), one priority above the
rule that bids. Partner reads the call by the higher rule alone
(docs/LANGUAGE.md section 8), so the description narrows and no call
changes (BIDDING-MODEL 3.6; the idiom of rkcb-1430.bid). The cost: these
calls count in compare's "calls read as a higher rule than chose them".

## Borrowing a king (Rick, 2026-11-26)

Rick: balancing calls are normally about three points lighter than the
same call in the direct seat, (1♣) P (P) 1NT 12-14 where the direct
1NT overcall is 15-17; partner subtracts the king when he answers, so
it is not counted twice, and his thresholds are about three points
higher (BIDDING-MODEL 3.8). What that changed:

- **The balancing 1NT** stays `nt_overcalls.balance.range_min/max`,
  default 12-15: three below the direct 15-18 that 21GF-DEFAULT and
  21GF-GIB play (neither card sets either range; both run on the
  defaults). The card has no way to say "three below whatever the direct
  range is", so a card that changes the direct range should change this
  one too. Advancer needs nothing: systems are on, and the strength
  bands count against the 12-15 the call showed (2NT invites with
  10-12, 3NT 13+, Stayman 10+; `rbb bid rules -a "1C P P 1N P"`).
- **Advancing the reopening double** has its own block now (the
  direct block in takeout-double.bid no longer carries the `(1x) P (P) X
  (P)` spelling): the cheapest suit 0-11 (direct 0-8), the jump 12-14
  (9-11), 1NT 10-13 (7-10) and above a four-card minor, 2NT 14-15
  (11-12), 3NT 15+ (12+), the cue bid 15+ (12+).
- **The reopening doubler's rebid**, three below the direct doubler's:
  pass with 13 or less (16), the raise 14-16 (17-19), the jump raise
  17-18 (20-21), game 19+ (22+); a new suit 16+ (18+), 1NT or 2NT 16-18,
  just above the balancing notrump (19-21 above the direct one).
- **The reopening double with any shape** starts at 16 total points
  (was the direct seat's 18): the balancing suit bids stop at 15, so a
  16-17 hand with a long suit and no takeout shape had no call and passed
  the opening out.
- **Advancing the balancing suit**: advances.bid, same date.

GIB's tree (archived, 21GF-GIB readings) after (1♣) P (P) X (P): the
cheapest suit 13-, a jump 9-15, 1NT 7-10, 2NT 11-14, 3NT 13+, the cue
11-16; after (1♦) P (P) X (P) 1♥ (P), the doubler's 1NT 16-21. GIB lifts
the cheapest answer by four but keeps the direct jump and 1NT floors;
ours lifts all of them by three, as Rick ruled. GIB's balancing 1NT is
11-14 HCP.

## Over their fit (Rick, 2026-11-26)

Rick: we never balanced in the pass-out seat after the opponents found a
fit and stopped low; the pass was our only call there (about 24,000
call-boards in a 100k random-deal comparison). Written now for the two
commonest stops:

- **(1x) P (2x) P (P)**: they raised. Note the geometry: the balancer is
  the player who passed the opening in the direct seat, so every hand
  with a direct call (an overcall, a 12+ takeout double, a five-five
  Unusual 2NT) is already gone. What is left is short in their suit with
  the unbid suits but under 12, a five-card suit too weak to overcall, a
  six-card minor below a two-level overcall, a five-four two-suiter.
  - **X**: a singleton or void in their suit, three or more in each
    unbid suit (over a minor, four-four in the majors with up to three
    of theirs), 8+ HCP. Partner reads 8-11 (his earlier pass caps it).
    A doubleton was allowed first and lost (Measurements).
  - **2S/2H/2D** (an unbid suit still at the two level): five cards,
    8+ total points, the longest unbid suit, above the double for a major.
  - **3C/3D/3H**: five cards, 11+ total points, six cards or 10 HCP,
    and a singleton or void in their suit.
  - **2NT**: two places to play, the two lowest unbid suits (the minors
    over a major, diamonds and hearts over clubs, clubs and hearts over
    diamonds), five-four or better, 9+ total points, no four cards in
    the unbid major; above the natural three-level suit. Moved here from
    two-suited-overcalls.bid, where it was the Unusual 2NT (five-five,
    11+) and only with the convention on.
- **(1x) P (1y) P (2y) P (P)**: opener raised responder. The balancer
  passed over the response; partner passed the opening.
  - **X**: a singleton or void in their suit, four or more in an unbid
    major, three or more in an unbid minor, 8+ HCP.
  - **2NT**: both unbid suits, four or more each and nine or more
    between them (`x+y<=4`), 9+ total points.
  - A natural suit as above, at the two or the three level.
- **Advancer** passed over the raise or the opening, so he has at most
  about 11 and partner's balance was made on his values. He answers the
  double at the cheapest level: a four-card major first, then a
  four-card minor, then the longest three-card suit (by priority; within
  each the longer, hearts and clubs on equal length), jumps in a
  major only with four and 12+, bids 3NT with 14+ balanced and their
  suit held, and passes the double with five of their trumps (GIB's
  tree reads that pass the same way). Over 2NT the longer of partner's
  two suits, the cheaper with equal length. Over a natural balance he
  passes (the defending side's fallback in advances.bid).

### Against GIB's tree (archived and fetched 2026-11-26)

| position | call | GIB | ours | why we differ |
|---|---|---|---|---|
| 1♥ P 2♥ P P | X | 2- ♥, 3+ others, 14-16 total | 1- ♥, 3+ others, 8-11 HCP | GIB counts shortness in its total; our floor is Rick's borrowed king (8 HCP), the earlier pass caps the top; the singleton is measured |
| 1♥ P 2♥ P P | 2♠ | 5+, 10-16 total | 5+, 8+ total (4-13 HCP) | the borrowed king: a sound 10 would usually have overcalled 1♠ |
| 1♥ P 2♥ P P | 3♣/3♦ | 5+, 10-16 total | 5+, 11+ total, six or 10 HCP | close |
| 1♥ P 2♥ P P | 2NT | Unusual, 5-5 minors, 14-16 | 5-4+ minors, 9+ | the five-five would have bid 2NT over 1♥ |
| 1♣ P 2♣ P P | X | 2- ♣, 3+ others, 14-16 | 1- ♣ (or 4-4 majors), 8+ HCP | as above |
| 1♣ P 2♣ P P | 2NT | Unusual, 5-5 ♦♥ | 5-4+ ♦♥ | as above |
| 1♦ P 1♠ P 2♠ P P | X | 4+ ♣, 4+ ♥, 14-20 | 1- ♠, 4+ ♥, 3+ ♣, 8+ HCP | ours allows a three-card minor |
| 1♦ P 1♠ P 2♠ P P | 2NT | Unusual 5-5 ♣♥ | 4+ each, nine cards | as above |
| 1♥ P 2♥ P P X P | 2♠/3♣/3♦ | 4+ in the suit | four-card major, four-card minor, else the longest; nothing shown | selection by `when`, so partner reads no length |
| 1♥ P 2♥ P P X P | 3♠ | 5+ ♠, 10+ HCP, forcing | 4+ ♠, 12+, invitational | Rick's three points |
| 1♥ P 2♥ P P X P | P | 5+ ♥ | 5+ ♥ | agreed (added after the check) |
| 1♥ P 2♥ P P 2NT P | 3♣/3♦ | 3+, 3- total points | the longer | GIB's 3- is an artefact of its other calls |
| 1♦ P 1♠ P 2♠ P P X P | 3♣/3♥ | 3+, 8- total | the longer | GIB jumps with more; we do not |

GIB has calls we do not (3♥ cue bids, 3NT, game jumps over the double);
left out, and so are jumps in the balancing seat over their fit.

## Measurements (2026-11-26)

Engine `freak-patterns` 070f438, card 21GF-DEFAULT (NS) / 21GF-GIB
(EW) as the corpus files say; base: pack `bottom-review` (5e0ce45),
variant this branch; `rbb compare` with `--rules-at`, scored by
`probes/tools/errors_diff.py` (the actor's contract errors, an overbid
going down undoubled taken as doubled; Rick 2026-10-31).

**100,000 random deals** (`.rbb-cache/random`, Random_Pavlicek_21GF),
final version (e44e095): 1,682 boards changed; the actor's contract
errors **+1,170 IMPs (+0.70 a board; halves +689 / +481)**, all errors
+2,076, distance from par +666, IMPs to the actor +2,245. By first
differing call:

- the reopening double's advances three points up gained most: P X P
  3NT→1NT +153 (34 boards), 3C→2C +146 (60), 3C→1NT +85, 2H→1H +81,
  2S→1S +79, 3D→1NT +61;
- the any-shape reopening double from 16 (was 18): (1♣) P (P) X −56 on 94
  boards, (1♦) P (P) X −33 on 114, by contract errors; by all errors
  +222 and +329 (advancer's penalty pass of the double, and the
  defence, gain). A bidding-or-doubling call: reported both ways, kept;
- over their fit (239 boards): X +26 (61 boards), 2NT +27 (105), 2♠ −12
  (40), the three-level suits +8 (31); over hearts +61, over spades −18.

**The singleton.** The first version let the balancer double, or bid a
three-level suit, with a doubleton in their suit. On the same deals
that version (fb555cb) lost on every such call: the double with a
doubleton −2.5 a board (129 boards under 11 HCP, −322 IMPs; −0.7 with
11+), the three-level suit −1.5 to −1.7; with a singleton or void both
gained (+0.25 to +3). So both now need shortness; 2NT (five-four) gained
with either and keeps no such condition, and the two-level suit with a
doubleton (−0.6 on 30 boards) is left allowed. The advancer bug found
on the way: `prefer` once let a three-card major outrank a four-card
minor (3♥ on a 6-card fit at the three level, 12 corpus boards).

**Corpus tripwire** (`compare --limit 50`, all 344 scenarios): 137
boards changed, the actor's contract errors +6 (halves −3 / +9), all
errors −24, distance from par −18: no calls outside the balancing seat
moved beyond noise. `bid test`: 3,359 cases, 5 failures, the known five
in serious-3nt.test.

## Sources

- **Rick's rulings:** follow BBA's meanings, which are the usual lighter
  balancing ranges (2026-09-22).
- **BBA evidence:** `bba-cli --all-meanings` on the Balancing scenario
  (21GF cards, 5,197 calls), tabled in "Evidence"; advancer's ranges over
  a balancing suit bid are BBA's own Balancing meanings. No
  `probes/*.toml` spec yet.
- **Book practice:** the lighter balancing ranges are standard practice,
  not yet cited to a book or article.
- **Corpus measurements:** the three balancing scenarios and the 46 that
  moved (2026-09-23).
- **Rick's rulings (2026-11-26):** balance over their fit at the two
  level; balancing calls about three points lighter than direct ones and
  advancer's thresholds about three higher ("borrowing a king"),
  BIDDING-MODEL 3.8.
- **Book practice:** competing over their fit at the two level rests on
  the Law of Total Tricks (Larry Cohen, *To Bid or Not to Bid*, 1992:
  when they have a fit, so do we, and their two-level partscore is the
  one not to sell out to). "Borrowing a king" (the balancer bids as if he
  held a king more, and partner takes it back) is standard teaching;
  the exact ranges here (8 HCP for the double, 8 total points for a
  two-level suit, 2NT five-four for two places to play, advancer three
  points up) are standard practice, not yet cited.
- **GIB's tree** for the new positions (archived 2026-11-26): the table
  in "Over their fit"; GIB is a check, not the target (Rick).
- GIB's bidding tree (BBO's `gibrest`, archived in rusty-bidding-bot `.rbb-cache/gib-tree/xml/`), agreed-path comparison on 21GF-GIB (top 5,000 positions of 100,000 random deals), Rick 2026-11-25 (BIDDING-MODEL 3.6 and 4.3): the description rules and floors in the section of that date above.
