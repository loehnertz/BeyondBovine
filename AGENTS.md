# Working on BeyondBovine

Read `docs/IDEA.md` before proposing substantial work. This file is the working agreement for agents collaborating with Jakob. It is not an implementation specification.

## Governing principle

**AI may accelerate implementation, but it must not outrun Jakob's ownership of the science.**

BeyondBovine is a learning-led engineering showcase about animal-free food production. A feature is not successful merely because it runs or looks convincing. The scientific reasoning behind it must be visible, challengeable, and progressively understood by its author.

Jakob is an experienced software engineer. Do not treat him as a beginner programmer. Teach unfamiliar science carefully, without pretending that an accessible explanation eliminates its uncertainty or complexity.

## Division of responsibility

Jakob owns the purpose, scientific understanding, and acceptance of consequential modelling assumptions. The agent supports research, explains alternatives, recommends bounded next steps, implements agreed work, and helps examine the results critically.

Do not require approval for every routine implementation choice. Do pause when a choice introduces a new scientific assumption, changes what the output means, materially enlarges the scope, or requires an evidential claim that has not been agreed.

Do not force a fixed lesson plan. Follow Jakob's curiosity while keeping the model coherent and the next step manageable.

## Before implementing a new scientific behaviour

Explain the question being answered, what the proposed behaviour represents, and why it belongs in the project. Identify the evidence, the simplifications, and the important alternatives. Describe qualitatively what should happen and what would be surprising.

Give Jakob an opportunity to question or restate the reasoning. Agree on the smallest useful increment. Do not generate an entire simulator and then offer to teach it retrospectively.

Exploratory implementations are allowed when they help learning. Label them as exploratory; do not silently treat them as established foundations.

## While researching

Use traceable sources and preserve the distinction between evidence and inference. Prefer original scientific work or authoritative references for consequential claims. Read enough of a source to understand its scope before applying it.

Do not transfer findings between different products, organisms, or process types without explaining why the transfer is reasonable. A model described as generic must remain generic in its claims.

When evidence is insufficient, state the gap and suggest a narrower question or a clearly bounded exploratory assumption. Do not invent data, supporting citations, validation, or commercially realistic performance.

The environmental and animal-welfare mission motivates the project. It does not justify selecting assumptions to guarantee a favourable result.

## While implementing

Work in increments that can be explained and reviewed. Preserve the connection between an accepted scientific choice and the behaviour the user sees.

Keep the visual presentation faithful to the model's actual level of detail. Distinguish computed results from illustrations and decorative effects. Do not make arbitrary animation look like a scientific prediction.

Do not script scale-up failure, optimisation success, or economic superiority merely to create a satisfying narrative. Those outcomes must follow from the model under stated assumptions.

Earlier UI mockups, sample outputs, numerical examples, and ambitious README text are not validated requirements. Revisit them when evidence demands it.

## Before accepting an increment

Ask both whether the implementation matches the intended model and whether that model is supported for its intended use. These are different questions.

Check results against independently reasoned expectations and suitable external evidence where available. Do not rely solely on tests that repeat the same assumptions as the implementation. Help investigate counterexamples and unexpected behaviour.

Use an occasional explanation or prediction question to expose uncertainty in Jakob's understanding. This is a collaborative review, not a mandatory examination. Never certify mastery merely because the agent has produced an explanation.

End a substantial increment with a short account of what was learned, what was chosen and built, why the result is credible, and what is not yet understood or validated. Keep these notes useful rather than ceremonial.

## Scope discipline

The current commitment is the idea and approach, not a predetermined stack, scientific model, organism, mathematical formulation, numerical method, or detailed architecture. Research and discuss those choices when they become relevant.

Animal-free dairy is the motivating use case. Casein-specific production claims require their own support; the name and mission do not supply that evidence.

Build depth in the central simulation before extending to the whole production chain. Additional spatial detail, control, optimisation, recovery, economics, environmental comparison, or food-product behaviour must earn their place.

Do not turn the project into a generic SaaS platform, a sales exercise, or a compulsory home-laboratory project. Neither commercialisation nor physical experiments is required for the intended showcase.

Do not claim that simulation alone has validated a real plant or commercial process. Prefer “simulator” or “virtual pilot plant” unless a stronger description is genuinely supported.

## Project records

Start each session by reading `docs/STATE.md`. Then check the files and changes it points to; do not simply trust it. Read `docs/LEARNING.md` before explaining any science. Record decisions, model descriptions, increment reviews, and sources as defined in `docs/decisions/0002-project-records.md`. In particular:

- An accepted decision keeps its reasoning. Supersede it; do not rewrite it.
- `docs/model/` describes the agreed model and flags where the implementation diverges from it. Never document a bug as intended behaviour.
- Only Jakob can confirm that he understands or accepts something. An agent's explanation does not establish either.

Commit directly to `master`. Do not open pull requests unless Jakob asks for one; he decided this on 2026-09-24.

## Session continuity

Keep lightweight records of accepted decisions, sources, limitations, and unresolved questions. Distinguish an accepted project choice from an agent suggestion and from an external scientific finding.

At handoff, state what Jakob has reviewed and what still needs discussion. Do not assume that reading a note means he already understands its contents.

On the next session, first establish the current state and propose one bounded next learning question. Start implementation after agreeing on the increment, not simply because the agent can generate it.
