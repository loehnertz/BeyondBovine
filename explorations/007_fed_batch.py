# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""EXPLORATORY: fed-batch with the step 5 model (005), predicting oxygen uptake and CO2 output.

Fed-batch goal (see docs/LEARNING.md). This is a learning model, not the engine.

What is new compared with 005 (agreed with Jakob):
- Operation: a batch phase, then an exponential feed of concentrated glucose (plus a little ethanol),
  so the volume grows and the broth is diluted by the feed.
- Outputs: oxygen uptake (OUR) and CO2 output (CPR), from a degree-of-reduction (electron) balance
  of each route. Derived, not fitted. They are checked against the van Hoek chemostat below.
- Deliberately NO oxygen-supply limit. Expected: the model misses the late phase, where CO2 out
  exceeds O2 in. That would be evidence for adding an oxygen limit next.

Cell parameters are the 005 calibration (Ji 40 g/L + van Hoek chemostat), used unchanged.
The fed-batch data (Moreno-Paz et al. 2022) are a TEST ONLY: nothing is fitted to them.
Caveats: a third strain (CEN.PK113-7D). The inoculum size and the initial feed rate are not reported,
so the feed follows the standard design rule and the inoculum is shown as a range.

Run with:  uv run explorations/007_fed_batch.py
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).parent
MW_GLC, MW_ETOH, MW_X = 180.16, 46.07, 24.6  # g/mol; biomass per C-mol (CH1.8O0.5N0.2, assumed)
GAMMA_X = 4.2  # degree of reduction of biomass per C-mol (textbook value for CH1.8O0.5N0.2)

# --- Cell model: 005 as calibrated (see explorations/005_state_dependent_uptake.out.txt) ---
Y_OX, Y_RED, Y_ETOH = 0.48, 0.10, 0.45
KS_HIGH_AFF, KE, K_REP, KR = 0.27, 0.1, 1.0, 0.5
QS_MAX, QCRIT_MIN, QCRIT_MAX, K_REC = 4.125, 0.299, 0.751, 4.721
QE_MAX, Y_XE, KS_LOW_AFF = 0.156, 0.330, 10.677

# --- Operation: Moreno-Paz et al. 2022, Appendix S1 ---
V0 = 0.4  # kg of batch medium (taken as litres)
S_BATCH = 2.5  # g/kg glucose in the batch medium
T_FEED = 4.0  # h, feed start
MU_SET = 0.05  # 1/h, the growth rate the feed was designed for
S_FEED, E_FEED = 209.0, 7.67  # g/kg glucose and ethanol in the feed
# NOT REPORTED -> standard design rule: F0 = mu_set * (biomass expected from the batch) / (Y * S_feed),
# with expected batch biomass = Y_OX * S_BATCH * V0 (full respiratory conversion; a designer's assumption).
F0 = MU_SET * (Y_OX * S_BATCH * V0) / (Y_OX * S_FEED)  # kg/h
X0_RANGE = (0.02, 0.05, 0.1)  # g/kg inoculum, NOT REPORTED: shown as a range


def route_stoichiometry():
    """mmol O2 and CO2 per mmol substrate for each route, from carbon and degree-of-reduction balances."""
    cx_resp = Y_OX * MW_GLC / MW_X  # C-mol cells per mol glucose respired
    cx_ferm = Y_RED * MW_GLC / MW_X
    etoh_ferm = Y_ETOH * MW_GLC / MW_ETOH  # mol ethanol per mol glucose fermented
    cx_etoh = Y_XE * MW_ETOH / MW_X  # C-mol cells per mol ethanol respired
    return {
        "resp": ((24 - GAMMA_X * cx_resp) / 4, 6 - cx_resp),  # glucose: 6 C, degree of reduction 24
        "ferm": (max((24 - GAMMA_X * cx_ferm - 12 * etoh_ferm) / 4, 0.0), 6 - cx_ferm - 2 * etoh_ferm),
        "etoh": ((12 - GAMMA_X * cx_etoh) / 4, 2 - cx_etoh),  # ethanol: 2 C, degree of reduction 12
    }


