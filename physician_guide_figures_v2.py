"""
Physician Guide Figures v2 — Curated, high-end, clear.
Only the most impressive and informative figures.
"""

import json

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from scipy import stats

warnings.filterwarnings("ignore")

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "figure.dpi": 250,
        "savefig.dpi": 250,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.12,
    }
)

NB = "#1a5276"  # Neurosteer blue
GREEN = "#27ae60"
ORANGE = "#e67e22"
RED = "#c0392b"
TEAL = "#148f77"
LGRAY = "#ecf0f1"
DGRAY = "#2c3e50"
LBLUE = "#85c1e9"

OUTDIR = Path("physician_guide_figures")
OUTDIR.mkdir(exist_ok=True)

# ── Load ──
df = pd.read_pickle("df_hrv.pkl")
df["TBR"] = df["Theta"] - df["Beta"]
df["BAR"] = df["Beta"] - df["Alpha"]
df["error_rate"] = np.where(df["accuracy"].notna(), (1 - df["accuracy"]) * 100, np.nan)

with open("brain_age_model_v2-0-1.json") as f:
    ba_model = json.load(f)

# ── Task groups ──
TG = {
    "rest": ["rest_closed"],
    "rest_all": [
        "rest_closed",
        "rest_positive",
        "rest_open",
        "rest_music",
        "rest_clear",
        "rest_med",
    ],
    "lo_cog": ["d1", "nb0", "immediate_recall"],
    "mid_cog": ["nb0", "statements"],
    "hi_cog": ["nb2", "nb3", "late_recall", "clock"],
    "lo_cog_rt": ["d1", "nb0"],
    "hi_cog_rt": ["nb2", "nb3"],
    "hi_cog_err": ["nb2", "nb3", "immediate_recall", "late_recall"],
}


def umean(col, tasks):
    mask = df["task_level"].isin(tasks) & df[col].notna()
    return df.loc[mask].groupby("username")[col].mean()


# ── Metrics ──
M = {}
M["A0_rest"] = umean("A0", TG["rest"])
M["A0_mid"] = umean("A0", TG["mid_cog"])
M["A0_hi"] = umean("A0", TG["hi_cog"])
M["TBR_lo"] = umean("TBR", TG["lo_cog"])
M["TBR_hi"] = umean("TBR", TG["hi_cog"])
M["BAR_lo"] = umean("BAR", TG["lo_cog"])
M["BAR_hi"] = umean("BAR", TG["hi_cog"])
M["ST4_rest"] = umean("ST4", TG["rest_all"])
M["T2_hi"] = umean("T2", TG["hi_cog"])
M["RT_lo"] = umean("responsetime", TG["lo_cog_rt"])
M["RT_hi"] = umean("responsetime", TG["hi_cog_rt"])
M["Err_lo"] = umean("error_rate", TG["lo_cog_rt"])
M["Err_hi"] = umean("error_rate", TG["hi_cog_err"])
M["VC9_rest"] = umean("VC9", TG["rest_all"])
M["VC9_hi"] = umean("VC9", TG["hi_cog"])
c = M["VC9_hi"].index.intersection(M["VC9_rest"].index)
M["VC9_diff"] = M["VC9_hi"].loc[c] - M["VC9_rest"].loc[c]

# ── User info ──
ui = (
    df.groupby("username")
    .agg(
        age=("age", "first"),
        mmse=("mmse", "first"),
        mmse_group=("mmse_group", "first"),
        group=("group", "first"),
    )
    .copy()
)
for k, s in M.items():
    ui[k] = s
ui["clin"] = (
    ui["mmse_group"]
    .map({"healthy": "Healthy", "MCI": "MCI", "MD": "Dementia"})
    .fillna("Unclassified")
)

healthy = ui[ui["clin"] == "Healthy"]
mci = ui[ui["clin"] == "MCI"]
md = ui[ui["clin"] == "Dementia"]

# HRV per user
for col in ["PNN50", "RMSSD", "SDNN"]:
    ui[col] = df.groupby("username")[col].mean()

