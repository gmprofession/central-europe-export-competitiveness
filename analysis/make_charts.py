"""Phase 4: export the 8 blueprint charts as PNG files for the report and GitHub (charts/ folder).

Usage: python make_charts.py <raw_WDI_Data.csv> <output_folder>
Reads the untouched World Bank CSV and computes the same derived series as 04_CALCULATIONS
(real export growth, trade balance % GDP, export index 2010 = 100). Same colours and markers as the workbook.
"""
import sys, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW, OUTDIR = sys.argv[1], sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)

ORDER = ["HUN", "POL", "CZE", "SVK"]
NAME = {"HUN": "Hungary", "POL": "Poland", "CZE": "Czechia", "SVK": "Slovakia"}
COLOR = {"HUN": "#e34948", "POL": "#2a78d6", "CZE": "#008300", "SVK": "#eda100"}   # validated set, CVD-checked
MARK = {"HUN": "o", "POL": "s", "CZE": "^", "SVK": "D"}                            # second cue besides colour
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

raw = pd.read_csv(RAW)
raw = raw[raw["Country Code"].isin(ORDER)]
yrs = [c for c in raw.columns if "YR" in c]
long = raw.melt(id_vars=["Country Code", "Series Code"], value_vars=yrs)
long["Year"] = long["variable"].str[:4].astype(int)
long["value"] = pd.to_numeric(long["value"], errors="coerce")   # '..' stays missing
W = long.pivot_table(index="Year", columns=["Series Code", "Country Code"], values="value")


def s(code):
    return W[code][ORDER]


win = slice(2010, 2025)
exp_gdp = s("NE.EXP.GNFS.ZS").loc[win]
trade = s("NE.TRD.GNFS.ZS").loc[win]
gdpg = s("NY.GDP.MKTP.KD.ZG").loc[win]
fdi = s("BX.KLT.DINV.WD.GD.ZS").loc[win]
kd = s("NE.EXP.GNFS.KD")
eg = (kd.pct_change() * 100).loc[win]                      # 2010 uses 2009 as the base year
tb = ((s("NE.EXP.GNFS.CD") - s("NE.IMP.GNFS.CD")) / s("NY.GDP.MKTP.CD") * 100).loc[win]
idx = (kd / kd.loc[2010] * 100).loc[win]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK})
SOURCE = "Source: World Bank, World Development Indicators (author's calculations)."


def frame(ax, ylabel, zero=False):
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xticks(range(2010, 2026, 1))
    ax.set_xticklabels([str(y) if y % 2 == 0 else "" for y in range(2010, 2026)])
    if zero:
        ax.axhline(0, color=INK2, linewidth=0.9)


def lines(ax, df, countries=ORDER, label_end=True, fmt="{:.0f}"):
    ends = []
    for c in countries:
        ax.plot(df.index, df[c], color=COLOR[c], marker=MARK[c], markersize=4.5, linewidth=2,
                label=NAME[c], markeredgecolor="white", markeredgewidth=0.6)
        ends.append([c, df[c].iloc[-1]])
    if label_end:   # direct labels at the line ends, nudged apart so they never overlap
        ends.sort(key=lambda e: e[1])
        span = np.nanmax(df[countries].values) - np.nanmin(df[countries].values)
        gap = span * 0.06
        for i in range(1, len(ends)):
            if ends[i][1] - ends[i - 1][1] < gap:
                ends[i][1] = ends[i - 1][1] + gap
        for c, y in ends:
            ax.annotate(f"{NAME[c]} {fmt.format(df[c].iloc[-1])}", xy=(2025, df[c].iloc[-1]), xytext=(2025.35, y),
                        va="center", fontsize=9, color=INK, annotation_clip=False)
        ax.set_xlim(2009.6, 2025.4)


def finish(fig, ax, name, title, subtitle, legend=True):
    ax.set_title(title, loc="left", pad=22)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9.5, color=INK2)
    if legend:
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=4, frameon=False)
    fig.text(0.01, -0.06, SOURCE, fontsize=8, color=INK2)
    fig.savefig(os.path.join(OUTDIR, name), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1 Exports % GDP
fig, ax = plt.subplots(figsize=(10, 5.6)); lines(ax, exp_gdp); frame(ax, "% of GDP")
finish(fig, ax, "01_exports_gdp.png", "Exports of goods and services, % of GDP",
       "Slovakia most export-intensive; Poland lowest but rising. Hungary, Poland and Slovakia peak in 2022.")

# 2 Trade openness
fig, ax = plt.subplots(figsize=(10, 5.6)); lines(ax, trade); frame(ax, "% of GDP")
ax.axhline(100, color=INK2, linewidth=0.8, linestyle=":")
finish(fig, ax, "02_trade_openness.png", "Trade openness: (exports + imports), % of GDP",
       "Hungary and Slovakia above Poland in all 16 years (H1 supported). Above 100% because trade is gross, GDP is value added.")

# 3 GDP growth, 2020 and 2022 shaded
fig, ax = plt.subplots(figsize=(10, 5.6))
for y, lab in ((2020, "COVID-19"), (2022, "Energy shock")):
    ax.axvspan(y - 0.45, y + 0.45, color="#ecebe7", zorder=0)
    ax.text(y, 0.02, lab, ha="center", va="bottom", fontsize=8.5, color=INK2, transform=ax.get_xaxis_transform())
lines(ax, gdpg, fmt="{:.1f}%"); frame(ax, "% change, constant prices", zero=True)
finish(fig, ax, "03_gdp_growth.png", "Real GDP growth, %",
       "All four contract in 2020 and rebound in 2021; growth slows sharply after 2022. Poland is the steadiest.")

# 4 FDI % GDP, two panels with their own scales
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})
lines(a1, fdi, countries=["POL", "CZE", "SVK"], fmt="{:.1f}%"); frame(a1, "% of GDP", zero=True)
a1.set_title("Poland, Czechia, Slovakia", loc="left", fontsize=11)
lines(a2, fdi, countries=["HUN"], label_end=False); frame(a2, "% of GDP (own scale)", zero=True)
a2.set_title("Hungary (note the scale)", loc="left", fontsize=11)
for y in (2016, 2018, 2020):
    v = fdi.loc[y, "HUN"]; a2.annotate(f"{v:.0f}%", (y, v), xytext=(0, 8 if v > 0 else -14), textcoords="offset points", ha="center", fontsize=8.5, color=INK)
