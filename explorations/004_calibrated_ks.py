# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""EXPLORATORY: 003 plus KS (uptake half-speed point) calibrated instead of fixed.

Step 5 of the first goal (see docs/LEARNING.md). This is a learning model, not the engine.
Identical to 003_with_yeast_extract.py except that KS is calibrated on the 40 g/L run.
Why: with KS fixed at 0.1 g/L (Verduyn 1990, glucose-limited chemostat, where high-affinity
transporters dominate) the model cannot reproduce the glucose tail at 40 g/L. In high-glucose
batch, low-affinity transporters dominate: their half-speed points are about 9-18 g/L (Hxt1/3),
~1.8 g/L (Hxt2/4) and 0.2-0.4 g/L (Hxt6/7) (Reifenberger et al. 1997). That range is used as a
plausibility check on the fitted KS, not as a constraint. Caveat: in wild type at high glucose,
transport may not be what limits uptake (Elbing et al. 2004), so KS here is an effective value
for the whole uptake step, not a transporter constant.

Otherwise identical to 002_overflow_repression.py except for yeast extract (YE).

Why: a carbon balance on Ji et al.'s 40 g/L yields needs more carbon than the glucose supplies.
Ji's batch medium contains about 0.22 g yeast extract per g glucose (Table 1), and yeast extract
is about 0.43 g carbon per g (Schroeder-Kleeberg et al. 2025). See docs/reviews.

How YE is represented, as the simplest assumption and without claiming a mechanism: YE is
co-consumed with glucose in the ratio in which it was added, and each gram of YE consumed adds
Y_XYE grams of cells. Y_XYE is calibrated on the 40 g/L run only, together with the other
calibrated parameters.

What it represents, per gram of cells:
- Sugar uptake slows when sugar is scarce (qs = QS_MAX * S / (KS + S)).
- Uptake up to a threshold is respired, at a high yield. Uptake above the threshold
  overflows to ethanol, at a low yield. The model does not claim WHY the threshold
  exists; see docs/SOURCES.md for the competing explanations.
- Respiratory machinery R (0 = fully repressed, 1 = fully derepressed) sets the threshold.
  R recovers when sugar is low and is repressed when sugar is high. Ethanol can only be
  used as far as the machinery is back (R), and not while glucose is high.
- The cells start repressed (R0 = 0), because Ji et al. precultured them on 20 g/L glucose.

Deliberate simplifications: perfect mixing, enough oxygen and other nutrients, one
average cell, no lag, no death, no ethanol evaporation, no carry-over from the preculture.

Evidence split (agreed with Jakob): calibrate ONLY on Ji et al. Figure 1 (40 g/L), then
predict the glucose-phase yields at 1, 5, 10 and 25 g/L and compare with Figure 2.

