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

1. **Extra carbon in the medium.** Yeast extract (about 0.22 g per g glucose; there is no peptone in the batch medium, see `SOURCES.md`) is scaled with glucose, so some biomass may come from it.
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

## Round 2: yeast extract as a second carbon source (`explorations/003_with_yeast_extract.py`)

**Carbon balance (chemistry only, no model).** Carbon fractions:

- glucose 0.400 (exact)
- ethanol 0.522 (exact)
- biomass 0.488 (assumed composition CH1.8O0.5N0.2)
- yeast extract 0.43 g C/g (Schröder-Kleeberg et al. 2025, Table A2)

At 40 g/L, Ji's cells plus ethanol, plus the unavoidable CO₂ released as ethanol forms, need **0.411 g C per g glucose**. The glucose supplies only **0.400**, and that is before any respiration. Yeast extract (0.22 g per g glucose in Ji's Table 1) supplies about **0.096 g C per g glucose** more. So some biomass very likely comes from yeast extract, or the measurements are biased. The extra cells per g of yeast extract needed to close the gap are about 0.06–0.25 at 5–40 g/L. That is consistent with a single value within the reading error. At 1 g/L it would take 0.53, which makes that point the outlier again.

**Model.** Yeast extract is co-consumed with glucose in the medium's ratio. It adds cells at a yield calibrated on 40 g/L only: 0.18–0.27 g cells per g yeast extract, in line with the carbon balance.

**Result.**
- **Cell yields:** slightly better. At 1 g/L the model gives 0.27 (Ji: 0.41); at 40 g/L it gives 0.16 (Ji: 0.20).
- **Ethanol yields:** now overshoot everywhere.
- **Parameters:** the fit pushes the repressed threshold to 0, so repressed cells ferment everything above the respiration they have left.

**What the result shows.** Yeast extract is real, but it is not the main problem. The dominant misfit is visible in the 40 g/L glucose panel. The model's glucose runs out abruptly at about 7.4 h. The data show a tail of 9.8 g/L at 7 h, 2.3 g/L at 8 h and 1.0 g/L at 9 h, and during that tail the cells grow from 6 to 8.75 g/L. Because the model cannot slow uptake at a few g/L of glucose, this growth is counted as the ethanol phase. That distorts the glucose-phase yields and keeps overflow going at low starting sugar.

**Candidate next step (not agreed):** calibrate KS, the sugar level at which uptake is half its maximum, on the 40 g/L tail instead of fixing it at 0.1 g/L. The justification is that Verduyn's value comes from glucose-limited chemostats, where high-affinity transporters dominate. In a high-glucose batch, low-affinity transporters dominate (Diderich et al. 1999). A source for their affinity values is still needed.

## Round 3: KS calibrated (`explorations/004_calibrated_ks.py`)

**Change.** KS, the sugar level at which uptake runs at half speed, is calibrated on the 40 g/L run instead of being fixed at 0.1 g/L. Everything else is as in 003.

**Plausibility check (passed).**
- The fitted KS is **8–14 g/L** across the variants.
- That falls inside the half-speed range of yeast's low-affinity glucose transporters, 50–100 mM or 9–18 g/L for Hxt1/3 (Reifenberger et al. 1997).
- The 0.1 g/L literature value came from glucose-limited chemostats. It was the wrong transfer for a high-glucose batch.

**Calibration.** The 40 g/L time course, including the glucose tail, is now reproduced well.

**Test (Figure 2, never fitted).**

| Starting glucose | Ji cells / ethanol | constant + YE | repression + YE (KR 0.5) |
|---|---|---|---|
| 1 | 0.41 / 0.22 | 0.47 / 0.00 | 0.52 / 0.00 |
| 5 | 0.26 / 0.285 | 0.32 / 0.11 | 0.45 / 0.00 |
| 10 | 0.24 / 0.31 | **0.24 / 0.27** | 0.33 / 0.17 |
| 25 | 0.215 / 0.365 | **0.19 / 0.37** | 0.22 / 0.33 |
| 40 | 0.20 / 0.40 | 0.17 / 0.39 (calibrated) | 0.18 / 0.37 (calibrated) |

