# Learning

This file records how Jakob learns the science in this project, what he has covered so far, and which of his questions are still waiting.

**Agents:** read this file before explaining anything scientific. Only Jakob's own statements count as evidence of what he understands. An agent's explanation does not count ([decision 0002](decisions/0002-project-records.md), rule 4).

## Approach

Agreed on 2026-09-24, after a trial on the first topic.

**Background.** Jakob is an experienced software engineer. His biology, chemistry, physics, and maths are at German high-school level; biology is a little stronger than the others. Assume no background in this domain. He wants to go deep, led by curiosity. Do not ask him to read textbooks from cover to cover.

**Per topic:**

1. **Predict first.** Jakob guesses before the explanation. Wrong guesses are welcome.
2. **Explain in small pieces.** Stop regularly so he can ask questions. Offer different angles when something doesn't land: programming, cooking, pictures, or equations. Drop an analogy that confuses him.
3. **Say it back.** Jakob restates the idea in his own words. The agent then points out what is missing or slightly off.
4. **Play with it**, when that helps: small interactive toys now, the simulator later.
5. **Check against something real**, such as a figure, a video, or data.

**Style:**

- When a question advances the discussion, ask one plainly worded question. Do not use labels such as "Prediction:" or force a check after every explanation.
- **Pace refinement from Jakob, 2026-09-24:** "Ethanol, c'mon, a touch less baby steps." Skip obvious recall questions and repeated requests to restate established points. Keep explanations accessible, but spend questions on meaningful mechanisms, uncertainties, and modelling choices.
- Introduce each technical term explicitly the first time it is used.
- Keep the chunks small. Jakob found the pace of the first session good.
- The agent is a tutor, not an authority. Flag uncertainty. Any claim the project relies on needs a source.
- At the start of a session, briefly revisit the last topic.

**Branching.** Jakob asks questions freely. The agent sorts each one:

- **Quick answer:** answer it now.
- **Park it:** add it to the list below, then return to it when it fits or when Jakob picks it.
- **Branch:** follow it now. This is Jakob's call, and the current thread is parked instead.

## Current goal

The first goal is to understand, predict, and simulate a **batch culture**: yeast grows on sugar until the sugar runs out. See [STATE.md](STATE.md) for the goal and its steps.

## Topics

### Step 1 — What happens when yeast grows on sugar? (done)

**Explained so far:**

- Sugar is both fuel and building material.
- The growth medium (the nutrients the yeast grows in).
- **Respiration** (with oxygen): sugar becomes new cells, CO₂, and water, and releases a lot of energy. Energy is carried by ATP. Heat is released.
- **Fermentation** (initially introduced as the route without oxygen): sugar becomes ethanol and CO₂, with less ATP per sugar than respiration. **Correction, step 5:** it also occurs with oxygen available; see the Crabtree discussion below.
- "Fermentation" means something different to biologists and to industry.
- What yeast is:
  - a single-celled fungus
  - its cells have a nucleus, like ours
  - it multiplies by budding
  - "yeast" covers many species; baker's yeast is *S. cerevisiae*
- Aerobic, anaerobic, and oxygen-limited conditions. With limited oxygen, yeast does a mix of respiration and fermentation.
- What matters is the oxygen dissolved in the liquid.

**Jakob's own statements:**

- He predicted that sugar is used as food and energy for multiplying. This is right; it misses the building-material role.
- He summarised: "sugar in, yeast out, and CO₂ and water out as well". The agent confirmed this for respiration and added heat.
- He explained that not all sugar becomes cells because of a loss, like friction or heat. This is partly right. The main reason is that some sugar must be burned for energy, so its carbon leaves as CO₂.
- He later restated it: part of the sugar is consumed as fuel for the building process, and that part leaves as CO₂. This is correct. He also assumed that mitochondria build the new cell. The agent corrected this: mitochondria are the power plant that burns sugar into CO₂ and water and makes ATP, and building happens elsewhere in the cell.
- He predicted *fewer* cells from the same sugar when yeast makes ethanol, because less energy is obtained per sugar. This is correct.

- He restated the energy split: part of the sugar becomes ATP because building new cells needs ATP. This is right. The agent added one nuance: sugar is used directly as building material (its carbon), and ATP supplies the energy to assemble it.

