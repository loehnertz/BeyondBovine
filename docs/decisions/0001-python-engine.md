# 0001 — Python for the simulation engine and backend

**Status:** Accepted by Jakob, 2026-09-24

## Context

The simulator needs to solve dynamic process models, which are typically stiff: dissolved oxygen changes over seconds while biomass changes over hours. Its model code must be readable enough for Jakob to audit, and the project needs scientific tooling around the model for plotting, parameter fitting, and sensitivity analysis.

Jakob chose a client–server architecture: server software performs the simulation and numerical work, and a separate frontend presents it. Both run locally for now.

Jakob is most fluent in Kotlin/Java, equally fluent in Python, and interested in but not fluent in Rust.

## Decision

Use Python for the simulation engine and the backend service.

## Alternatives considered

- **Kotlin/JVM.** Jakob's strongest language. Rejected because of ecosystem fit. As far as the agent knows, Hipparchus has non-stiff ODE integrators but no implicit stiff solvers, and Kotlin scientific libraries such as KMath remain experimental. Parameter fitting and sensitivity tooling are thin, and published bioprocess model code is rarely written for the JVM. This is the agent's assessment from general knowledge, not a systematic survey.
- **Rust.** Fast, and it can target WebAssembly. Rejected for now because its ODE ecosystem is younger, model code sits further from the equations, and learning it would compete with learning the science. It remains an option for measured performance problems, called from Python through PyO3.
- **Julia.** Arguably the strongest modelling tooling, including DifferentialEquations.jl and ModelingToolkit. Rejected because it is a new language and awkward to deploy.
- **TypeScript only (in the browser).** Simplest deployment and most immediate interaction. Rejected because the browser has no mature stiff-solver or fitting ecosystem.
- **MATLAB.** Historically common in bioprocess engineering. Rejected because it is poorly suited to server software. Reading MATLAB models from papers remains a useful skill.

## Consequences

- SciPy provides stiff solvers such as BDF, Radau, and LSODA. LSODA wraps ODEPACK.
- Python makes sloppy model code easy to write. The engine should use type hints, handle units explicitly, and expose a clear interface.
- These points are **not decided by this record**:
  - the frontend stack
  - the protocol between frontend and backend
  - the agent's suggestions that the engine be a standalone library behind a thin server, and that runs advance step by step with explicit state (advance, pause, intervene, resume)