STOICH = route_stoichiometry()


def feed_rate(t: float) -> float:
    return F0 * np.exp(MU_SET * (t - T_FEED)) if t >= T_FEED else 0.0


def rates(t, y):
    x, s, e, r, v = y
    s, e = max(s, 0.0), max(e, 0.0)
    g = s / (s + KR)
    ks = KS_HIGH_AFF * r + KS_LOW_AFF * (1 - r)
    qs = QS_MAX * s / (ks + s)
    qcrit = QCRIT_MIN + r * (QCRIT_MAX - QCRIT_MIN)
    q_resp = min(qs, qcrit)
    q_over = qs - q_resp
    qe = QE_MAX * e / (KE + e) * r * (1 - g)
    mu = Y_OX * q_resp + Y_RED * q_over + Y_XE * qe
    f = feed_rate(t)
    d = f / v
    deriv = (
        (mu - d) * x,
        d * (S_FEED - s) - qs * x,
        d * (E_FEED - e) + (Y_ETOH * q_over - qe) * x,
        K_REC * (1 - r) * (1 - g) - K_REP * r * g,
        f,
    )
    # gas exchange, mmol per kg broth per hour
    o2 = co2 = 0.0
    for q, key, mw in ((q_resp, "resp", MW_GLC), (q_over, "ferm", MW_GLC), (qe, "etoh", MW_ETOH)):
        rate = q / mw * 1000 * x  # mmol substrate / kg / h
        o2 += STOICH[key][0] * rate
        co2 += STOICH[key][1] * rate
    return deriv, (o2, co2, mu)


def simulate(x0: float, r0: float, t_end: float = 120.0):
    t_eval = np.linspace(0, t_end, 1201)
    sol = solve_ivp(lambda t, y: rates(t, y)[0], (0, t_end), [x0, S_BATCH, 0.0, r0, V0],
                    t_eval=t_eval, method="LSODA", rtol=1e-7, atol=1e-10, max_step=0.1)
    gas = np.array([rates(t, y)[1] for t, y in zip(sol.t, sol.y.T)])
    return sol.t, sol.y, gas


def load_data():
    lines = [l for l in open(HERE / "data" / "morenopaz2022_fedbatch.csv") if not l.startswith("#")]
    rows = list(csv.DictReader(lines))
    col = lambda k: np.array([float(r[k]) if r[k] else np.nan for r in rows])
    return col("t_h"), col("OUR_mmol_per_kg_h"), col("CPR_mmol_per_kg_h"), col("biomass_g_per_kg")


def main() -> None:
    print("Route stoichiometry (mmol O2, mmol CO2 per mmol substrate), derived:")
    for k, (o, c) in STOICH.items():
        print(f"  {k:5s} O2 {o:.2f}  CO2 {c:.2f}")
    print("  check vs van Hoek chemostat (respiratory, D=0.1-0.25): O2/glucose ~2.3, CO2/glucose ~2.5")
    print(f"\nFeed: F0 = {F0 * 1000:.3f} g/h at t = {T_FEED} h, growing at {MU_SET}/h (design rule, not reported)")

    t_d, our_d, cpr_d, bio_d = load_data()
    runs = {(x0, r0): simulate(x0, r0) for x0 in X0_RANGE for r0 in (0.0, 1.0)}
    base = runs[(0.05, 0.0)]
    t, y, gas = base
    print(f"\nBase case (inoculum 0.05 g/kg, starts repressed): final volume {y[4, -1]:.2f} kg")
    print("Test: biomass (g/kg), model range over inoculum/start state vs data")
    for tb, b in zip(t_d[~np.isnan(bio_d)], bio_d[~np.isnan(bio_d)]):
        vals = [np.interp(tb, run[0], run[1][0]) for run in runs.values()]
        print(f"  t={tb:6.1f} h  model {min(vals):6.2f}-{max(vals):6.2f}   data {b:6.2f}")
    print("Test: OUR and CPR (mmol/kg/h), base model vs data (1 h averages)")
    for tc in (10, 15, 25, 45, 70, 98, 105, 115):  # no gas data between ~81 and ~97 h
        m = (t_d > tc - 0.5) & (t_d < tc + 0.5)
        i = int(np.argmin(abs(t - tc)))
        print(f"  t={tc:4d} h  OUR {gas[i, 0]:7.1f} vs {np.nanmean(our_d[m]):7.1f}   "
              f"CPR {gas[i, 1]:7.1f} vs {np.nanmean(cpr_d[m]):7.1f}   "
              f"RQ {gas[i, 1] / max(gas[i, 0], 1e-9):4.2f} vs {np.nanmean(cpr_d[m]) / np.nanmean(our_d[m]):4.2f}")
    plot(runs, t_d, our_d, cpr_d, bio_d)