### Step 2 — How does a population of cells grow? (done)

**Explained so far:**

- Doubling means multiplying by 2 for each doubling time, so N = 2^(number of doublings).
- The worked example: 12 doublings in 24 hours gives 4,096 cells.
- Unlimited growth is impossible. Within about 10 days, one cell's descendants would outweigh the Earth. This is the agent's rough estimate, assuming a wet mass of about 60 picograms per cell.

**Jakob's own statements:**

- He recognised the growth as exponential and counted 12 doublings in 24 hours on his own. He was unsure whether the result is 2^12 or 12^2. The agent confirmed 2^12.
- Asked to write the growth as one line of code, he asked the agent to show it. The agent built it up: `cells = N0 * 2 ** (t / td)`. Jakob has not yet stated it himself, so revisit it lightly later.
- He said exponential growth stops because the sugar runs out. This is right for a simple batch. The agent added other possible limiting factors: oxygen, other nutrients, and toxic by-products such as ethanol.

### Step 3 — Why does growth stop, and how much yeast results? (done)

**Explained so far:**

- The limiting factor is whatever runs out first.
- Yield is roughly a fixed amount of yeast per gram of sugar: about 0.5 g/g with plenty of oxygen. The value is approximate and not yet sourced.
- Worked example: 20 g of sugar gives about 10 g of yeast.
- Two independent dials: speed (doubling time) sets *when*, and sugar × yield sets *how much*. The agent said reality has a twist here, to come in step 5; this is the withheld surprise.

**Jakob's own statements:**

- He said the growth formula makes sense once he saw it.
- He predicted that twice-as-fast growth gives the same final amount of yeast, reached sooner. He hesitated towards "less". The same amount is correct for the simple model.
- He asked why yeast makes ethanol if ethanol is toxic to it. The agent's partial answer: without oxygen, ethanol is the only way to get energy, and yeast tolerates ethanol better than its competitors. The fuller evolutionary answer is parked because it touches the withheld surprise.

### Step 4 — The first simulator (toy reviewed; reality comparison continues in step 5)

**Jakob's own statements:**

- He predicted that yeast rises exponentially (correct) and that sugar falls "logarithmically or negative-exponentially". The agent corrected this: sugar is the upside-down mirror of yeast. It falls slowly at first, then faster and faster, and crashes at the end.
- He assumed a constant sugar cost per unit of yeast, which is the fixed yield. This is correct.

**Explained so far:**

- In the last doubling time, the yeast eats as much sugar as in all earlier doublings combined.
- The simple model stops abruptly when the sugar runs out. Real cultures bend more smoothly; why is a later question.

**Increment (agreed: the agent writes it, Jakob reviews it; built 2026-09-24):**

- An exploratory loop in `explorations/` that tracks yeast and sugar.
- Illustrative numbers, not sourced: doubling time 2 h, yield 0.5 g/g, 20 g sugar, 0.1 g of yeast at the start.
- Independent checks: the final yeast should be about 10.1 g, and the sugar should run out after about 13 h.

- `explorations/001_batch_growth.py` is built and runs. Both independent checks match: 10.10 g of final yeast, and the sugar is gone at 13.32 h.
- Jakob reviewed the loop and correctly identified the `min(...)` line as the one that stops growth when the sugar is gone. He thought the sugar tapers through tiny numbers. The agent clarified that it hits exactly zero in one step, which causes the sharp corner. The `min` is where the "full speed until the sugar is gone" assumption lives in the code. Real cells slow down as sugar becomes scarce; this is a candidate later step, uptake kinetics.
- Jakob predicted that halving the doubling time (2 h to 1 h) gives the same final yeast, with the sugar gone in half the time. He ran the loop himself and it confirmed both: 10.10 g, and 6.66 h instead of 13.32 h. His step 3 prediction now holds without the earlier hesitation. He has not yet explained *why* the time halves (the number of doublings, 6.66, is fixed by the sugar and the yield, and only the time per doubling changed). Asked for the reason, he said it was already established and did not want to restate it; the agent did not press.
- He saw that the sugar corner is sharper with faster growth (correct), reasoning that more yeast eats more sugar. The agent refined this: both runs end with the same yeast, but at a 1 h doubling time each gram of yeast consumes sugar twice as fast, so the whole curve is compressed into half the time.
- This confirms the code matches the model. It says nothing about whether real yeast behaves this way; that is step 5.

