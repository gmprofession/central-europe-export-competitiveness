"""Build report/Central_Europe_Trade_Report.pdf from the chart PNGs and results.json.

Usage: python report/build_report.py <charts_dir> <results.json> <output.pdf>
Every number quoted in the text is read from results.json (produced by analysis/analysis.py),
except the few values written as plain text, which were checked against it (see docs/Phase5_Report_Log.md).
"""
import sys, json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak,
                                KeepTogether, CondPageBreak)
from PIL import Image as PILImage

CH, RES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
R = json.load(open(RES))
H = R["hypotheses"]; C = R["cagr"]; D = R["descriptives"]; CO = R["correlations"]; P = R["periods"]
ORDER = ["HUN", "POL", "CZE", "SVK"]
NAME = {"HUN": "Hungary", "POL": "Poland", "CZE": "Czechia", "SVK": "Slovakia"}

INK, INK2, ACC, RULE = colors.HexColor("#111111"), colors.HexColor("#555555"), colors.HexColor("#1F3864"), colors.HexColor("#C8C8C8")
base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5, alignment=TA_LEFT)
S = {
    "title": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=ACC, spaceAfter=4),
    "sub": ParagraphStyle("s", parent=base, fontSize=11, leading=14, textColor=INK2, spaceAfter=10),
    "meta": ParagraphStyle("m", parent=base, fontSize=8.6, leading=11.5, textColor=INK2, spaceAfter=2),
    "h1": ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=ACC, spaceBefore=10, spaceAfter=5, keepWithNext=1),
    "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13.5, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    "body": base,
    "cap": ParagraphStyle("c", parent=base, fontSize=8.2, leading=10.5, textColor=INK2, spaceAfter=9),
    "bul": ParagraphStyle("bu", parent=base, leftIndent=12, bulletIndent=2, spaceAfter=3),
    "cell": ParagraphStyle("ce", parent=base, fontSize=8.3, leading=10.4, spaceAfter=0),
    "cellb": ParagraphStyle("cb", parent=base, fontName="Helvetica-Bold", fontSize=8.3, leading=10.4, spaceAfter=0),
}
p = lambda t, st="body": Paragraph(t, S[st])
f1 = lambda x: f"{x:.1f}"
f2 = lambda x: f"{x:+.2f}"
pc = lambda x: f"{x*100:.1f}%"


def bullets(items):
    return [Paragraph(t, S["bul"], bulletText="•") for t in items]


def fig(name, caption, width=16.0):
    path = f"{CH}/{name}"
    w, h = PILImage.open(path).size
    img = Image(path, width=width * cm, height=width * cm * h / w)
    return KeepTogether([img, Spacer(1, 3), p(caption, "cap")])