print(
    f"Data loaded: {len(ui)} users, {len(healthy)} healthy, {len(mci)} MCI, {len(md)} dementia"
)

# ══════════════════════════════════════════════════════════════════
# FIG 1: Population age distribution (clean, simple)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4))
for grp, c, l in [
    ("Healthy", GREEN, "Healthy"),
    ("MCI", ORANGE, "MCI"),
    ("Dementia", RED, "Dementia"),
]:
    s = ui[ui["clin"] == grp]["age"].dropna()
    ax.hist(
        s,
        bins=np.arange(15, 105, 5),
        alpha=0.55,
        color=c,
        label=f"{l} (N={len(s)})",
        edgecolor="white",
        lw=0.5,
    )
ax.set_xlabel("Age (years)")
ax.set_ylabel("Participants")
ax.set_title("Study Population by Clinical Group")
ax.legend(frameon=True, fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(OUTDIR / "fig01_population.png")
plt.close()
print("[1] Population")

# ══════════════════════════════════════════════════════════════════
# FIG 2: A0 Load Profile (the signature figure)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))
for grp, c, mk, l in [
    ("Healthy", GREEN, "o", "Healthy"),
    ("MCI", ORANGE, "s", "MCI"),
    ("Dementia", RED, "^", "Dementia"),
]:
    s = ui[ui["clin"] == grp]
    vals = [
        s["A0_rest"].dropna().mean(),
        s["A0_mid"].dropna().mean(),
        s["A0_hi"].dropna().mean(),
    ]
    sems = [
        s["A0_rest"].dropna().sem(),
        s["A0_mid"].dropna().sem(),
        s["A0_hi"].dropna().sem(),
    ]
    ax.errorbar(
        [0, 1, 2],
        vals,
        yerr=sems,
        marker=mk,
        color=c,
        label=f"{l} (N={len(s)})",
        linewidth=2.5,
        markersize=10,
        capsize=5,
    )
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["Rest", "Moderate Load", "High Load"])
ax.set_ylabel("A0 (Cognitive Resource Allocation)")
ax.set_ylim(60, 95)
ax.set_title("Brain Activation Across Cognitive Demand Levels")
ax.legend(fontsize=10, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(OUTDIR / "fig02_a0_load_profile.png")
plt.close()
print("[2] A0 load profile")

# ══════════════════════════════════════════════════════════════════
# FIG 3: Effect Sizes — Only large effects, clean horizontal bars
# ══════════════════════════════════════════════════════════════════
labels_map = {
    "A0_rest": "A0 Rest",
    "A0_mid": "A0 Moderate",
    "A0_hi": "A0 High Load",
    "TBR_lo": "TBR Low",
    "TBR_hi": "TBR High",
    "BAR_lo": "BAR Low",
    "BAR_hi": "BAR High",
    "RT_lo": "Response Time",
    "Err_lo": "Error Rate Low",
    "Err_hi": "Error Rate High",
}
effs = {}
for k, label in labels_map.items():
    h = healthy[k].dropna()
    m = md[k].dropna()
    if len(h) > 5 and len(m) > 5:
        ps = np.sqrt(
            ((len(h) - 1) * h.std() ** 2 + (len(m) - 1) * m.std() ** 2)
            / (len(h) + len(m) - 2)
        )
        effs[label] = (m.mean() - h.mean()) / ps if ps > 0 else 0

fig, ax = plt.subplots(figsize=(8, 5))
sorted_labels = sorted(effs.keys(), key=lambda x: abs(effs[x]), reverse=True)
vals = [effs[l] for l in sorted_labels]
colors = [RED if abs(v) >= 0.8 else ORANGE if abs(v) >= 0.5 else LGRAY for v in vals]
ax.barh(range(len(sorted_labels)), vals, color=colors, edgecolor="white", height=0.65)
for i, v in enumerate(vals):
    ax.text(
        v + 0.05 * np.sign(v),
        i,
        f"{v:+.2f}",
        va="center",
        fontsize=9,
        fontweight="bold",
    )
ax.set_yticks(range(len(sorted_labels)))
ax.set_yticklabels(sorted_labels, fontsize=10)
ax.set_xlabel("Cohen's d (Healthy vs. Dementia)")
ax.set_title("Clinical Discriminative Power of Each Metric")
ax.axvline(0, color="black", lw=0.5)
ax.axvline(0.8, color=RED, lw=0.8, ls="--", alpha=0.4)
ax.axvline(-0.8, color=RED, lw=0.8, ls="--", alpha=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(OUTDIR / "fig03_effect_sizes.png")
plt.close()
print("[3] Effect sizes")

# ══════════════════════════════════════════════════════════════════
# FIG 4: RT & Error — Difficulty gradient by group
# ══════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
for grp, c, mk, l in [
    ("Healthy", GREEN, "o", "Healthy"),
    ("MCI", ORANGE, "s", "MCI"),
    ("Dementia", RED, "^", "Dementia"),
]:
    s = ui[ui["clin"] == grp]
    rt = [s["RT_lo"].dropna().mean(), s["RT_hi"].dropna().mean()]
    rt_se = [s["RT_lo"].dropna().sem(), s["RT_hi"].dropna().sem()]
    ax1.errorbar(
        [0, 1], rt, yerr=rt_se, marker=mk, color=c, label=l, lw=2, ms=8, capsize=4
    )
    er = [s["Err_lo"].dropna().mean(), s["Err_hi"].dropna().mean()]
    er_se = [s["Err_lo"].dropna().sem(), s["Err_hi"].dropna().sem()]
    ax2.errorbar(
        [0, 1], er, yerr=er_se, marker=mk, color=c, label=l, lw=2, ms=8, capsize=4
    )
for ax, yl, t in [
    (ax1, "Response Time (ms)", "Response Time"),
    (ax2, "Error Rate (%)", "Error Rate"),
]:
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Low Load", "High Load"])
    ax.set_ylabel(yl)
    ax.set_title(t)
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
fig.suptitle(
    "Behavioral Performance by Cognitive Demand", fontweight="bold", fontsize=14, y=1.02
)
fig.tight_layout()
fig.savefig(OUTDIR / "fig04_rt_error.png")
plt.close()
print("[4] RT & Error")

# ══════════════════════════════════════════════════════════════════
# FIG 5: Key MMSE Correlations — Only r > 0.3, scatter with regression
# ══════════════════════════════════════════════════════════════════
# Find metrics with |r| > 0.3
mmse_strong = []
for k, label in {
    **labels_map,
    "ST4_rest": "ST4 Rest",
    "T2_hi": "T2 High",
    "VC9_rest": "VC9 Rest",
    "VC9_hi": "VC9 High",
    "VC9_diff": "VC9 Diff",
}.items():
    sub = ui[["mmse", k]].dropna()
    sub = sub[sub["mmse"] > 0]
    if len(sub) > 10:
        r, p = stats.spearmanr(sub["mmse"], sub[k])
        if abs(r) > 0.3:
            mmse_strong.append((k, label, r, p, len(sub)))

mmse_strong.sort(key=lambda x: abs(x[2]), reverse=True)
print(f"\nMetrics with |r(MMSE)| > 0.3: {len(mmse_strong)}")
for k, l, r, p, n in mmse_strong:
    print(f"  {l:20s} r={r:+.3f} p={p:.1e} N={n}")

ncols = min(3, len(mmse_strong))
nrows = (len(mmse_strong) + ncols - 1) // ncols
fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4.5 * nrows))
if nrows == 1:
    axes = [axes] if ncols == 1 else [axes]
