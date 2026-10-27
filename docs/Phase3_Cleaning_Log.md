# Phase 3: Data Inspection, Cleaning and Workbook Log

**Project:** Export Competitiveness and Economic Performance in Central Europe (independent research project)
**Author:** Ghulam Mustafa | **Date:** 25 October 2026

## 1. Inputs inspected
| Item | Finding |
|---|---|
| Data file | `3ed9e304-...-Data.csv`: 56 data rows = 4 countries x 14 series, years 2009-2025 (17 columns), plus a 2-line footer |
| Metadata file | `...Series - Metadata.csv` is the standard DataBank export: it repeats the data, then adds a definitions table for the 14 series |
| WDI release stamp | Footer says `Last Updated: 10/08/2026`. Day/month order is not stated in the file. |

## 2. Checks and results
- **Coverage:** 14 series x 4 countries x 17 years = 952 cells. **0 missing**, no ".." markers, no blanks, 2025 present for every series.
- **Codes:** all 14 WDI codes match the metadata file. Only cosmetic difference: GDP growth is titled "GDP growth (annual %)" in the data and "GDP (annual % growth)" in the metadata.
- **Duplicates:** none. **Country names:** Czechia, Hungary, Poland, Slovak Republic (standardised to Slovakia; codes unchanged).
- **Units:** all % series are in percentage points (12.5 = 12.5%). Constant series is 2015 US$ (exports in 2015 equal the current-US$ value, which confirms the base year).
- **Identities hold to rounding (~1e-12):** Exports % GDP, Imports % GDP, Trade % GDP and FDI % GDP all equal the US$ series divided by GDP. Consequence: the % series are not independent sources, and Exports % GDP vs Trade % GDP correlate at 0.995 by construction.

## 3. Flags (kept, never removed)
1. **Hungary FDI is extreme:** -40% to +106% of GDP (US$ -71bn to +167bn), 12 of 16 years flagged.
2. **Merchandise exports exceed total goods-and-services exports for Czechia in 14 of 16 years** (WTO basis vs national accounts). Not used as a share of total exports.
3. **2010 export growth** (11-18% in all four countries) is the rebound from 2009; tagged "Rebound".
4. **COVID 2020:** GDP growth and export growth flagged for Czechia and Hungary (and Slovakia export growth).
5. **2022 energy shock:** trade balance flagged for Hungary, Czechia, Slovakia.
6. Current-US$ series move with exchange rates; 2025 values are the latest release and may be revised.

## 4. Decisions
- 2009 is not in the 64-row clean sheet; it is used only for 2010 export growth.
- `03_CLEAN_DATA` is formula-driven from `02_RAW_DATA` (blank = missing).
- Exports % GDP added as a sixth correlation variable because the frozen H2 rule is written on it.
- Ex-Hungary pooled correlation added as a supplementary robustness check (added after seeing the data); it does not replace the frozen test.
- Outlier rule: pooled 1.5 x IQR fence OR within-country |z| > 2.5.

## 5. Verification
2,672 formulas recalculated with 0 errors. All values recomputed independently in pandas from the raw CSV: 0 mismatches (`analysis/analysis_crosscheck.py`).

## 6. Frozen-rule checks
| Rule | Key numbers | Result |
|---|---|---|
| H1 | Mean Trade % GDP: SVK 178.5, HUN 161.8, POL 98.4 (CZE 140.4 extra); HUN and SVK above POL in 16/16 years | Supported |
| H2 | Pooled corr = 0.22 (< 0.3); ranking CZE > HUN > SVK > POL vs SVK > HUN > CZE > POL | Not supported |
| H3 | Pooled corr = -0.13; within HUN -0.28, POL +0.41, CZE +0.10, SVK +0.35; ex-HUN +0.26 (supplementary) | Not supported |
| H4 | 2020 export growth negative in all four; 2021 positive and above 2010-2019 mean in all four | Supported |
