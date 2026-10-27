# Data sources

## Primary data

**World Bank, World Development Indicators (WDI)**
- Access: DataBank, https://databank.worldbank.org (database: World Development Indicators)
- Downloaded by the author as CSV on 25 October 2026. File footer: "Data from database: World Development Indicators / Last Updated: 10/08/2026" (date as printed; DataBank does not state the day/month order in the file).
- Countries: Hungary (HUN), Poland (POL), Czechia (CZE), Slovak Republic (SVK). Years: 2009-2025 (2009 = base year only).
- Raw files: `data/raw/3ed9e304-4fec-4c09-ab92-21d2d709e1a1_Data.csv` and `..._Series - Metadata.csv` (untouched).

| # | Indicator | WDI code | Unit | Used for |
|---|---|---|---|---|
| 1 | GDP | NY.GDP.MKTP.CD | current US$ | denominators |
| 2 | GDP growth | NY.GDP.MKTP.KD.ZG | annual % | context, correlation |
| 3 | GDP per capita | NY.GDP.PCAP.CD | current US$ | context |
| 4 | Exports of goods and services | NE.EXP.GNFS.CD | current US$ | trade balance |
| 5 | Exports of goods and services | NE.EXP.GNFS.KD | constant 2015 US$ | real growth, CAGR, index |
| 6 | Imports of goods and services | NE.IMP.GNFS.CD | current US$ | trade balance |
| 7 | Exports of goods and services | NE.EXP.GNFS.ZS | % of GDP | Chart 1, H2 |
| 8 | Imports of goods and services | NE.IMP.GNFS.ZS | % of GDP | cross-check |
| 9 | Trade | NE.TRD.GNFS.ZS | % of GDP | H1, Chart 2 |
| 10 | FDI, net inflows (BoP) | BX.KLT.DINV.CD.WD | current US$ | context |
| 11 | FDI, net inflows | BX.KLT.DINV.WD.GD.ZS | % of GDP | H3, Charts 4 and 7 |
| 12 | Manufacturing, value added | NV.IND.MANF.ZS | % of GDP | H2 |
| A | Current account balance | BN.CAB.XOKA.GD.ZS | % of GDP | cross-check |
| B | Merchandise exports | TX.VAL.MRCH.CD.WT | current US$ | data-quality note only |

All codes were matched against the series metadata file included in the download.

## Context source (cited in the report)

- Eurostat, "EU imports of energy products - latest developments", Statistics Explained (data extracted September 2026): https://ec.europa.eu/eurostat/statistics-explained/index.php?title=EU_imports_of_energy_products_-_latest_developments . Used only for one fact: energy products peaked at 22.8% of total EU imports in 2022.

## Licence

WDI data are published by the World Bank under the Creative Commons Attribution 4.0 (CC BY 4.0) licence; cite as "World Bank, World Development Indicators".
