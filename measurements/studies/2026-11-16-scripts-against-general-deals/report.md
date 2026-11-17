# Do dealer scripts reach a convention's rules better than the general deals?

Measured 2026-11-16. Engine: rusty-bidding-bot main (c1f19ac), rules from the pack checkout (51cc7c4).
Scripts: Practice-Bidding-Scenarios origin/main, `dlr/<Name>.dlr` only: no levelled script, no levelling.
Each script: `rbb deal run --seed 1 -p 200 -g 20000000`. General set: the capture's 5,565 deals, bid with the same card.
A scenario's own rules: the rule files whose module names one of its tagged IDs in a `convention` or `skill` line.

## Totals

- Scenarios measured: 212 (163 whose tags name a rule file; 49 whose tags name no rule file). Skipped: 5. Failed: 1.
- Cards used: 21GF-DEFAULT, 21GF-Flannery, 21GF-GIB, 21GF-GIB-Bergen, 21GF-Gazzilli, 21GF-MSS, 21GF-MSTandMSS, 21GF-Multi, 21GF-NoInvertedMinor, 21GF-Ogust, 21GF-PolishTwoSuiters, 21GF-Puppet, 21GF-SPECIALS, 21GF-SPECIALS2, 21GF-WJS-MSS, Basic-Bridge, Precision, Precision-14-16.
- Rules fired at all (of 4,514 in the pack): scripted deals 2361; the general set on the same 18 cards 2226; either 2585; only scripts 359; only the general set 224.
- Own-convention rules fired: scripted 1213; general 1582; only scripts 169; only general 538.
- Median hit rate (boards where the convention's own rules made a call), scenarios with rule files: script 77.5%, general 3.4%.
- Scenarios where the script reaches own rules the general set does not: 58; where the general set reaches own rules the script does not: 118.
- Boards dealt from scripts: 41,365 against 100,170 general boards bid.

## Every scenario

| Scenario | Tagged | Card | Natural rate | Boards | Hit: script | Hit: general | Own rules: script | general | only script | only general |
|---|---|---|---|---|---|---|---|---|---|---|
| Ogust | ogust | 21GF-Ogust | 1 in 24,936 | 200 | 98.5% | 2.5% | 30 | 18 | 15 | 3 |
| Weak_Jump_Shift | weak_jump_shifts | 21GF-WJS-MSS | 1 in 2,045 | 200 | 79.5% | 0.1% | 18 | 3 | 15 | 0 |
| Opps_Michaels_and_Unusual | unusual_vs_unusual | 21GF-DEFAULT | 1 in 10,171 | 200 | 95.0% | 6.0% | 82 | 135 | 13 | 66 |
| Opps_2-Suited_Overcalls | unusual_vs_unusual | 21GF-DEFAULT | 1 in 6,927 | 200 | 74.5% | 6.0% | 87 | 135 | 13 | 61 |
| Opps_Preempt | defense_vs_preempts | 21GF-DEFAULT | 1 in 53 | 200 | 58.5% | 7.2% | 42 | 73 | 13 | 44 |
| Benjamin_2D | benjamin_2d | 21GF-PolishTwoSuiters | 1 in 264 | 200 | 94.0% | 3.1% | 30 | 19 | 11 | 0 |
| Basic_Weak_2 | weak_2s | Basic-Bridge | 1 in 378 | 200 | 79.0% | 7.9% | 33 | 39 | 10 | 16 |
| After_Partner_Takeout_Double | takeout_doubles | 21GF-DEFAULT | 1 in 12,265 | 200 | 89.5% | 13.9% | 34 | 141 | 9 | 116 |
| Inverted_Minors | inverted_minors | 21GF-DEFAULT | 1 in 3,810 | 200 | 88.5% | 2.1% | 34 | 30 | 9 | 5 |
| Preempts | preemptive_bids | 21GF-DEFAULT | 1 in 58 | 200 | 62.0% | 7.6% | 21 | 20 | 8 | 7 |
| Reverse_Flannery | reverse_flannery | 21GF-SPECIALS | 1 in 17,577 | 200 | 98.5% | 0.4% | 20 | 15 | 7 | 2 |
| Opps_Preempt_4M | defense_vs_preempts | 21GF-DEFAULT | 1 in 3,708 | 200 | 97.0% | 7.2% | 18 | 73 | 7 | 62 |
| Weak_2_Bids | weak_2s | 21GF-DEFAULT | 1 in 72 | 200 | 93.5% | 7.6% | 29 | 37 | 7 | 15 |
| Opps_Michaels_Cuebid | unusual_vs_unusual | 21GF-DEFAULT | 1 in 6,622 | 200 | 100.0% | 6.0% | 58 | 135 | 6 | 83 |
| Opps_Weak_Two | defense_vs_preempts | 21GF-DEFAULT | 1 in 55 | 200 | 93.5% | 7.2% | 44 | 73 | 6 | 35 |
| Weak_2_Bids_Lax | weak_2s | 21GF-DEFAULT | 1 in 60 | 200 | 90.0% | 7.6% | 28 | 37 | 6 | 15 |
| Takeout_Double | takeout_doubles | 21GF-DEFAULT | 1 in 108 | 200 | 58.0% | 13.9% | 44 | 141 | 6 | 103 |
| Game_Forcing_2C | strong_2c | 21GF-DEFAULT | 1 in 190 | 200 | 96.0% | 4.2% | 38 | 34 | 5 | 1 |
| Basic_Takeout_Double | takeout_doubles | Basic-Bridge | 1 in 173 | 200 | 85.0% | 14.5% | 43 | 135 | 5 | 97 |
| Ned_Weak_Two | weak_2s | 21GF-DEFAULT | 1 in 82 | 200 | 37.0% | 7.6% | 24 | 37 | 5 | 18 |
| Lebensohl | lebensohl | 21GF-SPECIALS | 1 in 9,131 | 200 | 9.5% | 7.4% | 18 | 87 | 5 | 74 |
| Gambling_3N | gambling_3nt | 21GF-SPECIALS | 1 in 2,132 | 200 | 100.0% | 0.8% | 11 | 7 | 4 | 0 |
| Gazzilli | gazzilli | 21GF-Gazzilli | 1 in 556 | 200 | 43.0% | 2.0% | 37 | 42 | 4 | 9 |
| Impossible_2S | impossible_2s | 21GF-DEFAULT | 1 in 175,439 | 114 | 35.1% | 0.3% | 12 | 9 | 4 | 1 |
| Flannery | flannery | 21GF-Flannery | 1 in 145 | 200 | 100.0% | 1.7% | 28 | 27 | 3 | 2 |
| Power_Double_Unbalanced | takeout_doubles | 21GF-DEFAULT | 1 in 640 | 200 | 97.5% | 13.9% | 49 | 141 | 3 | 95 |
| Support_Double | support_doubles | 21GF-DEFAULT | 1 in 1,071 | 200 | 97.0% | 0.8% | 12 | 10 | 3 | 1 |
| Fourth_Suit_Forcing | fourth_suit_forcing | 21GF-SPECIALS | 1 in 2,449 | 200 | 88.0% | 27.1% | 17 | 166 | 3 | 152 |
| We_X_Opps_Preempt | takeout_doubles, defense_vs_preempts | 21GF-DEFAULT | 1 in 42,874 | 200 | 86.5% | 13.9% | 36 | 141 | 3 | 108 |
| Multi_2D | multi_2d | 21GF-Multi | 1 in 99 | 200 | 70.0% | 3.8% | 48 | 50 | 3 | 5 |
| Gavin_Strong_Splinter | splinters | 21GF-DEFAULT | 1 in 12,551 | 200 | 58.5% | 0.9% | 10 | 15 | 3 | 8 |
| Splinters | splinters | 21GF-DEFAULT | 1 in 2,625 | 200 | 47.5% | 0.9% | 10 | 15 | 3 | 8 |
| Splinters_By_Opener | splinters | 21GF-DEFAULT | 1 in 5,661 | 200 | 19.5% | 0.9% | 9 | 15 | 3 | 9 |
| Reversed_Splinters_By_Opener | splinters | 21GF-DEFAULT | 1 in 4,960 | 200 | 19.0% | 0.9% | 9 | 15 | 3 | 9 |
| Lebensohl2 | lebensohl | 21GF-DEFAULT | 1 in 44,266 | 200 | 16.5% | 7.4% | 16 | 87 | 3 | 74 |
| We_X_Opps_Weak_2 | takeout_doubles, defense_vs_preempts | 21GF-DEFAULT | 1 in 24,569 | 200 | 100.0% | 13.9% | 41 | 141 | 2 | 102 |
| GIB_1N-P-2C | stayman | 21GF-GIB | 1 in 300 | 200 | 78.0% | 6.7% | 15 | 31 | 2 | 18 |
| Exclusion_After_Sta_Jac | exclusion_blackwood | 21GF-SPECIALS2 | 1 in 24,031 | 200 | 17.5% | 0.5% | 17 | 17 | 2 | 2 |
| Better_Minor_Lebensohl | lebensohl | 21GF-DEFAULT | 1 in 18,733 | 200 | 100.0% | 7.4% | 34 | 87 | 1 | 54 |
| Lebensohl_vs_Opps_W2_Bal | lebensohl | 21GF-DEFAULT | 1 in 40,380 | 200 | 100.0% | 7.4% | 38 | 87 | 1 | 50 |
| Lebensohl_vs_Opps_W2_Bal_or_Dir | lebensohl | 21GF-DEFAULT | 1 in 17,923 | 200 | 100.0% | 7.4% | 40 | 87 | 1 | 48 |
| Lebensohl_vs_Opps_W2_Dir | lebensohl | 21GF-DEFAULT | 1 in 16,512 | 200 | 100.0% | 7.4% | 42 | 87 | 1 | 46 |
| After_Partner_Overcalls | advancing_overcalls | 21GF-DEFAULT | 1 in 3,830 | 200 | 99.0% | 91.5% | 29 | 63 | 1 | 35 |
| Mixed_Raise_In_Comp | mixed_raise | 21GF-SPECIALS | 1 in 17,059 | 200 | 97.5% | 91.6% | 17 | 65 | 1 | 49 |
| Gavin_Mixed_Raise | mixed_raise | 21GF-DEFAULT | 1 in 268 | 200 | 94.0% | 91.5% | 16 | 63 | 1 | 48 |
| Texas_or_Jacoby | jacoby_transfers | 21GF-DEFAULT | 1 in 211 | 200 | 94.0% | 7.8% | 25 | 55 | 1 | 31 |
| Leaping_Michaels | leaping_michaels | 21GF-DEFAULT | 1 in 22,632 | 200 | 93.5% | 6.0% | 16 | 135 | 1 | 120 |
| Texas_Transfer | jacoby_transfers | 21GF-DEFAULT | 1 in 2,059 | 200 | 92.5% | 7.8% | 13 | 55 | 1 | 43 |
| Opps_Overcall_Stayman_or_Jacoby | stayman, jacoby_transfers | 21GF-DEFAULT | 1 in 3,670 | 200 | 90.0% | 13.0% | 33 | 72 | 1 | 40 |
| Opps_Open_1N_15-17 | defense_vs_1nt | 21GF-DEFAULT | 1 in 22 | 200 | 89.0% | 18.6% | 26 | 42 | 1 | 17 |
| GIB_1N-P-2C-BID | stayman | 21GF-GIB | 1 in 9,889 | 200 | 86.0% | 6.7% | 14 | 31 | 1 | 18 |
| 2N_and_Transfers | jacoby_transfers | 21GF-DEFAULT | 1 in 617 | 200 | 80.0% | 7.8% | 19 | 55 | 1 | 37 |
| Jordan_2N | jordan_2nt | 21GF-DEFAULT | 1 in 7,493 | 200 | 60.0% | 1.2% | 3 | 3 | 1 | 1 |
| WB5_Roudi | roudi | 21GF-SPECIALS2 | 1 in 1,483 | 200 | 39.0% | 1.3% | 17 | 17 | 1 | 1 |
| Negative_Double | negative_doubles | 21GF-DEFAULT | 1 in 67 | 200 | 34.5% | 29.0% | 36 | 76 | 1 | 41 |
| 2N_and_MSS | minor_suit_stayman | 21GF-MSS | 1 in 22,775 | 200 | 25.0% | 1.7% | 6 | 25 | 1 | 20 |
| Non_Leaping_Michaels_After_3-Bid | non_leaping_michaels | 21GF-DEFAULT | 1 in 68,111 | 200 | 22.5% | 6.0% | 9 | 135 | 1 | 127 |
| Exclusion_After_1M | exclusion_blackwood | 21GF-SPECIALS2 | 1 in 20,858 | 200 | 14.5% | 0.5% | 15 | 17 | 1 | 3 |
| Basic_NT | notrump_openings | Basic-Bridge | 1 in 516 | 200 | 100.0% | 23.4% | 9 | 25 | 0 | 16 |
| Major_Opener | major_suit_openings | 21GF-DEFAULT | 1 in 9 | 200 | 100.0% | 84.7% | 4 | 14 | 0 | 10 |
| Minor_Suit_Opener | minor_suit_openings | 21GF-DEFAULT | 1 in 6 | 200 | 100.0% | 84.7% | 6 | 14 | 0 | 8 |
| Minor_Suit_Transfer | minor_suit_transfers | 21GF-MSTandMSS | 1 in 210,526 | 95 | 100.0% | 1.3% | 6 | 6 | 0 | 0 |
| Power_Double_Balanced | takeout_doubles | 21GF-DEFAULT | 1 in 5,852 | 200 | 100.0% | 13.9% | 32 | 141 | 0 | 109 |
| Smolen | smolen | 21GF-GIB | 1 in 4,636 | 200 | 100.0% | 1.5% | 7 | 7 | 0 | 0 |
| Smolen_after_2N | smolen | 21GF-DEFAULT | 1 in 20,250 | 200 | 100.0% | 1.5% | 7 | 7 | 0 | 0 |
| Weak_NT_13-15 | notrump_openings | Precision | 1 in 1,002 | 200 | 100.0% | 21.7% | 8 | 14 | 0 | 6 |
| 1C_WalshStyle | walsh | 21GF-SPECIALS2 | 1 in 744 | 200 | 99.5% | 32.7% | 3 | 28 | 0 | 25 |
| Balancing | balancing | 21GF-DEFAULT | 1 in 1,700 | 200 | 99.5% | 2.1% | 10 | 10 | 0 | 0 |
| Reverse_After_Two_Over_One | reverse_bids, two_over_one | 21GF-DEFAULT | 1 in 20,966 | 200 | 99.5% | 54.7% | 8 | 178 | 0 | 170 |
| Basic_Major | major_suit_openings | Basic-Bridge | 1 in 30 | 200 | 99.0% | 85.9% | 7 | 14 | 0 | 7 |
| Basic_Minor | minor_suit_openings | Basic-Bridge | 1 in 21 | 200 | 99.0% | 85.9% | 6 | 14 | 0 | 8 |
| Gerber | gerber | 21GF-DEFAULT | 1 in 18,453 | 200 | 99.0% | 1.2% | 14 | 18 | 0 | 4 |
| Jacoby_Super-Accept | jacoby_transfers, super_accept | 21GF-DEFAULT | 1 in 2,731 | 200 | 98.5% | 7.8% | 16 | 60 | 0 | 44 |
| Jump_Overcalls | overcalls | 21GF-DEFAULT | 1 in 328 | 200 | 98.5% | 58.7% | 16 | 47 | 0 | 31 |
| We_Overcall_1N | overcalls | 21GF-DEFAULT | 1 in 285 | 200 | 98.0% | 58.7% | 5 | 47 | 0 | 42 |
| Forcing_NT | forcing_1nt | 21GF-DEFAULT | 1 in 5,846 | 200 | 97.5% | 35.6% | 15 | 33 | 0 | 18 |
| Reverse_By_Opener | reverse_bids | 21GF-DEFAULT | 1 in 3,841 | 200 | 97.5% | 54.7% | 27 | 178 | 0 | 151 |
| Drury | drury | 21GF-DEFAULT | 1 in 3,696 | 200 | 97.0% | 0.2% | 6 | 6 | 0 | 0 |
| Jacoby_Transfer | jacoby_transfers | 21GF-DEFAULT | 1 in 417 | 200 | 96.0% | 7.8% | 19 | 55 | 0 | 36 |
| Puppet_Stayman_1N | puppet_stayman | 21GF-Puppet | 1 in 167 | 200 | 96.0% | 6.3% | 2 | 2 | 0 | 0 |
| Basic_Overcall | overcalls | Basic-Bridge | 1 in 11 | 200 | 93.5% | 65.3% | 20 | 54 | 0 | 34 |
| Soloway_Jump_Shift | soloway | 21GF-SPECIALS2 | 1 in 10,388 | 200 | 92.0% | 1.6% | 8 | 8 | 0 | 0 |
| Soloway_Jump_Shift_Type-2 | soloway | 21GF-SPECIALS2 | 1 in 16,091 | 200 | 91.5% | 1.6% | 8 | 8 | 0 | 0 |
| Fit_Jumps_after_1M_Double | fit_showing_jumps | 21GF-GIB | 1 in 79,724 | 200 | 91.0% | 1.0% | 7 | 17 | 0 | 10 |
| MST_or_MSS | minor_suit_stayman, minor_suit_transfers | 21GF-MSTandMSS | 1 in 47,288 | 200 | 90.5% | 2.9% | 16 | 26 | 0 | 10 |
| Opps_Double_Stayman | stayman | 21GF-DEFAULT | 1 in 15,150 | 200 | 89.5% | 7.0% | 9 | 28 | 0 | 19 |
| Slam_after_Transfer | jacoby_transfers | 21GF-DEFAULT | 1 in 3,252 | 200 | 89.5% | 7.8% | 27 | 55 | 0 | 28 |
| Minor_Suit_Opener_Mixed_Raise | mixed_raise | 21GF-NoInvertedMinor | 1 in 23,956 | 200 | 89.0% | 91.6% | 2 | 63 | 0 | 61 |
| We_Overcall_NT_then_Smolen | smolen | 21GF-GIB | 1 in 104,167 | 192 | 88.5% | 1.5% | 5 | 7 | 0 | 2 |
| Soloway_Jump_Shift_Type-1 | soloway | 21GF-SPECIALS2 | 1 in 10,178 | 200 | 87.0% | 1.6% | 7 | 8 | 0 | 1 |
| Opps_Double_Jacoby | jacoby_transfers | 21GF-DEFAULT | 1 in 59,145 | 200 | 85.5% | 7.8% | 20 | 55 | 0 | 35 |
| Weak_NT_14-15 | notrump_openings | Precision-14-16 | 1 in 19 | 200 | 85.5% | 23.7% | 10 | 19 | 0 | 9 |
| Jacoby_2N | jacoby_2nt | 21GF-DEFAULT | 1 in 2,002 | 200 | 84.5% | 2.5% | 9 | 9 | 0 | 0 |
| We_Overcall | overcalls | 21GF-DEFAULT | 1 in 35 | 200 | 83.5% | 58.7% | 17 | 47 | 0 | 30 |
| Jacoby_2N_4x_void | jacoby_2nt | 21GF-DEFAULT | 1 in 712 | 200 | 83.0% | 2.5% | 9 | 9 | 0 | 0 |
| New_Minor_Forcing | new_minor_forcing | 21GF-DEFAULT | 1 in 6,194 | 200 | 83.0% | 2.2% | 13 | 25 | 0 | 12 |
| 1N | notrump_openings | 21GF-DEFAULT | 1 in 17 | 200 | 82.5% | 22.4% | 13 | 20 | 0 | 7 |
| Reverse_By_Responder | reverse_bids | 21GF-DEFAULT | 1 in 5,990 | 200 | 82.0% | 54.7% | 8 | 178 | 0 | 170 |
| Soloway_Jump_Shift_Type-3 | soloway | 21GF-SPECIALS2 | 1 in 10,277 | 200 | 80.0% | 1.6% | 7 | 8 | 0 | 1 |
| Fit_Showing_Jumps | fit_showing_jumps | 21GF-GIB | 1 in 22,832 | 200 | 78.5% | 1.0% | 9 | 17 | 0 | 8 |
| Minor_Suit_Stayman | minor_suit_stayman | 21GF-MSTandMSS | 1 in 1,623 | 200 | 78.5% | 1.6% | 20 | 20 | 0 | 0 |
| We_Overcall_NT_then_Jacoby | jacoby_transfers | 21GF-DEFAULT | 1 in 1,552 | 200 | 77.5% | 7.8% | 19 | 55 | 0 | 36 |
| We_Overcall_NT_then_Texas | jacoby_transfers | 21GF-DEFAULT | 1 in 10,089 | 200 | 77.5% | 7.8% | 14 | 55 | 0 | 41 |
| Cappelletti | cappelletti | 21GF-GIB | 1 in 218 | 200 | 77.0% | 3.4% | 14 | 14 | 0 | 0 |
| Kokish_Relay | kokish | 21GF-SPECIALS | 1 in 1,840 | 200 | 74.5% | 0.6% | 10 | 10 | 0 | 0 |
| Slam_after_Stayman_or_Jacoby_w30plus | stayman, jacoby_transfers | 21GF-DEFAULT | 1 in 2,136 | 200 | 72.0% | 13.0% | 38 | 72 | 0 | 34 |
| Cappelletti_in_4th | cappelletti | 21GF-GIB | 1 in 651 | 200 | 71.0% | 3.4% | 14 | 14 | 0 | 0 |
| Bergen_Raises | bergen_raises | 21GF-GIB-Bergen | 1 in 279 | 200 | 70.5% | 2.4% | 12 | 12 | 0 | 0 |
| Smolen_Invitational | smolen | 21GF-DEFAULT | 1 in 9,858 | 200 | 68.0% | 1.5% | 6 | 7 | 0 | 1 |
| Stayman | stayman | 21GF-DEFAULT | 1 in 530 | 200 | 68.0% | 7.0% | 10 | 28 | 0 | 18 |
| Slam_after_Stayman_or_Jacoby_w31plus | stayman, jacoby_transfers | 21GF-DEFAULT | 1 in 4,131 | 200 | 67.5% | 13.0% | 33 | 72 | 0 | 39 |
| We_Overcall_NT_then_MSS | minor_suit_stayman | 21GF-MSTandMSS | 1 in 25,616 | 200 | 65.0% | 1.6% | 17 | 20 | 0 | 3 |
| Multi_Landy | multi_landy | 21GF-SPECIALS2 | 1 in 152 | 200 | 61.5% | 2.3% | 12 | 12 | 0 | 0 |
| Gavin_Semi-Forcing_NT_with_Fit | semi_forcing_1nt | 21GF-DEFAULT | 1 in 169 | 200 | 59.5% | 35.6% | 5 | 33 | 0 | 28 |
| Non_Leaping_Michaels_After_2-Bid | non_leaping_michaels | 21GF-DEFAULT | 1 in 23,871 | 200 | 58.5% | 6.0% | 10 | 135 | 0 | 125 |
| Gerber_By_Responder | gerber | 21GF-GIB | 1 in 5,976 | 200 | 57.5% | 1.2% | 17 | 18 | 0 | 1 |
| Two-Way_Game_Try | two_way_game_tries | 21GF-GIB | 1 in 43,068 | 200 | 48.5% | 0.7% | 17 | 18 | 0 | 1 |
| We_Overcall_NT_then_MST | minor_suit_transfers | 21GF-MSTandMSS | 1 in 12,170 | 200 | 46.5% | 1.3% | 5 | 6 | 0 | 1 |
| Slam_after_Stayman | stayman | 21GF-DEFAULT | 1 in 4,829 | 200 | 44.5% | 7.0% | 10 | 28 | 0 | 18 |
| Weak_NT_11-16 | notrump_openings | Precision | 1 in 5 | 200 | 43.0% | 21.7% | 8 | 14 | 0 | 6 |
| We_Overcall_NT_then_Stayman | stayman | 21GF-DEFAULT | 1 in 2,816 | 200 | 42.5% | 7.0% | 10 | 28 | 0 | 18 |
| Soloway_Jump_Shift_Type-4 | soloway | 21GF-SPECIALS2 | 1 in 6,145 | 200 | 42.0% | 1.6% | 7 | 8 | 0 | 1 |
| Weak_NT_09-15 | notrump_openings | Precision | 1 in 3 | 200 | 33.0% | 21.7% | 8 | 14 | 0 | 6 |
| Responsive_Double | responsive_doubles | 21GF-GIB | 1 in 150,376 | 133 | 27.1% | 0.3% | 6 | 8 | 0 | 2 |
| Help_Suit_Game_Try | help_suit_game_try | 21GF-GIB | 1 in 11,114 | 200 | 27.0% | 0.7% | 17 | 18 | 0 | 1 |
| Weak_NT_10-13 | notrump_openings | Precision | 1 in 5 | 200 | 25.5% | 21.7% | 8 | 14 | 0 | 6 |
| 3N | notrump_openings | 21GF-GIB | 1 in 8,271 | 200 | 24.0% | 22.6% | 1 | 13 | 0 | 12 |
| Weak_NT_09-12 | notrump_openings | Precision | 1 in 5 | 200 | 16.0% | 21.7% | 6 | 14 | 0 | 8 |
| Weak_NT_10-12 | notrump_openings | Precision | 1 in 7 | 200 | 14.0% | 21.7% | 7 | 14 | 0 | 7 |
| Gavin_Weak_Splinter | splinters | 21GF-DEFAULT | 1 in 21,055 | 200 | 4.0% | 0.9% | 4 | 15 | 0 | 11 |
| Responsive_Double_after_Overcall | responsive_doubles | 21GF-GIB | 1 in 512,821 | 39 | 2.6% | 0.3% | 2 | 8 | 0 | 6 |
| 2N | notrump_openings | 21GF-DEFAULT | 1 in 2,144 | 200 | 2.0% | 22.4% | 1 | 20 | 0 | 19 |
| Gerber_By_Opener | gerber | 21GF-GIB | 1 in 129,032 | 155 | 0.6% | 1.2% | 5 | 18 | 0 | 13 |
| 1M-3N_Picture_Bid | picture_3nt | 21GF-DEFAULT | 1 in 7,722 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| BART | bart | 21GF-DEFAULT | 1 in 23,059 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Bergen_Thrump_X_after_Preempt | thrump_double | 21GF-DEFAULT | 1 in 8,987 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| CRASH | crash | 21GF-DEFAULT | 1 in 1,023 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| DONT | dont | 21GF-GIB | 1 in 1,826 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| DOPI_ROPI | dopi_ropi | 21GF-DEFAULT | 1 in 666,667 | 30 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Equal_Level_Conversion | equal_level_conversion | 21GF-DEFAULT | 1 in 22,132 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Exit_Transfers | exit_transfers | 21GF-DEFAULT | 1 in 12,700 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Forcing_Pass | forcing_pass | 21GF-DEFAULT | 1 in 136,054 | 147 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| GIB_Sandwich_NT_BPH | sandwich_nt | 21GF-GIB | 1 in 9,948 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| GSF_after_Preempt | grand_slam_force | 21GF-DEFAULT | 1 in 23,806 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Good_Bad_2N | good_bad_2nt | 21GF-DEFAULT | 1 in 7,177 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Grand_Slam_Force | grand_slam_force | 21GF-DEFAULT | 1 in 3,286 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Grand_Slam_Force_2 | grand_slam_force | 21GF-DEFAULT | 1 in 2,967 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Lars_Multi_2D | lars_multi | 21GF-Multi | 1 in 68 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Last_Train_GT2 | last_train | 21GF-DEFAULT | 1 in 47,175 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Last_Train_Game_Try | last_train | 21GF-DEFAULT | 1 in 73,789 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Lead_Directing_Double | lead_directing_doubles | 21GF-GIB | 1 in 721 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Losing_Trick_Count | hand_evaluation | 21GF-DEFAULT | 1 in 13 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Mathe | mathe | 21GF-DEFAULT | 1 in 24 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Maximal_After_Overcall | maximal_doubles | 21GF-SPECIALS | 1 in 22,545 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Maximal_Double | maximal_doubles | 21GF-SPECIALS | 1 in 80,112 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| McCabe_After_Weak_2 | mccabe | 21GF-DEFAULT | 1 in 7,154 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| McCabe_after_WJO | mccabe | 21GF-DEFAULT | 1 in 285,714 | 70 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Meckwell | meckwell | 21GF-SPECIALS2 | 1 in 880 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Michaels_Cuebid | michaels | 21GF-DEFAULT | 1 in 9,686 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Michaels_after_1m | michaels | 21GF-DEFAULT | 1 in 4,034 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Michaels_and_Unusual | michaels, unusual_notrump | 21GF-DEFAULT | 1 in 10,305 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Mini-Maxi_Roman_2D | mini_roman_2d | 21GF-DEFAULT | 1 in 138 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Mitchell_Stayman | mitchell_stayman | 21GF-DEFAULT | 1 in 18,704 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Muiderberg_Two_Bids | muiderberg | 21GF-PolishTwoSuiters | 1 in 54 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| NT_Splinter | splinters | 21GF-GIB | 1 in 9,440 | 200 | 0.0% | 0.9% | 0 | 15 | 0 | 15 |
| Namyats | namyats | 21GF-SPECIALS | 1 in 2,018 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Preempt_Keycard | preempt_keycard | 21GF-DEFAULT | 1 in 5,713 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Puppet_Stayman_2N | puppet_stayman | 21GF-MSTandMSS | 1 in 668 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Rosenkranz_Double | rosenkranz | 21GF-GIB | 1 in 138 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_1SuitedOpnr | precision_1c | Precision | 1 in 398 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_1SuitedResp | precision_1c | Precision | 1 in 388 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_3-Suit_Resp | precision_1c | Precision | 1 in 449 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_3-Suit_Resp_5-7 | precision_1c | Precision | 1 in 712 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_54_Resp | precision_1c | Precision | 1 in 63 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_55_Resp | precision_1c | Precision | 1 in 368 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_any_0-4_Resp | precision_1c | Precision | 1 in 47 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_any_5-7_Resp | precision_1c | Precision | 1 in 31 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1C_any_8plus_Resp | precision_1c | Precision | 1 in 31 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS16_1or2C | precision_1c | Precision | 1 in 42 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_3-Suit_Resp | precision_1c | Precision | 1 in 294 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_3-Suit_Resp_5-7 | precision_1c | Precision | 1 in 501 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_54_Resp | precision_1c | Precision | 1 in 45 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_55_Resp | precision_1c | Precision | 1 in 256 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_any_0-4_Resp | precision_1c | Precision | 1 in 38 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_any_5-7_Resp | precision_1c | Precision | 1 in 21 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_1C_any_8plus_Resp | precision_1c | Precision | 1 in 18 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SCS_Impossible_Negative | precision_1c | Precision | 1 in 937 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Scrambling_2NT | scrambling_2nt | 21GF-DEFAULT | 1 in 10,759 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Serious | serious_3nt | 21GF-DEFAULT | 1 in 9,302 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Six_Key_RKC | six_key_rkcb | 21GF-DEFAULT | 1 in 149,254 | 134 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Size_Asking_Minor_Suit_Stayman | minor_suit_stayman | 21GF-DEFAULT | 1 in 164 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Snapdragon_Double | snapdragon | 21GF-SPECIALS | 1 in 357,143 | 56 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Spear | spear | 21GF-DEFAULT | 1 in 16,425 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Spiral_Raises_Weinstein | spiral | 21GF-DEFAULT | 1 in 4,494 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Spiral_Raises_Wolpert | spiral | 21GF-DEFAULT | 1 in 10,308 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Splinters_after_Minor | splinters | 21GF-DEFAULT | 1 in 12,716 | 200 | 0.0% | 0.9% | 0 | 15 | 0 | 15 |
| Suction | suction | 21GF-DEFAULT | 1 in 900 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| SupportX_by_Advancer | support_doubles | 21GF-DEFAULT | 1 in 23,737 | 200 | 0.0% | 0.8% | 0 | 10 | 0 | 10 |
| Tislevoll_after_Opps_Preempt | tislevoll | 21GF-DEFAULT | 1 in 16,958 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Transfer_Advances | transfer_advances | 21GF-DEFAULT | 1 in 456 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Transfer_Walsh | transfer_walsh | 21GF-DEFAULT | 1 in 18 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Transfers_after_1M_X | transfers_after_double | 21GF-DEFAULT | 1 in 970 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Two-Suited_Overcalls | michaels, unusual_notrump | 21GF-DEFAULT | 1 in 7,924 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Two-Way_New_Minor_Forcing_aka_xyNT | two_way_nmf | 21GF-DEFAULT | 1 in 171 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Two_Over_One | two_over_one | 21GF-DEFAULT | 1 in 407 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Unusual_2N | unusual_notrump | 21GF-GIB | 1 in 409 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| WB5_Collante | collante | 21GF-SPECIALS2 | 1 in 4,026 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| WB5_Rodrigue | rodrigue | 21GF-SPECIALS2 | 1 in 6,925 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| We_Overcall_1N_then_Gerber | gerber | 21GF-SPECIALS | 1 in 30,047 | 200 | 0.0% | 1.4% | 0 | 18 | 0 | 18 |
| Western_Cue_Bid | western_cuebid | 21GF-DEFAULT | 1 in 129 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| XYZ | xyz | 21GF-DEFAULT | 1 in 731 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |
| Xfer_after_1M_X | transfers_after_double | 21GF-DEFAULT | 1 in 1,332 | 200 | 0.0% | 0.0% | 0 | 0 | 0 | 0 |

## Scripts that never reach their own convention's rules

- DONT (dont; card 21GF-GIB; general set fires 0 of its rules)
- DOPI_ROPI (dopi_ropi; card 21GF-DEFAULT; general set fires 0 of its rules)
- GIB_Sandwich_NT_BPH (sandwich_nt; card 21GF-GIB; general set fires 0 of its rules)
- Lead_Directing_Double (lead_directing_doubles; card 21GF-GIB; general set fires 0 of its rules)
- Maximal_After_Overcall (maximal_doubles; card 21GF-SPECIALS; general set fires 0 of its rules)
- Maximal_Double (maximal_doubles; card 21GF-SPECIALS; general set fires 0 of its rules)
- McCabe_After_Weak_2 (mccabe; card 21GF-DEFAULT; general set fires 0 of its rules)
- McCabe_after_WJO (mccabe; card 21GF-DEFAULT; general set fires 0 of its rules)
- Meckwell (meckwell; card 21GF-SPECIALS2; general set fires 0 of its rules)
- Mini-Maxi_Roman_2D (mini_roman_2d; card 21GF-DEFAULT; general set fires 0 of its rules)
- NT_Splinter (splinters; card 21GF-GIB; general set fires 15 of its rules)
- Namyats (namyats; card 21GF-SPECIALS; general set fires 0 of its rules)
- Puppet_Stayman_2N (puppet_stayman; card 21GF-MSTandMSS; general set fires 0 of its rules)
- Scrambling_2NT (scrambling_2nt; card 21GF-DEFAULT; general set fires 0 of its rules)
- Serious (serious_3nt; card 21GF-DEFAULT; general set fires 0 of its rules)
- Size_Asking_Minor_Suit_Stayman (minor_suit_stayman; card 21GF-DEFAULT; general set fires 0 of its rules)
- Snapdragon_Double (snapdragon; card 21GF-SPECIALS; general set fires 0 of its rules)
- Spiral_Raises_Weinstein (spiral; card 21GF-DEFAULT; general set fires 0 of its rules)
- Spiral_Raises_Wolpert (spiral; card 21GF-DEFAULT; general set fires 0 of its rules)
- Splinters_after_Minor (splinters; card 21GF-DEFAULT; general set fires 15 of its rules)
- Suction (suction; card 21GF-DEFAULT; general set fires 0 of its rules)
- SupportX_by_Advancer (support_doubles; card 21GF-DEFAULT; general set fires 10 of its rules)
- Transfer_Walsh (transfer_walsh; card 21GF-DEFAULT; general set fires 0 of its rules)
- Transfers_after_1M_X (transfers_after_double; card 21GF-DEFAULT; general set fires 0 of its rules)
- Two-Way_New_Minor_Forcing_aka_xyNT (two_way_nmf; card 21GF-DEFAULT; general set fires 0 of its rules)
- Two_Over_One (two_over_one; card 21GF-DEFAULT; general set fires 0 of its rules)
- We_Overcall_1N_then_Gerber (gerber; card 21GF-SPECIALS; general set fires 18 of its rules)
- Western_Cue_Bid (western_cuebid; card 21GF-DEFAULT; general set fires 0 of its rules)
- XYZ (xyz; card 21GF-DEFAULT; general set fires 0 of its rules)
- Xfer_after_1M_X (transfers_after_double; card 21GF-DEFAULT; general set fires 0 of its rules)

## Scenarios whose tags name no rule file

- 1M-3N_Picture_Bid: bidding_conventions/picture_3nt
- BART: bidding_conventions/bart
- Bergen_Thrump_X_after_Preempt: competitive_bidding/thrump_double
- CRASH: competitive_bidding/crash
- Equal_Level_Conversion: competitive_bidding/equal_level_conversion
- Exit_Transfers: competitive_bidding/exit_transfers
- Forcing_Pass: competitive_bidding/forcing_pass
- GSF_after_Preempt: bidding_conventions/grand_slam_force
- Good_Bad_2N: competitive_bidding/good_bad_2nt
- Grand_Slam_Force: bidding_conventions/grand_slam_force
- Grand_Slam_Force_2: bidding_conventions/grand_slam_force
- Lars_Multi_2D: bidding_conventions/lars_multi
- Last_Train_GT2: bidding_conventions/last_train
- Last_Train_Game_Try: bidding_conventions/last_train
- Losing_Trick_Count: basic_bidding/hand_evaluation
- Mathe: competitive_bidding/mathe
- Michaels_Cuebid: competitive_bidding/michaels
- Michaels_after_1m: competitive_bidding/michaels
- Michaels_and_Unusual: competitive_bidding/michaels, competitive_bidding/unusual_notrump
- Mitchell_Stayman: competitive_bidding/mitchell_stayman
- Muiderberg_Two_Bids: bidding_conventions/muiderberg
- Preempt_Keycard: bidding_conventions/preempt_keycard
- Rosenkranz_Double: competitive_bidding/rosenkranz
- SCS16_1C_1SuitedOpnr: bidding_conventions/precision_1c
- SCS16_1C_1SuitedResp: bidding_conventions/precision_1c
- SCS16_1C_3-Suit_Resp: bidding_conventions/precision_1c
- SCS16_1C_3-Suit_Resp_5-7: bidding_conventions/precision_1c
- SCS16_1C_54_Resp: bidding_conventions/precision_1c
- SCS16_1C_55_Resp: bidding_conventions/precision_1c
- SCS16_1C_any_0-4_Resp: bidding_conventions/precision_1c
- SCS16_1C_any_5-7_Resp: bidding_conventions/precision_1c
- SCS16_1C_any_8plus_Resp: bidding_conventions/precision_1c
- SCS16_1or2C: bidding_conventions/precision_1c
- SCS_1C_3-Suit_Resp: bidding_conventions/precision_1c
- SCS_1C_3-Suit_Resp_5-7: bidding_conventions/precision_1c
- SCS_1C_54_Resp: bidding_conventions/precision_1c
- SCS_1C_55_Resp: bidding_conventions/precision_1c
- SCS_1C_any_0-4_Resp: bidding_conventions/precision_1c
- SCS_1C_any_5-7_Resp: bidding_conventions/precision_1c
- SCS_1C_any_8plus_Resp: bidding_conventions/precision_1c
- SCS_Impossible_Negative: bidding_conventions/precision_1c
- Six_Key_RKC: bidding_conventions/six_key_rkcb
- Spear: competitive_bidding/spear
- Tislevoll_after_Opps_Preempt: bidding_conventions/tislevoll
- Transfer_Advances: competitive_bidding/transfer_advances
- Two-Suited_Overcalls: competitive_bidding/michaels, competitive_bidding/unusual_notrump
- Unusual_2N: competitive_bidding/unusual_notrump
- WB5_Collante: competitive_bidding/collante
- WB5_Rodrigue: competitive_bidding/rodrigue

## Skipped and failed

- skipped Jacoby_2N_4x_void_Leveled: a levelled script
- skipped Jacoby_2N_Leveled: a levelled script
- skipped Ned_Weak_Two_Leveled: a levelled script
- skipped Weak_2_Bids_Lax_Leveled: a levelled script
- skipped Weak_2_Bids_Leveled: a levelled script
- failed Bust_Over_Strong_2C: no deal in 20000000 dealt

## What the zero-hit list mostly is

Of the 30 scripts that never reach their convention's rules, 26 name a convention whose rules fire nowhere in the general set either, on the same card. The stock card the scenario names (or 21GF-DEFAULT) does not switch that convention on as Rusty reads it: DONT, Meckwell and Suction (the card's defence to 1NT is another), XYZ, Two-way NMF, Transfer Walsh, transfers after 1M-(X), Namyats, Mini-Roman, McCabe, Spiral, Serious 3NT, Maximal doubles, Snapdragon, Scrambling 2NT, Western cue bid, DOPI/ROPI, sandwich NT, lead-directing doubles, puppet over 2NT, size-asking minor-suit Stayman. Two_Over_One names `game-force.bid`, which sets a state and makes no call. So these are a card question (which card plays it, or a `--set`), not evidence about the scripts.

