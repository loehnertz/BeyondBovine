# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""EXPLORATORY: a fermentative yield for cells that still have some oxygen, then cross-dataset tests.

Follows 008 (see docs/reviews/2026-09-25-oxygen-limited-cells.md). Agreed with Jakob:
1. CALIBRATE one number, the cell yield of fermented sugar when oxygen is present (Y_RED_OX), on the
   oxygen-limited Jouhten et al. 2008 chemostats (2.8, 1.0 and 0.5 % O2). The anaerobic value (0.10)
   stays for cells without any oxygen.
   Ethanol per fermented glucose follows from the carbon balance: mol ethanol = (6 - C-mol cells) / 3.
2. Re-calibrate the 005 cell model on its usual calibration data (Ji 40 g/L + van Hoek chemostat), now
   with Y_RED_OX for aerobic overflow, because Ji's overflow happens in cells WITH oxygen.
3. TEST, never fitted: Ji et al. Figure 2 (does the round 1 carbon gap close?), the compiled 8 g/L
   batch, and the Moreno-Paz fed-batch (via 007).

005 and 007 are reused unchanged by loading them and replacing their yield constants.

Run with:  uv run explorations/009_oxygen_present_yield.py
"""

import csv
import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).parent
MW_GLC, MW_ETOH, MW_X = 180.16, 46.07, 24.6
Y_OX, O2_PER_GLC_RESP, D_JOUHTEN, S_IN_JOUHTEN = 0.48, 2.31, 0.10, 10.0


def ethanol_yield(y_red: float) -> float:
    """g ethanol per g glucose fermented, from the carbon balance for a given fermentative cell yield."""
    cx = y_red * MW_GLC / MW_X  # C-mol cells per mol glucose
    return (6 - cx) / 3 * MW_ETOH / MW_GLC


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), HERE / name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- Step 1: calibrate Y_RED_OX on Jouhten's oxygen-limited conditions ---
def jouhten_rows():
    lines = [l for l in open(HERE / "data" / "jouhten2008_oxygen_chemostat.csv") if not l.startswith("#")]
    return [r for r in csv.DictReader(lines)]


def jouhten_steady_state(our: float, y_red: float):
    q_resp = min(D_JOUHTEN / Y_OX, our / O2_PER_GLC_RESP * MW_GLC / 1000)
    q_over = (D_JOUHTEN - Y_OX * q_resp) / y_red
    qs = q_resp + q_over
    return qs / MW_GLC * 1000, ethanol_yield(y_red) * q_over / MW_ETOH * 1000, D_JOUHTEN * S_IN_JOUHTEN / qs


def calibrate_y_red_ox() -> float:
    limited = [r for r in jouhten_rows() if 0 < float(r["o2_inlet_pct"]) < 20]

    def err(y):
        e = 0.0
        for r in limited:
            _, me, mx = jouhten_steady_state(float(r["OUR"]), y)
            e += ((me - float(r["q_ethanol"])) / 3.0) ** 2 + ((mx - float(r["biomass_g_per_L"])) / 3.0) ** 2
        return e

    return minimize_scalar(err, bounds=(0.05, 0.45), method="bounded").x


def main() -> None:
    y_red_ox = calibrate_y_red_ox()
    y_etoh_ox = ethanol_yield(y_red_ox)
    print(f"Step 1, calibrated on Jouhten oxygen-limited chemostats: Y_RED_OX = {y_red_ox:.3f} g/g, "
          f"ethanol {y_etoh_ox:.3f} g/g (anaerobic: 0.10 / {ethanol_yield(0.10):.3f})")
    for r in jouhten_rows():
        _, me, mx = jouhten_steady_state(float(r["OUR"]), y_red_ox if float(r["OUR"]) > 0 else 0.10)
        print(f"  {r['o2_inlet_pct']:>5}% {r['culture']:>2}  ethanol {me:5.2f} vs {float(r['q_ethanol']):5.2f}   "
              f"biomass {mx:5.2f} vs {float(r['biomass_g_per_L']):5.2f}")

    # --- Step 2: re-calibrate 005 with the oxygen-present fermentative yield ---
    m5 = load_module("005_state_dependent_uptake.py")
    m5.Y_RED, m5.Y_ETOH = y_red_ox, y_etoh_ox
    ji, vh, hb = m5.load_csv("ji2016_fig1_40gL.csv"), m5.load_csv("vanhoek1998_chemostat.csv"), m5.load_csv("compiled_batch_8gL.csv")
    p = m5.calibrate(ji, vh)
    print("\nStep 2, 005 re-calibrated on Ji 40 g/L + van Hoek with Y_RED_OX:")
    print("  " + "  ".join(f"{k}={v:.3f}" for k, v in p.__dict__.items() if k not in ("ye_ratio", "dilution", "s_feed")))
    chem_err = []
    for d, qg, qe in zip(vh["D_per_h"], vh["q_glucose"], vh["q_ethanol"]):
        m_qg, m_qe, _ = m5.chemostat_steady_state(p, d)
        chem_err.append((d, m_qg / MW_GLC * 1000, qg, m_qe / MW_ETOH * 1000, qe))
    print("  chemostat (calibration) D: glucose / ethanol model vs data")
    for d, a, b, c, e in chem_err:
        print(f"    {d:5.3f}: {a:5.2f} vs {b:5.2f}   {c:5.2f} vs {e:5.2f}")

    # --- Step 3a: Ji Figure 2 test ---
    x0 = ji["cells_g_per_L"][0]
    levels = sorted(m5.FIG2)
    table = [m5.glucose_phase_yields(*m5.simulate_batch(p, s0, x0, 40.0), s0, x0) for s0 in levels]
    old = {1: (0.46, 0.01), 5: (0.31, 0.19), 10: (0.25, 0.27), 25: (0.19, 0.34), 40: (0.18, 0.37)}  # 005 output
    print("\nStep 3a, TEST Ji Fig. 2 (cells / ethanol, g/g): new model | 005 | Ji")
    for s0, (mx, me) in zip(levels, table):
        print(f"  {s0:>3} g/L  {mx:.2f} / {me:.2f}  |  {old[s0][0]:.2f} / {old[s0][1]:.2f}  |  "
              f"{m5.FIG2[s0][0]:.2f} / {m5.FIG2[s0][1]:.2f}{'  (calibration level)' if s0 == 40 else ''}")
    hx0 = hb["cells_g_per_L"][0]
    i_end = int(np.argmax(hb["glucose_g_per_L"] <= 0))
    my = m5.glucose_phase_yields(*m5.simulate_batch(p, 8.0, hx0, 30.0, r0=0.0, with_ye=False), 8.0, hx0)
    print(f"  compiled 8 g/L batch: {my[0]:.2f} / {my[1]:.2f}  |  005: 0.26 / 0.25  |  data "
          f"{(hb['cells_g_per_L'][i_end] - hx0) / 8:.2f} / {hb['ethanol_g_per_L'][i_end] / 8:.2f}")

    # --- Step 3b: fed-batch test via 007 with the new cell parameters ---
    m7 = load_module("007_fed_batch.py")
    m7.Y_RED, m7.Y_ETOH = y_red_ox, y_etoh_ox
    m7.QS_MAX, m7.QCRIT_MIN, m7.QCRIT_MAX, m7.K_REC = p.qs_max, p.qcrit_min, p.qcrit_max, p.k_rec
    m7.QE_MAX, m7.Y_XE, m7.KS_LOW_AFF = p.qe_max, p.y_xe, p.ks_low_aff
    m7.STOICH = m7.route_stoichiometry()
    t, y, gas = m7.simulate(0.05, 0.0)
    t_d, our_d, cpr_d, bio_d = m7.load_data()
    print("\nStep 3b, TEST fed-batch (base case): OUR model vs data, biomass model vs data")
    for tc in (10, 15, 25, 45, 70, 98):
        msk = (t_d > tc - 0.5) & (t_d < tc + 0.5)
        i = int(np.argmin(abs(t - tc)))
        print(f"  t={tc:3d} h  OUR {gas[i, 0]:6.1f} vs {np.nanmean(our_d[msk]):6.1f}")
    for tb, b in zip(t_d[~np.isnan(bio_d)], bio_d[~np.isnan(bio_d)]):
        print(f"  t={tb:6.1f} h  biomass {np.interp(tb, t, y[0]):6.2f} vs {b:6.2f}")

    plot(levels, table, old, m5.FIG2)


def plot(levels, table, old, fig2) -> None:
    ink, muted, grid, blue = "#0b0b0b", "#52514e", "#e1e0d9", "#2a78d6"
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, j, title in ((axes[0], 0, "TEST: Ji cell yield, glucose phase (g/g)"),
                         (axes[1], 1, "TEST: Ji ethanol yield, glucose phase (g/g)")):
        ax.plot(levels, [old[s][j] for s in levels], color="#a3a29c", linewidth=2, marker="o", ms=4, label="005 (anaerobic fermentative yield)")
        ax.plot(levels, [v[j] for v in table], color=blue, linewidth=2, marker="o", ms=4, label="009 (oxygen-present yield)")
        ax.plot(levels, [fig2[s][j] for s in levels], "^", mfc="none", mec=ink, ms=7, label="Ji Fig. 2")
        ax.set_ylim(0, 0.55)
        ax.set_title(title, loc="left", color=ink, fontsize=10)
        ax.set_xlabel("Starting glucose (g/L); 40 g/L is the calibration level", color=muted, fontsize=9)
        ax.grid(True, color=grid, linewidth=0.8)
        ax.tick_params(colors=muted, labelsize=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        ax.legend(fontsize=7, frameon=False)
    fig.suptitle("Oxygen-present fermentative yield (from Jouhten): cross-dataset test on Ji", color=ink, fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "009_oxygen_present_yield.png", dpi=140)


if __name__ == "__main__":
    main()
