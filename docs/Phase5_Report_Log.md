# Phase 5: Report, Repository and Career Outputs Log

**Project:** Export Competitiveness and Economic Performance in Central Europe (independent research project)
**Author:** Ghulam Mustafa | **Date:** 26 October 2026 | **Status:** Phase 5 built and verified; remaining steps are yours (GitHub push, LinkedIn, CV)

## 1. What was built
| Output | Content |
|---|---|
| `report/Central_Europe_Trade_Report.pdf` | 8 pages: ~6.5 pages of body (executive summary, introduction, data and method, results with 6 charts, conclusion, limitations) + 1-page appendix (statistics, frozen results, data quality, sources) |
| `report/build_report.py` | Builds the PDF; every number in the text is read from `results.json` |
| `analysis/analysis.py` | New. Recomputes every headline number and the 4 frozen tests from the raw CSV (no Excel needed) and writes `results.json` |
| Repository folder | Blueprint structure: README, data/raw, data/cleaned, analysis, charts, report, sources/data_sources.md, docs, requirements.txt, .gitignore |
| `Phase5_Career_Outputs.md` | LinkedIn post and CV bullets (kept OUT of the public repository) |

Charts in the report: 2 (openness), 8 (export index), 6 (export growth), 5 (trade balance), 4 (FDI), 7 (FDI scatter). Charts 1 and 3 are in the repo and workbook only.

## 2. Phase 4 open items, closed
| Item | Resolution |
|---|---|
| WDI "Last Updated 10/08/2026" date format | Cited exactly as printed in the file, with the access date (25 Oct 2026). DataBank is US-based and the WDI has quarterly updates (the July 2026 update was 1 July 2026), so 8 October 2026 is the likely reading, but the report does not assert it. |
| External source for 2022 energy context | Eurostat, "EU imports of energy products - latest developments" (Statistics Explained, data extracted Sept 2026): energy products peaked at 22.8% of total EU imports in 2022. This is the only external fact used. |

## 3. Corrections to earlier wording (Phase 4 text in 05_CHARTS is unchanged; the report uses the corrected wording)
1. **Export index:** Phase 4 said the four "tracked fairly closely" up to 2019. Not quite: in 2019 Poland was already at 176.9 vs 153.7-162.4 for the others (a 15-23 point lead). The gap then widened to 55-61 points by 2025. The report says this.
2. **"Hungary and Slovakia, the most dependent on Russian gas"** (Phase 4, Chart 5) and **"slowdown in car and battery production"** (Chart 6) are not supported by any source in this project. They were removed from the report. If you want to keep them, find a citation first.
3. **Poland after 2022:** growth was 7.4% in 2022, then 2-5% a year (Phase 4 said "2-7%"; both are true, the report is more precise).

## 4. New observations added in the report (no verdict changed)
- **H2 nuance:** the pooled correlation fails (+0.22), but within countries manufacturing share and exports % GDP move together over time in Czechia (+0.82) and Hungary (+0.77). Reported as an observation.
- **H2 measurement mismatch:** the hypothesis says "merchandise export performance" but the frozen rule uses total exports % GDP. Stated as a limitation, not used to change the result.
- **Export growth vs GDP growth:** pooled r = +0.73, between +0.69 and +0.77 in every country. Answers the first blueprint correlation question. Interpreted as two outcomes reacting to the same shocks, not causation.
- **FDI vs openness:** pooled r = +0.02 (only Poland positive, +0.58).

## 5. Verification
- Full pipeline rebuilt from the untouched raw CSV: `build_workbook.py` -> `add_charts.py` -> recalculation -> `analysis_crosscheck.py`: **0 failures**, verdicts H1 supported, H2 not, H3 not, H4 supported. The uploaded workbook also passes (0 failures).
- `analysis.py` reproduces the same verdicts and numbers independently.
- Raw CSV in the repo is byte-identical to the Project file (MD5 c4f2a30bd42b7f47f4c224c78857b2aa).
- Every number in the PDF text was checked against `results.json` or the raw CSV. PDF pages rendered and checked visually.

## 6. What you need to do (I cannot)
1. Create the GitHub repository `central-europe-export-competitiveness` and upload the folder contents (or `git init`, commit, push).
2. Note: `analysis/trade_analysis.xlsx` is the Phase 4 workbook unchanged.
3. Post on LinkedIn and update your CV using `Phase5_Career_Outputs.md`, after reading them critically.

## 7. Addendum, 26 October 2026: literature review added
Your point: the report relied only on World Bank data and one Eurostat fact, with no literature.

**Added**
- Report Section 3, "Literature review" (~1.3 pages, 5 themes: competitiveness concept; size/openness/value chains (H1); FDI-led manufacturing model (H2); FDI effects and FDI measurement (H3); COVID-19 and 2022 shocks (H4)).
- One-sentence literature comparisons inside results 5.1-5.6, and a "literature vs our findings" table in the conclusion.
- Appendix D is now a full reference list (2 data sources + 15 literature sources). `sources/literature.md` gives the link and the exact point used for each.
- Sections renumbered: 3 Literature, 4 Data and method, 5 Results, 6 Conclusion, 7 Limitations.

**Honesty points written into the report**
- The review was compiled after the analysis; it is used to interpret results and did not shape the hypotheses or tests.
- The unsourced line "all four import most of their energy" was replaced with sourced EBRD (2022) and Eurostat facts.
- New limitation: the MNB publishes Hungary FDI excluding special purpose entities and capital in transit; re-running H3 on it (as a supplementary check) is the obvious next step.
- Talar (2023) finds no annual fall in Polish export volume in 2020; the WDI shows -1.1%. The report explains the difference (goods and services vs goods; services fell sharply in 2020).

**Trade-off:** the main text is now about 8.5 pages, above the blueprint's ~6. Trimming options: drop Figure 4 (trade balance) or shorten the literature review to ~0.7 pages.
