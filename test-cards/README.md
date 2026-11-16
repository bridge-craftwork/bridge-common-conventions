# Test cards

Cards made to exercise the rules. Nobody plays them: each is a mixture
chosen so that, between them, every card setting the rule files read is
tried. They are generated, never edited:

    node scripts/design-cards.mjs ../convention-card test-cards/designed

- `designed/designed-NN.json`: the cards, in card schema 3.
- `designed.json`: what each card turns on, what the set covers, and the
  groups of settings that cannot share a card.

## What the set promises

Of the settings the rule files read (a `param` or `card` line, or the
convention a module's `convention` line names):

- every yes/no setting is on in at least one card and off in another;
- every option of every choice is chosen in at least one card;
- five numbers are at their default, below it and above it.

It does not try combinations. What cannot be on together comes from the
pack: the settings of one choice group, and the conventions that fill one
function. A setting those exclusions leave without a card gets a card
opened for it, which is the only way the set grows.

## A draft (2026-11-16)

Measured over the 5,565 deals of the capture, by which rules made a call:

| Cards | Rules that fired, of 4,514 |
|---|---|
| The 47 captured cards (22 public, 25 hand-made) | 2,677 |
| The 11 designed cards | 2,901 |
| Three designed cards (08, 09, 07), for a fast check | 2,401 |
| The best three of the 47 captured cards | 2,085 |

Not yet right:

- **345 rules fire with a captured card and with no designed one.** Some
  are conventions that are on but silenced by another on the same card,
  which the pack does not record as an exclusion: Lebensohl with
  Rubensohl (its rules say "not Rubensohl"), Reverse Flannery with an
  invitational jump shift. The next step is to require, for each rule
  module, a card where the module is on with each of its own settings on
  and another with it off, and to report every module that is on yet
  silent.
- Ranges other than the five with a default are not varied, nor is the
  system name (2/1, Precision, the Brill card), which the rules also read.
- One card (designed-08) fails the card checker on an other-agreements
  entry.
- The three for a fast check are picked by measurement, not recorded.

Rules that still never fire need deals, not cards.
