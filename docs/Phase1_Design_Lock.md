# Phase 1: Design Lock (FROZEN)

**Project:** Export Competitiveness and Economic Performance in Central Europe: A Comparative Analysis of Hungary, Poland, Czechia and Slovakia
**Type:** Independent research project
**Author:** Ghulam Mustafa
**Hypotheses log date:** 25 October 2026
**Status:** Hypotheses and test rules below are frozen. They are not changed after seeing results. If results contradict a hypothesis, the report says so.

---

## 1. Research question

How has export competitiveness evolved across Hungary, Poland, Czechia and Slovakia since 2010, and what economic factors help explain differences in their trade performance?

## 2. Scope

- Countries: Hungary (HUN), Poland (POL), Czechia (CZE), Slovakia (SVK)
- Analysis window: 2010-2025 (annual), 4 countries x 16 years = 64 country-year observations
- Download window: **2009-2025**. The year 2009 is a base year only, used to calculate 2010 export growth. It is not part of the analysis window.
- Source: World Bank, World Development Indicators (databank.worldbank.org)

## 3. Hypotheses and pre-defined test rules

| ID | Hypothesis | Test rule (decided before seeing data) |
|---|---|---|
| H1 | Smaller economies (HUN, SVK) have higher trade-to-GDP than Poland | **Supported** if HUN and SVK both have a higher period mean of Trade % GDP (2010-2025) than POL, AND each is above POL in at least 14 of 16 years. Otherwise not supported. Czechia is reported alongside as an extra case but is not part of the test. |
| H2 | Manufacturing-intensive economies show stronger merchandise export performance | **Supported** if the pooled correlation between manufacturing value added % GDP and exports % GDP is positive and at least 0.3, AND the country ranking by mean manufacturing share matches the ranking by mean exports % GDP. |
| H3 | Higher FDI inflows are associated with stronger export performance | **Supported** if the pooled correlation between FDI % GDP and export growth (same year, no lags) is positive, AND the within-country correlation is positive in at least 3 of 4 countries. |
| H4 | COVID-19 produces a visible disruption in trade, followed by recovery | **Supported** if 2020 export growth (constant prices) is negative in all four countries, AND 2021 export growth is positive and above each country's 2010-2019 average. |

Notes:
- "Association" language only. No causal claims.
- H3 is expected to be the weakest (FDI is distorted by special-purpose entities and reinvested earnings in Hungary and Czechia). A failed H3 is a legitimate finding.
- 2010 export growth is a rebound from the 2009 crisis. It is flagged as a likely outlier, not removed.

## 4. Indicators (12 core + 2 optional)

| # | Variable | WDI code | Unit | Role |
|---|---|---|---|---|
| 1 | GDP | NY.GDP.MKTP.CD | current US$ | denominator, balance calcs |
| 2 | GDP growth | NY.GDP.MKTP.KD.ZG | % | H4, correlation |
| 3 | GDP per capita | NY.GDP.PCAP.CD | current US$ | context |
| 4 | Exports of goods & services | NE.EXP.GNFS.CD | current US$ | trade balance |
| 5 | Exports of goods & services | NE.EXP.GNFS.KD | constant 2015 US$ | export growth, CAGR, index |
| 6 | Imports of goods & services | NE.IMP.GNFS.CD | current US$ | trade balance |
| 7 | Exports % GDP | NE.EXP.GNFS.ZS | % | chart 1, H2 |
| 8 | Imports % GDP | NE.IMP.GNFS.ZS | % | cross-check |
| 9 | Trade % GDP | NE.TRD.GNFS.ZS | % | H1, chart 2 |
| 10 | FDI net inflows | BX.KLT.DINV.CD.WD | current US$ | context |
| 11 | FDI net inflows % GDP | BX.KLT.DINV.WD.GD.ZS | % | H3, chart 4 |
| 12 | Manufacturing value added | NV.IND.MANF.ZS | % GDP | H2 |
| Opt A | Current account balance | BN.CAB.XOKA.GD.ZS | % GDP | trade balance cross-check |
| Opt B | Merchandise exports | TX.VAL.MRCH.CD.WT | current US$ | tests H2 more directly |

The constant-price export series (NE.EXP.GNFS.KD) uses 2015 as the base year. Export growth calculated from it is real (price-adjusted) growth.

## 5. Data rules

- Raw data is never edited.
- Missing values stay missing. Nothing is estimated or filled.
- Missing data is reported in a data-quality table (Variable | Missing values | Available period | Source).
- Outliers are flagged, not dropped. Medians are reported next to means.
- Workbook sheets: 01_README, 02_RAW_DATA, 03_CLEAN_DATA, 04_CALCULATIONS, 05_CHARTS, 06_SUMMARY.

## 6. Decisions log

| Date | Decision |
|---|---|
| 2026-10-25 | Keep all 12 core indicators (the blueprint said "10"; corrected to 12). |
| 2026-10-25 | Download from 2009 as a base year so 2010 export growth can be calculated. |
| 2026-10-25 | Hypothesis test rules (section 3) approved and frozen. |
