# Sources

References the project relies on. Each entry notes what the source justifies and its scope.

## Ji et al. 2016 — aerobic batch culture of baker's yeast

Ji M, Miao Y, Chen JY, You Y, Liu F, Xu L. *Growth characteristics of freeze-tolerant baker's yeast Saccharomyces cerevisiae AFY in aerobic batch culture.* SpringerPlus 5:503 (2016). doi:[10.1186/s40064-016-2151-3](https://doi.org/10.1186/s40064-016-2151-3). Open access, CC BY 4.0. Full text: [PMC4842200](https://pmc.ncbi.nlm.nih.gov/articles/PMC4842200/).

- **Status:** Figure 1 reviewed qualitatively with Jakob on 2026-09-24. Used as evidence of aerobic ethanol production and subsequent growth on ethanol; no parameters adopted and no model fitted.
- **Figure 1:** circles = cells on the left logarithmic axis; triangles = glucose and squares = ethanol on the right linear axis. The later ethanol decrease accompanies further cell growth.
- **Methods and model scope:** medium sterilised before inoculation. The ethanol-growth equations assume other nutrients sufficient. Neither that assumption nor the paper's equations have been adopted for our simulator.
- **What it measured:** dry biomass (g/L, via OD600), glucose, and ethanol, sampled every 2 h. **Discrepancy:** Figure 1 appears to show markers at roughly 1 h spacing. Do not rely on the sampling interval, for example to argue what delay could be resolved, without clarifying this.
- **Conditions:** one industrial strain (AFY); YPD-based medium with minerals and vitamins; 30 °C, pH 5.0; 1.2 L in a 3 L stirred tank; air 200 L/h; dissolved oxygen held at 20 % of saturation by varying stirrer speed; starting glucose 1, 5, 10, 25, and 40 g/L.
- **Scope and caveats:** a single freeze-tolerant commercial strain, not a lab reference strain. The medium contains yeast extract and peptone, which are extra carbon and nitrogen beyond glucose. Biomass comes from an OD calibration. Its reported maximum growth rate (0.99 h⁻¹) looks high compared with commonly cited values for *S. cerevisiae* on glucose and needs cross-checking against a second source before any number is used in the model.

## Malina et al. 2021 — machinery cost and the Crabtree effect