**Side questions answered:**

- **What happens when the sugar runs out?** **Correction from step 5:** growth need not stop if another usable carbon source remains and conditions permit its use. The earlier explanation below assumed no such source. Yeast doesn't die immediately. It enters the **stationary phase**: it stops dividing, lives on internal reserves, and becomes more stress-resistant. It can survive for a long time, and it resumes growing after a delay if sugar is added. The classic batch phases are **lag, exponential, stationary, and death**. Dried baker's yeast is an extreme form of this dormancy.
- **Logarithmic versus exponential:** the logarithm is the inverse of the exponential. It answers "how many doublings to get this big?": log₂(4096) = 12. Logarithmic growth gets slower and slower. On a log-scale plot, exponential growth becomes a straight line.

### Step 5 — Comparing with real growth (consolidated 2026-09-25; low-sugar gap open)

**Jakob's own statements and review:**

- Predicted that more sugar would let growth continue longer, and that sufficient oxygen meant no ethanol. This followed the toy and the earlier incomplete explanation; the agent corrected the oxygen-only account.
- Suggested supplying sugar "Over time?" to avoid accumulation. This introduced fed-batch conceptually; feed-rate limits remain deferred.
- Asked repeatedly why abundant sugar lowers yield, distinguishing this from oxygen shortage. After the protein-machinery versus sugar-efficiency explanation, said "Now I get it" and asked how cells detect abundance.
- Asked whether the response is "pre-programmed in its DNA"; confirmed the distinction between inherited response machinery and a changing cellular state with "Yup".
- Restated the Crabtree effect: "too much sugar makes the cell also use fermentation ... because of the abundance". The agent confirmed, qualifying that this means abundant enough to trigger the behaviour, not necessarily harmful sugar concentrations.
- Viewed Figure 1 of Ji et al. after the remote image failed and a direct attachment was provided. Correctly interpreted the later phase: "It consumes its own previous output" (ethanol). Identified ethanol as the missing tracked substance without needing an elementary check.
- Chose to learn the biological switch before examining numerical parameters. Said "I guess it matters" about the adaptation period, then independently asked whether nitrogen and other inputs need tracking. This is interest in model scope, not acceptance of a specific delay or nutrient model.
- Asked about yeast extract and described feeding processed yeast to yeast as "Cannibalism?"; the agent distinguished nutrient recycling from engulfing live cells.

- Asked whether the cells visibly pause between glucose running out and ethanol starting to fall in Figure 1, he said "no visible pause". The agent's reading largely agreed: there is no clear plateau in the cell curve. At most there is a one- to two-point shoulder at the ethanol peak, which is within what the resolution and scatter allow. The dominant feature is the large drop in growth rate after the switch, not a delay.

- Chose to model the Crabtree mechanism rather than one fixed condition: "model the mechanism, no? The Crabtree effect is real."

**Explained, not independently demonstrated or accepted as a model:**

- Growth rate, yield per gram of sugar, and total final yeast are different quantities. Abundant sugar can support fast growth with lower yield; a lower yield need not mean less total yeast.
- Crabtree effect: aerobic ethanol production at abundant glucose. A protein-allocation trade-off helps explain it: fermentation uses more sugar but can require less enzyme machinery for a given ATP production rate. This is a supported explanatory account, not a conscious choice or a complete universal mechanism.
- A qualitative sugar/oxygen matrix. Oxygen sufficiency is relative to demand, and there is no universal ranking of growth speeds across four boxes.
- Ethanol retains usable chemical energy and carbon. Respiration can extract more energy; breaking bonds alone costs energy, and the net reaction determines energy release. CO₂ and water are oxidised end products in this context; restoring fuel from them requires an energy input.
- Glucose repression, the diauxic shift, and respiratory growth on ethanol. Changing gene activity produces messenger RNA, which ribosomes use to build enzymes; protein abundance and activity change without changing the DNA. ADH2 was introduced as one example, not the entire switch.
- Nitrogen for proteins and nucleic acids; other nutrient requirements. Tracking a nutrient is distinct from assuming it remains sufficient. Nitrogen depletion could prevent further growth even with ethanol left.
- Yeast extract as soluble material from disrupted yeast; peptone and yeast extract make the medium chemically complex. (Correction: the batch medium has yeast extract only; the peptone was in the preculture.) Exact nutrient composition cannot be inferred from their total mass alone. No quantitative nutrient composition has been adopted.
- Contamination: other organisms could compete or alter products. The paper reports medium sterilisation, but this is not proof of exhaustive contamination checks. The toy contains only one population.
- Wine was an analogy, not a new project direction: ordinary storage is not the continuously aerated experiment. Ethanol consumption requires suitable living yeast and oxygen; air exposure can also enable spoilage. Sugar respiration has been studied for alcohol reduction, with flavour and oxidation trade-offs. Jakob explicitly said he is not interested in winemaking per se and returned to the main thread.