- **10–40 g/L:** the constant-threshold variant is now close to Ji.
- **1–5 g/L:** the failure has flipped. The model predicts little or no ethanol, but Ji's yeast made substantial ethanol even at 1 g/L. With KS around 10 g/L, uptake at 1–5 g/L stays below the respiration threshold, so the model respires. In the repression variants, fast recovery also re-derepresses the cells almost immediately.
- **Repression makes the low-sugar prediction worse, not better.** This is the opposite of what we hoped for when we chose to include it. Recovery must be fast to show "no pause" at 40 g/L, and fast recovery removes overflow at low sugar.

**Model flexibility warning.** Seven parameters are calibrated on one run. Several run to their bounds (qcrit_min → 0, k_rec → 20), and they trade off against KR. A good 40 g/L fit therefore proves little on its own. The test is what carries the evidence.

**What this means.** No single set of *current-state* rules (uptake depending on current glucose, recovery depending on current glucose) fits both the 40 g/L run and the low-sugar runs. Candidate explanations, none of them tested:

- **The cells' history matters.** Transporter makeup and repression may carry over from the high-glucose preculture, and Walsh et al. 1994 report that transport affinity changes during growth on glucose.
- **The 1–5 g/L points are unreliable.** Their glucose phase lasts about 1–2 h, which is only 1–2 samples.
- **Carry-over from the preculture** of glucose or ethanol, which matters most at low levels.

**Relevance to the project.** Fed-batch deliberately holds glucose low, which is exactly the regime where this model now fails. Low-sugar behaviour is therefore not a side issue for the deferred fed-batch question. It is the main one.

## Round 4: uptake affinity linked to repression, with chemostat data (`explorations/005_state_dependent_uptake.py`)

**Change (agreed with Jakob).** The uptake half-speed point depends on the repression state R. At R = 0 (repressed) it uses the low-affinity value, calibrated. At R = 1 (derepressed) it uses the high-affinity value, KS = 0.27 g/L (Reifenberger 1997). The model is calibrated jointly on Ji's 40 g/L run and the van Hoek 1998 chemostat, which uses an industrial baker's yeast. Tested on Ji Figure 2 and on the compiled 8 g/L batch. Neither test set was fitted.

**New data.** Both files are in `explorations/data/` and come from the MIT-licensed Moreno-Paz et al. 2022 compilation.

- `vanhoek1998_chemostat.csv` was checked against the original abstract.
- `compiled_batch_8gL.csv` has no identified original source, and it is internally inconsistent early on: 1 g/L ethanol after only 0.5 g/L glucose, which is stoichiometrically impossible. Only its yields at glucose exhaustion are used, and only as a test.

**Calibration.**

- **Chemostat:** reproduced well. The model is fully respiratory up to D ≈ 0.30, against 0.28 in the data, with a sharp ethanol rise above that. It misses the small onset at D = 0.28–0.30.
- **Ji 40 g/L:** the cells and ethanol fit well. Early glucose consumption lags the data by about 1 h, a compromise with the chemostat.
- **Low-affinity KS:** 10.7 g/L, which is the Hxt1/3 range again.
- **Respiration thresholds:** 0.30 g/g/h when repressed and 0.75 g/g/h when derepressed.
- **Yeast-extract yield:** fell to 0.05, so it now contributes little.

**Test.**

| Starting glucose | 004 (constant + YE) | 005 | Ji |
|---|---|---|---|
| 1 | 0.47 / 0.00 | 0.46 / 0.01 | 0.41 / 0.22 |
| 5 | 0.32 / 0.11 | **0.31 / 0.19** | 0.26 / 0.285 |
| 10 | 0.24 / 0.27 | **0.25 / 0.27** | 0.24 / 0.31 |
| 25 | 0.19 / 0.37 | 0.19 / 0.34 | 0.215 / 0.365 |

- **Compiled 8 g/L batch:** the model gives 0.26 / 0.25 and the data give 0.14 / 0.39. The model under-predicts overflow. The result does not depend on whether the cells start repressed or derepressed.

**Reading.**