def plot(runs, t_d, our_d, cpr_d, bio_d) -> None:
    ink, muted, grid, blue, orange = "#0b0b0b", "#52514e", "#e1e0d9", "#2a78d6", "#eb6834"

    def style(ax, title, ylabel=None):
        ax.set_title(title, loc="left", color=ink, fontsize=10)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted, labelsize=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        ax.set_xlabel("Time (h)", color=muted, fontsize=9)

    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))
    t, y, gas = runs[(0.05, 0.0)]
    all_gas = np.array([run[2] for run in runs.values()])
    all_x = np.array([run[1][0] for run in runs.values()])

    for ax, j, data, color, title in ((axes[0, 0], 0, our_d, blue, "TEST: oxygen uptake OUR (mmol/kg/h)"),
                                      (axes[0, 1], 1, cpr_d, orange, "TEST: CO2 output CPR (mmol/kg/h)")):
        ax.plot(t_d, data, color=muted, linewidth=0.6, label="data (off-gas, Moreno-Paz 2022)")
        ax.fill_between(t, all_gas[:, :, j].min(0), all_gas[:, :, j].max(0), color=color, alpha=0.2, linewidth=0,
                        label="model range (inoculum, start state)")
        ax.plot(t, gas[:, j], color=color, linewidth=2, label="model, no oxygen limit")
        style(ax, title)
        ax.legend(fontsize=7, frameon=False, loc="upper left")

    ax = axes[1, 0]
    with np.errstate(invalid="ignore", divide="ignore"):
        rq_d = np.convolve(cpr_d, np.ones(30) / 30, "same") / np.convolve(our_d, np.ones(30) / 30, "same")
    ok = t_d > 3
    ax.plot(t_d[ok], rq_d[ok], color=muted, linewidth=0.8, label="data (1 h moving average)")
    ax.plot(t, gas[:, 1] / np.maximum(gas[:, 0], 1e-9), color=blue, linewidth=2, label="model")
    ax.axhline(1.0, color=grid, linewidth=1)
    ax.set_ylim(0.5, 2.0)
    style(ax, "TEST: CO2 out / O2 in (RQ); above ~1 means fermentation")
    ax.legend(fontsize=7, frameon=False, loc="upper right")

    ax = axes[1, 1]
    ax.fill_between(t, all_x.min(0), all_x.max(0), color=blue, alpha=0.2, linewidth=0, label="model range")
    ax.plot(t, y[0], color=blue, linewidth=2, label="model")
    m = ~np.isnan(bio_d)
    ax.plot(t_d[m], bio_d[m], "o", mfc="none", mec=ink, ms=6, label="data")
    ax.set_yscale("log")
    style(ax, "TEST: biomass (g/kg, log scale)")
    ax.legend(fontsize=7, frameon=False, loc="lower right")

    fig.suptitle("Fed-batch with the step 5 cell model (005), no oxygen limit: exploratory, nothing fitted to these data",
                 color=ink, fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "007_fed_batch.png", dpi=140)


if __name__ == "__main__":
    main()
