"""Reproduce every headline number in the report from the untouched World Bank CSV.

Usage:  python analysis/analysis.py data/raw/<..._Data.csv> [results.json]

Independent of Excel: it recomputes the derived indicators, descriptive statistics,
CAGR, correlations and the four frozen hypothesis tests (Phase1_Design_Lock.md, section 3)
and prints them. The Excel workbook (analysis/trade_analysis.xlsx) does the same with live
formulas; analysis_crosscheck.py confirms the two agree.
Missing values stay missing (NaN); nothing is filled or dropped.
"""
import sys, json
import numpy as np
import pandas as pd

RAW = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
ORDER = ["HUN", "POL", "CZE", "SVK"]

raw = pd.read_csv(RAW)
raw = raw[raw["Country Code"].isin(ORDER)]                      # drops the 2-line WDI footer
yrs = [c for c in raw.columns if "YR" in c]
long = raw.melt(id_vars=["Country Code", "Series Code"], value_vars=yrs)
long["Year"] = long["variable"].str[:4].astype(int)
long["value"] = pd.to_numeric(long["value"], errors="coerce")    # '..' -> NaN, never filled
W = long.pivot_table(index="Year", columns=["Series Code", "Country Code"], values="value", dropna=False)
s = lambda code: W[code][ORDER]
win = slice(2010, 2025)

# ---- variables (analysis window 2010-2025; 2009 used only as the base for 2010 growth)
kd = s("NE.EXP.GNFS.KD")                                   # exports, constant 2015 US$
V = {
    "exports_pct_gdp": s("NE.EXP.GNFS.ZS").loc[win],
    "trade_pct_gdp": s("NE.TRD.GNFS.ZS").loc[win],
    "gdp_growth": s("NY.GDP.MKTP.KD.ZG").loc[win],
    "fdi_pct_gdp": s("BX.KLT.DINV.WD.GD.ZS").loc[win],
    "manufacturing_pct_gdp": s("NV.IND.MANF.ZS").loc[win],
    "current_account_pct_gdp": s("BN.CAB.XOKA.GD.ZS").loc[win],
    "export_growth_real": (kd.pct_change() * 100).loc[win],
    "trade_balance_pct_gdp": ((s("NE.EXP.GNFS.CD") - s("NE.IMP.GNFS.CD")) / s("NY.GDP.MKTP.CD") * 100).loc[win],
    "export_index_2010": (kd / kd.loc[2010] * 100).loc[win],
}
R = {"missing_values_in_window": int(sum(V[k].isna().sum().sum() for k in V))}


def pooled(a, b, cs=ORDER):
    x = np.concatenate([V[a][c].values for c in cs]); y = np.concatenate([V[b][c].values for c in cs])
    m = ~(np.isnan(x) | np.isnan(y))
    return float(np.corrcoef(x[m], y[m])[0, 1])


def within(a, b, c):
    d = pd.concat([V[a][c], V[b][c]], axis=1).dropna()
    return float(np.corrcoef(d.iloc[:, 0], d.iloc[:, 1])[0, 1])


# ---- descriptive statistics (mean next to median, as the data rules require)
R["descriptives"] = {k: {c: {"mean": V[k][c].mean(), "median": V[k][c].median(), "min": V[k][c].min(),
                            "max": V[k][c].max(), "sd": V[k][c].std(ddof=1), "y2010": V[k][c].loc[2010],
                            "y2025": V[k][c].loc[2025]} for c in ORDER} for k in V}

# ---- export CAGR, constant prices
R["cagr"] = {c: {"2010_2025": (kd.loc[2025, c] / kd.loc[2010, c]) ** (1 / 15) - 1,
                 "2010_2019": (kd.loc[2019, c] / kd.loc[2010, c]) ** (1 / 9) - 1,
                 "2019_2025": (kd.loc[2025, c] / kd.loc[2019, c]) ** (1 / 6) - 1,
                 "index_2019": V["export_index_2010"].loc[2019, c],
                 "index_2025": V["export_index_2010"].loc[2025, c]} for c in ORDER}

# ---- period averages
R["periods"] = {k: {c: {"pre_2010_19": V[k][c].loc[2010:2019].mean(), "covid_2020_21": V[k][c].loc[2020:2021].mean(),
                        "post_2022_25": V[k][c].loc[2022:2025].mean()} for c in ORDER}
                for k in ("export_growth_real", "gdp_growth", "trade_balance_pct_gdp", "exports_pct_gdp")}