Run with:  uv run explorations/004_calibrated_ks.py
"""

import csv
from dataclasses import dataclass, replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

HERE = Path(__file__).parent

# --- Fixed parameters: literature (other strains) or derived. See docs/SOURCES.md. ---
Y_OX = 0.50  # g cells / g glucose respired (Postma 1989, CBS 8066 chemostat)
Y_RED = 0.10  # g cells / g glucose fermented (Verduyn 1990, anaerobic chemostat)
Y_ETOH = 0.45  # g ethanol / g glucose fermented. Derived: 0.51 stoichiometric maximum, minus
#               the carbon that goes into 0.10 g of cells (assumed composition CH1.8O0.5N0.2).
KS_LITERATURE = 0.1  # g/L, from Verduyn 1990 (~0.55 mM). REPLACED here by a calibrated p.ks.
KE = 0.1  # g/L, the same for ethanol. ASSUMPTION: order of magnitude, borrowed from KS_LITERATURE.
QCRIT_MAX = 0.8  # g glucose / g cells / h, threshold when derepressed (inferred from Postma 1989)
K_REP = 1.0  # 1/h, repression rate. NOT SOURCED and not calibrated. It is not irrelevant:
#             together with k_rec it sets how much machinery survives while glucose is high.
#             Only the balance between the two is visible in one run.
R0 = 0.0  # starting machinery: fully repressed (Ji et al. preculture)

# Starting glucose level at which repression is half-active. NOT SOURCED: shown as a range.
KR_VALUES = (0.1, 0.5, 2.0)

# Ji et al. Table 1: yeast extract (g/L) for each starting glucose level (g/L).
YE0 = {1: 0.2, 5: 1.1, 10: 2.2, 25: 5.6, 40: 8.9}

# Ji et al. Figure 2, read from the image. RESERVED AS THE TEST: never used for fitting.
FIG2 = {1: (0.41, 0.22), 5: (0.26, 0.285), 10: (0.24, 0.31), 25: (0.215, 0.365), 40: (0.20, 0.40)}


@dataclass(frozen=True)
class Params:
    qs_max: float  # g glucose / g cells / h
    qcrit_min: float  # g glucose / g cells / h, threshold when fully repressed
    k_rec: float  # 1/h, recovery rate of the machinery
    qe_max: float  # g ethanol / g cells / h
    y_xe: float  # g cells / g ethanol
    kr: float  # g/L, see KR_VALUES
    repression: bool = True  # False: constant threshold, machinery always available
    y_xye: float = 0.0  # g cells / g yeast extract consumed
    yeast_extract: bool = True
    ye_ratio: float = 0.0  # g YE per g glucose in the medium; set per run in simulate()
    ks: float = KS_LITERATURE  # g/L, calibrated


def rates(p: Params, x: float, s: float, e: float, r: float, ye: float) -> tuple[float, ...]:
    s, e = max(s, 0.0), max(e, 0.0)
    g = s / (s + p.kr)  # how strongly glucose is signalling "repress" (0..1)
    avail = r if p.repression else 1.0
    qs = p.qs_max * s / (p.ks + s)
    qcrit = p.qcrit_min + avail * (QCRIT_MAX - p.qcrit_min) if p.repression else p.qcrit_min
    q_resp = min(qs, qcrit)  # respired part of the uptake
    q_over = qs - q_resp  # overflow part, fermented to ethanol
    qe = p.qe_max * e / (KE + e) * avail * (1 - g)  # ethanol use needs machinery and low glucose
    q_ye = qs * p.ye_ratio if ye > 0 else 0.0  # co-consumed with glucose, in the medium's ratio
    mu = Y_OX * q_resp + Y_RED * q_over + p.y_xe * qe + p.y_xye * q_ye
    dx = mu * x
    ds = -qs * x
    de = (Y_ETOH * q_over - qe) * x
    dr = (p.k_rec * (1 - r) * (1 - g) - K_REP * r * g) if p.repression else 0.0
    return dx, ds, de, dr, -q_ye * x


def simulate(p: Params, s0: float, x0: float, t_end: float, t_eval=None):
    ye0 = YE0[int(s0)] if p.yeast_extract else 0.0
    p = replace(p, ye_ratio=ye0 / s0)
    sol = solve_ivp(
        lambda t, y: rates(p, *y), (0, t_end), [x0, s0, 0.0, R0, ye0],
        t_eval=t_eval, max_step=0.05, rtol=1e-7, atol=1e-9,
    )
    return sol.t, sol.y


def glucose_phase_yields(p: Params, s0: float, x0: float) -> tuple[float, float]:
    """Ji's definition: cells and ethanol formed per gram of glucose, up to glucose exhaustion."""
    t, (x, s, e, _, _) = simulate(p, s0, x0, t_end=40.0)
    i = int(np.argmax(s < 0.01 * s0))  # first time 99 % of the glucose is gone
    return (x[i] - x0) / s0, e[i] / s0


def load_fig1() -> dict[str, np.ndarray]:
    lines = [l for l in open(HERE / "data" / "ji2016_fig1_40gL.csv") if not l.startswith("#")]
    rows = list(csv.DictReader(lines))
    return {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}


def calibrate(data: dict[str, np.ndarray], kr: float, repression: bool, yeast_extract: bool) -> Params:
    t = data["t_h"]

    def make(v) -> Params:
        return Params(*v[:5], kr=kr, repression=repression, yeast_extract=yeast_extract,
                      ks=v[5], y_xye=v[6] if yeast_extract else 0.0)

    def residuals(v):
        p = make(v)
        _, (x, s, e, _, _) = simulate(p, 40.0, data["cells_g_per_L"][0], t[-1], t_eval=t)
        if len(x) != len(t):
            return np.full(3 * len(t), 10.0)
        return np.concatenate([
            np.log(x) - np.log(data["cells_g_per_L"]),  # relative error on cells
            (s - data["glucose_g_per_L"]) / 10.0,  # ~0.2 g/L reading error scaled like the cells
            (e - data["ethanol_g_per_L"]) / 10.0,
        ])

    #         qs_max qcrit_min k_rec qe_max y_xe ks [y_xye]
    start = [2.0, 0.2, 1.0, 0.3, 0.4, 1.0] + ([0.3] if yeast_extract else [])
    lower = [0.2, 0.0, 0.01, 0.01, 0.05, 0.05] + ([0.0] if yeast_extract else [])
    upper = [10.0, QCRIT_MAX, 20.0, 3.0, 0.8, 30.0] + ([1.0] if yeast_extract else [])
    fit = least_squares(residuals, start, bounds=(lower, upper))
    return make(fit.x)