- **Improvement in the intended direction.** The model is now consistent with chemostat physiology, and 5 g/L improved. The low-sugar failure was not fixed, however. At 1 g/L and in the 8 g/L batch, real yeast overflows much more than the model allows.
- **Why the model cannot overflow at low sugar.** Overflow needs *fast uptake* and a *low respiration threshold* at the same time. The model ties both to one state R, so when cells switch to high-affinity uptake they also raise their respiration threshold, and the overflow disappears.
- **Candidate hypothesis, not agreed and not tested.** Transporter affinity may respond quickly to the glucose level, while respiratory derepression is slower. Then cells coming from a high-glucose preculture into low sugar would briefly have high-affinity uptake *and* low respiration, and would overflow. This would require two separate states, with an extra rate parameter and no quantitative source for it yet. Transporter expression is known to track glucose level (Diderich 1999) and affinity is known to change during growth (Walsh 1994). The relative speeds of these changes have not been sourced.
- **Other open issues:**
  - The 8 g/L batch uses a different lab strain (H1022), with unknown medium and preculture.
  - The model now has 8 calibrated parameters.
  - Combining two strains in one parameter set is an assumption.

## Round 5: two adaptation states (`explorations/006_two_states.py`)

**Change (agreed with Jakob).** Transporter affinity T and respiratory derepression R became separate states. T adapts `speed_ratio` times faster than R, with the ratio calibrated and constrained to be at least 1. The hypothesis was that cells arriving in low sugar briefly combine fast uptake with low respiration, and so overflow.

**Result: the hypothesis did not rescue the low-sugar predictions.**

- **Calibration:** as good as 005. The chemostat onset at D = 0.30 is slightly better. The fitted speed ratio is 4.3, and the repressed threshold rose to 0.43 g/g/h.
- **Ji test:**

  | Starting glucose | 006 (cells / ethanol) | 005 | Ji |
  |---|---|---|---|
  | 1 g/L | 0.48 / 0.00 | 0.46 / 0.01 | 0.41 / 0.22 |
  | 5 g/L | 0.34 / 0.15 | 0.31 / 0.19 | 0.26 / 0.285 |
  | 10 g/L | 0.26 / 0.25 | 0.25 / 0.27 | 0.24 / 0.31 |
  | 25 g/L | 0.20 / 0.33 | 0.19 / 0.34 | 0.215 / 0.365 |

- **8 g/L batch:** 0.28 / 0.22, against 0.14 / 0.39 in the data.

**Why it failed.** Calibrating on 40 g/L plus the chemostat sets the respiration thresholds so that the chemostat stays fully respiratory up to D ≈ 0.28. At 1–5 g/L, even with faster high-affinity uptake, the uptake barely exceeds those thresholds. The extra state gives the model freedom that the calibration data do not use in the way the test needs. This is a falsification of the hypothesis *as implemented*, and it is recorded as such.

**Weaknesses in the low-sugar evidence itself**, raised to keep the conclusion honest:

- **Ji 1 g/L:** the inoculum is 5 % of a 21 h YPD preculture. Ethanol carried over from it could be comparable to the ethanol formed from 1 g/L glucose. Ji's Figure 1 shows about 0.1 g/L ethanol at t = 0 in the 40 g/L run, which is within the reading error of zero. If the same carry-over were present at 1 g/L, it would account for up to about 0.1 of the 0.22 g/g. It is unknown whether Ji subtracted it.
- **Compiled 8 g/L batch:** the original source is not identified, and the early points are stoichiometrically impossible.
- **Ji 5 g/L:** this remains the cleanest unexplained gap. The model gives 0.15–0.19 ethanol against Ji's 0.285.

**Overall status after five rounds.**

- **What works:** one structure (overflow above a threshold, repression, yeast extract, state-dependent uptake) reproduces a baker's-yeast chemostat and a 40 g/L batch. It predicts untouched batch yields at 10–40 g/L within about 0.02–0.05 g/g.
- **What fails:** it under-predicts overflow at low starting sugar, and none of three mechanism additions fixed that.
- **What the model has become:** nine calibrated parameters on two calibration sets. Further mechanism should wait for better low-sugar data: batch time courses with dense early sampling, known preculture, defined medium, and a strain close to the calibration strain.