# ---- correlation matrix (blueprint variables + exports % GDP needed by H2)
CV = ["export_growth_real", "fdi_pct_gdp", "gdp_growth", "trade_pct_gdp", "manufacturing_pct_gdp", "exports_pct_gdp"]
R["correlations"] = {f"{a} | {b}": {"pooled": pooled(a, b), **{c: within(a, b, c) for c in ORDER},
                                    "pooled_excl_HUN": pooled(a, b, ORDER[1:])}
                     for i, a in enumerate(CV) for b in CV[i + 1:]}

# ---- frozen hypothesis tests (rules exactly as in Phase1_Design_Lock.md, section 3)
t = V["trade_pct_gdp"]
h1 = {"mean": {c: t[c].mean() for c in ORDER}, "years_above_POL": {c: int((t[c] > t["POL"]).sum()) for c in ("HUN", "CZE", "SVK")}}
h1["supported"] = bool(all(h1["mean"][c] > h1["mean"]["POL"] and h1["years_above_POL"][c] >= 14 for c in ("HUN", "SVK")))

man = {c: V["manufacturing_pct_gdp"][c].mean() for c in ORDER}
exm = {c: V["exports_pct_gdp"][c].mean() for c in ORDER}
rk_m = sorted(ORDER, key=lambda c: -man[c]); rk_e = sorted(ORDER, key=lambda c: -exm[c])
r2 = pooled("manufacturing_pct_gdp", "exports_pct_gdp")
h2 = {"pooled_r": r2, "rank_manufacturing": rk_m, "rank_exports_pct_gdp": rk_e, "mean_manufacturing": man, "mean_exports_pct_gdp": exm,
      "supported": bool(r2 >= 0.3 and rk_m == rk_e)}

r3 = pooled("fdi_pct_gdp", "export_growth_real")
w3 = {c: within("fdi_pct_gdp", "export_growth_real", c) for c in ORDER}
h3 = {"pooled_r": r3, "within": w3, "n_positive": sum(v > 0 for v in w3.values()),
      "supplementary_pooled_excl_HUN": pooled("fdi_pct_gdp", "export_growth_real", ORDER[1:])}
h3["supported"] = bool(r3 > 0 and h3["n_positive"] >= 3)

eg = V["export_growth_real"]
h4 = {c: {"g2020": eg.loc[2020, c], "g2021": eg.loc[2021, c], "mean_2010_19": eg.loc[2010:2019, c].mean()} for c in ORDER}
h4_ok = all(h4[c]["g2020"] < 0 and h4[c]["g2021"] > 0 and h4[c]["g2021"] > h4[c]["mean_2010_19"] for c in ORDER)
R["hypotheses"] = {"H1": h1, "H2": h2, "H3": h3, "H4": {"by_country": h4, "supported": bool(h4_ok)}}

# ---- print
f = lambda x: f"{x:+.2f}"
print(f"Missing values in 2010-2025 window: {R['missing_values_in_window']}")
print("\nH1 mean Trade % GDP:", {c: round(v, 1) for c, v in h1["mean"].items()}, "| years above POL:", h1["years_above_POL"],
      "->", "SUPPORTED" if h1["supported"] else "NOT SUPPORTED")
print("H2 pooled r(manufacturing, exports % GDP) =", f(r2), "| rank manuf.", rk_m, "| rank exports", rk_e,
      "->", "SUPPORTED" if h2["supported"] else "NOT SUPPORTED")
print("H3 pooled r(FDI % GDP, export growth) =", f(r3), "| within", {c: f(v) for c, v in w3.items()},
      "| excl. HUN", f(h3["supplementary_pooled_excl_HUN"]), "->", "SUPPORTED" if h3["supported"] else "NOT SUPPORTED")
print("H4", {c: (round(v["g2020"], 1), round(v["g2021"], 1), round(v["mean_2010_19"], 1)) for c, v in h4.items()},
      "->", "SUPPORTED" if h4_ok else "NOT SUPPORTED")
print("\nExport index 2025 (2010=100) and CAGR 2010-2025:")
for c in ORDER:
    print(f"  {c}: {R['cagr'][c]['index_2025']:.1f}  CAGR {R['cagr'][c]['2010_2025']*100:.2f}%  "
          f"(2010-19 {R['cagr'][c]['2010_2019']*100:.2f}%, 2019-25 {R['cagr'][c]['2019_2025']*100:.2f}%)")

if OUT:
    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)): return None if np.isnan(o) else float(o)
        if isinstance(o, (np.integer,)): return int(o)
        return o
    json.dump(clean(R), open(OUT, "w"), indent=1)
    print("\nwrote", OUT)
