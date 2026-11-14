# Worked examples: three conventions in the new format

A test of [CONTRACT.md](CONTRACT.md) against real content, written
2026-11-13 before anything is moved. Three conventions, chosen to cover three
different cases:

| Convention | Case it tests |
|---|---|
| Texas transfers | A convention with treatments, split from the ID it shares today |
| Bergen raises | A style choice (Reverse Bergen) that has its own ID |
| DONT | A defence, switched on in two ways |

Each is shown as it stands today and as it would look here: the definition
and the rule file's header. Nothing below is content of this repo yet. The
files are illustrations, and the summaries and references are placeholders
taken from today's files.

Sources read: `convention-card` v0.44.0 (`spec/fields.toml`,
`spec/conventions/`) and `rusty-bidding-bot` v0.15.3 (`conventions/`).

**The disagreements between the format and the content are the point.** They
are numbered D1 to D14 and gathered in [the last section](#what-the-examples-showed),
each with a proposal.

## 1. Texas transfers

### Today

Texas has a card switch but no ID of its own. Its switch and all six of its
treatments name Jacoby transfers.

```toml
# convention-card spec/fields.toml, section [notrump]
"texas.play"      = { kind = "bool", label = "Texas transfers", skill = "bidding_conventions/jacoby_transfers", level = 4 }
"texas.bid_4c"    = { kind = "bool", label = "4♣ is a transfer", level = 6, ... }
"texas.bid_4d"    = { kind = "bool", label = "4♦ is a transfer", level = 4, ... }
"texas.bid_4h"    = { kind = "bool", label = "4♥ is a transfer", level = 4, ... }
"texas.bid_4s"    = { kind = "bool", label = "4♠ is a transfer", level = 6, ... }
"texas.two_under" = { kind = "bool", label = "2-under Texas", level = 7, ... }
"texas.over_2nt"  = { kind = "bool", label = "Texas transfers over 2NT (4♦/4♥)", level = 4, ... }
```

```
# rusty-bidding-bot conventions/notrump/texas-transfers.bid
module texas-transfers "Texas Transfers"
  kind   convention
  card   notrump.texas.play
  needs  notrump-base
  skill  bidding_conventions/jacoby_transfers
  param  tu  = notrump.texas.two_under default false
  param  o23 = notrump.jacoby_transfers.over_2c_3nt default true
```

The Jacoby transfers definition holds Texas's names ("Texas", "Texas
transfers", "4-level transfers"), one sentence of its summary and its Bridge
Bum reference.

### Here

`conventions/bidding_conventions/texas/convention.toml`:

```toml
id = "bidding_conventions/texas"
name = "Texas transfers"
contexts = ["notrump_openings"]
level = 4
taught_under = ["bidding_conventions/jacoby_transfers"]
summary = """
Over partner's 1NT, 4♦ shows six or more hearts and 4♥ six or more spades;
opener bids the suit, so the strong hand declares. Responder has game values
with no slam interest, or enough for slam and asks for keycards next.
"""

[treatments.over_2nt]
kind = "bool"
label = "Texas transfers over 2NT (4♦/4♥)"
level = 4

[treatments.two_under]
kind = "bool"
label = "2-under Texas"
desc = """
Texas one step lower: 4♣ transfers to ♥ and 4♦ to ♠. Opener's bid of the suit
in between is a super-accept; four of the major is a plain completion.
"""
level = 7

[treatments.bid_4c]
kind = "bool"
label = "4♣ is a transfer"
level = 6

# bid_4d, bid_4h and bid_4s follow the same pattern.

[[deals]]
name = "Texas transfer"
url = "https://github.com/bridge-craftwork/Practice-Bidding-Scenarios/blob/main/dlr/Texas_Transfer.dlr"

[[references]]
role = "about"
kind = "published"
title = "Texas Transfer"
site = "Bridge Bum"
url = "https://www.bridgebum.com/texas_transfer.php"

[[references]]
role = "basis"
kind = "personal"
by = "Rick Wilson"
title = "Rulings on Texas: strength bands, where it applies, 2-under Texas"
used = 2026-10-29
```

`conventions/bidding_conventions/texas/texas-transfers.bid` (beside the
definition, because it carries the `convention` header):

```
module texas-transfers "Texas Transfers"
  kind        convention
  convention  bidding_conventions/texas
  needs       notrump-base
  skill       bidding_conventions/jacoby_transfers
  param  tu  = two_under default false
  param  o23 = bidding_conventions/jacoby_transfers:over_2c_3nt default true
```

On a card:

```json
"conventions": {
  "bidding_conventions/jacoby_transfers": { "over_2nt": true },
  "bidding_conventions/texas": { "over_2nt": true, "two_under": false }
}
```

### What it showed

- **The format fits.** The switch becomes an entry, the six treatments keep
  their names, and the rule file's two reads are an own treatment and another
  convention's treatment, one of each shape.
- **D1. Texas's names are on Jacoby.** Moving "Texas" to the new definition
  changes what the text recogniser ticks, which is a behaviour change.
- **D2. Four treatments are a printed card's boxes.** `bid_4c` to `bid_4s`
  exist because one card prints "Transfers: 4♣ 4♦ 4♥". They say which bids are
  transfers, and overlap `two_under`.
- **D3. Texas's own scenario is tagged Jacoby.** Three
  Practice-Bidding-Scenarios scripts (`Texas_Transfer`, `Texas_or_Jacoby`,
  `We_Overcall_NT_then_Texas`) carry `bidding_conventions/jacoby_transfers`.
- **D4. The existing references have no date and no role.** Today's `see`
  lists carry neither.

## 2. Bergen raises and Reverse Bergen

### Today

Two IDs, one card group. `reverse` is stored as a treatment but behaves as an
alternative: the two boxes are a choice group, at most one on, and the rules
fire on either.

```toml
# convention-card spec/fields.toml, section [major_openings]
"bergen_raises.play"    = { kind = "bool", label = "Bergen raises", skill = "bidding_conventions/bergen_raises", level = 5, choice = "major_openings.bergen" }
"bergen_raises.reverse" = { kind = "bool", label = "Reverse Bergen raises", skill = "bidding_conventions/reverse_bergen_raises", level = 6, choice = "major_openings.bergen" }
"bergen_raises_notes"   = { kind = "text", label = "Bergen raises notes", note = true }
```

```
# rusty-bidding-bot conventions/majors/bergen.bid
module bergen "Bergen raises: four-card raises at the three level"
  kind   convention
  needs  responses
  skill  bidding_conventions/bergen_raises
  skill  bidding_conventions/reverse_bergen_raises
  param  bergen  = major_openings.bergen_raises.play default false
  param  reverse = major_openings.bergen_raises.reverse default false
  param  drury   = major_openings.drury.play default false
  param  drury_r = major_openings.drury.reverse default false

after 1M (P) when bergen | reverse
```

### Here, in Phase 3 (no behaviour change)

`conventions/bidding_conventions/bergen_raises/convention.toml`:

```toml
id = "bidding_conventions/bergen_raises"
name = "Bergen raises"
contexts = ["major_openings"]
level = 5
names = ["Bergen", "Bergen raises", "Bergen raise"]
summary = """
Over partner's 1♥ or 1♠, responder's jumps to 3♣ and 3♦ show four-card
raises of different strength (usually 3♣ constructive, 3♦ limit) and 3M is
preemptive, so opener knows the fit and strength at once.
"""

[treatments.reverse]
kind = "bool"
label = "Reverse Bergen raises"
level = 6

[[references]]
role = "about"
kind = "published"
title = "Bergen Raises"
site = "Bridge Bum"
url = "https://www.bridgebum.com/bergen_raises.php"

[[references]]
role = "about"
kind = "published"
medium = "book"
title = "25 Bridge Conventions You Should Know"
chapter = 13
```

`conventions/bidding_conventions/reverse_bergen_raises/convention.toml`, a
variant: it keeps its ID and points at its parent.

```toml
id = "bidding_conventions/reverse_bergen_raises"
name = "Reverse Bergen raises"
level = 6
names = ["Reverse Bergen"]
summary = """
Bergen raises with the meanings of 3♣ and 3♦ swapped.
"""

[variant]
of = "bidding_conventions/bergen_raises"
sets = { reverse = true }
```

`rules/majors/bergen.bid` (under `rules/`, with no `convention` header,
because it fires on `reverse` alone):

```
module bergen "Bergen raises: four-card raises at the three level"
  kind   convention
  needs  responses
  skill  bidding_conventions/bergen_raises
  skill  bidding_conventions/reverse_bergen_raises
  param  bergen  = bidding_conventions/bergen_raises default false
  param  reverse = bidding_conventions/bergen_raises:reverse default false
  param  drury   = bidding_conventions/drury default false
  param  drury_r = bidding_conventions/drury:reverse default false

after 1M (P) when bergen | reverse
```

On a card that plays Reverse Bergen today (`reverse` on, `play` off or
unset), migrated without change:

```json
"conventions": {
  "bidding_conventions/bergen_raises": { "play": false, "reverse": true }
}
```

### Here, after the Phase 5 correction

The treatment becomes a style, the rule file takes the header and moves
beside the definition, and a migration rewrites cards.

```toml
[treatments.style]
kind = "enum"
options = ["standard", "reverse"]
default = "standard"
```

```
module bergen "Bergen raises: four-card raises at the three level"
  kind        convention
  convention  bidding_conventions/bergen_raises
  param  style = style default standard
```

```json
"bidding_conventions/bergen_raises": { "style": "reverse" }
```

### What it showed

- **The variant pointer works.** A lesson tagged Reverse Bergen finds cards
  playing Bergen with `reverse` on, through `[variant]`.
- **D5. A treatment that switches its convention on.** The format says a
  treatment means nothing while its convention is off. Today's rules say
  otherwise, and not only for Bergen: Drury (`when drury | reverse`) and
  fourth suit forcing (`fsf_play | fsf_round | fsf_gf`) do the same.
- **D6. An entry with treatments and no switch.** "`play` defaults to true"
  is right for a card written by hand, but a migrated card can hold a
  convention's treatments with its switch never set. On 22 public cards (18
  from Practice-Bidding-Scenarios, 4 of Rusty's), 77 groups are like this; in
  24 of them a treatment is on or filled in (fourth suit forcing on 18 cards,
  Blackwood on 4, 2/1 and Lebensohl on one each). Reading those as "played"
  changes behaviour.
- **D7. The level is stated twice.** Reverse Bergen's level 6 is on the
  variant's definition and on the parent's treatment.
- **D8. Bergen's notes are a setting.** `major_openings.bergen_raises_notes`
  sits outside the group.

## 3. DONT

### Today

DONT has its own switch, and it is also one option of the setting that names
the defence to a strong 1NT. The rules accept either.

```toml
# convention-card spec/fields.toml, section [competitive]
"vs_1nt_strong.system" = { kind = "enum", label = "Defense vs strong 1NT", options = ["cappelletti", "modified_cappelletti", "landy", "multi_landy", "dont", "meckwell", "suction", "natural", "other"], ... }
"vs_1nt_weak.system"   = { kind = "enum", label = "Defense vs weak 1NT", options = [ the same nine ], ... }
"vs_1nt_strong.dbl"    = { kind = "text", label = "Vs strong 1NT: double", explains = "competitive.vs_1nt_strong.system" }
"dont.play"            = { kind = "bool", label = "DONT", desc = "... plays DONT when vs_1nt_strong.system is unset or other", skill = "competitive_bidding/dont", level = 5 }
```

```
# rusty-bidding-bot conventions/competitive/dont.bid
module dont "DONT over their 1NT"
  kind   convention
  needs  vs-1nt
  skill  competitive_bidding/dont
  skill  competitive_bidding/defense_vs_1nt
  param  def       = competitive.vs_1nt_strong.system default other
  param  dont_play = competitive.dont.play default false

after (1N) | (1N) P (P) when def is dont | (dont_play, def is other)
```

### Here

`conventions/competitive_bidding/dont/convention.toml`:

```toml
id = "competitive_bidding/dont"
name = "DONT"
contexts = ["vs_notrump"]
level = 5
names = ["DONT", "D.O.N.T.", "Disturb Opponents' No Trump", "Disturbing Opponents NT"]
taught_under = ["competitive_bidding/defense_vs_1nt"]
summary = """
Over their strong 1NT: double shows one long suit (partner relays 2♣); 2♣
and 2♦ show that suit and a higher one; 2♥ both majors; 2♠ six or more
spades.
"""

[[deals]]
name = "DONT"
url = "https://github.com/bridge-craftwork/Practice-Bidding-Scenarios/blob/main/dlr/DONT.dlr"

[[references]]
role = "basis"
kind = "published"
title = "DONT"
site = "Bridge Bum"
url = "https://www.bridgebum.com/dont.php"

[[references]]
role = "about"
kind = "published"
title = "NT Bidding: DONT and Meckwell"
by = "Robert S. Todd"
site = "Advancing in Bridge"
url = "https://www.advinbridge.com/this-week-in-bridge/541"
```

`settings/competitive.toml` keeps the setting, and says which options play a
convention:

```toml
"vs_1nt_strong.system" = { kind = "enum", label = "Defense vs strong 1NT",
  options = ["cappelletti", "modified_cappelletti", "landy", "multi_landy", "dont", "meckwell", "suction", "natural", "other"],
  plays = { dont = "competitive_bidding/dont", cappelletti = "competitive_bidding/cappelletti", meckwell = "competitive_bidding/meckwell" } }
```

`rules/competitive/dont.bid` (under `rules/`, with no `convention` header,
because it is on two ways):

```
module dont "DONT over their 1NT"
  kind   convention
  needs  vs-1nt
  skill  competitive_bidding/dont
  skill  competitive_bidding/defense_vs_1nt
  param  def       = competitive.vs_1nt_strong.system default other
  param  dont_play = competitive_bidding/dont default false

after (1N) | (1N) P (P) when def is dont | (dont_play, def is other)
```

### What it showed

- **D9. "Does this card play DONT" has two answers.** The card's
  `conventions` may not list DONT while the setting chooses it. Four
  defences to 1NT are chosen only through that setting (Cappelletti,
  Meckwell, Suction, Multi-Landy), DONT has it as a second way on, and four
  other settings already carry a `plays` attribute (three two-level openings whose
  "weak" option plays Weak Twos, and the 2/1 rebid style that plays the
  Schuler Shift).
- **D10. The same defence against a weak notrump.** The setting for the weak
  1NT offers DONT, but the rules read only the strong one.
- **D11. Text that spells out a chosen convention.** Seven write-in settings
  per notrump strength (`vs_1nt_strong.dbl`, `.2c` and so on) explain
  whichever defence the setting names.
- **D12. One source is not a publication.** The rules' notes cite another
  tool's source file for the editor's wording of DONT.
- **D13. Only one bidder can make DONT's examples.** The scenario is marked
  as one BBA cannot bid.
- **D14. A choice between conventions.** Not DONT's, but found while
  checking it: Blackwood or Roman Keycard, and Leaping or Non-leaping
  Michaels, are choice groups across two conventions. A definition names no
  card, so the choice has to live in the definitions.

## What the examples showed

The format holds for all three. Fourteen points need a ruling or a note in
the contract. "Contract" in the last column means CONTRACT.md already says
this, as a proposal for Rick to accept or change.

| | Disagreement | Proposal | Where |
|---|---|---|---|
| D1 | Texas's names, summary sentence and reference sit on Jacoby | In Phase 3 the new definition carries no `names`, so the recogniser is unchanged; Phase 5 moves them, as the plan lists | Plan, Phase 5 |
| D2 | Treatments that are a printed card's boxes (`bid_4c` to `bid_4s`) | Carried as treatments unchanged; review with the lone boxes | Plan, Phase 6 |
| D3 | A convention's own scenario is tagged with the ID it is taught under | The check accepts a scenario tagged with the convention or with any ID in its `taught_under`; retagging is the scenario author's choice | Contract |
| D4 | Migrated references have no date and no role | `used` is left out when unknown, never invented; `role` defaults to `about` and is raised to `basis` by hand | Contract |
| D5 | A treatment that switches its convention on (Bergen, Drury, fourth suit forcing) | Phase 3 keeps the rules as they are, with every read spelled out; Phase 5 enforces "nothing while off" with a migration | Plan, Phase 5 |
| D6 | A migrated entry with treatments and no switch (77 groups on 22 public cards) | `"play": null` means "the card has not said": a reader uses its own default, as it does today. Only the migration writes it; a card written by hand never needs it | Contract |
| D7 | A variant's level is stated twice | The treatment's level is the one tools read; a variant's definition may omit `level` | Contract |
| D8 | Write-in notes for a convention that sit outside its group | Stay settings in Phase 3; Phase 5 moves them to the entry's `text`, as the plan lists for Bergen | Plan, Phase 5 |
| D9 | A convention chosen as an option of a setting | A setting keeps `plays = { option = ID }`. A card plays a convention when its entry says so or a setting's chosen option plays it. Rule files keep spelling out both reads | Contract |
| D10 | A defence offered against a weak notrump that the rules never read | Record in the inventory; a behaviour question for Phase 5 or later | Phase 1 inventory |
| D11 | Write-ins that spell out a chosen convention | Stay settings, with `explains` naming the setting | Contract |
| D12 | A source that is not a publication | `kind = "personal"` covers a ruling; code in another tool is cited as a tool, by name and date, with no path | Contract |
| D13 | Generated examples that only one bidder can make | Already covered: each example names its bidder | Contract |
| D14 | A choice between two conventions | `alternatives = [ID, ...]` on each definition; a card that plays two is reported as a conflict | Contract |

Two of these change how a decision of 2026-11-13 reads, and need Rick's
answer before the contract is accepted:

- **D6** refines "`play` defaults to true" (issue #3) with a third value.
- **D9** means the bare-ID address in a rule file (issue #4) reads the
  card's entry only, not a setting that chooses the convention.
