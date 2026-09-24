# 0002 — How project records are structured

**Status:** Accepted by Jakob, 2026-09-24, together with the refinements from his review

## Context

This project must preserve four things separately:
- what is intended
- what was decided
- what currently works
- what can actually be justified

It must also preserve a fifth thing: what Jakob understands well enough to challenge. Documentation fails quietly in two ways. Records that were once true stop being true, and assumptions or implementation progress come to look like established science or understanding.

## Decision

### Documents

| Path | Kind | Purpose |
|---|---|---|
| `docs/IDEA.md` | Intent | Project intent. It may be ambitious and is not a claim about current capabilities. |
| `docs/STATE.md` | Handoff | Where the project stands and what comes next. |
| `docs/decisions/` | History | One short record for each consequential decision, whether technical or scientific. |
| `docs/model/` | Current state | The agreed model and its implementation status. |
| `docs/reviews/` | History | End-of-increment notes: what was learned, chosen, and built, why the result is credible, and what is not yet understood or validated. |
| `docs/sources.md` | Reference | References, each with a note on what it justifies and what its scope is. |

Create folders and files only when they are first needed.

### Rules

1. **History keeps its reasoning.** A proposed record can be edited during discussion. An accepted record keeps its substantive reasoning. Only status changes, links to a superseding record, and clearly marked corrections are allowed.
2. **Current state records uncertainty.**
   - `model/` describes the *agreed* model. It does not describe whatever the code happens to do.
   - It flags known gaps between the implementation and the agreed model. A bug must never be documented as intended behaviour.
   - It keeps four questions apart:
     - what we chose to represent
     - whether the implementation follows that choice (verification)
     - whether the model adequately represents reality for its intended use (validation)
     - whether Jakob has reviewed and accepted it
3. **Basis, applicability, and status are recorded separately.**
   - *Basis:* published evidence, our own derivation, or a deliberately chosen assumption.
   - *Applicability:* whether the source covers our scenario or whether we are extrapolating from it.
   - *Decision status:* proposed, accepted, or superseded.

   A one-line note is enough. For example: "published under different conditions; transfer is provisional; accepted as exploratory; not validated."
4. **Understanding is confirmed only by Jakob.** An agent explaining something does not establish that Jakob understands it or has approved it. Approving a provisional exploration is also different from claiming to understand it fully.
5. **Each project fact has one authoritative home.**
   - Documents link to each other instead of copying.
   - Parameter values live in a single data file with a unit and a source for each value.
   - A scientific claim may still draw on several sources, including conflicting ones.
   - A single home guarantees consistency, not correctness. The meaning, units, and applicability of each value still need independent review.
6. **Documentation changes with behaviour.** A commit that changes model behaviour also updates `model/`, and it adds a decision record when the change is consequential.
7. **`STATE.md` is a navigation aid, not an authority.**
   - It is updated at meaningful checkpoints and before handoff.
   - An open question persists until it is resolved or explicitly dropped.
   - At the start of a session, an agent reads it and then checks the files and changes it points to. The agent does not trust it blindly, and it does not audit the whole project each time.

### Explicit non-goals

- No documentation generators.
- No claim registries.
- No records for routine coding choices.

## Consequences

`AGENTS.md` points to this record so that every agent follows the structure without being told.

The verification and validation distinction follows general simulation practice. NASA-STD-7009 (Standard for Models and Simulations) and its handbook, for example, separate these questions. The decision-record format follows Michael Nygard, "Documenting Architecture Decisions", 2011.