def main() -> None:
    data = load_fig1()
    x0 = data["cells_g_per_L"][0]  # same 5 % inoculum in every run
    models = {f"repression+YE, KR={kr}": calibrate(data, kr, True, True) for kr in KR_VALUES}
    models["constant+YE"] = calibrate(data, KR_VALUES[1], False, True)
    models["repression, no YE"] = calibrate(data, KR_VALUES[1], True, False)

    print("Calibrated on 40 g/L only:")
    for name, p in models.items():
        print(f"  {name:24s} qs_max={p.qs_max:.2f} qcrit_min={p.qcrit_min:.2f} "
              f"k_rec={p.k_rec:.2f} qe_max={p.qe_max:.2f} y_xe={p.y_xe:.2f} y_xye={p.y_xye:.2f} KS={p.ks:.2f}")

    print("\nTest: glucose-phase cell yield (g/g), model vs Ji Fig. 2")
    levels = sorted(FIG2)
    print("  S0      Ji  " + "  ".join(f"{n[:22]:>22s}" for n in models))
    table = {n: [glucose_phase_yields(p, s0, x0) for s0 in levels] for n, p in models.items()}
    for i, s0 in enumerate(levels):
        tag = "(calib.)" if s0 == 40 else ""
        print(f"  {s0:>3} {FIG2[s0][0]:6.2f}  " + "  ".join(f"{table[n][i][0]:22.2f}" for n in models) + f"  {tag}")
    print("\nTest: glucose-phase ethanol yield (g/g)")
    for i, s0 in enumerate(levels):
        print(f"  {s0:>3} {FIG2[s0][1]:6.2f}  " + "  ".join(f"{table[n][i][1]:22.2f}" for n in models))

    plot(data, models, table, levels)


def plot(data, models, table, levels) -> None:
    ink, muted, grid = "#0b0b0b", "#52514e", "#e1e0d9"
    main_name = "repression+YE, KR=0.5"
    colors = {main_name: "#2a78d6", "constant+YE": "#eb6834", "repression, no YE": "#a3a29c"}

    def style(ax, title):
        ax.set_title(title, loc="left", color=ink, fontsize=10)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted, labelsize=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    t = np.linspace(0, 26, 400)
    for ax, key, title, log in (
        (axes[0, 0], "cells_g_per_L", "Cells (g/L), log scale", True),
        (axes[0, 1], "glucose_g_per_L", "Glucose (g/L)", False),
        (axes[0, 2], "ethanol_g_per_L", "Ethanol (g/L)", False),
    ):
        idx = {"cells_g_per_L": 0, "glucose_g_per_L": 1, "ethanol_g_per_L": 2}[key]
        for name, color in colors.items():
            _, y = simulate(models[name], 40.0, data["cells_g_per_L"][0], 26, t_eval=t)
            ax.plot(t, y[idx], color=color, linewidth=2, label=f"model: {name}")
        ax.plot(data["t_h"], data[key], "o", mfc="none", mec=ink, ms=5, label="Ji et al. Fig. 1 (read from image)")
        if log:
            ax.set_yscale("log")
        style(ax, title)
        ax.set_xlabel("Time (h)", color=muted, fontsize=9)
    axes[0, 0].legend(fontsize=7, frameon=False, loc="lower right")

    for ax, j, title in ((axes[1, 0], 0, "Test: cell yield, glucose phase (g/g)"),
                         (axes[1, 1], 1, "Test: ethanol yield, glucose phase (g/g)")):
        kr_names = [n for n in models if n.startswith("repression+YE")]
        lo = [min(table[n][i][j] for n in kr_names) for i in range(len(levels))]
        hi = [max(table[n][i][j] for n in kr_names) for i in range(len(levels))]
        ax.fill_between(levels, lo, hi, color="#2a78d6", alpha=0.15, linewidth=0,
                        label="repression+YE, KR 0.1–2 g/L")
        for name, color in colors.items():
            ax.plot(levels, [v[j] for v in table[name]], color=color, linewidth=2, marker="o", ms=4,
                    label=f"model: {name}")
        ax.plot(levels, [FIG2[s][j] for s in levels], "^", mfc="none", mec=ink, ms=7,
                label="Ji et al. Fig. 2 (read from image)")
        ax.set_ylim(0, 0.55)
        style(ax, title)
        ax.set_xlabel("Starting glucose (g/L); 40 g/L was used for calibration", color=muted, fontsize=9)
    axes[1, 0].legend(fontsize=7, frameon=False, loc="upper right")

    _, y = simulate(models[main_name], 40.0, data["cells_g_per_L"][0], 26, t_eval=t)
    axes[1, 2].plot(t, y[3], color="#2a78d6", linewidth=2)
    axes[1, 2].set_ylim(-0.05, 1.05)
    style(axes[1, 2], "Respiratory machinery R, 40 g/L run (model only)")
    axes[1, 2].set_xlabel("Time (h)", color=muted, fontsize=9)

    fig.suptitle("Overflow + repression + yeast extract + calibrated KS: exploratory, calibrated on 40 g/L only",
                 color=ink, fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "004_calibrated_ks.png", dpi=140)


if __name__ == "__main__":
    main()