*Adaptations in metabolism and protein translation give rise to the Crabtree effect in yeast.* PNAS 118(51), e2112836118. doi:[10.1073/pnas.2112836118](https://doi.org/10.1073/pnas.2112836118). [Author-hosted full text](https://backend.orbit.dtu.dk/ws/portalfiles/portal/269333976/e2112836118.full.pdf).

- **Use:** supports the qualitative trade-off between ATP yield per sugar and protein machinery required for energy production. Discussed with Jakob; not an accepted quantitative model.
- **Scope:** compares four yeast species using physiological measurements, protein measurements and metabolic modelling under glucose excess. It does not establish one universal sensor threshold or rate law. Differences between species and conditions matter; its numbers must not be transferred directly to AFY.

## DeRisi, Iyer and Brown 1997 — gene activity during the diauxic shift

*Exploring the metabolic and genetic control of gene expression on a genomic scale.* Science 278, 680–686. doi:[10.1126/science.278.5338.680](https://doi.org/10.1126/science.278.5338.680). [PubMed](https://pubmed.ncbi.nlm.nih.gov/9381177/).

- **Use:** evidence that the transition involves broad changes in gene expression. Abstract and associated research descriptions consulted; no quantitative adaptation time extracted.
- **Scope:** gene-expression changes do not directly determine enzyme activities or justify a particular delay equation for our strain.

## Vallari et al. 1992 — ADH2 regulation

*Glucose repression of the yeast ADH2 gene occurs through multiple mechanisms, including control of the protein synthesis of its transcriptional activator, ADR1.* Molecular and Cellular Biology 12, 1663–1673. doi:[10.1128/MCB.12.4.1663-1673.1992](https://doi.org/10.1128/MCB.12.4.1663-1673.1992). [PubMed](https://pubmed.ncbi.nlm.nih.gov/1549119/).

- **Use:** concrete example of glucose-regulated machinery for ethanol use; abstract consulted. ADH2 transcription rises on shifting from glucose to ethanol growth conditions.
- **Scope:** one regulatory component, not a complete diauxic-switch model. No parameter adopted.

## Postma et al. 1989 — where aerobic fermentation starts, in a chemostat

Postma E, Verduyn C, Scheffers WA, van Dijken JP. *Enzymic analysis of the Crabtree effect in glucose-limited chemostat cultures of Saccharomyces cerevisiae.* Applied and Environmental Microbiology 55(2), 468–477 (1989). doi:[10.1128/aem.55.2.468-477.1989](https://doi.org/10.1128/aem.55.2.468-477.1989). Full text: [PMC184133](https://pmc.ncbi.nlm.nih.gov/articles/PMC184133/).

- **Read status:** abstract only. The PDF could not be retrieved from the cloud session because of a CAPTCHA.
- **What the abstract reports:** strain CBS 8066, grown in glucose-limited chemostat cultures.
  - Below a growth rate of 0.30 h⁻¹, glucose is fully respired, with a yield of 0.50 g/g.
  - Above it, acetate and pyruvate appear and the yield drops to 0.47 g/g.
  - At 0.38 h⁻¹, oxygen uptake reaches its maximum of 12 mmol O₂ per g dry weight per hour.
  - Above that, aerobic alcoholic fermentation appears and the yield falls towards 0.16 g/g.
- **Mechanism:** the authors conclude that fermentation is *not primarily* caused by limited respiratory capacity. This contradicts the mechanistic interpretation of Sonnleitner & Käppeli 1986. Malina et al. 2021 offers a protein-allocation explanation instead.
- **Candidate use:** the threshold at which aerobic ethanol production starts, and the respiratory yield.
  - Agent's inference: the threshold corresponds to roughly 0.38 / 0.47 ≈ 0.8 g glucose per g cells per hour.
  - Caveats: this is a different strain from Ji et al., and it was measured in a chemostat, where growth is held steady. A batch culture's changing conditions may behave differently.
  - No value has been adopted.

## Supporting discussion references (not model inputs)

- [Oxygen dependence of metabolic fluxes and energy generation of S. cerevisiae CEN.PK113-1A](https://pmc.ncbi.nlm.nih.gov/articles/PMC2507709/): controlled oxygenation in glucose-limited cultures; supports changes in fermentation and biomass yield with oxygen availability. Different strain and continuous-culture conditions from Ji et al.; used qualitatively.
- [Selection of non-Saccharomyces yeast strains for reducing alcohol levels in wine by sugar respiration](https://pubmed.ncbi.nlm.nih.gov/24831930/): abstract consulted for the wine analogy; supports feasibility of alcohol reduction and oxidation/acetic-acid trade-offs, not alcohol-free wine by indefinite storage.
- Australian Wine Research Institute: [lees contact](https://www.awri.com.au/industry_support/winemaking_resources/winemaking-practices/winemaking-treatment-lees-contact/) and [wine faults](https://www.awri.com.au/industry_support/winemaking_resources/sensory_assessment/recognition-of-wine-faults-and-taints/wine_faults/). Authoritative practice references for oxygen exposure and spoilage; not simulator evidence.
- Eppendorf [bioreactor sampling guidance](https://www.eppendorf.com/at-en/lab-academy/applied-industries/bioprocessing/automated-bioreactor-sampling-with-the-eppendorf-bioprocess-autosampler/): manufacturer guidance on contamination prevention during sampling; does not document the apparatus used by Ji et al.
- Historical aside: Crabtree's [1929 tumour-metabolism paper](https://doi.org/10.1042/bj0230536) and De Deken's [1966 yeast paper](https://doi.org/10.1099/00221287-44-2-149). Name origin only; not evidence for a modern quantitative mechanism.

The elementary explanations of bond energetics, nutrient roles and yeast-extract manufacture are learning context, not a sourced parameter set. Obtain suitable reference data before using them quantitatively.
