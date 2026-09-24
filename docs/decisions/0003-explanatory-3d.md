# 0003 — Early 3D explains the science

**Status:** Accepted by Jakob, 2026-09-24

## Context

Jakob does not yet know the biology or the equipment of fermentation. He wants the early 3D work to help him understand the science, not to be a full control UI for the simulator. A control UI is still wanted eventually, but it is not the first priority.

## Decision

Early 3D consists of explanatory views on a single scale, from the equipment down to the cell:

1. **Equipment:** the vessel, stirrer, air inlet, feed, probes, cooling, and the inputs and outputs of the process.
2. **Broth:** oxygen moving from air bubbles into the liquid and on to the cells.
3. **Cell:** what happens to sugar inside a cell. For example, whether the cell respires it or ferments it.
4. **Later, protein production:** from gene to secreted protein.

The views stay connected by zooming, so that a quantity measured in the tank can be understood as the sum of what happens in many cells.

## Rules

- These views are **explanatory illustrations** in the sense of IDEA.md §5, and they are labelled as such. They are not computed results.
- "Molecular level" means schematic compartments and pathways. It does not mean atomistic detail, which would imply a molecular simulation the project does not have.
- Each view is built after the science question it explains has been discussed. It is not built in advance of that question.
- A view may later draw some of its values from the simulator. Those values must then be labelled as computed.

## Consequences

- The vessel and cell views become learning milestones and are no longer only presentation.
- The simulator's control UI is deferred. It is not dropped.
- The frontend technology is still open.
