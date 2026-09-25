# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""EXPLORATORY: what yeast does when it cannot get enough oxygen (cell level), tested on Jouhten et al. 2008.

Oxygen-limit goal, step 1 (see docs/LEARNING.md). This is a learning model, not the engine.

Rule added (agreed with Jakob): respiration needs oxygen. The respired glucose flux is capped at
    q_resp <= q_O2_available / O2_PER_GLUCOSE_RESPIRED
where the oxygen needed per glucose respired (2.31 mol/mol) comes from the electron balance in 007,
checked against the van Hoek chemostat. Sugar beyond what respiration can handle is fermented,
with the 005 yields: Y_RED = 0.10 g cells/g and Y_ETOH = 0.45 g ethanol/g.

Test (nothing fitted): in a glucose-limited chemostat at D = 0.1 1/h, impose each condition's MEASURED
oxygen uptake as the cap. Steady state requires growth = D, so the model must predict glucose uptake,
ethanol production and biomass. Cells here are derepressed and far below the Crabtree threshold, so
oxygen is the only limit. Not represented: glycerol (made under oxygen shortage for redox balance),
maintenance, and the ergosterol/Tween supplement.

Run with:  uv run explorations/008_oxygen_limited_cells.py
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
MW_GLC, MW_ETOH = 180.16, 46.07
Y_OX, Y_RED, Y_ETOH = 0.48, 0.10, 0.45  # g/g, as in 005
O2_PER_GLC_RESP = 2.31  # mol O2 / mol glucose respired (electron balance, see 007)
D, S_IN = 0.10, 10.0  # 1/h, g/L glucose in the feed (Jouhten et al. methods)


def steady_state(our: float) -> tuple[float, float, float]:
    """Predicted glucose uptake (mmol/g/h), ethanol production (mmol/g/h) and biomass (g/L) at growth rate D."""
    q_resp_needed = D / Y_OX  # g/g/h if fully respiratory
    q_resp_cap = our / O2_PER_GLC_RESP * MW_GLC / 1000  # g/g/h that the oxygen allows
    q_resp = min(q_resp_needed, q_resp_cap)
    q_over = (D - Y_OX * q_resp) / Y_RED  # fermented glucose needed to still grow at D
    qs = q_resp + q_over
    return qs / MW_GLC * 1000, Y_ETOH * q_over / MW_ETOH * 1000, D * S_IN / qs


def implied_fermentative_yield(our: float, q_glc: float) -> float:
    """Diagnostic, not used by the model: the fermentative yield that would make growth = D with the measured rates."""
    q_resp = min(our / O2_PER_GLC_RESP, q_glc) * MW_GLC / 1000
    q_over = q_glc * MW_GLC / 1000 - q_resp
    return (D - Y_OX * q_resp) / q_over if q_over > 1e-6 else float("nan")


def main() -> None:
    lines = [l for l in open(HERE / "data" / "jouhten2008_oxygen_chemostat.csv") if not l.startswith("#")]
    rows = list(csv.DictReader(lines))
    print("O2 in gas | OUR | glucose uptake model vs data | ethanol model vs data | biomass model vs data | implied Y_RED")
    table = []
    for r in rows:
        our, qg, qe, x = float(r["OUR"]), float(r["q_glucose"]), float(r["q_ethanol"]), float(r["biomass_g_per_L"])
        mg, me, mx = steady_state(our)
        yr = implied_fermentative_yield(our, qg)
        table.append((float(r["o2_inlet_pct"]), our, mg, qg, me, qe, mx, x))
        print(f"  {r['o2_inlet_pct']:>5}% {r['culture']:>2} | {our:4.1f} | {mg:5.2f} vs {qg:5.2f} | {me:5.2f} vs {qe:5.2f} | "
              f"{mx:5.2f} vs {x:5.2f} | {yr:5.2f}")
    plot(np.array(table))


def plot(t: np.ndarray) -> None:
    ink, muted, grid, blue, orange = "#0b0b0b", "#52514e", "#e1e0d9", "#2a78d6", "#eb6834"
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    our_line = np.linspace(0, 3.0, 200)
    model = np.array([steady_state(o) for o in our_line])
    for ax, j_model, j_data, title, color in ((axes[0], 0, 3, "Glucose uptake (mmol/g/h)", blue),
                                              (axes[1], 1, 5, "Ethanol production (mmol/g/h)", orange),
                                              (axes[2], 2, 7, "Biomass (g/L)", blue)):
        ax.plot(our_line, model[:, j_model], color=color, linewidth=2, label="model (measured OUR imposed)")
        ax.plot(t[:, 1], t[:, j_data], "o", mfc="none", mec=ink, ms=6, label="Jouhten et al. 2008")
        ax.set_title(title, loc="left", color=ink, fontsize=10)
        ax.set_xlabel("Oxygen uptake allowed (mmol/g/h)", color=muted, fontsize=9)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted, labelsize=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        ax.legend(fontsize=7, frameon=False)
    fig.suptitle("TEST: oxygen-limited yeast in a chemostat (D = 0.1/h). Nothing fitted.", color=ink, fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "008_oxygen_limited_cells.png", dpi=140)


if __name__ == "__main__":
    main()
