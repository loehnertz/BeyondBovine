# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""EXPLORATORY: yeast growing on sugar in a batch, as a simple loop.

A learning toy for step 4 of the first goal (see docs/LEARNING.md). It is not
part of the simulation engine.

Deliberate simplifications:
- One perfectly mixed litre.
- The yeast grows at full speed until the sugar is gone, then stops abruptly.
- The yield is fixed: plenty of oxygen, respiration only, no ethanol.
- No delay at the start and no dying cells.

The numbers are illustrative and not sourced. Step 5 compares them with real data.

Run with:  uv run explorations/001_batch_growth.py
"""

import math

import matplotlib.pyplot as plt

DOUBLING_TIME_H = 2.0  # hours for the yeast to double
YIELD_G_PER_G = 0.5  # grams of new yeast per gram of sugar consumed
SUGAR_START_G = 20.0  # grams of sugar in the litre at the start
YEAST_START_G = 0.1  # grams of yeast at the start
DT_H = 0.01  # time step, in hours
END_H = 18.0  # how long to simulate


def simulate() -> tuple[list[float], list[float], list[float]]:
    t, yeast, sugar = 0.0, YEAST_START_G, SUGAR_START_G
    times, yeasts, sugars = [t], [yeast], [sugar]
    while t < END_H:
        # Growth in one step: the yeast multiplies by 2 ** (dt / doubling time).
        wanted_growth = yeast * (2 ** (DT_H / DOUBLING_TIME_H) - 1)
        # It can't grow more than the remaining sugar allows.
        growth = min(wanted_growth, sugar * YIELD_G_PER_G)
        yeast += growth
        sugar -= growth / YIELD_G_PER_G
        t += DT_H
        times.append(t)
        yeasts.append(yeast)
        sugars.append(sugar)
    return times, yeasts, sugars


def check(times: list[float], yeasts: list[float], sugars: list[float]) -> None:
    """Compare the loop with answers worked out independently, without the loop."""
    expected_final_yeast = YEAST_START_G + YIELD_G_PER_G * SUGAR_START_G
    fold = expected_final_yeast / YEAST_START_G
    expected_end_h = DOUBLING_TIME_H * math.log2(fold)
    sugar_gone_h = next(t for t, s in zip(times, sugars) if s <= 1e-9)
    print(f"final yeast:     {yeasts[-1]:.2f} g   (expected {expected_final_yeast:.2f} g from the yield)")
    print(f"sugar gone at:   {sugar_gone_h:.2f} h   (expected {expected_end_h:.2f} h: "
          f"{fold:.0f}-fold growth = {math.log2(fold):.2f} doublings)")


def plot(times: list[float], yeasts: list[float], sugars: list[float]) -> None:
    ink, muted, grid = "#0b0b0b", "#52514e", "#e1e0d9"
    fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
    panels = [
        (axes[0], yeasts, "#2a78d6", "Yeast (g)", "linear"),
        (axes[1], sugars, "#eb6834", "Sugar (g)", "linear"),
        (axes[2], yeasts, "#2a78d6", "Yeast (g), log scale", "log"),
    ]
    for ax, values, color, title, scale in panels:
        ax.plot(times, values, color=color, linewidth=2)
        ax.set_yscale(scale)
        ax.set_title(title, loc="left", color=ink, fontsize=11)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
    axes[-1].set_xlabel("Time (hours)", color=muted)
    fig.suptitle("Batch culture: exploratory toy model, illustrative numbers", color=ink)
    fig.tight_layout()
    fig.savefig("explorations/001_batch_growth.png", dpi=150)


if __name__ == "__main__":
    times, yeasts, sugars = simulate()
    check(times, yeasts, sugars)
    plot(times, yeasts, sugars)