fig.suptitle("FDI net inflows, % of GDP", x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)
fig.text(0.01, 0.92, "Hungary's swings (-40% to +106%) look like pass-through capital, not new factories, so it gets its own panel.", fontsize=9.5, color=INK2)
handles = [plt.Line2D([], [], color=COLOR[c], marker=MARK[c], linewidth=2, label=NAME[c]) for c in ORDER]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.04))
fig.text(0.01, -0.06, SOURCE, fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 0.9))
fig.savefig(os.path.join(OUTDIR, "04_fdi_gdp.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)

# 5 Trade balance
fig, ax = plt.subplots(figsize=(10, 5.6)); lines(ax, tb, fmt="{:.1f}%"); frame(ax, "% of GDP", zero=True)
ax.axvspan(2021.55, 2022.45, color="#ecebe7", zorder=0)
ax.text(2022, 0.97, "2022 energy shock", ha="center", va="top", fontsize=8.5, color=INK2, transform=ax.get_xaxis_transform())
finish(fig, ax, "05_trade_balance.png", "Trade balance (exports - imports), % of GDP",
       "Poland moved from deficit to surplus; Hungary and Slovakia fell into deficit in 2022 as energy import bills rose.")

# 6 Export growth
fig, ax = plt.subplots(figsize=(10, 5.6)); lines(ax, eg, fmt="{:.1f}%"); frame(ax, "% change, constant 2015 US$", zero=True)
ax.annotate("2010 = rebound\nfrom 2009", (2010, eg.loc[2010].max()), xytext=(2010.35, eg.loc[2010].max() - 0.5), va="center", fontsize=8.5, color=INK2)
finish(fig, ax, "06_export_growth.png", "Real export growth, % per year",
       "All four fall in 2020 and recover in 2021 (H4 supported). Poland is the most consistent performer.")

# 7 Scatter: export growth vs FDI, all four + excluding Hungary
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4))
for ax, cs, ttl in ((a1, ORDER, "All four countries (frozen H3 test)"), (a2, ["POL", "CZE", "SVK"], "Excluding Hungary (supplementary check)")):
    for c in cs:
        ax.scatter(fdi[c], eg[c], color=COLOR[c], marker=MARK[c], s=38, edgecolor="white", linewidth=0.7, label=NAME[c], zorder=3)
    x = np.concatenate([fdi[c].values for c in cs]); y = np.concatenate([eg[c].values for c in cs])
    r = np.corrcoef(x, y)[0, 1]
    ax.text(0.98, 0.96, f"Pooled r = {r:+.2f} (n = {len(x)})", transform=ax.transAxes, fontsize=9.5, color=INK, va="top", ha="right")
    ax.set_title(ttl, loc="left", fontsize=11)
    ax.set_xlabel("FDI net inflows, % of GDP"); ax.set_ylabel("Real export growth, %")
    ax.grid(color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.axhline(0, color=INK2, linewidth=0.9); ax.axvline(0, color=INK2, linewidth=0.9)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.suptitle("Real export growth vs FDI inflows (same year, 2010-2025)", x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)
fig.text(0.01, 0.92, "H3 not supported: no pooled association. Outside Hungary the link is weakly positive, but suggestive only.", fontsize=9.5, color=INK2)
handles = [plt.Line2D([], [], color=COLOR[c], marker=MARK[c], linestyle="", markersize=7, label=NAME[c]) for c in ORDER]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.04))
fig.text(0.01, -0.06, SOURCE, fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 0.9))
fig.savefig(os.path.join(OUTDIR, "07_export_growth_vs_fdi.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)

# 8 Export index
fig, ax = plt.subplots(figsize=(10, 5.6)); lines(ax, idx); frame(ax, "Index, 2010 = 100")
ax.axhline(100, color=INK2, linewidth=0.8, linestyle=":")
finish(fig, ax, "08_export_index.png", "Real exports, index 2010 = 100 (constant 2015 US$)",
       "Poland's real exports more than doubled (233); the other three end between 173 and 179. The gap opened after 2019.")
print("saved 8 charts to", OUTDIR)
