# Project state

**Last updated:** 2026-09-24

This file is a navigation aid. See [decision 0002](decisions/0002-project-records.md) for how project records work.

## What exists

- **Project intent:** `docs/IDEA.md`.
- **Working agreement:** `AGENTS.md`, with `CLAUDE.md` as a symlink to it.
- **Decisions:** [0001](decisions/0001-python-engine.md) (Python engine and backend), [0002](decisions/0002-project-records.md) (project records), [0003](decisions/0003-explanatory-3d.md) (early 3D explains the science), and [0004](decisions/0004-learning-record.md) (learning record).
- **Learning record:** [LEARNING.md](LEARNING.md). It holds the learning approach, the topics covered with Jakob's own statements, and parked questions.
- **Sources:** `docs/SOURCES.md`. Ji et al. Figure 1 has now been reviewed qualitatively with Jakob; supporting mechanism references and limitations are recorded there. No parameters have been adopted.
- **Exploration:** `explorations/001_batch_growth.py`. This is an exploratory toy batch model and not the engine. Jakob has reviewed the loop (see LEARNING.md, step 4).
- **Exploration:** `explorations/002_overflow_repression.py`, an overflow model with glucose repression calibrated on Ji et al. 40 g/L. Its test failed on magnitude; see [the review](reviews/2026-09-24-overflow-repression.md). Jakob has not yet reviewed it.
- **Model description:** [model/batch-overflow.md](model/batch-overflow.md). It is exploratory, with reference implementation `005`. It is supported for 10–40 g/L batch cultures and for the chemostat. It is not supported for low starting sugar.
- **No engine code yet.**

## Jakob has reviewed and decided

- **Technology stack.** Jakob reviewed the options and chose Python for the engine and the backend, in a client–server architecture ([0001](decisions/0001-python-engine.md)).
- **Documentation structure.** Jakob approved it with his own refinements ([0002](decisions/0002-project-records.md)).
- **Purpose of early 3D.** Early 3D consists of explanatory views on one scale, from the equipment through the broth to the cell. Each view is built after the science question it explains ([0003](decisions/0003-explanatory-3d.md)).

- **Learning approach.** Jakob tried the approach on the first topic, liked it, and asked for it to be documented ([0004](decisions/0004-learning-record.md), [LEARNING.md](LEARNING.md)).

Scientific learning has started; see [LEARNING.md](LEARNING.md) for what Jakob has stated himself.

## Provisional: agent suggestions not yet accepted

- **Engine design.** The engine should be a standalone library behind a thin server. Runs should use explicit step-by-step state (advance, pause, intervene, resume) so that interventions can happen during a run.
- **Frontend.** TypeScript with Three.js or React Three Fiber. The frontend stack is still open.
- **Agent's initial view of the project.** These are opinions and have not been decided:
  - Public process data is likely to be scarce, casein-specific data especially.
  - A single well-mixed model can produce scale-up limits from oxygen transfer and heat removal. Mixing gradients need spatial detail.

## Current goal

**First goal (proposed by the agent; Jakob started working on it and has not objected):** understand, predict, and simulate a **batch culture**, in which yeast grows on sugar until the sugar runs out. The goal is reached when Jakob:

- can explain it in his own words
- predicted the behaviour of a small simulator before it was built
- has compared the simulator with a published growth curve and can say where the simple model is wrong

**Steps:**

1. What is a fermentation? What goes in and what comes out? (done)
2. How does a population of cells grow? This covers exponential growth and doubling time. (done)
3. Why does growth stop? This covers the yield: roughly a fixed amount of yeast per gram of sugar. (done)
4. A first simulator: yeast and sugar updated step by step in Python (toy reviewed).
5. Compare the simulator with real data (qualitative comparison started; see LEARNING.md).

The organism is not yet formally chosen. Baker's yeast (*S. cerevisiae*) is the working example used while learning.

## Open questions

- **GitHub issues.** The agent advised against them for now. They may be useful later for concrete engineering tasks. If they are used, `STATE.md` should link to them rather than copy them. Jakob has not decided.
- **Fed-batch (deferred).** The question is what limits the feed rate in a fed-batch run, and what happens beyond that limit. It comes after the first goal. Two prediction questions posed earlier are also deferred, because they assume knowledge that has not been covered yet:
  1. With a constant feed rate, once sugar is consumed as fast as it arrives, how do the growth rate and dissolved oxygen change over time?
  2. With an exponentially increasing feed, what happens to dissolved oxygen, and what ends that phase of the run?
- **Host organism and agreed model scope** remain open beyond the existing exploratory toy.
- **Next scientific increment:** ethanol production/consumption, whether to represent adaptation, and whether to assume other nutrients sufficient. These are discussed proposals, not accepted model choices; see LEARNING.md.

## Proposed next step

Jakob reviews the cell-level oxygen limit (`explorations/008_oxygen_limited_cells.py`; [review](reviews/2026-09-25-oxygen-limited-cells.md)).

- Fully aerobic and fully anaerobic conditions are predicted well.
- Oxygen-limited conditions are not: about 2× too much ethanol and too little biomass.
- The implied fermentative yield when some oxygen is present is 0.13–0.18 g/g, against 0.10 without oxygen.

**Candidate next step (not agreed):** calibrate that yield on Jouhten, then test it on Ji Figure 2 and the fed-batch. After that, the vessel oxygen-supply part, which remains exploratory.
