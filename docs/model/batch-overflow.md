# Model: yeast batch and chemostat with overflow, repression and adaptive uptake

**Status:** exploratory. It is not the engine, and it is not validated for low starting sugar.

**Reference implementation:** `explorations/005_state_dependent_uptake.py`.

**Last reviewed with Jakob:** 2026-09-25. Jakob agreed each mechanism step by step. The full history, including the failed variants, is in [the review](../reviews/2026-09-24-overflow-repression.md).

## What it represents

Aerobic *S. cerevisiae* growing on glucose in one perfectly mixed vessel. It covers:

- a batch culture, and a chemostat (fresh medium in, broth out)
- enough oxygen and nutrients throughout
- one average cell type

## State

| Quantity | Meaning |
|---|---|
| X | cells, g/L |
| S | glucose, g/L |
| E | ethanol, g/L |
| YE | yeast extract, g/L; only in Ji's medium |
| R | respiratory machinery, 0 = repressed, 1 = derepressed |

## Rules

1. **Uptake slows when sugar is scarce.** qs = qs_max · S / (KS + S).
2. **The uptake affinity follows R.** KS = 0.27 g/L when derepressed (high-affinity transporters) and ks_low_aff when repressed (low-affinity transporters).
3. **Overflow above a threshold.** Uptake up to the threshold qcrit(R) is respired, at a yield of 0.48 g cells per g glucose. Uptake above it goes to ethanol, at 0.45 g ethanol and 0.10 g cells per g glucose. The model does not claim *why* the threshold exists; see the competing explanations in `SOURCES.md`.
4. **Repression and recovery.** R falls while glucose is high and recovers when it is low. The repression signal is g = S / (S + 0.5 g/L).
5. **Ethanol use** needs derepressed machinery (R) and low glucose.
6. **Yeast extract** is consumed alongside glucose, in the ratio of Ji's medium, and adds cells.

## Parameters

| Parameter | Value | Basis | Applicability | Status |
|---|---|---|---|---|
| Respiratory yield | 0.48 g/g | van Hoek 1998 chemostat | industrial baker's yeast, a different strain from Ji's | accepted |
| Fermentative cell yield | 0.10 g/g | Verduyn 1990 | anaerobic lab strain; transfer to aerobic overflow is uncertain | accepted, exploratory |
| Ethanol per fermented glucose | 0.45 g/g | stoichiometry minus biomass carbon | derivation | accepted |
| High-affinity KS | 0.27 g/L | Reifenberger 1997 (Hxt6/7) | single-transporter strains | accepted |
| Low-affinity KS | 10.7 g/L | calibrated | falls in the Hxt1/3 range, 9–18 g/L | plausibility check passed |
| Thresholds (repressed / derepressed) | 0.30 / 0.75 g/g/h | calibrated | chemostat onset reproduced | calibrated |
| KR, KE, K_REP | 0.5 g/L, 0.1 g/L, 1/h | **not sourced** | — | assumption |
| qs_max, k_rec, qe_max, y_xe, y_xye | see `005_…out.txt` | calibrated | — | calibrated |

## Evidence

- **Calibrated on:**
  - Ji et al. 2016, 40 g/L batch, digitised from Figure 1
  - van Hoek 1998 chemostat
- **Tested on (never fitted):**
  - Ji Figure 2, glucose-phase yields at 1–25 g/L
  - a compiled 8 g/L batch whose original source is not identified

## What it is supported for, and what it is not

- **Supported (qualitatively, within the tested range):**
  - Batch cultures starting at 10–40 g/L glucose: predicted glucose-phase yields are within about 0.02–0.05 g/g of Ji.
  - The respiratory-to-overflow transition in a chemostat, with onset near D ≈ 0.28–0.30 1/h.
- **Not supported:** batch cultures starting at low sugar (1–8 g/L). The model makes too little ethanol there: at 5 g/L it gives 0.19 g/g against Ji's 0.285. Three mechanism additions did not fix this.
- **Not represented at all:**
  - oxygen limitation and transfer
  - temperature and pH
  - maintenance at low growth rates
  - lag and death
  - ethanol evaporation
  - carry-over from the preculture
  - strain differences, since one parameter set is used for two industrial strains

## Verification and validation

- **Verification** (does the code implement the model above?):
  - The code was reviewed by the agent.
  - Calibration outputs are plotted against data.
  - **Not yet done:** an automated carbon-balance check of the simulated runs, and unit tests. Needed before this becomes engine code.
- **Validation** (does the model represent reality for its purpose?):
  - Partial, and only for the scope marked "supported" above.
  - Two industrial strains and two labs are involved, and the data were digitised or compiled second-hand.
  - This is not a validated process model.
