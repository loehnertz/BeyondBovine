# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""EXPLORATORY: overflow + repression + yeast extract, with uptake affinity that depends on repression.

Step 5 of the first goal (see docs/LEARNING.md and docs/reviews/2026-09-24-overflow-repression.md).
This is a learning model, not the engine.

Why this version: 004 fitted an uptake half-speed point KS of about 10 g/L to Ji's high-glucose
batch, while glucose-limited chemostats show cells respiring on only traces of glucose, which
needs high-affinity uptake. Yeast changes its transporters with its situation (Diderich 1999,
Walsh 1994). Agreed with Jakob: link affinity to the repression state R that the model already has.

    KS(R) = KS_HIGH_AFF * R + ks_low_aff * (1 - R)
    repressed cells (R = 0): low-affinity transporters; derepressed (R = 1): high-affinity.

Everything else as in 004. Additions for the chemostat: a dilution term (feed in, broth out).

Evidence split (agreed with Jakob):
- CALIBRATE on Ji et al. Figure 1 (40 g/L batch) + van Hoek 1998 chemostat (industrial baker's yeast).
- TEST, never fitted: Ji et al. Figure 2 (1-25 g/L yields) and the compiled 8 g/L batch.
Known compromise: Ji's strain (AFY) and van Hoek's (DS28911) are different industrial baker's
yeasts, so one parameter set describing both is an assumption.

Run with:  uv run explorations/005_state_dependent_uptake.py
"""

import csv
from dataclasses import dataclass, replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

HERE = Path(__file__).parent
MW_GLC, MW_ETOH = 180.16, 46.07  # g/mol

# --- Fixed: literature or derived (see docs/SOURCES.md) ---
Y_OX = 0.48  # g cells / g glucose respired (van Hoek 1998, 0.47-0.49 at D = 0.05-0.25 1/h)
Y_RED = 0.10  # g cells / g glucose fermented (Verduyn 1990, anaerobic; transfer caveat)
Y_ETOH = 0.45  # g ethanol / g glucose fermented (derived from stoichiometry, see 002)
KS_HIGH_AFF = 0.27  # g/L, ~1.5 mM, high-affinity transporters Hxt6/7 (Reifenberger 1997)
KE = 0.1  # g/L, ethanol uptake half-speed point. ASSUMPTION (order of magnitude).
K_REP = 1.0  # 1/h, repression rate. NOT SOURCED; only its balance with k_rec matters in these data.
KR = 0.5  # g/L, glucose level at which the repression signal is half-active. NOT SOURCED.

YE0 = {1: 0.2, 5: 1.1, 10: 2.2, 25: 5.6, 40: 8.9}  # Ji et al. Table 1, g/L yeast extract
FIG2 = {1: (0.41, 0.22), 5: (0.26, 0.285), 10: (0.24, 0.31), 25: (0.215, 0.365), 40: (0.20, 0.40)}
VANHOEK_FEED = 7.5  # g/L glucose in the chemostat feed (41.7 mmol/L)
CHEMOSTAT_D = (0.1, 0.15, 0.2, 0.25, 0.28, 0.3, 0.35, 0.4)  # below 0.1, maintenance matters (not modelled)


@dataclass(frozen=True)
class Params:
    qs_max: float  # g glucose / g cells / h
    qcrit_min: float  # respiration threshold when repressed, g glucose / g cells / h
    qcrit_max: float  # ... when derepressed
    k_rec: float  # 1/h
    qe_max: float  # g ethanol / g cells / h
    y_xe: float  # g cells / g ethanol
    ks_low_aff: float  # g/L, KS of repressed cells
    y_xye: float  # g cells / g yeast extract
    ye_ratio: float = 0.0  # g YE per g glucose in the medium (set per run)
    dilution: float = 0.0  # 1/h, 0 for batch
    s_feed: float = 0.0  # g/L glucose in the feed


def rates(p: Params, x, s, e, r, ye):
    s, e, ye = max(s, 0.0), max(e, 0.0), max(ye, 0.0)
    g = s / (s + KR)
    ks = KS_HIGH_AFF * r + p.ks_low_aff * (1 - r)
    qs = p.qs_max * s / (ks + s)
    qcrit = p.qcrit_min + r * (p.qcrit_max - p.qcrit_min)
    q_resp = min(qs, qcrit)
    q_over = qs - q_resp
    qe = p.qe_max * e / (KE + e) * r * (1 - g)
    q_ye = qs * p.ye_ratio if ye > 0 else 0.0
    mu = Y_OX * q_resp + Y_RED * q_over + p.y_xe * qe + p.y_xye * q_ye
    d = p.dilution
    return (
        (mu - d) * x,
        d * (p.s_feed - s) - qs * x,
        (Y_ETOH * q_over - qe) * x - d * e,
        p.k_rec * (1 - r) * (1 - g) - K_REP * r * g,
        -q_ye * x - d * ye,
    ), (qs, Y_ETOH * q_over - qe)


def simulate_batch(p: Params, s0: float, x0: float, t_end: float, t_eval=None, r0=0.0, with_ye=True):
    ye0 = YE0.get(int(s0), 0.0) if with_ye else 0.0
    p = replace(p, ye_ratio=ye0 / s0, dilution=0.0)
    sol = solve_ivp(lambda t, y: rates(p, *y)[0], (0, t_end), [x0, s0, 0.0, r0, ye0],
                    t_eval=t_eval, max_step=0.05, rtol=1e-7, atol=1e-9)
    return sol.t, sol.y


def chemostat_steady_state(p: Params, d: float) -> tuple[float, float, float]:
    """Run the chemostat until steady. Returns (glucose uptake, net ethanol production, cells), per g cells."""
    p = replace(p, dilution=d, s_feed=VANHOEK_FEED, ye_ratio=0.0)
    y0 = [Y_OX * VANHOEK_FEED * 0.9, 0.05, 0.0, 1.0, 0.0]
    sol = solve_ivp(lambda t, y: rates(p, *y)[0], (0, 150), y0, method="LSODA", rtol=1e-7, atol=1e-9)
    x, s, e, r, ye = sol.y[:, -1]
    (_, (qs, qe_net)) = rates(p, x, s, e, r, ye)
    return qs, qe_net, x


def glucose_phase_yields(t, y, s0, x0):
    x, s, e = y[0], y[1], y[2]
    i = int(np.argmax(s < 0.01 * s0))
    return (x[i] - x0) / s0, e[i] / s0


def load_csv(name: str) -> dict[str, np.ndarray]:
    lines = [l for l in open(HERE / "data" / name) if not l.startswith("#")]
    rows = list(csv.DictReader(lines))
    return {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}


def calibrate(ji: dict, vh: dict) -> Params:
    t = ji["t_h"]
    idx = [i for i, d in enumerate(vh["D_per_h"]) if round(d, 3) in CHEMOSTAT_D]
    d_list = vh["D_per_h"][idx]
    q_glc = vh["q_glucose"][idx] * MW_GLC / 1000  # g/g/h
    q_eth = vh["q_ethanol"][idx] * MW_ETOH / 1000

    def residuals(v):
        p = Params(*v)
        _, y = simulate_batch(p, 40.0, ji["cells_g_per_L"][0], t[-1], t_eval=t)
        if y.shape[1] != len(t):
            return np.full(3 * len(t) + 2 * len(idx), 10.0)
        batch = np.concatenate([
            np.log(y[0]) - np.log(ji["cells_g_per_L"]),
            (y[1] - ji["glucose_g_per_L"]) / 10.0,
            (y[2] - ji["ethanol_g_per_L"]) / 10.0,
        ])
        chem = []
        for d, qg, qe in zip(d_list, q_glc, q_eth):
            m_qg, m_qe, _ = chemostat_steady_state(p, d)
            chem += [(m_qg - qg) / 0.2, (m_qe - qe) / 0.2]  # ~0.2 g/g/h scale, comparable weight to batch
        return np.concatenate([batch, np.array(chem)])

    #         qs_max qcrit_min qcrit_max k_rec qe_max y_xe ks_low y_xye
    start = [3.0, 0.1, 0.6, 5.0, 0.2, 0.3, 8.0, 0.15]
    lower = [0.5, 0.0, 0.2, 0.05, 0.01, 0.05, 0.3, 0.0]
    upper = [10.0, 1.5, 1.5, 20.0, 3.0, 0.8, 30.0, 1.0]
    fit = least_squares(residuals, start, bounds=(lower, upper), x_scale="jac")
    return Params(*fit.x)


def main() -> None:
    ji = load_csv("ji2016_fig1_40gL.csv")
    vh = load_csv("vanhoek1998_chemostat.csv")
    hb = load_csv("compiled_batch_8gL.csv")
    p = calibrate(ji, vh)
    print("Calibrated on Ji 40 g/L + van Hoek chemostat:")
    for k, v in p.__dict__.items():
        if k not in ("ye_ratio", "dilution", "s_feed"):
            print(f"  {k:11s} {v:.3f}")

    print("\nChemostat (calibration): D, glucose uptake and ethanol production in mmol/g/h, model vs van Hoek")
    chem = []
    for d, qg, qe in zip(vh["D_per_h"], vh["q_glucose"], vh["q_ethanol"]):
        m_qg, m_qe, _ = chemostat_steady_state(p, d)
        chem.append((d, m_qg / MW_GLC * 1000, m_qe / MW_ETOH * 1000, qg, qe))
        print(f"  D={d:5.3f}  glucose {chem[-1][1]:5.2f} vs {qg:5.2f}   ethanol {chem[-1][2]:5.2f} vs {qe:5.2f}")

    x0 = ji["cells_g_per_L"][0]
    levels = sorted(FIG2)
    table = [glucose_phase_yields(*simulate_batch(p, s0, x0, 40.0), s0, x0) for s0 in levels]
    print("\nTest: Ji Fig. 2 glucose-phase yields (cells / ethanol, g/g), model vs Ji")
    for s0, (mx, me) in zip(levels, table):
        tag = "(calibration level)" if s0 == 40 else ""
        print(f"  {s0:>3} g/L  model {mx:.2f} / {me:.2f}   Ji {FIG2[s0][0]:.2f} / {FIG2[s0][1]:.2f}  {tag}")

    print("\nTest: compiled 8 g/L batch (no yeast extract assumed), glucose-phase yields at glucose exhaustion")
    hx0 = hb["cells_g_per_L"][0]
    i_end = int(np.argmax(hb["glucose_g_per_L"] <= 0))
    data_y = ((hb["cells_g_per_L"][i_end] - hx0) / 8.0, hb["ethanol_g_per_L"][i_end] / 8.0)
    hb_runs = {}
    for r0, label in ((0.0, "starts repressed"), (1.0, "starts derepressed")):
        t_h, y_h = simulate_batch(p, 8.0, hx0, 14.0, t_eval=np.linspace(0, 14, 300), r0=r0, with_ye=False)
        hb_runs[label] = (t_h, y_h)
        my = glucose_phase_yields(*simulate_batch(p, 8.0, hx0, 30.0, r0=r0, with_ye=False), 8.0, hx0)
        print(f"  model ({label}): {my[0]:.2f} / {my[1]:.2f}   data {data_y[0]:.2f} / {data_y[1]:.2f}")

    plot(p, ji, chem, levels, table, hb, hb_runs)


def plot(p, ji, chem, levels, table, hb, hb_runs) -> None:
    ink, muted, grid, blue, orange = "#0b0b0b", "#52514e", "#e1e0d9", "#2a78d6", "#eb6834"

    def style(ax, title, xlabel):
        ax.set_title(title, loc="left", color=ink, fontsize=10)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted, labelsize=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        ax.set_xlabel(xlabel, color=muted, fontsize=9)

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    t = np.linspace(0, 26, 400)
    _, y = simulate_batch(p, 40.0, ji["cells_g_per_L"][0], 26, t_eval=t)
    for ax, i, key, title, log in ((axes[0, 0], 0, "cells_g_per_L", "Calibration: Ji 40 g/L, cells (g/L, log)", True),
                                   (axes[0, 1], 2, "ethanol_g_per_L", "Calibration: Ji 40 g/L, ethanol and glucose (g/L)", False)):
        ax.plot(t, y[i], color=blue, linewidth=2, label="model")
        ax.plot(ji["t_h"], ji[key], "o", mfc="none", mec=ink, ms=5, label="Ji Fig. 1 (read from image)")
        if not log:
            ax.plot(t, y[1], color=orange, linewidth=2, label="model glucose")
            ax.plot(ji["t_h"], ji["glucose_g_per_L"], "^", mfc="none", mec=muted, ms=5, label="Ji glucose")
        else:
            ax.set_yscale("log")
        style(ax, title, "Time (h)")
        ax.legend(fontsize=7, frameon=False)

    d = [c[0] for c in chem]
    ax = axes[0, 2]
    ax.plot(d, [c[1] for c in chem], color=blue, linewidth=2, label="model glucose uptake")
    ax.plot(d, [c[3] for c in chem], "o", mfc="none", mec=blue, ms=5, label="van Hoek glucose uptake")
    ax.plot(d, [c[2] for c in chem], color=orange, linewidth=2, label="model ethanol production")
    ax.plot(d, [c[4] for c in chem], "s", mfc="none", mec=orange, ms=5, label="van Hoek ethanol production")
    style(ax, "Calibration: chemostat fluxes (mmol/g/h)", "Growth rate = dilution rate D (1/h)")
    ax.legend(fontsize=7, frameon=False)

    for ax, j, title in ((axes[1, 0], 0, "TEST: Ji cell yield, glucose phase (g/g)"),
                         (axes[1, 1], 1, "TEST: Ji ethanol yield, glucose phase (g/g)")):
        ax.plot(levels, [v[j] for v in table], color=blue, linewidth=2, marker="o", ms=4, label="model")
        ax.plot(levels, [FIG2[s][j] for s in levels], "^", mfc="none", mec=ink, ms=7, label="Ji Fig. 2 (read from image)")
        ax.set_ylim(0, 0.55)
        style(ax, title, "Starting glucose (g/L); 40 g/L is the calibration level")
        ax.legend(fontsize=7, frameon=False)

    ax = axes[1, 2]
    for (label, (th, yh)), ls in zip(hb_runs.items(), ("-", "--")):
        ax.plot(th, yh[2], color=orange, linewidth=2, linestyle=ls, label=f"model ethanol, {label}")
        ax.plot(th, yh[1], color=blue, linewidth=2, linestyle=ls, label=f"model glucose, {label}")
    ax.plot(hb["t_h"], hb["ethanol_g_per_L"], "s", mfc="none", mec=orange, ms=5, label="data ethanol")
    ax.plot(hb["t_h"], hb["glucose_g_per_L"], "^", mfc="none", mec=blue, ms=5, label="data glucose")
    style(ax, "TEST: compiled 8 g/L batch (g/L)", "Time (h)")
    ax.legend(fontsize=6, frameon=False)

    fig.suptitle("Uptake affinity linked to repression: exploratory, calibrated on Ji 40 g/L + van Hoek chemostat",
                 color=ink, fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "005_state_dependent_uptake.png", dpi=140)


if __name__ == "__main__":
    main()