Four are different: the general set does fire the convention's rules on that card (NT_Splinter and Splinters_after_Minor against `splinters.bid`, SupportX_by_Advancer against `support-doubles.bid`, We_Overcall_1N_then_Gerber against `gerber.bid`). There the script deals a variant the tagged file does not cover (a splinter over notrump or a minor; a support double by advancer; Gerber after our overcall), or Rusty bids those hands another way.

## Conclusion

**Per board, a script is far better at reaching its convention.** Median share of boards where the convention's own rules make a call: 77.5% from the script, 3.4% from the general set (163 scenarios whose tags name a rule file). 83 scripts are at 75% or more.

**In rules reached, scripts add to the general set; they do not replace it.** 41,365 scripted boards fired 2,361 of the pack's 4,514 rules; 100,170 general boards on the same 18 cards fired 2,226. Together 2,585: scripts alone reach 359 the general set does not, and the general set 224 the scripts do not. For the convention's own rules, 58 scenarios reach rules the general set misses, and 118 miss rules the general set reaches, which is 200 boards against 5,565.

**What this cannot show**

- The "general set" is not random deals. It is the first boards of every scenario's PBN file in Practice-Bidding-Scenarios, which were themselves dealt from these scripts (levelled, and kept where BBA bid the scenario). So this compares 200 deals of one script with a blend of about 15 deals from every script, not scripted deals with unscripted ones. A random-deal baseline would show the scripts' advantage more starkly.
- One seed and 200 boards a script. Eleven scripts produced fewer within 20,000,000 deals, and one produced none (Bust_Over_Strong_2C).
- "Own rules" is by rule file. A tag that names a natural method points at a large shared file (`rebids.bid`, `responder-rebids.bid`), where 200 boards cannot compete with 5,565; 49 scenarios' tags name no rule file at all and have no hit rate.
- A rule firing says the auction was reached, not that the call was right.
- Whether a convention is on depends on the card. Only stock cards were used, as the scenario names them, with no settings changed.

**Natural rate.** The scripts' conditions are met between 31% of deals and 1 in 666,667; the median is 1 in 3,103. Each scenario's rate is in the table and in `scenarios.json` (`rate`, `produced`, `generated`), from non-levelled scripts with no levelling, for use as importance weights.
