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

- End with one question, plainly worded. Do not use labels such as "Prediction:".
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

### Step 1 — What happens when yeast grows on sugar? (essentially done)

**Explained so far:**

- Sugar is both fuel and building material.
- The growth medium (the nutrients the yeast grows in).
- **Respiration** (with oxygen): sugar becomes new cells, CO₂, and water, and releases a lot of energy. Energy is carried by ATP. Heat is released.
- **Fermentation** (without oxygen): sugar becomes ethanol and CO₂, and releases little energy.
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

<details>
<summary>Withheld on purpose (for agents; spoiler for Jakob)</summary>

Yeast also makes ethanol *with* plenty of oxygen, when sugar is abundant. This is the Crabtree effect, or overflow metabolism. It is the surprise planned for step 5 of the first goal, when the batch model is compared with real data. It is also why fed-batch exists. Let Jakob discover it; do not reveal it earlier.
</details>

## Parked questions

- **Why is ethanol, specifically, the product when yeast ferments?** Jakob suspects a chemical logic and is right. It needs some groundwork on how sugar is broken down. (Raised 2026-09-24.)