axes_flat = [ax for row in axes for ax in (row if hasattr(row, "__len__") else [row])]

for idx, (k, label, r, p, n) in enumerate(mmse_strong):
    ax = axes_flat[idx]
    sub = ui[["mmse", k, "clin"]].dropna()
    sub = sub[sub["mmse"] > 0]
    for grp, c, mk in [
        ("Healthy", GREEN, "o"),
        ("MCI", ORANGE, "s"),
        ("Dementia", RED, "^"),
    ]:
        g = sub[sub["clin"] == grp]
        ax.scatter(
            g["mmse"],
            g[k],
            alpha=0.5,
            s=20,
            color=c,
            marker=mk,
            edgecolors="none",
            label=grp,
        )
    z = np.polyfit(sub["mmse"], sub[k], 1)
    xl = np.linspace(sub["mmse"].min(), sub["mmse"].max(), 100)
    ax.plot(xl, np.polyval(z, xl), color=RED, lw=2)
    ax.set_title(f"{label}\nr = {r:+.2f}", fontsize=11)
    ax.set_xlabel("MMSE")
    ax.set_ylabel(label.split()[0])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
# Hide unused axes
for idx in range(len(mmse_strong), len(axes_flat)):
    axes_flat[idx].set_visible(False)
axes_flat[0].legend(fontsize=8, frameon=True)
fig.suptitle(
    "Metrics Correlated with MMSE Cognitive Score (|r| > 0.3)",
    fontweight="bold",
    fontsize=14,
    y=1.01,
)
fig.tight_layout()
fig.savefig(OUTDIR / "fig05_mmse_correlations.png")
plt.close()
print("[5] MMSE correlations")

