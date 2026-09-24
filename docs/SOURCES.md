# Sources

References the project relies on. Each entry notes what the source justifies and its scope.

## Ji et al. 2016 — aerobic batch culture of baker's yeast

Ji M, Miao Y, Chen JY, You Y, Liu F, Xu L. *Growth characteristics of freeze-tolerant baker's yeast Saccharomyces cerevisiae AFY in aerobic batch culture.* SpringerPlus 5:503 (2016). doi:[10.1186/s40064-016-2151-3](https://doi.org/10.1186/s40064-016-2151-3). Open access, CC BY 4.0. Full text: [PMC4842200](https://pmc.ncbi.nlm.nih.gov/articles/PMC4842200/).

- **Status (update):** the Figure 1 40 g/L time course was digitised on 2026-09-24 into `explorations/data/ji2016_fig1_40gL.csv`, read by eye with an image overlay check. It is used to calibrate `002_overflow_repression`. Figure 2 is used only as the test.
- **Status:** Figure 1 reviewed qualitatively with Jakob on 2026-09-24. Used as evidence of aerobic ethanol production and subsequent growth on ethanol; no parameters adopted and no model fitted.
- **Figure 1:** circles = cells on the left logarithmic axis; triangles = glucose and squares = ethanol on the right linear axis. The later ethanol decrease accompanies further cell growth.
- **Methods and model scope:** medium sterilised before inoculation. The ethanol-growth equations assume other nutrients sufficient. Neither that assumption nor the paper's equations have been adopted for our simulator.
- **What it measured:** dry biomass (g/L, via OD600), glucose, and ethanol, sampled every 2 h. **Discrepancy:** Figure 1 appears to show markers at roughly 1 h spacing. Do not rely on the sampling interval, for example to argue what delay could be resolved, without clarifying this.
- **Conditions:** one industrial strain (AFY); YPD-based medium with minerals and vitamins; 30 °C, pH 5.0; 1.2 L in a 3 L stirred tank; air 200 L/h; dissolved oxygen held at 20 % of saturation by varying stirrer speed; starting glucose 1, 5, 10, 25, and 40 g/L.
- **Scope and caveats:** a single freeze-tolerant commercial strain, not a lab reference strain. The medium contains yeast extract and peptone, which are extra carbon and nitrogen beyond glucose. Biomass comes from an OD calibration. Its reported maximum growth rate (0.99 h⁻¹) looks high compared with commonly cited values for *S. cerevisiae* on glucose and needs cross-checking against a second source before any number is used in the model.

