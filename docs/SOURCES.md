# Sources

References the project relies on. Each entry notes what the source justifies and its scope.

## Ji et al. 2016 — aerobic batch culture of baker's yeast

Ji M, Miao Y, Chen JY, You Y, Liu F, Xu L. *Growth characteristics of freeze-tolerant baker's yeast Saccharomyces cerevisiae AFY in aerobic batch culture.* SpringerPlus 5:503 (2016). doi:[10.1186/s40064-016-2151-3](https://doi.org/10.1186/s40064-016-2151-3). Open access, CC BY 4.0. Full text: [PMC4842200](https://pmc.ncbi.nlm.nih.gov/articles/PMC4842200/).

- **Status:** candidate for step 5 (comparing the batch toy with real data). Found by the agent on 2026-09-24; Jakob has not yet reviewed it.
- **What it measured:** dry biomass (g/L, via OD600), glucose, and ethanol, sampled every 2 h.
- **Conditions:** one industrial strain (AFY); YPD-based medium with minerals and vitamins; 30 °C, pH 5.0; 1.2 L in a 3 L stirred tank; air 200 L/h; dissolved oxygen held at 20 % of saturation by varying stirrer speed; starting glucose 1, 5, 10, 25, and 40 g/L.
- **Scope and caveats:** a single freeze-tolerant commercial strain, not a lab reference strain. The medium contains yeast extract and peptone, which are extra carbon and nitrogen beyond glucose. Biomass comes from an OD calibration. Its reported maximum growth rate (0.99 h⁻¹) looks high compared with commonly cited values for *S. cerevisiae* on glucose and needs cross-checking against a second source before any number is used in the model.