**Figure interpretation and limits:**

- Ji et al. Figure 1: circles = cells, left logarithmic axis; triangles = glucose and squares = ethanol, right linear axis. Time is in hours. The agent initially swapped glucose/ethanol symbols and corrected this when attaching the actual figure. Do not repeat that error.
- The qualitative comparison reveals ethanol production and continued growth after glucose depletion, neither represented in the toy. There has been no digitisation, parameter fit, numerical overlay, or validation of an extended model.
- The paper's unusually high fitted growth-rate values still need cross-checking. Glucose-stage yield must not be treated as whole-run yield when ethanol is subsequently consumed.

**Proposals awaiting agreement:**

- **Bottleneck increment (proposed 2026-09-24):** an exploratory `explorations/002_…` using the respiratory-bottleneck idea (Sonnleitner & Käppeli 1986). Sugar uptake depends on the current sugar concentration. Respiration has a maximum capacity per cell, and uptake beyond that capacity overflows to ethanol at a lower yield. A sharp switch to slower ethanol growth follows once the glucose is gone.
  - **Assumptions:** sufficient dissolved oxygen and nutrients, perfect mixing, no switch delay.
  - **Parameters:** need research first, and the transfer between strains must be justified or labelled.
  - **Parameter research (2026-09-24, in progress):**
    - The original Sonnleitner & Käppeli paper is paywalled, and its parameter table has not been found in an open source.
    - Postma et al. 1989 (abstract only) gives a respiratory yield of 0.50 g/g and a fermentation onset between 0.30 and 0.38 h⁻¹ growth rate, for a different strain, in a chemostat.
    - Postma et al. dispute that limited respiratory capacity is the *cause*. The agent therefore proposed a mechanism-neutral framing: a threshold on the sugar uptake rate, above which the excess goes to ethanol. This uses the same mathematics without claiming why the threshold exists. It awaits Jakob's decision.
    - Parameters still missing: the maximum uptake rate, and how uptake slows at low sugar.
    - Ji's Figure 2 must not be used for fitting, because it is the independent test.
  - **Mechanism research (2026-09-24):** Jakob asked how overflow actually works in *S. cerevisiae*. The open literature (see `SOURCES.md`) indicates:
    - **Established:** ethanol production rises with the sugar uptake rate above a strain-dependent threshold. Slowing uptake genetically makes *S. cerevisiae* fully respiratory even at high glucose (Otterstedt 2004).
    - **S. cerevisiae specifically:** besides the immediate short-term effect, high glucose *represses* respiratory machinery over time (the long-term effect, or glucose repression). The threshold may therefore not be constant during a batch.
    - **Unsettled:** *why* the threshold exists. Four competing explanations are recorded in `SOURCES.md`.
    - **Agent recommendation:** first model a constant uptake threshold and test it against Ji's Figure 2. If the steep yield drop is not reproduced, glucose repression becomes the prime candidate for the next increment. This awaits Jakob's decision.
  - **Jakob's choice (2026-09-24):** include glucose repression from the start ("Let's go for glucose repression!"). The agent had recommended a constant threshold first.
    - **Proposed representation:** a tracked respiratory-capacity quantity that sets the overflow threshold. It declines while sugar is high and recovers once sugar is gone.
    - **Expected:** a lower yield at high starting sugar, because exposure lasts longer.
    - **Consistency check:** recovery must not create a visible pause, because Figure 1 shows none.
    - **Proposed evidence split (awaiting Jakob's agreement):** calibrate only on Ji's 40 g/L time course (Figure 1). Predict the 1, 5, 10, and 25 g/L levels and compare them with Figure 2 without tuning. Repression is switchable, so the constant-threshold version remains available as a comparison.
    - **Next:** parameter research, including the repression and recovery rates.
  - **Evidence split agreed by Jakob (2026-09-24):** calibrate on the 40 g/L run, test on 1, 5, 10, and 25 g/L, with repression switchable.
  - **Parameter proposal (2026-09-24, awaiting acceptance):**
    - **From literature, other strains:**
      - respiratory yield 0.50 g/g (Postma)
      - fermentative biomass yield ~0.10 g/g (Verduyn, anaerobic)
      - glucose affinity ~0.1 g/L (Verduyn)
      - initial overflow threshold ~0.8 g/g/h (inferred from Postma)
    - **Derived:** ethanol ≤ 0.51 g/g (stoichiometry).
    - **Calibrated on 40 g/L only:**
      - maximum sugar uptake rate
      - repression rate
      - recovery rate
      - repressed threshold floor
      - ethanol-phase growth rate and yield
    - **Identifiability risk:** one time course may not pin down both the repression and recovery rates.
    - **Finding:** Ji's preculture (20 g/L glucose, late exponential) means the cells probably start repressed. The yield trend may then reflect *recovery* during low-sugar runs more than repression building up. This changes the explanation the model offers, and should be discussed.
  - **Built (2026-09-24), after Jakob accepted the parameters, including "starts repressed":** `explorations/002_overflow_repression.py`, with Figure 1 digitised into `explorations/data/`. Results are in [the review](reviews/2026-09-24-overflow-repression.md):
    - the calibration fit is rough
    - the test gets the trend direction right, but the magnitude is far off
    - the recovery rate goes to its upper bound, so there is no memory
    - the fixed literature yields cannot reproduce Ji's measured yield pairs, whatever the model structure

    Jakob has not yet reviewed these results.
  - **Round 2 (2026-09-24):** asked what the agent would do, Jakob agreed to investigate yeast extract first.
    - The carbon balance supports extra carbon.
    - The model with yeast extract (`003`) improved cell yields only slightly and made ethanol overshoot.
    - The main misfit is the glucose tail (uptake kinetics).
    - Next proposal: calibrate KS. Not yet agreed.
  - **Round 3 (2026-09-24):** Jakob asked what KS is. The agent explained it as the half-speed sugar level of uptake, using the Monod equation, and linked it to his step 4 "tiny number" intuition. Jakob has not restated it yet.
    - The calibrated KS (8–14 g/L) fits the literature for low-affinity transporters.
    - The test fits at 10–40 g/L. At 1–5 g/L the failure flips: the model makes too little ethanol.
    - Repression worsens the low-sugar prediction.
    - Low sugar is the regime fed-batch depends on.
  - **Round 4 (2026-09-24):**
    - Jakob chose to solve the low-sugar problem before fed-batch ("we have to solve at low sugar first").
    - A second dataset (the compilation, chemostat and 8 g/L batch) confirmed strong overflow at low sugar in batch, and high-affinity respiratory growth in chemostats.
    - Jakob agreed to link affinity to repression (`005`). This improved 5 g/L and fits the chemostat, but not 1 g/L or the 8 g/L batch.
    - The next hypothesis is two states with different speeds.
  - **Round 5 (2026-09-24):** Jakob chose to try the two-state version (fast transporters, slow respiration) instead of consolidating. It did not fix the low-sugar failure. The hypothesis is falsified as implemented. The agent recommends consolidating and looking for better low-sugar data.
  - **Independent test:** whether Ji's Figure 2 trend (lower yield at higher starting sugar, dropping steeply between 1 and 5 g/L) emerges without fitting. Failure would be a finding, not a reason to tune.

- Explore a two-stage glucose/ethanol model under sufficient oxygen and other nutrients. A sharp switch would be an explicit simplification; a dynamic adaptation mechanism would need evidence and a defined purpose.
- The agent recommended keeping nitrogen sufficient initially and considering nitrogen limitation later. Jakob has not accepted that scope or an implementation increment.
- No simulator code or accepted scientific model changed during this session.

### Step 5 — consolidation (2026-09-25)

**Agent's summary of what step 5 taught. Jakob has not yet confirmed it; ask him to challenge or restate it.**

1. **Overflow (the Crabtree effect).** Above a certain sugar uptake rate, yeast sends the excess to ethanol even with oxygen present. The trigger is *how fast* sugar flows in; why the threshold exists is still debated.
2. **Glucose repression.** High sugar switches off respiratory machinery. Cells carry a history, so the starting culture matters.
3. **Uptake kinetics.** KS is the half-speed sugar level. Yeast changes its transporters with its situation: low-affinity at high sugar (KS ≈ 10 g/L) and high-affinity at low sugar (KS ≈ 0.3 g/L).
4. **Chemostat versus batch.** A chemostat holds growth steady at low sugar, which reveals clean thresholds. A batch sweeps through changing conditions. The same yeast can look different in each.
5. **Complex media.** Yeast extract adds carbon. A carbon balance showed Ji's yields were impossible from glucose alone.
6. **Method.** Keep calibration and test data apart. Never tune to the test. Distrust transferred parameters, as KS = 0.1 g/L showed. A failed prediction is information. Each added parameter makes a good fit mean less.
7. **Where it stands.** The model works for 10–40 g/L batches and for the chemostat. It fails at low starting sugar, and that is exactly the fed-batch regime, so better low-sugar data come first.

The model as it stands is described in [model/batch-overflow.md](model/batch-overflow.md).

### Next goal — fed-batch (started 2026-09-25)

- Jakob accepted the reframing that fed-batch mostly runs adapted cells at low sugar, which is closer to the chemostat. The low-sugar batch transient stays open.
- **Prediction (the exponential-feed question deferred since the start):** Jakob said oxygen demand grows exponentially with the cells until it outruns what the vessel can supply ("even a whole room wouldn't supply enough"). **Correct.** The agent added:
  - once supply falls short, dissolved oxygen falls to near zero
  - cells can no longer respire all the sugar, so they ferment: CO₂ out exceeds O₂ in, and the yield falls
  - the late phase of the fed-batch dataset shows exactly that signature
  - a bigger vessel does not automatically supply more oxygen per litre, which is a scale-up issue for later
  - the standard fix is to stop increasing the feed at the oxygen limit

- **Fed-batch prediction (2026-09-25):** Jakob agreed to build it without an oxygen limit.
  - Gas exchange is well predicted from 20 to 97 h, with nothing fitted.
  - The late phase shows the predicted fermentation signature, confounded by a process change.
  - Biomass is about 30 % low mid-run, unresolved.
  - See [the review](reviews/2026-09-25-fed-batch.md).

- **Cell-level oxygen limit (2026-09-25):**
  - Jakob asked for other papers instead of emailing the authors. Jouhten et al. 2008 was found: a chemostat with 5 oxygen levels.
  - The test with nothing fitted confirmed the agent's pre-run expectation: the model is good when fully aerobic and fully anaerobic, and about 2× too much ethanol when oxygen-limited.
  - Lesson: fermenting while some oxygen is present yields more cells (implied 0.13–0.18 against 0.10). A plausible reason is the glycerol/redox cost that only applies without oxygen.

- **Oxygen-present yield (009, 2026-09-25):** calibrated on Jouhten, 0.174 g/g against 0.10 anaerobic. The Ji test now matches at 5–25 g/L and the yeast extract is no longer needed.
  - **Lesson:** the long low-sugar failure was mostly *one mis-transferred parameter*, an anaerobic yield used for aerobic overflow. It was not missing mechanism. Three mechanism additions failed where one better-sourced number succeeded.

## Parked questions

- **Why is ethanol, specifically, the product when yeast ferments?** Jakob suspects a chemical logic and is right. It needs some groundwork on how sugar is broken down. (Raised 2026-09-24.)
- **Why does yeast make ethanol if it harms the yeast itself?** This is the evolutionary angle. The machinery/efficiency trade-off has now been discussed, but ethanol toxicity, ecological competition, and the evolutionary argument have not been fully resolved. Parts of the explanation are debated, so use sources. (Raised 2026-09-24.)
