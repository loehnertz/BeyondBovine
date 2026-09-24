# BeyondBovine

## Project brief

BeyondBovine is a personal research-engineering showcase: an interactive, visually compelling simulation of precision fermentation for animal-free food ingredients. It is intended to become a virtual pilot plant for exploring how a biological production process behaves, how it can be controlled, and what changes when it is scaled.

The project has two equally important outputs: a convincing scientific-engineering application, and an author who genuinely understands the science represented by it.

**Current stage:** the direction and working approach are chosen; the scientific scope and implementation are not yet fixed. Inspect the repository before assuming that any feature exists. Descriptions and mockups may express ambitions rather than completed capabilities.

Read this document alongside `AGENTS.md`. This brief captures project intent; `AGENTS.md` governs how an agent should collaborate with Jakob. New explicit decisions from Jakob take precedence over this brief. Earlier conversations, README examples, and UI mockups are not binding scientific specifications.

## 1. Why this exists

Jakob wants to help move food production away from reliance on animals, principally to reduce animal suffering and environmental harm. His interest is in making useful, appealing alternatives possible through science and engineering—not merely building software in a food-related industry.

Animal-free dairy, and initially the question of how to make convincing mozzarella, provided the starting point. The chosen project focuses further upstream: the production process that could supply a useful food ingredient. Casein is a motivating example, not yet a commitment to a scientifically justified casein-specific model.

This is not a commercial product, a startup-validation exercise, or an application built to acquire customers. There is no requirement for monetisation or a broad feature set. It is acceptable to invest deeply in a narrow, memorable experience because the purpose is understanding and demonstration.

The mission determines which questions matter. It must not predetermine their answers. An honest simulation may expose unattractive trade-offs, limits, or unfavourable scenarios. Those are valuable findings, not outcomes to hide.

## 2. Who is building it, and what it should demonstrate

Jakob has worked professionally as a software engineer since 2019. He enjoys cooking, is developing a serious interest in food science, and wants to add one or two substantial scientific domains to his existing engineering expertise.

His eventual career interest is hands-on engineering close to food R&D, fermentation, pilot plants, and production. He is particularly drawn to the idea of being an engineer inside a company that physically makes animal-free food—not simply implementing business software for that sector. He does not want a project-management role or to pretend that self-study has already made him a trained food scientist.

The showcase should support that direction: an experienced engineer who can understand a scientific problem, ask good questions, make defensible modelling decisions, and turn those decisions into a coherent working system.

A polished interface alone would not demonstrate this. Neither would an elaborate simulator that Jakob cannot explain. The strongest result combines substantive understanding, rigorous engineering, and an experience that makes the process intelligible to someone else.

## 3. The central learning agreement

**Jakob owns the scientific understanding and engineering judgement. Agentic AI handles most implementation work.**

He wants to build the project gradually while learning the science himself. The agents should accelerate construction and help investigate unfamiliar material, but they must not create an opaque system that he is expected to trust.

For each consequential part of the model, Jakob should progressively be able to explain:

- What it represents in the real process, and why it belongs in the simulation.
- What assumptions and evidence support it, and which alternatives were considered.
- What behaviour should be expected, what a suspicious result would look like, and how to investigate it.
- Where the model stops being a reliable representation, and what remains uncertain.

“Understand everything” means ownership of the scientific reasoning that determines the results, with enough numerical and software understanding to interrogate their implementation. It does not mean memorising every dependency or mastering all of biotechnology before writing the first feature.

Understanding can develop through small exploratory implementations as well as reading. A provisional experiment may help answer a question, provided it is identified as provisional and is reviewed before becoming an accepted part of the simulator.

The desired pace is deliberate, not artificially slow. Avoid both extremes: building months of unexplained functionality in advance, and requiring encyclopaedic mastery before making any progress.

## 4. The experience we want to build

The intended experience is a virtual pilot plant centred on a fermentation vessel.

A visitor should be able to follow a simulated production run, inspect what is happening, make meaningful process interventions, and see their consequences. They should be able to compare operating choices and eventually investigate how a change in scale affects the same process.