- **Preculture (methods):** YPD with 20 g/L glucose, 21 h at 30 °C, harvested in late exponential phase, 5 % v/v inoculum. **Implication:** the cells very likely start the batch already glucose-repressed, whatever the starting glucose. The stated inoculum of "1.2 × 10⁷ viable cells per liter" is inconsistent with the ~0.2 g/L starting biomass in Figure 1. It is probably per mL, but this is unclarified.
- **Figure 2 (agent's reading of a 360 px image, approximate ±0.01 g/g):** glucose-phase yields against starting glucose.

  | Starting glucose (g/L) | Cell yield (g/g) | Ethanol yield (g/g) |
  |---|---|---|
  | 1 | 0.41 | 0.22 |
  | 5 | 0.26 | 0.285 |
  | 10 | 0.24 | 0.31 |
  | 25 | 0.215 | 0.365 |
  | 40 | 0.195–0.20 | 0.40 |

  The endpoints match the text (0.41/0.22 and 0.20/0.40). Reserved as the independent test; do not fit to it.

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

## Mechanism of the Crabtree effect in *S. cerevisiae*: open literature read on 2026-09-24

These sources were read to decide how to represent overflow. Agents read the abstracts, and the key passages where a full text was available. No parameter has been adopted from them.

- **Otterstedt K et al. (2004).** *Switching the mode of metabolism in the yeast Saccharomyces cerevisiae.* EMBO Reports. doi:[10.1038/sj.embor.7400132](https://doi.org/10.1038/sj.embor.7400132), [PMC1299050](https://pmc.ncbi.nlm.nih.gov/articles/PMC1299050/). A strain engineered to take up glucose more slowly is fully respiratory even at high glucose. It ferments only when oxygen is lacking. **Supports:** ethanol production is controlled by the sugar uptake rate, which is causal evidence for a threshold framing. **Scope:** an engineered lab strain.
- **Elbing K et al. (2004).** *Role of hexose transport in control of glycolytic flux in Saccharomyces cerevisiae.* Applied and Environmental Microbiology 70, 5323–5330. doi:[10.1128/aem.70.9.5323-5330.2004](https://doi.org/10.1128/aem.70.9.5323-5330.2004), [PMC520882](https://pmc.ncbi.nlm.nih.gov/articles/PMC520882/). As transporter-limited uptake decreases, ethanol production decreases proportionally. In wild-type cells at high glucose during exponential batch growth, uptake capacity does *not* control the glycolytic flux. **Implication:** the maximum sugar consumption rate of wild type is set by the whole pathway, not by the transporter alone.
- **Hagman A, Säll T, Piškur J (2014).** *Analysis of the yeast short-term Crabtree effect and its origin.* FEBS Journal. doi:[10.1111/febs.13019](https://doi.org/10.1111/febs.13019), [PMC4240471](https://pmc.ncbi.nlm.nih.gov/articles/PMC4240471/). **Short-term effect:** ethanol appears immediately when sugar-limited cells receive a pulse of sugar. Pure respiration is possible only while glucose is kept low, either below the critical dilution rate or in fed-batch.
- **Hagman A, Piškur J (2015).** *A study on the fundamental mechanism and the evolutionary driving forces behind aerobic fermentation in yeast.* PLoS ONE 10, e0116942. doi:[10.1371/journal.pone.0116942](https://doi.org/10.1371/journal.pone.0116942), [PMC4305316](https://pmc.ncbi.nlm.nih.gov/articles/PMC4305316/). Overflow is the fundamental mechanism behind both the short-term and the long-term effect. **Glucose repression of respiration**, the long-term effect, is confined mainly to *S. cerevisiae* and close relatives. Proposed evolutionary drivers are faster energy production and consuming sugar quickly to starve competitors. **Relevant to the parked evolution question.**
- **Review, 2025.** *Overflow metabolism in bacterial, yeast, and mammalian cells: different names, same game.* Molecular Systems Biology. doi:[10.1038/s44320-025-00145-x](https://doi.org/10.1038/s44320-025-00145-x), [PMC12583676](https://pmc.ncbi.nlm.nih.gov/articles/PMC12583676/). Overflow flux depends on the glycolytic (sugar-processing) flux above an organism-dependent threshold. Lowering sugar transport reduces by-products. Several competing explanations of *why* remain under debate:
  - limited respiratory capacity (Sonnleitner & Käppeli 1986)
  - protein and proteome allocation (Malina et al. 2021)
  - membrane-space competition (Zhuang et al. 2011, [PMC3159977](https://pmc.ncbi.nlm.nih.gov/articles/PMC3159977/), shown in *E. coli*)
  - a limit on Gibbs energy dissipation (Niebel et al. 2019)
- **Access notes:** Sonnleitner & Käppeli 1986 is paywalled, and Unpaywall finds no legal open copy. Jakob asked about Sci-Hub; the agent declined because it infringes copyright. Legal routes are library access, author copies, and browser download of PMC PDFs.

## Parameter candidates from other strains (abstracts read, 2026-09-24)

- **Verduyn C, Postma E, Scheffers WA, van Dijken JP (1990).** *Physiology of Saccharomyces cerevisiae in anaerobic glucose-limited chemostat cultures.* Journal of General Microbiology 136, 395–403. doi:[10.1099/00221287-136-3-395](https://doi.org/10.1099/00221287-136-3-395). Strain CBS 8066, **anaerobic**. The abstract reports a maximum biomass yield of **0.10 g/g**, a Ks for glucose of **0.55 mM (≈ 0.1 g/L)**, and μmax 0.31 h⁻¹. **Candidate use:** the fermentative biomass yield, and the order of magnitude of how sugar uptake slows at low sugar. **Transfer caveat:** these are anaerobic values, whereas the overflow fraction in aerobic cells may differ. The strain also differs from AFY.
- **Jones KD, Kompala DS (1999).** *Cybernetic model of the growth dynamics of Saccharomyces cerevisiae in batch and continuous cultures.* Journal of Biotechnology. doi:[10.1016/s0168-1656(99)00017-6](https://doi.org/10.1016/s0168-1656(99)00017-6). Their aerobic batch shows an **intermediate lag phase** between the glucose and ethanol phases. Ji's AFY shows no visible pause, so strains differ in how fast they switch. Paywalled; abstract only.
- **Diderich JA et al. (1999).** *Glucose uptake kinetics and transcription of HXT genes in chemostat cultures of Saccharomyces cerevisiae.* Journal of Biological Chemistry 274, 15350–15359. doi:[10.1074/jbc.274.22.15350](https://doi.org/10.1074/jbc.274.22.15350). Transporter kinetics depend on growth conditions. This is background for why a single uptake affinity is a simplification. Abstract only.
- **Ethanol per glucose, stoichiometric maximum:** C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ gives 92/180 ≈ **0.51 g/g**. This is a derivation, not a measurement. The actual value is lower because some carbon goes to biomass.

## Supporting discussion references (not model inputs)

- [Oxygen dependence of metabolic fluxes and energy generation of S. cerevisiae CEN.PK113-1A](https://pmc.ncbi.nlm.nih.gov/articles/PMC2507709/): controlled oxygenation in glucose-limited cultures; supports changes in fermentation and biomass yield with oxygen availability. Different strain and continuous-culture conditions from Ji et al.; used qualitatively.
- [Selection of non-Saccharomyces yeast strains for reducing alcohol levels in wine by sugar respiration](https://pubmed.ncbi.nlm.nih.gov/24831930/): abstract consulted for the wine analogy; supports feasibility of alcohol reduction and oxidation/acetic-acid trade-offs, not alcohol-free wine by indefinite storage.
- Australian Wine Research Institute: [lees contact](https://www.awri.com.au/industry_support/winemaking_resources/winemaking-practices/winemaking-treatment-lees-contact/) and [wine faults](https://www.awri.com.au/industry_support/winemaking_resources/sensory_assessment/recognition-of-wine-faults-and-taints/wine_faults/). Authoritative practice references for oxygen exposure and spoilage; not simulator evidence.
- Eppendorf [bioreactor sampling guidance](https://www.eppendorf.com/at-en/lab-academy/applied-industries/bioprocessing/automated-bioreactor-sampling-with-the-eppendorf-bioprocess-autosampler/): manufacturer guidance on contamination prevention during sampling; does not document the apparatus used by Ji et al.
- Historical aside: Crabtree's [1929 tumour-metabolism paper](https://doi.org/10.1042/bj0230536) and De Deken's [1966 yeast paper](https://doi.org/10.1099/00221287-44-2-149). Name origin only; not evidence for a modern quantitative mechanism.

The elementary explanations of bond energetics, nutrient roles and yeast-extract manufacture are learning context, not a sourced parameter set. Obtain suitable reference data before using them quantitatively.
