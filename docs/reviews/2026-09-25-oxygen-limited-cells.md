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
