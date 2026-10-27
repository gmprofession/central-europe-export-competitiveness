# Phase 4: Charts and Interpretation Log

**Project:** Export Competitiveness and Economic Performance in Central Europe (independent research project)
**Author:** Ghulam Mustafa | **Date:** 25 October 2026

## 1. What was built
- `analysis/trade_analysis.xlsx`, sheet `05_CHARTS`: the 8 blueprint charts as live Excel charts linked to `03_CLEAN_DATA` / `04_CALCULATIONS`, each with Observation -> Explanation -> Economic implication. Chart 7 has a live correlation box linked to `06_SUMMARY`.
- `charts/01_...png` to `08_...png`: the same charts as PNG (200 dpi), built by `analysis/make_charts.py` directly from the raw CSV.

Design: same colour and marker per country everywhere (Hungary red circle, Poland blue square, Czechia green triangle, Slovakia yellow diamond); Hungary FDI on its own panel and scale; Chart 7 shown for all four (frozen test) and excluding Hungary (supplementary).

## 2. Corrections recorded during Phase 4
1. Not all four countries peak in 2022 on Charts 1-2: Hungary, Poland and Slovakia do; Czechia peaked in 2014.
2. Hungary's within-country FDI/export-growth correlation is -0.28 and the ex-Hungary pooled value +0.26 (Phase 3 rounded to -0.29 / +0.27). Verdict unchanged.
3. Hungary did not run surpluses every year before 2022: 2021 was a small deficit (-0.4% of GDP).

## 3. Interpretation summary
| Chart | Key finding | Hypothesis link |
|---|---|---|
| 1 Exports % GDP | SVK highest; POL lowest but rising (40% -> 50%); HUN down to 73% since 2022 | Trade intensity, not competitiveness |
| 2 Trade openness | Means SVK 178.5, HUN 161.8, CZE 140.4, POL 98.4 | H1 supported |
| 3 GDP growth | All contract in 2020, rebound 2021, slow after 2022; POL steadiest | Context for H4 |
| 4 FDI % GDP | POL/CZE/SVK 0-6%; HUN -40% to +106% | Explains H3 failure |
| 5 Trade balance | POL deficit -> surplus; HUN -5.3%, SVK -5.9% in 2022 | Sub-question 3 |
| 6 Export growth | All fall in 2020, all above 2010-19 average in 2021 | H4 supported |
| 7 Growth vs FDI | Pooled r = -0.13; ex-HUN +0.26 (supplementary) | H3 not supported |
| 8 Export index | POL 233, SVK 179, HUN 176, CZE 173 | Sub-questions 1 and 7 |

## 4. Verification
Workbook rebuilt from the untouched raw CSV and re-checked: 0 failures; 2,694 formulas, 0 errors. All charts rendered and checked visually.