The central question is:

> What makes this process work, what constrains it, and why does changing an operating decision or the scale change the outcome?

The eventual experience should connect three views of the same process: the physical vessel, its changing state, and the decisions used to operate it. It should help people understand causality rather than merely watch charts update.

An important prospective demonstration is that a strategy that works under one set of conditions may perform differently under another. But the simulator must earn that behaviour. Do not script a large reactor to fail just because scale-up failure makes a good demonstration. The outcome should follow from the researched model and its assumptions.

## 5. The role of 3D and visual design

A compelling 3D presentation is part of the ambition, not an incidental extra. Jakob wants an impressive showcase and already has software experience he can bring to the visual side.

However, visual richness must not imply scientific resolution that the model does not possess. If the simulation treats the contents as uniform, the scientific display must not invent detailed concentration gradients. If a later model represents distinct regions, the display can show those regions while making the approximation clear.

Distinguish three kinds of visual content: computed results, explanatory illustrations, and decorative context. All can be useful, but viewers should not mistake one for another.

The design goal is not photorealism for its own sake. It is an experience where the appearance helps someone understand the model, identify a problem, or compare alternatives. A visitor should be able to ask, “Why does that part of the screen look like that?” and receive a defensible answer.

An earlier UI image is an aesthetic reference only. Its numbers, spatial effects, controls, labels, and apparent capabilities are not validated specifications.

## 6. Scope: the anchor and the open questions

The anchor is an interactive fermentation-process simulator for an animal-free food application. The intended emphasis is process behaviour, operation, control, and scale-up, with scientific visualisation exposing what the model actually represents.

The first meaningful milestone should be a small, coherent simulated production run that Jakob can explain and audit. It should contain at least one meaningful intervention with an understandable consequence. The precise scientific content of that milestone must follow research and discussion, not the desire to reproduce an ambitious mockup immediately.

The following decisions remain open:

- Which organism, product, and process make the best initial scientifically supportable case.
- What public evidence is available, and what level of realism that evidence can justify.
- Which behaviours to model first and which simplifying assumptions are acceptable.
- When more detailed spatial behaviour, control, or optimisation is worth introducing.
- How to judge whether each addition improves scientific usefulness rather than just complexity.

Do not select those answers implicitly while coding. In particular, a generic protein-production model must not acquire casein-specific claims simply because the project originated in a conversation about cheese.

## 7. Future directions, not current commitments

Possible later extensions include richer scale-up exploration, process optimisation, recovery and purification of the ingredient, resource use, process economics, and environmental comparisons. A connection from the ingredient to an actual food product could eventually make the mission more tangible.

These are options, not a six-module delivery promise. Add one only when it serves a question Jakob cares about and the evidence can support the required claims.

Keep the core simulator deep before making the project broad. A small number of thoroughly understood behaviours is more valuable than a whole virtual factory held together by unexamined assumptions.

Cost or environmental outputs would require their own defensible scope, evidence, and treatment of uncertainty. They must not be presented as authoritative consequences of a fermentation animation.

## 8. Scientific credibility

The project should be transparent about what it knows and how it knows it.

Research consequential choices using traceable scientific sources and authoritative references. Distinguish evidence from a particular experiment or process from assumptions made to construct the simulation. Keep enough provenance that a reviewer can follow an important claim back to its source and see whether the application is justified.

Simplification is expected. Undisclosed simplification is not. A model can be useful without describing every mechanism, provided its purpose and limits are explicit.

Two separate questions must be kept visible:

**Did we build the intended model correctly?** This concerns whether the implementation faithfully follows the model that was selected.

**Does that model adequately represent the process for the question being asked?** This concerns evidence about the real world. Agreement between an agent's code and that same agent's tests does not, by itself, settle this question.

Use independently reasoned expectations, appropriate external comparisons where available, and deliberate attempts to find counterexamples. Investigate unexpected results rather than immediately explaining them away or changing the model to make a demonstration look right.