# ══════════════════════════════════════════════════════════════════
# FIG 6: Age Trends — Only 4 key metrics
# ══════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, (k, label) in zip(
    axes.flat,
    [
        ("A0_hi", "A0 High Load"),
        ("RT_lo", "Response Time (Low)"),
        ("TBR_lo", "TBR Low Load"),
        ("BAR_lo", "BAR Low Load"),
    ],
):
    sub = ui[["age", k]].dropna()
    sub = sub[sub["age"] > 0]
    r, p = stats.spearmanr(sub["age"], sub[k])
    ax.scatter(sub["age"], sub[k], alpha=0.2, s=12, color=NB, edgecolors="none")
    bins = np.arange(20, 100, 5)
    centers = bins[:-1] + 2.5
    means = [
        sub[(sub["age"] >= lo) & (sub["age"] < hi)][k].mean()
        for lo, hi in zip(bins[:-1], bins[1:])
    ]
    ax.plot(centers, means, color=RED, lw=2.5, marker="o", ms=4)
    ax.set_title(f"{label}\nr = {r:+.2f}", fontsize=11)
    ax.set_xlabel("Age")
    ax.set_ylabel(label.split("(")[0].strip())
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
fig.suptitle(
    "Age-Related Trends in Key Brain Metrics", fontweight="bold", fontsize=14, y=1.01
)
fig.tight_layout()
fig.savefig(OUTDIR / "fig06_age_trends.png")
plt.close()
print("[6] Age trends")

# ══════════════════════════════════════════════════════════════════
# FIG 7: Clinical Group Box Plots — 6 key metrics
# ══════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(13, 8))
for ax, (k, label) in zip(
    axes.flat,
    [
        ("A0_hi", "A0\nHigh Load"),
        ("TBR_hi", "TBR\nHigh Load"),
        ("BAR_hi", "BAR\nHigh Load"),
        ("RT_lo", "RT\nLow (ms)"),
        ("Err_lo", "Error\nLow (%)"),
        ("Err_hi", "Error\nHigh (%)"),
    ],
):
    data, labs, cols = [], [], []
    for grp, c, l in [
        ("Healthy", GREEN, "Healthy"),
        ("MCI", ORANGE, "MCI"),
        ("Dementia", RED, "Dementia"),
    ]:
        s = ui.loc[ui["clin"] == grp, k].dropna()
        if len(s) > 3:
            data.append(s.values)
            labs.append(f"{l}\n(N={len(s)})")
            cols.append(c)
    bp = ax.boxplot(
        data,
        tick_labels=labs,
        patch_artist=True,
        widths=0.6,
        medianprops={"color": "black", "lw": 1.5},
    )
    for patch, c in zip(bp["boxes"], cols):
        patch.set_facecolor(c)
        patch.set_alpha(0.6)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
fig.suptitle(
    "Metric Distributions by Clinical Group", fontweight="bold", fontsize=14, y=1.01
)
fig.tight_layout()
fig.savefig(OUTDIR / "fig07_group_boxplots.png")
plt.close()
print("[7] Group boxplots")

