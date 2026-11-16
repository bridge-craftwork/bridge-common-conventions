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
- every rule module is on in some card, and on together with each setting
  it reads, both ways (424 such combinations today, 402 of them in two
  cards or more);
- five numbers are at their default, below it and above it, and a setting
  written as text takes each value a rule tests it for.

It does not try other combinations: there is no end of them. What cannot
be on together comes from the pack: the settings of one choice group, and
the conventions that fill one function. A setting those exclusions leave
without a card gets a card opened for it, which is the only way the set
grows. Today that is one card of the eleven.

## The fast three

`fast.txt` names the three cards that between them fire the most rules:

    python3 scripts/capture.py --cards test-cards/designed --only @test-cards/fast.txt ...

## Measured (2026-11-16)

Over the 5,565 deals of the capture, by which rules made a call:

| Cards | Rules that fired, of 4,514 | Time |
|---|---|---|
| The 47 captured cards (22 public, 25 hand-made) | 2,677 | about 10 min |
| The 11 designed cards | 3,028 | about 2 min |
| The fast three (06, 07, 05) | 2,458 | 34 s; 10 s on the sample of deals |
| The best three of the 47 captured cards | 2,085 | |

Still open:

- **Some rules still fire with a captured card and with no designed one**
  (#118). Which cards the settings in no group land on is decided by
  each setting's name and a starting value; ten starting values gave
  totals 3% apart on a sample of deals, and the best is kept. So part of
  what is missed is the luck of the layout, and the rest is combinations
  across rule modules, which the set does not try. Reverse Flannery and
  Lebensohl, which were silenced by a convention sharing their card, bid
  now that the pack records those exclusions (#117).
- Ranges other than the five with a default are not varied.
- The fast three are chosen by measurement and written by hand; a rule
  change can change which three are best.

Rules that still never fire need deals, not cards.