def table(rows, widths, header=True, zebra=True):
    data = [[Paragraph(str(c), S["cellb" if (header and i == 0) else "cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], hAlign="LEFT")
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACC),
          ("LINEBELOW", (0, -1), (-1, -1), 0.5, RULE), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("LEFTPADDING", (0, 0), (-1, -1), 4)]
    if zebra:
        for i in range(1, len(rows)):
            if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F3F4F7")))
    t.setStyle(TableStyle(st))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(INK2)
    canvas.drawString(2 * cm, 1.2 * cm, "Export Competitiveness in Central Europe | Independent research project | Ghulam Mustafa, 2026")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


h1, h2, h3, h4 = H["H1"], H["H2"], H["H3"], H["H4"]["by_country"]
eg_gdp = CO["export_growth_real | gdp_growth"]; fdi_trd = CO["fdi_pct_gdp | trade_pct_gdp"]
man_exp = CO["manufacturing_pct_gdp | exports_pct_gdp"]
tbP = P["trade_balance_pct_gdp"]["POL"]
st = []

# ------------------------------------------------------------------ title
st += [p("Export Competitiveness and Economic Performance in Central Europe", "title"),
       p("A Comparative Analysis of Hungary, Poland, Czechia and Slovakia, 2010-2025", "sub"),
       p("Ghulam Mustafa | Independent research project (not employer or coursework) | October 2026", "meta"),
       p("Data: World Bank, World Development Indicators (WDI), DataBank download, file stamp \"Last Updated: 10/08/2026\". "
         "Workbook, code and charts: see the GitHub repository (README).", "meta"),
       Spacer(1, 8)]

# ------------------------------------------------------------------ 1 Executive summary
st += [p("1. Executive summary", "h1"),
       p("<b>Question.</b> How has export competitiveness evolved across Hungary, Poland, Czechia and Slovakia since 2010, and what economic "
         "factors help explain differences in their trade performance?"),
       p("<b>Method and data.</b> Fourteen World Bank WDI indicators for 4 countries over 2010-2025 (64 country-years, no missing values in this "
         "release). Real export growth, trade balance, a 2010 = 100 export index and CAGR were calculated with live Excel formulas and "
         "re-computed independently in Python with zero mismatches. Four hypotheses and their pass/fail rules were written down and frozen "
         "before the data were analysed. The analysis is descriptive: correlations show association, not cause. Results are compared "
         "with research on country size and openness, Central Europe's FDI-led manufacturing model, FDI measurement and recent trade shocks."),
       p(f"<b>Findings.</b> Poland is the clear leader on real export growth: its export volume rose to {f1(C['POL']['index_2025'])} "
         f"(2010 = 100), a CAGR of {pc(C['POL']['2010_2025'])}, against {f1(C['CZE']['index_2025'])}-{f1(C['SVK']['index_2025'])} "
         f"({pc(C['CZE']['2010_2025'])}-{pc(C['SVK']['2010_2025'])}) for the other three, and the gap widened mainly after 2019. Poland also "
         f"moved from a trade deficit ({f1(D['trade_balance_pct_gdp']['POL']['y2010'])}% of GDP in 2010) to steady surpluses. Of the four "
         "frozen hypotheses, two are supported and two are not:"),
       *bullets([
           f"<b>H1 supported:</b> the smaller economies are more open. Mean trade-to-GDP: Slovakia {f1(h1['mean']['SVK'])}%, Hungary "
           f"{f1(h1['mean']['HUN'])}%, Poland {f1(h1['mean']['POL'])}%; Hungary and Slovakia above Poland in all 16 years.",
           f"<b>H2 not supported:</b> manufacturing share and export intensity correlate only weakly across the pooled sample (r = "
           f"{f2(h2['pooled_r'])}, rule required 0.30) and the country rankings differ.",
           f"<b>H3 not supported:</b> FDI inflows show no pooled association with real export growth (r = {f2(h3['pooled_r'])}). Hungary's "
           "FDI series swings from -40% to +106% of GDP and is not a reliable measure of productive investment.",
           "<b>H4 supported:</b> real exports fell in all four countries in 2020 and in 2021 grew faster than each country's 2010-2019 average."]),
       p("<b>Conclusion.</b> High openness is not the same as strong export performance. The two most open economies (Slovakia, Hungary) grew "
         "their real exports more slowly than Poland, the least open one. In these data, Poland is the country that appears to have strengthened "
         "its international competitiveness the most, but the indicators used cannot identify why."),
       ]

# ------------------------------------------------------------------ 2 Introduction
st += [p("2. Introduction", "h1"),
       p("Hungary, Poland, Czechia and Slovakia joined the EU together in 2004 and built much of their growth on export manufacturing tied to "
         "Western European, and especially German, supply chains. They are similar in history and location but differ in size: Poland's GDP "
         "(about US$1.0 trillion in 2025) is larger than the other three combined. That makes them a useful set for asking whether size, "
         "manufacturing, foreign investment and shocks line up with differences in trade performance."),
       p("The study answers seven sub-questions (strongest export growth, trade dependence, trade balances, FDI, manufacturing, COVID-19 and the "
         "post-2022 environment, and overall competitiveness) and tests four hypotheses. The hypotheses and their numerical test rules were "
         "logged on 25 October 2026 before any analysis and were not changed after the results were seen:"),
       table([["ID", "Hypothesis", "Pre-defined test rule"],
              ["H1", "Smaller economies (HUN, SVK) have higher trade-to-GDP than Poland",
               "HUN and SVK both have a higher 2010-2025 mean of Trade % GDP than POL, and each is above POL in at least 14 of 16 years"],
              ["H2", "Manufacturing-intensive economies show stronger merchandise export performance",
               "Pooled correlation of manufacturing VA % GDP with exports % GDP is at least 0.30, and the country rankings on the two means match"],
              ["H3", "Higher FDI inflows are associated with stronger export performance",
               "Pooled correlation of FDI % GDP with real export growth (same year) is positive, and positive within at least 3 of 4 countries"],
              ["H4", "COVID-19 produces a visible disruption in trade, followed by recovery",
               "2020 real export growth negative in all four, and 2021 growth positive and above each country's 2010-2019 average"]],
             [1.0, 6.2, 9.3]),
       Spacer(1, 6)]


# ------------------------------------------------------------------ 3 Literature review
st += [p("3. Literature review", "h1"),
       p("This review places the four hypotheses in existing research. It was compiled after the analysis was finished, to interpret the results; "
         "the hypotheses and test rules were fixed beforehand and were not changed.", "cap"),
       p("<b>What \"competitiveness\" can and cannot mean.</b> Krugman (1994) argued that treating countries like firms competing for market "
         "share is misleading: living standards follow domestic productivity, and trade between advanced economies is not zero-sum. This is why the "
         "study does not read a high exports-to-GDP ratio as competitiveness. It uses real export growth and the trade balance alongside "
         "trade-intensity measures, and treats all of them as partial indicators."),
       p("<b>Country size, openness and value chains (H1).</b> Alesina and Wacziarg (1998) show that smaller countries are systematically more open "
         "to trade, which is the basis of H1. In Central Europe openness is also a product of production sharing. Baldwin and Lopez-Gonzalez (2013) "
         "describe a \"Factory Europe\" with Germany as the hub and neighbouring economies such as Poland and the Czech Republic as spokes; they "
         "note that about 15% of German exports to the Czech Republic are re-imported after processing. Because gross trade counts the same value "
         "several times as parts cross borders, Koopman, Wang and Wei (2014) separate gross exports into value-added and double-counted parts. "
         "Their framework explains why trade-to-GDP ratios above 100% are possible and why they overstate how much domestic value is traded."),
       p("<b>Central Europe's FDI-led manufacturing model (H2).</b> Nölke and Vliegenthart (2009) classify the four countries as \"dependent market "
         "economies\": foreign capital is the main source of investment, coordination runs through the hierarchies of multinational firms, and "
         "comparative advantage lies in assembling semi-standardised industrial goods. They call the model successful but vulnerable to "
         "relocation and to decisions made by foreign headquarters. Bohle and Greskovits (2012) describe the same group as having built "
         "export manufacturing by attracting FDI. The IMF (2013) documents the resulting German-Central European supply chain: rapid "
         "bilateral trade growth, technology transfer, fast growth in knowledge-intensive exports and more synchronised business cycles. "
         "Stehrer and Stöllinger (2015) measure this \"Central European manufacturing core\" (Germany, Austria and the four Visegrad countries): "
         "its share of EU manufacturing value-added exports rose to 42.6% by 2011, five industries led by transport equipment account for 92% "
         "of its value-chain participation, and German value added makes up roughly 10-13% of the core countries' gross exports. This literature "
         "predicts a link between manufacturing and exports, but through integration and imported inputs rather than through the size of the "
         "manufacturing sector alone."),
       p("<b>FDI and export performance (H3).</b> Firm-level studies find that FDI can raise performance, but through specific channels that take "
         "time. Javorcik (2004), using Lithuanian firm data, finds productivity spillovers to domestic suppliers through backward linkages. "
         "Harding and Javorcik (2012) find that FDI in targeted sectors is associated with higher export unit values (quality upgrading) in "
         "developing countries, with ambiguous results for high-income ones. A separate strand questions the macro data themselves. Damgaard, "
         "Elkjaer and Johannesen (2019) estimate that almost 40% of global FDI is \"phantom\" investment passing through corporate shells with no "
         "real activity. For Hungary specifically, the central bank (MNB) has published balance-of-payments data excluding special purpose "
         "entities since 2006, and FDI flows excluding \"capital in transit\" and asset restructuring since 2012, because in a small economy with a "
         "few large multinationals these flows make headline FDI figures hard to interpret."),
       p("<b>Shocks: COVID-19 and the 2022 energy crisis (H4).</b> The IMF (2022) finds that global goods trade fell about 12% at its trough in the "
         "second quarter of 2020 and was back to pre-pandemic levels by October 2021, with value chains proving fairly resilient. For Poland, "
         "Talar (2023) reports that export volume did not fall over 2020 as a whole, while world exports fell 4.7% and EU exports 7.4%, and links "
         "this to fast changes in the product structure of exports. In 2022 European gas prices averaged about 2.5 times their 2021 level, and the "
         "EBRD (2022) described Czechia and Slovakia as among the economies most exposed to the loss of Russian energy imports."),
       p("<b>Contribution of this study.</b> The study adds no new theory. It offers a consistent comparison of the four economies through 2025, "
         "covering both the COVID-19 and 2022 shocks, using public data, a fully reproducible workflow and hypotheses fixed in advance. Its "
         "results can therefore be checked against the expectations above (summarised in Section 6)."),
      ]

# ------------------------------------------------------------------ 4 Data and methodology
st += [p("4. Data and methodology", "h1"),
       p("<b>Source and coverage.</b> All data come from the World Bank's World Development Indicators, downloaded as CSV from DataBank by the "
         "author. Twelve core indicators were used (GDP, GDP growth, GDP per capita, exports in current and constant 2015 US$, imports, exports, "
         "imports and trade as % of GDP, FDI net inflows in US$ and % of GDP, manufacturing value added % of GDP) plus two optional ones "
         "(current account balance % of GDP, merchandise exports). Each code was checked against the WDI series metadata. 2009 was "
         "downloaded only as a base year for 2010 export growth."),
       p("<b>Cleaning rules.</b> The raw file is never edited. A long-format clean sheet (country, year, 14 variables) is built entirely with "
         "lookup formulas, so a new download refreshes every result. Missing values stay missing and are reported in a data-quality table; in "
         f"this release there are {R['missing_values_in_window']} missing values in the analysis window. Outliers are flagged, never removed: "
         "a value is flagged if it lies outside the pooled 1.5 x IQR fence or more than 2.5 standard deviations from its own country's mean. "
         "Medians are reported next to means."),
       p("<b>Calculated indicators.</b> Real export growth = (X<sub>t</sub> / X<sub>t-1</sub> - 1) x 100 using constant-price exports; trade balance = "
         "(exports - imports) / GDP x 100; trade openness = (exports + imports) / GDP x 100, which matched the WDI series to rounding; export "
         "index = X<sub>t</sub> / X<sub>2010</sub> x 100; CAGR = (end / start)<super>1/n</super> - 1. Periods: pre-COVID 2010-2019, COVID 2020-2021, "
         "post-COVID and energy shock 2022-2025."),
       p("<b>Statistics.</b> Pearson correlations are reported pooled (n = 64) and within each country (n = 16). The 64 observations are not "
         "independent (16 consecutive years from each of 4 countries), so no significance tests are claimed; correlations are suggestive only. "
         "A pooled correlation excluding Hungary was added <i>after</i> seeing the FDI data, as a robustness check. It does not replace the frozen test."),
       p("<b>Verification.</b> Every figure in the workbook (2,694 formulas, zero errors) was recomputed from the raw CSV with an independent "
         "Python script; there were no mismatches."),
       ]

# ------------------------------------------------------------------ 4 Results
st += [p("5. Results", "h1"),
       p("5.1 Trade dependence and openness (sub-question 2, H1)", "h2"),
       fig("02_trade_openness.png", "Figure 1. Trade openness, (exports + imports) as % of GDP, 2010-2025. Source: World Bank WDI; author's calculations.", 15.0),
       p(f"<b>Observation.</b> Slovakia is the most open economy (mean {f1(h1['mean']['SVK'])}% of GDP), followed by Hungary "
         f"({f1(h1['mean']['HUN'])}%), Czechia ({f1(h1['mean']['CZE'])}%) and Poland ({f1(h1['mean']['POL'])}%). Hungary and Slovakia are above "
         "Poland in every year, so <b>H1 is supported</b>. Openness peaked in 2022 for Hungary, Poland and Slovakia (Slovakia 204%); Czechia's "
         "peak was 2014 (156%). Since 2022 Hungary has fallen furthest, from 185% to 141%."),
       p("<b>Explanation.</b> Small economies cannot produce every input at home, so they import components, assemble and re-export; the same "
         "value crosses the border twice, which is also why ratios above 100% are possible (trade is measured gross, GDP as value added). "
         "This is the size effect documented by Alesina and Wacziarg (1998), and the double counting described by Koopman, Wang and Wei (2014). "
         "Poland's large home market means less of its activity needs to be traded. The common 2022 peak is consistent with a price effect: "
         "real export volumes did not jump that year (Section 5.3), while energy products reached their highest share of EU imports, 22.8% in "
         "2022, according to Eurostat."),
       p("<b>Implication.</b> Openness signals deep integration in European value chains, but it measures trade <i>intensity</i>, not competitiveness, "
         "and it brings exposure to external demand and import prices."),

       p("5.2 Export growth (sub-questions 1 and 7)", "h2"),
       fig("08_export_index.png", "Figure 2. Real exports of goods and services, index 2010 = 100 (constant 2015 US$). Source: World Bank WDI; author's calculations."),
       p(f"<b>Observation.</b> By 2025 Poland's real exports reached {f1(C['POL']['index_2025'])}, more than double their 2010 level (CAGR "
         f"{pc(C['POL']['2010_2025'])}). Slovakia ({f1(C['SVK']['index_2025'])}), Hungary ({f1(C['HUN']['index_2025'])}) and Czechia "
         f"({f1(C['CZE']['index_2025'])}) grew at {pc(C['CZE']['2010_2025'])}-{pc(C['SVK']['2010_2025'])} a year. Poland was already ahead in 2019 "
         f"({f1(C['POL']['index_2019'])} vs {f1(C['CZE']['index_2019'])}-{f1(C['SVK']['index_2019'])}), but the gap widened from roughly 15-23 "
         f"points to 55-61 points by 2025. Since 2019 Poland's real exports grew {pc(C['POL']['2019_2025'])} a year, the others "
         f"{pc(C['SVK']['2019_2025'])}-{pc(C['HUN']['2019_2025'])}; Hungary's index has edged down since 2023."),
       p("<b>Explanation.</b> Poland's larger and more diversified economy appears less tied to a single sector, while the other three lean "
         "more heavily on car production and demand from Germany, the hub of the regional supply chain (IMF, 2013; Stehrer and Stöllinger, 2015). "
         "This fits the vulnerability Nölke and Vliegenthart (2009) attribute to assembly-based growth models. These data show the pattern; they cannot show the cause. Note also that "
         "growth measured from 2010 includes the rebound from the 2009 crisis, and that a CAGR hides the path between the end points."),
       p("<b>Implication.</b> On the one measure that strips out prices and exchange rates, Poland is the strongest performer of the four."),
      ]

st += [CondPageBreak(9 * cm), p("5.3 COVID-19 and the post-2022 environment (sub-question 6, H4)", "h2"),
       fig("06_export_growth.png", "Figure 3. Annual real export growth, % (constant 2015 US$). 2010 is the rebound from the 2009 crisis. Source: World Bank WDI; author's calculations.", 15.0),
       p(f"<b>Observation.</b> In 2020 real exports fell in every country: Czechia {f1(h4['CZE']['g2020'])}%, Slovakia {f1(h4['SVK']['g2020'])}%, "
         f"Hungary {f1(h4['HUN']['g2020'])}% and Poland only {f1(h4['POL']['g2020'])}%. In 2021 all four grew faster than their 2010-2019 "
         f"average (for example Poland {f1(h4['POL']['g2021'])}% against {f1(h4['POL']['mean_2010_19'])}%), so <b>H4 is supported</b>. "
         "After 2022 the paths split: Poland kept growing (7.4% in 2022, then 2-5% a year), while Hungary's exports fell slightly in 2024 and 2025 and Slovakia's "
         "were flat or negative in 2023-2024."),
       p(f"<b>Explanation.</b> The COVID shock was a sharp, short disruption to supply chains and demand, and the recovery was equally fast. "
         f"The post-2022 slowdown is broader: average real export growth in 2022-2025 was {f1(P['export_growth_real']['POL']['post_2022_25'])}% "
         f"for Poland but only {f1(P['export_growth_real']['SVK']['post_2022_25'])}-{f1(P['export_growth_real']['CZE']['post_2022_25'])}% "
         "for the others. This is consistent with weak demand in their main markets, but the data cannot isolate the cause."),
       p("<b>Comparison with the literature.</b> The fast 2021 rebound matches the IMF (2022) finding that goods trade and value chains recovered "
         "quickly. Poland's small fall also agrees with Talar (2023), who finds no annual fall in Polish export volume in 2020. The two figures "
         "differ (-1.1% here) because the WDI series covers goods and services in national-accounts terms, and services such as travel fell "
         "sharply in 2020."),
       CondPageBreak(9 * cm), p("5.4 Trade balances (sub-question 3)", "h2"),
       fig("05_trade_balance.png", "Figure 4. Trade balance in goods and services, % of GDP. Source: World Bank WDI; author's calculations.", 15.0),
       p(f"<b>Observation.</b> Poland moved from a deficit of {f1(D['trade_balance_pct_gdp']['POL']['y2010'])}% of GDP in 2010 to surpluses "
         f"(period averages: {f1(tbP['pre_2010_19'])}% before COVID, {f1(tbP['covid_2020_21'])}% in 2020-2021, {f1(tbP['post_2022_25'])}% after 2022). "
         f"Czechia ran the most consistent surplus (mean {f1(D['trade_balance_pct_gdp']['CZE']['mean'])}%) but it nearly vanished in 2022 (0.8%). "
         "2022 is the clear break: Hungary fell to -5.3% and Slovakia to -5.9%, the worst value in the sample. Hungary and Czechia recovered "
         "in 2023; Slovakia has stayed around zero. The current-account series shows the same 2022 dip (Hungary -8.8%, Slovakia -9.6%)."),
       p("<b>Explanation and implication.</b> European gas prices averaged about 2.5 times their 2021 level after February 2022, and the EBRD (2022) "
         "named Czechia and Slovakia among the economies most exposed to the loss of Russian energy imports; energy products also peaked at 22.8% "
         "of EU imports that year (Eurostat). The 2022 deficits are consistent with a higher energy import bill rising faster than export earnings. In very open economies the balance can turn quickly with import prices. Poland's lasting move from deficit to "
         "surplus is one of the stronger signals of improved competitiveness in this dataset."),
      ]

st += [CondPageBreak(9 * cm), p("5.5 FDI and export performance (sub-question 4, H3)", "h2"),
       fig("04_fdi_gdp.png", "Figure 5. FDI net inflows, % of GDP. Hungary is shown on its own scale. Source: World Bank WDI; author's calculations.", 15.5),
       p(f"<b>Observation.</b> Poland, Czechia and Slovakia receive modest, fairly stable inflows (means {f1(D['fdi_pct_gdp']['POL']['mean'])}%, "
         f"{f1(D['fdi_pct_gdp']['CZE']['mean'])}% and {f1(D['fdi_pct_gdp']['SVK']['mean'])}% of GDP). Czechia attracts the most relative to its "
         "economy on a steady basis. Hungary is on a different scale: +106% of GDP in 2020, -40% in 2018 and around -30% in 2023-2025; 12 of its "
         f"16 years are flagged as outliers. Its mean ({f1(D['fdi_pct_gdp']['HUN']['mean'])}%) and median ({f1(D['fdi_pct_gdp']['HUN']['median'])}%) "
         "even have opposite signs."),
       fig("07_export_growth_vs_fdi.png", "Figure 6. Real export growth against FDI inflows (% of GDP), same year. Left: all four countries (frozen H3 test). Right: excluding Hungary (supplementary, added after seeing the data).", 15.5),
       p(f"<b>Observation.</b> The pooled correlation between FDI and real export growth is {f2(h3['pooled_r'])}. Within countries it is "
         f"{f2(h3['within']['POL'])} in Poland, {f2(h3['within']['SVK'])} in Slovakia, {f2(h3['within']['CZE'])} in Czechia and "
         f"{f2(h3['within']['HUN'])} in Hungary. Three of four are positive, but the pooled value is negative, so <b>H3 is not supported</b>. "
         f"Excluding Hungary, the pooled value is {f2(h3['supplementary_pooled_excl_HUN'])}."),
       p("<b>Explanation.</b> Swings of this size cannot be factories being built and closed. They are consistent with pass-through capital "
         "(holding companies, special-purpose entities, intra-group transfers) recorded in the balance of payments, which the WDI series "
         "includes. This is the measurement problem described by Damgaard, Elkjaer and Johannesen (2019), and the reason Hungary's central bank "
         "publishes FDI flows excluding special purpose entities and capital in transit. In addition, the test is same-year, while the channels found "
         "in firm-level research (supplier linkages, export quality upgrading; Javorcik, 2004; Harding and Javorcik, 2012) take years, so even a "
         "real effect would show weakly."),
       p("<b>Implication.</b> Headline FDI statistics are a weak guide to productive investment in Hungary. Outside Hungary there is a modest "
         "positive association, but with 16 points per country and a check chosen after seeing the data, it is suggestive only."),
       p("5.6 Manufacturing and exports (sub-question 5, H2)", "h2"),
       p(f"<b>Observation.</b> Czechia has the highest manufacturing share ({f1(h2['mean_manufacturing']['CZE'])}% of GDP), then Hungary "
         f"({f1(h2['mean_manufacturing']['HUN'])}%), Slovakia ({f1(h2['mean_manufacturing']['SVK'])}%) and Poland "
         f"({f1(h2['mean_manufacturing']['POL'])}%). By exports % of GDP the order is Slovakia, Hungary, Czechia, Poland. The pooled correlation "
         f"is {f2(h2['pooled_r'])}, below the 0.30 threshold, and the rankings differ, so <b>H2 is not supported</b>. Within countries, however, "
         f"the two move together over time in Czechia ({f2(man_exp['CZE'])}) and Hungary ({f2(man_exp['HUN'])})."),
       p("<b>Explanation and implication.</b> A larger manufacturing share does not by itself mean a more export-intensive economy across countries: "
         "Slovakia exports more relative to GDP than Czechia with a smaller manufacturing share, which is consistent with heavier use of "
         "imported inputs. That fits the value-chain literature: German value added alone accounts for roughly 10-13% of the core countries' "
         "gross exports (Stehrer and Stöllinger, 2015), so export intensity reflects integration as much as domestic manufacturing. The test also measures total exports of goods and services rather than \"merchandise export performance\" as the "
         "hypothesis is worded; the merchandise series could not be used as a share of exports because, for Czechia, it exceeds total exports "
         "in 14 of 16 years (different compilation basis). This mismatch is a limitation of the test, not a reason to change the verdict."),
      ]

st += [p("5.7 Other associations from the correlation analysis", "h2"),
       table([["Question (blueprint section 9)", "Pooled r (n=64)", "Within-country r (HUN / POL / CZE / SVK)", "Reading"],
              ["Is export growth associated with GDP growth?", f2(eg_gdp["pooled"]),
               " / ".join(f2(eg_gdp[c]) for c in ORDER), "Strong and consistent in every country"],
              ["Is FDI associated with trade openness?", f2(fdi_trd["pooled"]),
               " / ".join(f2(fdi_trd[c]) for c in ORDER), "No pooled association; positive only in Poland"],
              ["Is manufacturing intensity associated with export dependence?", f2(man_exp["pooled"]),
               " / ".join(f2(man_exp[c]) for c in ORDER), "Weak across countries, stronger over time within CZE and HUN"]],
             [5.2, 2.2, 4.8, 4.3]),
       p("The strong link between real export growth and GDP growth is expected: exports are a large part of demand in all four economies, and "
         "both series react to the same shocks (2020, 2021). It is an association between two outcomes, not evidence that one drives the other.", "cap"),
      ]

# ------------------------------------------------------------------ 5 Conclusion
st += [p("6. Conclusion", "h1"),
       p("<b>Which country strengthened its competitiveness most?</b> On the evidence here, Poland: the fastest real export growth "
         f"({f1(C['POL']['index_2025'])} vs {f1(C['CZE']['index_2025'])}-{f1(C['SVK']['index_2025'])}), the smallest COVID fall, a durable move "
         f"from trade deficit to surplus, and the steadiest GDP growth (mean {f1(D['gdp_growth']['POL']['mean'])}%, only one negative year). "
         "Its exports-to-GDP ratio also rose from 40% to 50%, which shows growing integration rather than competitiveness on its own."),
       p("<b>What explains the differences?</b> Size explains openness well (H1). It does not explain growth: the most open economies grew their "
         "real exports more slowly. Neither manufacturing share (H2) nor FDI inflows (H3) line up with export performance under the frozen "
         "rules. The data are consistent with Poland's diversification being an advantage, but this was not tested directly."),
       p("<b>What changed?</b> Until 2019 the four followed broadly similar paths, with Poland already somewhat ahead. COVID-19 produced a short, shared shock and a fast "
         "recovery (H4). The real divergence came after 2022, when higher energy import costs pushed Hungary and Slovakia into trade deficits "
         "and export growth in Hungary, Czechia and Slovakia slowed, while Poland's continued."),
       p("<b>How the results compare with the literature.</b>"),
       table([["Theme", "What the literature leads us to expect", "What this study finds"],
              ["Size and openness (H1)", "Small economies are more open (Alesina and Wacziarg, 1998)", "Confirmed: HUN and SVK above POL in all 16 years"],
              ["Manufacturing (H2)", "Exports rise with integration in the German-centred core (IMF, 2013; Stehrer and Stöllinger, 2015)",
               "Not by manufacturing share across countries; yes over time within CZE and HUN"],
              ["FDI (H3)", "Gains via linkages and upgrading over time (Javorcik, 2004; Harding and Javorcik, 2012); headline FDI distorted (Damgaard et al., 2019)",
               "No same-year pooled link; Hungary's data match the distortion warning"],
              ["COVID-19 (H4)", "Sharp fall, fast recovery; resilient value chains (IMF, 2022)", "Confirmed in all four; Poland's fall smallest, as Talar (2023) finds"],
              ["Growth model", "Assembly-based model successful but vulnerable (Nölke and Vliegenthart, 2009)",
               "After 2019 the three most trade-open economies slowed while Poland kept growing"]],
             [3.2, 7.0, 6.3]),
       Spacer(1, 4),
       p("7. Limitations", "h1"),
       *bullets([
           "Descriptive analysis only. Correlations show association, not causation, and no causal model was estimated.",
           "Small, non-independent sample: 64 country-years from 4 countries. Within-country correlations rest on 16 points each; no significance is claimed.",
           "FDI is volatile and distorted by special-purpose entities, pass-through capital and reinvested earnings, most visibly in Hungary.",
           "Exports/GDP and trade/GDP measure trade intensity, not competitiveness. Current-US$ series also move with exchange rates; real growth uses constant 2015 US$.",
           "Economic structures differ (size, sector mix, energy mix), which limits direct comparison.",
           "2025 values are the latest release and may be revised; no values were missing in this release, but a later download may differ.",
           "The H2 test uses total exports of goods and services because the merchandise series is on a different basis; the H3 test is same-year, with no lags.",
           "The ex-Hungary FDI check was chosen after seeing the data and is reported as supplementary only. The MNB's Hungary FDI series excluding special purpose entities and capital in transit was not used; re-running H3 with it, as a supplementary check, is the obvious next step.",
           "The literature review was compiled after the analysis and is used for interpretation only; it did not shape the hypotheses or tests.",
           "Product composition, value added in trade and price competitiveness (e.g. unit labour costs) were not analysed; Eurostat, OECD TiVA or UN Comtrade data would be the next step."]),
       ]

# ------------------------------------------------------------------ Appendix
st += [PageBreak(), p("Appendix A. Summary statistics, 2010-2025 (mean | median)", "h1")]
rows = [["Indicator", "Hungary", "Poland", "Czechia", "Slovakia"]]
for k, lab in [("exports_pct_gdp", "Exports, % of GDP"), ("trade_pct_gdp", "Trade, % of GDP"), ("gdp_growth", "Real GDP growth, %"),
               ("export_growth_real", "Real export growth, %"), ("trade_balance_pct_gdp", "Trade balance, % of GDP"),
               ("current_account_pct_gdp", "Current account, % of GDP"), ("fdi_pct_gdp", "FDI net inflows, % of GDP"),
               ("manufacturing_pct_gdp", "Manufacturing VA, % of GDP")]:
    rows.append([lab] + [f"{D[k][c]['mean']:.1f} | {D[k][c]['median']:.1f}" for c in ORDER])
rows.append(["Export index 2025 (2010 = 100)"] + [f1(C[c]["index_2025"]) for c in ORDER])
rows.append(["Real export CAGR 2010-2025"] + [pc(C[c]["2010_2025"]) for c in ORDER])
st += [table(rows, [5.5, 2.75, 2.75, 2.75, 2.75]), Spacer(1, 8)]

st += [p("Appendix B. Frozen hypothesis results", "h1"),
       table([["ID", "Key numbers", "Result"],
              ["H1", f"Mean Trade % GDP: SVK {f1(h1['mean']['SVK'])}, HUN {f1(h1['mean']['HUN'])}, POL {f1(h1['mean']['POL'])} (CZE {f1(h1['mean']['CZE'])}, not tested); "
                     f"years above POL: HUN {h1['years_above_POL']['HUN']}/16, SVK {h1['years_above_POL']['SVK']}/16", "Supported"],
              ["H2", f"Pooled r = {f2(h2['pooled_r'])} (rule: at least 0.30); rank by manufacturing {' > '.join(h2['rank_manufacturing'])}; "
                     f"by exports % GDP {' > '.join(h2['rank_exports_pct_gdp'])}", "Not supported"],
              ["H3", f"Pooled r = {f2(h3['pooled_r'])} (rule: positive); within: " + ", ".join(f"{c} {f2(h3['within'][c])}" for c in ORDER)
                     + f"; supplementary excl. HUN {f2(h3['supplementary_pooled_excl_HUN'])}", "Not supported"],
              ["H4", "2020 growth: " + ", ".join(f"{c} {f1(h4[c]['g2020'])}%" for c in ORDER) + "; 2021 growth vs 2010-19 mean: "
                     + ", ".join(f"{c} {f1(h4[c]['g2021'])} vs {f1(h4[c]['mean_2010_19'])}" for c in ORDER), "Supported"]],
             [1.0, 12.8, 2.7]),
       Spacer(1, 8),
       p("Appendix C. Data quality and outlier flags", "h1"),
       *bullets([
           "Coverage: 14 series x 4 countries x 17 years (2009-2025) = 952 cells, 0 missing. All 14 WDI codes match the series metadata.",
           "Identities hold to rounding: exports, imports, trade and FDI as % of GDP equal the US$ series divided by GDP; trade openness recomputed "
           "from exports and imports matches the WDI series. These ratio series are therefore not independent sources.",
           "Flagged and kept: Hungary FDI (12 of 16 years); 2010 export growth in all four (rebound from 2009); COVID 2020 GDP and export growth "
           "(Czechia, Hungary; Slovakia export growth); 2022 trade balance (Hungary, Czechia, Slovakia); Czechia manufacturing 2015-2016.",
           "Merchandise exports (WTO basis) exceed total goods-and-services exports for Czechia in 14 of 16 years; the series is not used as a share of exports."]),
       Spacer(1, 6),
       p("Appendix D. References", "h1"),
       *bullets([
           "<b>Data</b>",
           "World Bank. World Development Indicators. DataBank, databank.worldbank.org. CSV download by the author; file stamp \"Last Updated: "
           "10/08/2026\"; accessed 25 October 2026.",
           "Eurostat. \"EU imports of energy products - latest developments\". Statistics Explained, data extracted September 2026.",
           "<b>Literature</b>",
           "Alesina, A. and Wacziarg, R. (1998). Openness, country size and government. <i>Journal of Public Economics</i>, 69(3), 305-321.",
           "Baldwin, R. and Lopez-Gonzalez, J. (2013). Supply-chain trade: A portrait of global patterns and several testable hypotheses. NBER Working Paper 18957.",
           "Bohle, D. and Greskovits, B. (2012). <i>Capitalist Diversity on Europe's Periphery</i>. Ithaca: Cornell University Press.",
           "Damgaard, J., Elkjaer, T. and Johannesen, N. (2019). What is real and what is not in the global FDI network? IMF Working Paper 19/274.",
           "EBRD (2022). <i>Regional Economic Prospects in the EBRD Regions: A cold winter ahead? Confronting the energy crunch</i>. September 2022.",
           "Harding, T. and Javorcik, B. S. (2012). Foreign direct investment and export upgrading. <i>Review of Economics and Statistics</i>, 94(4), 964-980.",
           "IMF (2013). <i>German-Central European Supply Chain - Cluster Report</i>. IMF Country Report 13/263.",
           "IMF (2022). Global trade and value chains during the pandemic. <i>World Economic Outlook</i>, April 2022, Chapter 4.",
           "Javorcik, B. S. (2004). Does foreign direct investment increase the productivity of domestic firms? In search of spillovers through "
           "backward linkages. <i>American Economic Review</i>, 94(3), 605-627.",
           "Koopman, R., Wang, Z. and Wei, S.-J. (2014). Tracing value-added and double counting in gross exports. <i>American Economic Review</i>, 104(2), 459-494.",
           "Krugman, P. (1994). Competitiveness: A dangerous obsession. <i>Foreign Affairs</i>, 73(2), 28-44.",
           "Magyar Nemzeti Bank. FDI flows excluding capital in transit and restructuring of asset portfolios (statistical page); and "
           "<i>Methodology of the compilation of the balance of payments and international investment position statistics</i>.",
           "Nölke, A. and Vliegenthart, A. (2009). Enlarging the varieties of capitalism: The emergence of dependent market economies in East "
           "Central Europe. <i>World Politics</i>, 61(4), 670-702.",
           "Stehrer, R. and Stöllinger, R. (2015). The Central European manufacturing core: What is driving regional production sharing? "
           "FIW Research Report 2014/15 No. 02.",
           "Talar, S. (2023). Resilience of Polish exports to non-economic external shocks. <i>Studia Sieci Uniwersytetów Pogranicza</i>, 7, 319-334."]),
       ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title="Export Competitiveness and Economic Performance in Central Europe", author="Ghulam Mustafa",
                        subject="Independent research project: Hungary, Poland, Czechia, Slovakia, 2010-2025")
doc.build(st, onFirstPage=footer, onLaterPages=footer)
print("saved", OUT)
