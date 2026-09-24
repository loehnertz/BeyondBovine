# Project state

**Last updated:** 2026-09-24

This file is a navigation aid. See [decision 0002](decisions/0002-project-records.md) for how project records work.

## What exists

- **Project intent:** `docs/IDEA.md`.
- **Working agreement:** `AGENTS.md`, with `CLAUDE.md` as a symlink to it.
- **Decisions:** [0001](decisions/0001-python-engine.md) (Python engine and backend), [0002](decisions/0002-project-records.md) (project records), and [0003](decisions/0003-explanatory-3d.md) (early 3D explains the science).
- **Sources:** `docs/SOURCES.md`. It is empty for now.
- **No code and no model yet.**

## Jakob has reviewed and decided

- **Technology stack.** Jakob reviewed the options and chose Python for the engine and the backend, in a client–server architecture ([0001](decisions/0001-python-engine.md)).
- **Documentation structure.** Jakob approved it with his own refinements ([0002](decisions/0002-project-records.md)).
- **Purpose of early 3D.** Early 3D consists of explanatory views on one scale, from the equipment through the broth to the cell. Each view is built after the science question it explains ([0003](decisions/0003-explanatory-3d.md)).

No scientific content has been discussed in depth yet. Jakob has not confirmed understanding of any scientific topic.

## Provisional: agent suggestions not yet accepted

- **Engine design.** The engine should be a standalone library behind a thin server. Runs should use explicit step-by-step state (advance, pause, intervene, resume) so that interventions can happen during a run.
- **Frontend.** TypeScript with Three.js or React Three Fiber. The frontend stack is still open.
- **Agent's initial view of the project.** These are opinions and have not been decided:
  - Public process data is likely to be scarce, casein-specific data especially.
  - A single well-mixed model can produce scale-up limits from oxygen transfer and heat removal. Mixing gradients need spatial detail.

## Open questions

- **Current topic.** Jakob chose to start with this question: in a fed-batch run, what limits the feed rate, and what happens beyond that limit? The discussion paused to settle the stack and the records first.
- **Host organism.** The agent recommended *S. cerevisiae*, glucose-limited. The alternatives are *E. coli*, *Pichia pastoris*, and filamentous fungi. This has not been discussed.
- **First simplification.** The agent proposed a respiration-only model that flags the ethanol-overflow regime as outside its validity. This has not been discussed.
- **Two prediction questions for Jakob.** They are unanswered, and the agent has deliberately not given its reasoning yet.
  1. With a constant feed rate, once sugar is consumed as fast as it arrives, how do the growth rate and dissolved oxygen change over time?
  2. With an exponentially increasing feed, what happens to dissolved oxygen, and what ends that phase of the run?

## Proposed next step

Resume the fed-batch question at Jakob's pace. Start with the host-organism choice and Jakob's predictions. Build nothing until the increment is agreed.
