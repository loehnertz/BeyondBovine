# 2026-09-25: Cell-level oxygen limit, tested on Jouhten et al. 2008

**Status:** exploratory increment, agreed with Jakob. Nothing was fitted to the test data.

## What was built

`explorations/008_oxygen_limited_cells.py`: the respired glucose flux is capped by the available oxygen, using 2.31 mol O₂ per mol glucose from the electron balance in 007. Any remaining sugar is fermented with the 005 yields: 0.10 g cells and 0.45 g ethanol per g glucose.

**Test.** Each condition's measured oxygen uptake is imposed on a glucose-limited chemostat at D = 0.1 1/h. The model then predicts glucose uptake, ethanol production and biomass. The data are in `explorations/data/jouhten2008_oxygen_chemostat.csv`.

## Results

| Condition | Model vs data |
|---|---|
| Fully aerobic, 20.9 % O₂ | good: no ethanol; biomass 4.8 vs 5.2–5.3 g/L |
| Fully anaerobic, 0 % O₂ | good: ethanol 9.8 vs 9.1–9.5, biomass 1.0 vs 1.0 |
| **Oxygen-limited, 2.8 / 1.0 / 0.5 %** | **poor: about 2× too much ethanol and 25–40 % too little biomass**. At 1 % O₂: ethanol 3.6 vs 1.6–2.0, biomass 2.0 vs 2.7–3.2 |

This is the outcome expected before the run.

**Diagnostic (not a fit).** The cell yield of the fermented share that would reproduce the measured rates is **0.13–0.18 g/g** under oxygen limitation. It is **0.08–0.09 when anaerobic**, which matches our 0.10.

## What was learned

- **Fermenting in the presence of some oxygen is more efficient than fermenting without any.**
- **A plausible mechanism, from textbook physiology and not tested here:** without oxygen, yeast must make glycerol to rebalance its redox state, which costs carbon and energy. Glycerol appears in these data only at 0 % O₂, at 1.05–1.11 mmol/g/h. Even a little oxygen lets the respiratory chain do that job instead.
- **Link to step 5.** In round 1, Ji's 40 g/L yields were impossible with a fermentative yield of 0.10, which needed about 0.144 against the measured 0.20. Aerobic overflow is fermentation in cells *with* oxygen, so a higher fermentative yield under oxygen is a candidate explanation for that gap too, alongside yeast extract.

## Not yet done

- The fermentative yield has not been changed in any model. Setting it from these same data and re-testing here would be circular.
- **Candidate next step (not agreed):** calibrate an oxygen-present fermentative yield on Jouhten's oxygen-limited conditions, then test it on *other* data: Ji Figure 2 (does the round 1 gap close?) and the fed-batch.

## Follow-up: an oxygen-present fermentative yield, with cross-dataset tests (`explorations/009_oxygen_present_yield.py`)

**Agreed with Jakob.** One number was calibrated on Jouhten's oxygen-limited chemostats only: the cell yield of fermented sugar when oxygen is present. The 005 model was then re-calibrated on its usual data, Ji 40 g/L plus van Hoek, using that yield for aerobic overflow. It was then tested on other data.

**Calibration.** The yield is **0.174 g cells per g**, compared with 0.10 without oxygen. The ethanol yield follows from the carbon balance: 0.403 g/g. Jouhten's 1.0 and 0.5 % conditions are now matched to within about 15 %. At 2.8 %, the model still predicts some ethanol (0.32) where almost none was measured (0.07–0.10).

**Re-calibrated 005.**
- The yeast-extract yield went to **0**: extra carbon from the medium is no longer needed to explain Ji's yields.
- The low-affinity KS is 5.2 g/L, between the Hxt2/4 and Hxt1/3 ranges.
- The repressed threshold is close to 0, and the derepressed threshold is 0.50 g/g/h.
- The chemostat is still reproduced, with the onset of ethanol slightly early, at D ≈ 0.25–0.28.

**Test: Ji Figure 2 (cells / ethanol, g/g).**

| Starting glucose | 009 | 005 | Ji |
|---|---|---|---|
| 1 | 0.35 / 0.13 | 0.46 / 0.01 | 0.41 / 0.22 |
| 5 | **0.25 / 0.28** | 0.31 / 0.19 | 0.26 / 0.285 |
| 10 | **0.22 / 0.33** | 0.25 / 0.27 | 0.24 / 0.31 |
| 25 | **0.20 / 0.37** | 0.19 / 0.34 | 0.215 / 0.365 |

The compiled 8 g/L batch gives 0.23 / 0.31, against the data's 0.14 / 0.39; 005 gave 0.25 for ethanol.

**Fed-batch.** Gas exchange from 25 to 98 h is unchanged and good. The transition at 15 h is worse (OUR 6.9 vs 0.9). Biomass is still about 30 % low in the middle of the run.

## What was learned (the main lesson of the whole overflow thread)

- **The step 5 low-sugar failure was mostly a mis-transferred parameter, not missing mechanism.** The fermentative yield came from *anaerobic* cells (Verduyn 1990), but Crabtree overflow happens in cells *with* oxygen. Three added mechanisms (rounds 3–5) could not fix it. One parameter, calibrated on an independent dataset about oxygen, fixed 5 and 10 g/L and most of 1 g/L.
- **The round 1 carbon-balance puzzle is resolved without yeast extract.** Whether some yeast-extract carbon is used remains possible, but it is not needed.
- **Caveats:**
  - The yield comes from a lab strain (CEN.PK) and is applied to an industrial strain (AFY).
  - 1 g/L remains under-predicted for ethanol, although the possible preculture carry-over applies there.
  - The compiled 8 g/L batch remains off, but it has no identified source.