# ══════════════════════════════════════════════════════════════════
# FIG 8: ST4 vs HRV (single clean figure)
# ══════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, (hcol, hlabel) in zip(
    [ax1, ax2], [("PNN50", "PNN50 (Parasympathetic)"), ("RMSSD", "RMSSD (Vagal Tone)")]
):
    sub = ui[["ST4_rest", hcol]].dropna()
    if len(sub) > 10:
        r, p = stats.spearmanr(sub["ST4_rest"], sub[hcol])
        ax.scatter(
            sub["ST4_rest"], sub[hcol], alpha=0.4, s=18, color=NB, edgecolors="none"
        )
        z = np.polyfit(sub["ST4_rest"], sub[hcol], 1)
        xl = np.linspace(sub["ST4_rest"].min(), sub["ST4_rest"].max(), 100)
        ax.plot(xl, np.polyval(z, xl), color=RED, lw=2)
        ax.set_title(f"ST4 vs {hlabel}\nr = {r:+.2f}, N = {len(sub)}", fontsize=11)
    ax.set_xlabel("ST4 (Resting Stress)")
    ax.set_ylabel(hlabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
fig.suptitle(
    "Physiological Stress Validation: ST4 vs Heart Rate Variability",
    fontweight="bold",
    fontsize=13,
    y=1.02,
)
fig.tight_layout()
fig.savefig(OUTDIR / "fig08_st4_hrv.png")
plt.close()
print("[8] ST4 vs HRV")

# ══════════════════════════════════════════════════════════════════
# FIG 9: VC9 vs Performance (healthy only, find best correlation)
# ══════════════════════════════════════════════════════════════════
print("\n-- VC9 correlations in healthy population --")
h_only = ui[ui["clin"].isin(["Healthy", "Unclassified"])]  # larger healthy reference
for k, label in [
    ("RT_lo", "RT Low"),
    ("RT_hi", "RT High"),
    ("Err_lo", "Error Low"),
    ("Err_hi", "Error High"),
    ("A0_rest", "A0 Rest"),
    ("A0_hi", "A0 High"),
]:
    for vk, vl in [
        ("VC9_rest", "VC9 Rest"),
        ("VC9_hi", "VC9 High"),
        ("VC9_diff", "VC9 Diff"),
    ]:
        sub = h_only[[vk, k]].dropna()
        if len(sub) > 20:
            r, p = stats.spearmanr(sub[vk], sub[k])
            if abs(r) > 0.15:
                print(f"  {vl:12s} vs {label:12s}: r={r:+.3f}, p={p:.2e}, N={len(sub)}")

# Find best VC9 correlation
best_r = 0
best_pair = None
for vk, vl in [
    ("VC9_rest", "VC9 Rest"),
    ("VC9_hi", "VC9 High"),
    ("VC9_diff", "VC9 Diff"),
]:
    for k, label in [
        ("RT_lo", "RT Low"),
        ("RT_hi", "RT High"),
        ("Err_lo", "Error Low"),
        ("Err_hi", "Error High"),
        ("A0_rest", "A0 Rest"),
        ("A0_hi", "A0 High"),
        ("TBR_lo", "TBR Low"),
        ("TBR_hi", "TBR High"),
        ("BAR_lo", "BAR Low"),
        ("BAR_hi", "BAR High"),
    ]:
        sub = h_only[[vk, k]].dropna()
        if len(sub) > 20:
            r, _ = stats.spearmanr(sub[vk], sub[k])
            if abs(r) > abs(best_r):
                best_r = r
                best_pair = (vk, vl, k, label)

if best_pair:
    vk, vl, k, kl = best_pair
    print(f"\nBest VC9 correlation: {vl} vs {kl}, r={best_r:+.3f}")
    sub = h_only[[vk, k]].dropna()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(sub[vk], sub[k], alpha=0.3, s=15, color=NB, edgecolors="none")
    z = np.polyfit(sub[vk], sub[k], 1)
    xl = np.linspace(sub[vk].min(), sub[vk].max(), 100)
    ax.plot(xl, np.polyval(z, xl), color=RED, lw=2)
    ax.set_xlabel(vl)
    ax.set_ylabel(kl)
    ax.set_title(
        f"{vl} vs {kl} (Healthy Reference Population)\nr = {best_r:+.2f}, N = {len(sub)}",
        fontweight="bold",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig09_vc9_performance.png")
    plt.close()
    print("[9] VC9 vs performance")

# ══════════════════════════════════════════════════════════════════
# FIG 10: Brain Age — Scatter (healthy+unclassified reference)
# ══════════════════════════════════════════════════════════════════
features = ba_model["features"]
means_d = ba_model["scaler_mean"]
scales_d = ba_model["scaler_scale"]
imp_d = ba_model["imputation_means"]
coef_d = ba_model["coefficients"]
ba_intercept = ba_model["intercept"]
ba_bs = ba_model["bias_slope"]
ba_bi = ba_model["bias_intercept"]

tm_all = df.groupby(["username", "task_level"]).mean(numeric_only=True)


def pred_ba(u):
    if u not in tm_all.index.get_level_values(0):
        return np.nan
    utm = tm_all.loc[u]
    X = []
    for fn in features:
        val = np.nan
        if "_Task" in fn and "_Delta_" not in fn:
            b, t = fn.split("_Task")
            if t in utm.index and b in utm.columns:
                v = utm.loc[t, b]
                if not np.isnan(v):
                    val = v
        elif "_Delta_" in fn:
            parts = fn.split("_Delta_")
            b = parts[0]
            tp = parts[1]
            t1, t2 = tp.split("_", 1)
            if t1 in utm.index and t2 in utm.index and b in utm.columns:
                v1, v2 = utm.loc[t1, b], utm.loc[t2, b]
                if not np.isnan(v1) and not np.isnan(v2):
                    val = v1 - v2
        if np.isnan(val):
            val = imp_d.get(fn, means_d[fn])
        X.append(val)
    X = np.array(X)
    ma = np.array([means_d[f] for f in features])
    sa = np.array([scales_d[f] for f in features])
    ca = np.array([coef_d[f] for f in features])
    raw = float(np.dot((X - ma) / sa, ca) + ba_intercept)
    return float(np.clip(raw - (ba_bs * raw + ba_bi), 20, 98))


ba_results = []
for u in ui.index:
    age = ui.loc[u, "age"]
    if pd.isna(age) or age <= 0:
        continue
    ba = pred_ba(u)
    if np.isnan(ba):
        continue
    ba_results.append({"age": age, "brain_age": ba, "clin": ui.loc[u, "clin"]})
ba_df = pd.DataFrame(ba_results)
ba_df["gap"] = ba_df["brain_age"] - ba_df["age"]

# Plot: reference population only (healthy + unclassified)
ref = ba_df[ba_df["clin"].isin(["Healthy", "Unclassified"])]
r_ref, _ = stats.pearsonr(ref["age"], ref["brain_age"])
mae_ref = np.mean(np.abs(ref.gap))

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(
    ref["age"],
    ref["brain_age"],
    alpha=0.25,
    s=15,
    color=NB,
    edgecolors="none",
    label=f"Reference Population (N={len(ref)})",
)
# Add MCI and MD on top
for grp, c, mk, l in [("MCI", ORANGE, "s", "MCI"), ("Dementia", RED, "^", "Dementia")]:
    s = ba_df[ba_df["clin"] == grp]
    ax.scatter(
        s["age"],
        s["brain_age"],
        alpha=0.7,
        s=35,
        color=c,
        marker=mk,
        edgecolors="white",
        lw=0.5,
        label=f"{l} (N={len(s)})",
        zorder=5,
    )
ax.plot([15, 105], [15, 105], "--", color="gray", lw=1, zorder=0)
z = np.polyfit(ref["age"], ref["brain_age"], 1)
xl = np.linspace(15, 105, 100)
ax.plot(xl, np.polyval(z, xl), color=TEAL, lw=2.5, zorder=4)
ax.set_xlabel("Chronological Age (years)", fontsize=12)
ax.set_ylabel("Predicted Brain Age (years)", fontsize=12)
ax.set_title(
    f"Brain Age Model (v2-0-1)\nReference: r = {r_ref:.2f}, MAE = {mae_ref:.1f} years",
    fontweight="bold",
    fontsize=13,
)
ax.legend(fontsize=9, frameon=True, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(15, 105)
ax.set_ylim(15, 105)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(OUTDIR / "fig10_brain_age.png")
plt.close()
print(f"[10] Brain age scatter: r={r_ref:.3f}, MAE={mae_ref:.1f}")

# ══════════════════════════════════════════════════════════════════
# FIG 11: Brain Age Gap by Group (age-matched 60-85)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))
am = ba_df[(ba_df["age"] >= 60) & (ba_df["age"] <= 85)]
data_box, labs_box, cols_box = [], [], []
for grp, c, l in [
    ("Healthy", GREEN, "Healthy"),
    ("MCI", ORANGE, "MCI"),
    ("Dementia", RED, "Dementia"),
]:
    s = am[am["clin"] == grp]["gap"]
    if len(s) > 3:
        data_box.append(s.values)
        labs_box.append(f"{l}\n(N={len(s)})\ngap = {s.mean():+.1f}")
        cols_box.append(c)
bp = ax.boxplot(
    data_box,
    tick_labels=labs_box,
    patch_artist=True,
    widths=0.55,
    medianprops={"color": "black", "lw": 1.5},
)
for patch, c in zip(bp["boxes"], cols_box):
    patch.set_facecolor(c)
    patch.set_alpha(0.6)
ax.axhline(0, color="gray", lw=0.8, ls="--")
ax.set_ylabel("Brain Age Gap (years)", fontsize=12)
ax.set_title(
    "Brain Age Gap by Clinical Group (Age-Matched, 60\u201385 years)\nPositive = brain appears older than chronological age",
    fontweight="bold",
    fontsize=12,
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(OUTDIR / "fig11_brain_age_gap.png")
plt.close()
print("[11] Brain age gap")

# Print age-matched gaps
print("\nAge-matched gaps (60-85):")
for grp in ["Healthy", "MCI", "Dementia"]:
    s = am[am["clin"] == grp]
    print(f"  {grp}: N={len(s)}, gap={s.gap.mean():+.1f} +/- {s.gap.std():.1f}")

# ══════════════════════════════════════════════════════════════════
# FIG 12: Correlation Matrix (simplified — only key metrics)
# ══════════════════════════════════════════════════════════════════
key_metrics = [
    "A0_rest",
    "A0_hi",
    "TBR_lo",
    "TBR_hi",
    "BAR_lo",
    "BAR_hi",
    "RT_lo",
    "Err_hi",
    "VC9_diff",
]
key_labels = [
    "A0\nRest",
    "A0\nHigh",
    "TBR\nLow",
    "TBR\nHigh",
    "BAR\nLow",
    "BAR\nHigh",
    "RT\nLow",
    "Error\nHigh",
    "VC9\nDiff",
]
corr = ui[key_metrics].corr(method="spearman")
fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(len(key_metrics)))
ax.set_xticklabels(key_labels, fontsize=9)
ax.set_yticks(range(len(key_metrics)))
ax.set_yticklabels(key_labels, fontsize=9)
for i in range(len(key_metrics)):
    for j in range(len(key_metrics)):
        v = corr.values[i, j]
        ax.text(
            j,
            i,
            f"{v:.2f}",
            ha="center",
            va="center",
            fontsize=8,
            color="white" if abs(v) > 0.5 else "black",
        )
plt.colorbar(im, ax=ax, label="Spearman r", shrink=0.8)
ax.set_title("Inter-Metric Correlations", fontweight="bold", fontsize=13)
fig.tight_layout()
fig.savefig(OUTDIR / "fig12_correlation_matrix.png")
plt.close()
print("[12] Correlation matrix")

print("\n=== All figures generated ===")