Where evidence is missing, narrow the claim, reduce the ambition, or identify the behaviour as exploratory. Do not fill gaps with plausible-looking values or confident prose.

Describe the project as a simulator or virtual pilot plant. Do not present it as a validated digital twin of a real production facility without the real-world connection and evidence to support that description.

## 9. The learn–build–audit loop

Each substantial increment should follow a short cycle.

### Ask and investigate

Choose one worthwhile question about the process. Explain why it matters to the project and investigate the relevant science. Prefer a manageable question over a broad request to “learn fermentation”.

### Explain and choose

Present the concept, the plausible approaches, the evidence, and the important limitations. Help Jakob form an expectation about what should happen. Agree on a bounded next step and record any consequential assumption being accepted.

### Build and explore

Let the implementation agent carry out that step. Routine implementation choices can be delegated. New scientific assumptions or a significant expansion of scope should be brought back for discussion rather than silently introduced.

### Audit and consolidate

Examine whether the result matches the intended reasoning and whether that reasoning is itself defensible. Use a surprising result or a counterfactual question to test understanding. Record what was learned, what changed, why it is credible, and what remains unresolved.

Then select the next question. This cycle is the project roadmap: curiosity and evidence determine the next useful increment.

Do not turn the collaboration into compulsory quizzes or a rigid curriculum. Invite Jakob to explain or challenge important behaviour; use gaps in understanding to guide the next conversation. Completion of a feature is not automatically completion of the learning step.

## 10. Collaboration and decision-making

The agent should act as a research partner, tutor, implementation partner, and critical reviewer—not as an unquestioned scientific authority.

Jakob decides the goals, accepts consequential modelling choices, and determines whether a step is sufficiently understood to become the foundation for more work. The agent should bring recommendations rather than push every routine decision back to him.

Disagreement is useful. If a proposed feature cannot be justified, say so and offer a narrower way to explore the question. Do not optimise for agreeing with the mission, reproducing a previously suggested result, or making the project appear more advanced than it is.

Maintain lightweight records of sources, assumptions, decisions, unresolved questions, and learning progress. Their purpose is to preserve reasoning across agent sessions. Do not create a documentation system that becomes a project of its own.

## 11. What success looks like

Jakob can demonstrate the application and explain the causal story behind its behaviour. When something looks wrong, he can formulate an expectation, identify a questionable assumption or implementation, and investigate rather than merely ask the agent to fix it.

A technically knowledgeable visitor can inspect the project, understand its scope, trace important choices, and distinguish supported results from illustrative or exploratory content.

A non-specialist can see why the process matters and why operating and scaling it is an engineering problem.

The visible experience is memorable because it makes a real model understandable—not because it disguises uncertainty with a beautiful interface.

The professional story is: “I used my software-engineering experience and AI tools to investigate a scientific domain deeply, make explicit choices, and build something I can defend.” It is not: “An agent generated a simulator that looks scientific.”

## 12. Explicit non-goals

This is not an attempt to replace food scientists, claim laboratory validation without experiments, or predict the performance of every organism, protein, or industrial facility.

Owning laboratory equipment or conducting physical experiments is not a prerequisite. Public evidence and transparent simulation are the intended starting point. Collaboration with domain specialists would be valuable if it becomes available, but is not assumed.

Commercial application infrastructure, customer acquisition, generic assistant features, and maximum feature count are not objectives. AI is primarily a means of research and construction; it does not need to become a feature of the finished product.

Do not make the project impressive at the expense of its author's understanding.

## 13. Starting a new agent session

Read this brief and `AGENTS.md`, then inspect any existing project material. Separate what is implemented, what is supported by evidence, and what is merely proposed.

Begin by briefly restating the aim and identifying the most important unresolved scientific choice. Recommend a small first research-and-learning step, including what Jakob should understand afterwards and why it is a useful foundation.

Do not begin with a complete architecture, a large backlog, a chosen mathematical model, or a bulk implementation. First agree on the question being investigated. Then let research, understanding, and small validated advances shape the project.
