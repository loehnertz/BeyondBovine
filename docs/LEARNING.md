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

### Step 1 — What happens when yeast grows on sugar? (done)

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

### Step 3 — Why does growth stop, and how much yeast results? (in progress)

**Explained so far:**

- The limiting factor is whatever runs out first.
- Yield is roughly a fixed amount of yeast per gram of sugar: about 0.5 g/g with plenty of oxygen. The value is approximate and not yet sourced.
- Worked example: 20 g of sugar gives about 10 g of yeast.

<details>
<summary>Withheld on purpose (for agents; spoiler for Jakob)</summary>

Yeast also makes ethanol *with* plenty of oxygen, when sugar is abundant. This is the Crabtree effect, or overflow metabolism. It is the surprise planned for step 5 of the first goal, when the batch model is compared with real data. It is also why fed-batch exists. Let Jakob discover it; do not reveal it earlier.
</details>

## Parked questions

- **Why is ethanol, specifically, the product when yeast ferments?** Jakob suspects a chemical logic and is right. It needs some groundwork on how sugar is broken down. (Raised 2026-09-24.)
