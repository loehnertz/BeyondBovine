# 2026-09-24 — Overflow with glucose repression: first calibration and test

**Status:** exploratory increment. Built as agreed with Jakob. Not an accepted model.

## What was built

- `explorations/data/ji2016_fig1_40gL.csv` holds the 40 g/L time course, read by eye from Ji et al. Figure 1 on a pixel grid. The points were checked by overlaying them on the image. The estimated error is about ±3 % for cells and about ±0.2 g/L for glucose and ethanol.
- `explorations/002_overflow_repression.py` models:
  - uptake that slows when sugar is scarce
  - a respiration threshold with overflow to ethanol
  - respiratory machinery R that starts repressed and recovers when glucose is low
  - ethanol use gated by R and by glucose
  - a constant-threshold variant for comparison

  Five parameters were calibrated on the 40 g/L run only. The other parameters are fixed from the literature or derived; see the file header.
- The output is saved in `002_overflow_repression.png` and `002_overflow_repression.out.txt`.

## Results

- **Calibration (40 g/L):** the time course is reproduced roughly.
  - The model runs out of glucose about 1.5 h too early, and it misses the tail where the data still show 2.3 g/L at 8 h and 1.0 g/L at 9 h. The fixed uptake affinity (KS = 0.1 g/L) is probably too tight for this strain at these concentrations.
  - The model gives a glucose-phase cell yield of 0.15, where Ji measured 0.20.
- **Test (1–25 g/L, never fitted):** the *direction* is right. The yield rises at lower starting sugar, and repression makes the rise stronger than a constant threshold does. The *size* is far off: at 1 g/L the model gives 0.24 and Ji measured 0.41. The ethanol yields are too high at low sugar.
- **Recovery rate:** k_rec runs to its upper bound. The data favour almost instant recovery, which is consistent with "no visible pause". The machinery therefore tracks the current glucose level instead of carrying a memory. With one run, only the balance between recovery and repression is visible.

## Why the test fails: a finding independent of the model

With the fixed literature yields, no model of this form can hit Ji's measured yield pairs:

| Starting glucose | Fermented share needed for Ji's ethanol yield | Implied cell yield | Ji's cell yield |
|---|---|---|---|
| 40 g/L | 0.89 (ethanol 0.40 g/g) | 0.144 | 0.20 |
| 1 g/L | 0.49 (ethanol 0.22 g/g) | 0.30 | 0.41 |

Ji's cells grew more per gram of glucose than the fixed yields allow. Candidate explanations, none of them tested:

1. **Extra carbon in the medium.** Yeast extract and peptone are scaled with glucose, so some biomass may come from them.
2. **Higher yields in aerobic cells.** The biomass yield of the fermented share may be higher in aerobic respiro-fermenting cells than the anaerobic 0.10 (Verduyn 1990).
3. **Different strain.** AFY may have a higher respiratory yield than CBS 8066.
4. **Measurement.** The biomass comes from an OD calibration.

The 1 g/L point is also the weakest test case. The glucose phase lasts only about 1–2 h, so the state of the inoculum and carry-over from the preculture matter most there.

## Credibility

The code matches the stated model, and the calibrated run reproduces the data roughly. The model is **not** supported for predicting yields across starting sugar levels. It gets the trend direction right, but it fails on magnitude.

## Not done or open

- No parameter was tuned against Figure 2.
- The repression and recovery rates are not identifiable from this data.
- KR, KE and K_REP are unsourced.
- Ethanol evaporation under strong aeration (200 L/h into 1.2 L) is ignored. It would make the measured ethanol *lower* than what was produced.
- **Next decision (Jakob):** which explanation to investigate first. No explanation should be patched into the model without evidence.
