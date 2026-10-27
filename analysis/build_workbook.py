import csv, itertools, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

RAWCSV = sys.argv[1]
OUT = sys.argv[2]

F = "Arial"
BLUE = Font(name=F, size=10, color="0000FF")
BLK = Font(name=F, size=10, color="000000")
BOLD = Font(name=F, size=10, bold=True)
HDR = Font(name=F, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=F, size=14, bold=True)
SEC = Font(name=F, size=11, bold=True, color="1F3864")
NOTE = Font(name=F, size=9, italic=True, color="595959")
HFILL = PatternFill("solid", fgColor="1F3864")
SFILL = PatternFill("solid", fgColor="D9E1F2")
YFILL = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

RW, CL, CA, RD, SM = ("'02_RAW_DATA'", "'03_CLEAN_DATA'", "'04_CALCULATIONS'",
                      "'01_README'", "'06_SUMMARY'")

wb = Workbook()
ws1 = wb.active; ws1.title = "01_README"
ws2 = wb.create_sheet("02_RAW_DATA")
ws3 = wb.create_sheet("03_CLEAN_DATA")
ws4 = wb.create_sheet("04_CALCULATIONS")
ws5 = wb.create_sheet("05_CHARTS")
ws6 = wb.create_sheet("06_SUMMARY")


def put(ws, ref, v, font=BLK, fmt=None, fill=None, bold=False, wrap=False, border=False, align=None):
    c = ws[ref]
    c.value = v
    c.font = Font(name=font.name, size=font.size, bold=bold or font.bold, italic=font.italic, color=font.color)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap or align: c.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=align)
    if border: c.border = BOX
    return c


def header(ws, row, labels, col0=1, height=None):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col0 + i, value=t)
        c.font = HDR; c.fill = HFILL; c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    if height: ws.row_dimensions[row].height = height


# ------------------------------------------------------------------ 02_RAW_DATA
rows = list(csv.reader(open(RAWCSV, encoding="utf-8")))
for r, row in enumerate(rows, start=1):
    for c, v in enumerate(row, start=1):
        if v == "":
            continue
        cell = ws2.cell(row=r, column=c)
        try:
            cell.value = float(v) if (c >= 5 and r > 1 and v != "..") else v
        except ValueError:
            cell.value = v
        cell.font = BLUE if (r > 1 and c >= 5 and r <= 57) else BLK
RAW_LAST = 57   # header + 56 data rows
assert rows[56][1] == "SVK" and rows[1][1] == "HUN"
for c in range(1, 22):
    ws2.column_dimensions[L(c)].width = 16 if c >= 5 else (20 if c in (1, 3) else 14)
ws2.column_dimensions["C"].width = 52
for c in range(1, 22):
    ws2.cell(row=1, column=c).font = BOLD
ws2.freeze_panes = "E2"

# ------------------------------------------------------------------ variable dictionary
VARS = [
    # name, WDI code, WDI series name, unit, role, tier, fmt
    ("GDP_current_USD", "NY.GDP.MKTP.CD", "GDP (current US$)", "current US$", "denominator; trade balance", "Core", "#,##0"),
    ("GDP_growth_pct", "NY.GDP.MKTP.KD.ZG", "GDP growth (annual %)", "%", "H4; correlation", "Core", "0.00"),
    ("GDP_per_capita_USD", "NY.GDP.PCAP.CD", "GDP per capita (current US$)", "current US$", "context", "Core", "#,##0"),
    ("Exports_current_USD", "NE.EXP.GNFS.CD", "Exports of goods and services (current US$)", "current US$", "trade balance", "Core", "#,##0"),
    ("Exports_constant2015_USD", "NE.EXP.GNFS.KD", "Exports of goods and services (constant 2015 US$)", "constant 2015 US$", "export growth, CAGR, index", "Core", "#,##0"),
    ("Imports_current_USD", "NE.IMP.GNFS.CD", "Imports of goods and services (current US$)", "current US$", "trade balance", "Core", "#,##0"),
    ("Exports_pct_GDP", "NE.EXP.GNFS.ZS", "Exports of goods and services (% of GDP)", "% of GDP", "chart 1; H2", "Core", "0.00"),
    ("Imports_pct_GDP", "NE.IMP.GNFS.ZS", "Imports of goods and services (% of GDP)", "% of GDP", "cross-check", "Core", "0.00"),
    ("Trade_pct_GDP", "NE.TRD.GNFS.ZS", "Trade (% of GDP)", "% of GDP", "H1; chart 2 (trade openness)", "Core", "0.00"),
    ("FDI_inflows_USD", "BX.KLT.DINV.CD.WD", "Foreign direct investment, net inflows (BoP, current US$)", "current US$", "context", "Core", "#,##0"),
    ("FDI_pct_GDP", "BX.KLT.DINV.WD.GD.ZS", "Foreign direct investment, net inflows (% of GDP)", "% of GDP", "H3; chart 4", "Core", "0.00"),
    ("Manufacturing_VA_pct_GDP", "NV.IND.MANF.ZS", "Manufacturing, value added (% of GDP)", "% of GDP", "H2", "Core", "0.00"),
    ("CurrentAccount_pct_GDP", "BN.CAB.XOKA.GD.ZS", "Current account balance (% of GDP)", "% of GDP", "trade balance cross-check", "Optional A", "0.00"),
    ("Merchandise_exports_USD", "TX.VAL.MRCH.CD.WT", "Merchandise exports (current US$)", "current US$", "tests H2 more directly", "Optional B", "#,##0"),
]
NV = len(VARS)
DICT0 = 27  # first dictionary data row on README
VCOL = {v[0]: L(4 + i) for i, v in enumerate(VARS)}   # clean sheet column letters (D..Q)
VFMT = {v[0]: v[6] for v in VARS}
VCODE_CELL = {v[0]: f"{RD}!$C${DICT0 + i}" for i, v in enumerate(VARS)}

COUNTRIES = [("Hungary", "HUN"), ("Poland", "POL"), ("Czechia", "CZE"), ("Slovakia", "SVK")]
YEARS = list(range(2010, 2026))
N = 64
R0, R1 = 2, 65     # data rows on clean / calc


def blk(i):
    s = 2 + 16 * i
    return s, s + 15


# ------------------------------------------------------------------ 03_CLEAN_DATA
header(ws3, 1, ["Country", "Code", "Year"] + [v[0] for v in VARS], height=45)
ycol = f"{RW}!$E$1:$U$1"
for ci, (cn, cc) in enumerate(COUNTRIES):
    for yi, y in enumerate(YEARS):
        r = 2 + 16 * ci + yi
        put(ws3, f"A{r}", cn, BLUE); put(ws3, f"B{r}", cc, BLUE); put(ws3, f"C{r}", y, BLUE)
        for vi, v in enumerate(VARS):
            col = L(4 + vi)
            code = VCODE_CELL[v[0]]
            yr = f'INDEX({RW}!$E$2:$U${RAW_LAST},0,MATCH($C{r}&" [YR"&$C{r}&"]",{ycol},0))'
            f = (f'=IF(COUNTIFS({RW}!$B$2:$B${RAW_LAST},$B{r},{RW}!$D$2:$D${RAW_LAST},{code},{yr},">-1E+300")=0,"",'
                 f'SUMIFS({yr},{RW}!$B$2:$B${RAW_LAST},$B{r},{RW}!$D$2:$D${RAW_LAST},{code}))')
            put(ws3, f"{col}{r}", f, BLK, v[6])
ws3.freeze_panes = "D2"
for c in range(1, 4 + NV):
    ws3.column_dimensions[L(c)].width = 22 if c > 3 else 11
ws3.column_dimensions["A"].width = 12

# ------------------------------------------------------------------ 04_CALCULATIONS
header(ws4, 1, ["Country", "Code", "Year", "Export_growth_real_pct", "Trade_balance_pct_GDP",
                "Trade_openness_calc_pct", "Openness_check_diff (calc - WDI)", "Export_index_2010=100",
                "Period",
                "Flag_Export_growth", "Flag_GDP_growth", "Flag_FDI_pct_GDP", "Flag_Manufacturing",
                "Flag_Trade_balance", "Flag_Trade_openness"], height=48)
put(ws4, "Q1", "PARAMETERS (blue = input)", SEC)
put(ws4, "Q2", "IQR fence multiplier"); put(ws4, "R2", 1.5, BLUE, fill=YFILL)
put(ws4, "Q3", "Within-country |z| cutoff"); put(ws4, "R3", 2.5, BLUE, fill=YFILL)
put(ws4, "Q4", "Index base year"); put(ws4, "R4", 2010, BLUE, fill=YFILL)
put(ws4, "S2", "Outlier rule: flag if outside pooled Q1-k*IQR / Q3+k*IQR (64 obs) OR |z| > cutoff within country. Flagged, never removed.", NOTE)
put(ws4, "Q6", "BASE YEAR 2009 - constant-price exports (US$)", SEC)
put(ws4, "Q7", "Code", BOLD); put(ws4, "R7", "Exports 2009 (const 2015 US$)", BOLD)
put(ws4, "S7", "Used only as the denominator for 2010 export growth; 2009 is not in the analysis window.", NOTE)
KD = VCODE_CELL["Exports_constant2015_USD"]
for i, (cn, cc) in enumerate(COUNTRIES):
    r = 8 + i
    put(ws4, f"Q{r}", cc, BLUE)
    put(ws4, f"R{r}", f'=IF(COUNTIFS({RW}!$B$2:$B${RAW_LAST},Q{r},{RW}!$D$2:$D${RAW_LAST},{KD},{RW}!$E$2:$E${RAW_LAST},">-1E+300")=0,"",'
                      f'SUMIFS({RW}!$E$2:$E${RAW_LAST},{RW}!$B$2:$B${RAW_LAST},Q{r},{RW}!$D$2:$D${RAW_LAST},{KD}))', BLK, "#,##0")
put(ws4, "Q13", "POOLED IQR FENCES (2010-2025, 64 obs)", SEC)
header(ws4, 14, ["Variable", "Q1", "Q3", "Lower fence", "Upper fence"], col0=17)
FLAGS = [  # flag col, label, source sheet, source col, calc col in CA
    ("J", "Export growth", CA, "D"),
    ("K", "GDP growth", CL, VCOL["GDP_growth_pct"]),
    ("L", "FDI % GDP", CL, VCOL["FDI_pct_GDP"]),
    ("M", "Manufacturing VA % GDP", CL, VCOL["Manufacturing_VA_pct_GDP"]),
    ("N", "Trade balance % GDP", CA, "E"),
    ("O", "Trade % GDP", CL, VCOL["Trade_pct_GDP"]),
]
FENCE = {}
for k, (fc, lab, sh, sc) in enumerate(FLAGS):
    r = 15 + k
    FENCE[fc] = r
    rg = f"{sh}!${sc}${R0}:${sc}${R1}"
    put(ws4, f"Q{r}", lab)
    put(ws4, f"R{r}", f"=QUARTILE({rg},1)", BLK, "0.00")
    put(ws4, f"S{r}", f"=QUARTILE({rg},3)", BLK, "0.00")
    put(ws4, f"T{r}", f"=R{r}-$R$2*(S{r}-R{r})", BLK, "0.00")
    put(ws4, f"U{r}", f"=S{r}+$R$2*(S{r}-R{r})", BLK, "0.00")

for ci, (cn, cc) in enumerate(COUNTRIES):
    s, e = blk(ci)
    for r in range(s, e + 1):
        put(ws4, f"A{r}", f"={CL}!A{r}"); put(ws4, f"B{r}", f"={CL}!B{r}"); put(ws4, f"C{r}", f"={CL}!C{r}")
        kd = f"{CL}!{VCOL['Exports_constant2015_USD']}"
        put(ws4, f"D{r}",
            f'=IF(C{r}=2010,IF(OR({kd}{r}="",INDEX($R$8:$R$11,MATCH(B{r},$Q$8:$Q$11,0))=""),"",({kd}{r}/INDEX($R$8:$R$11,MATCH(B{r},$Q$8:$Q$11,0))-1)*100),'
            f'IF(OR({kd}{r}="",{kd}{r-1}=""),"",({kd}{r}/{kd}{r-1}-1)*100))', BLK, "0.00")
        ex, im, gd = (f"{CL}!{VCOL['Exports_current_USD']}{r}", f"{CL}!{VCOL['Imports_current_USD']}{r}", f"{CL}!{VCOL['GDP_current_USD']}{r}")
        put(ws4, f"E{r}", f'=IF(OR({ex}="",{im}="",{gd}=""),"",({ex}-{im})/{gd}*100)', BLK, "0.00")
        put(ws4, f"F{r}", f'=IF(OR({ex}="",{im}="",{gd}=""),"",({ex}+{im})/{gd}*100)', BLK, "0.00")
        tr = f"{CL}!{VCOL['Trade_pct_GDP']}{r}"
        put(ws4, f"G{r}", f'=IF(OR(F{r}="",{tr}=""),"",F{r}-{tr})', BLK, "0.0000000000")
        kdc = VCOL['Exports_constant2015_USD']
        put(ws4, f"H{r}", f'=IF({kd}{r}="","",{kd}{r}/SUMIFS({CL}!${kdc}${R0}:${kdc}${R1},{CL}!$B${R0}:$B${R1},B{r},{CL}!$C${R0}:$C${R1},$R$4)*100)', BLK, "0.0")
        put(ws4, f"I{r}", f'=IF(C{r}<=2019,"Pre-COVID (2010-2019)",IF(C{r}<=2021,"COVID (2020-2021)","Post-COVID (2022-2025)"))')
        for fc, lab, sh, sc in FLAGS:
            x = f"{sh}!{sc}{r}"
            blkr = f"{sh}!${sc}${s}:${sc}${e}"
            fr = FENCE[fc]
            reb = '&IF($C{r}=2010," Rebound","")'.format(r=r) if fc == "J" else ""
            put(ws4, f"{fc}{r}",
                f'=IF({x}="","MISSING",TRIM(IF(OR({x}<$T${fr},{x}>$U${fr}),"IQR ","")&IF(ABS(({x}-AVERAGE({blkr}))/STDEV({blkr}))>$R$3," Z","")' + reb + '))')
ws4.freeze_panes = "D2"
for c, w in zip("ABCDEFGHI", [12, 7, 7, 16, 16, 16, 18, 14, 22]):
    ws4.column_dimensions[c].width = w
for c in "JKLMNO":
    ws4.column_dimensions[c].width = 14
ws4.column_dimensions["Q"].width = 40
for c in "RSTU":
    ws4.column_dimensions[c].width = 16

# ------------------------------------------------------------------ 05_CHARTS
put(ws5, "A1", "05_CHARTS", TITLE)
put(ws5, "A3", "Placeholder. The 8 charts are built in Phase 4 (charts and interpretation), from 03_CLEAN_DATA and 04_CALCULATIONS.", BLK)

# ------------------------------------------------------------------ 06_SUMMARY
S = ws6
put(S, "A1", "06_SUMMARY - data quality, descriptive statistics, correlation, frozen-rule checks", TITLE)
put(S, "A2", "All figures are live formulas on 03_CLEAN_DATA / 04_CALCULATIONS. Mechanical results only: interpretation is Phase 4. Association language only, no causal claims.", NOTE)


def cl(v):  # clean-sheet full range for variable name
    c = VCOL[v]; return f"{CL}!${c}${R0}:${c}${R1}"


def clb(v, i):
    c = VCOL[v]; s, e = blk(i); return f"{CL}!${c}${s}:${c}${e}"


def cab(col, i):
    s, e = blk(i); return f"{CA}!${col}${s}:${col}${e}"


def caall(col):
    return f"{CA}!${col}${R0}:${col}${R1}"


row = 4
# ---- S1 data quality
put(S, f"A{row}", "1. DATA-QUALITY TABLE (analysis window 2010-2025: 4 countries x 16 years = 64 observations per variable)", SEC); row += 1
header(S, row, ["Variable", "WDI code", "Unit", "Missing values (of 64)", "Missing in raw file (of 68, incl. 2009)",
                "Available period", "Source (per WDI metadata)", "Missing HUN", "Missing POL", "Missing CZE", "Missing SVK",
                "Outlier flags (count)", "Notes"], height=48)
SRC = {
    "NY.GDP.MKTP.CD": "National statistical offices; OECD national accounts; World Bank staff estimates",
    "NY.GDP.MKTP.KD.ZG": "National statistical offices; OECD national accounts; World Bank staff estimates",
    "NY.GDP.PCAP.CD": "National statistical offices; OECD national accounts; World Bank staff estimates",
    "NE.EXP.GNFS.CD": "National statistical offices; central banks; World Bank staff estimates",
    "NE.EXP.GNFS.KD": "National statistical offices; OECD national accounts; World Bank staff estimates",
    "NE.IMP.GNFS.CD": "National statistical offices; central banks; World Bank staff estimates",
    "NE.EXP.GNFS.ZS": "National statistical offices; central banks; World Bank staff estimates",
    "NE.IMP.GNFS.ZS": "National statistical offices; central banks; World Bank staff estimates",
    "NE.TRD.GNFS.ZS": "National statistical offices; OECD national accounts; World Bank staff estimates",
    "BX.KLT.DINV.CD.WD": "IMF Balance of Payments; UNCTAD; official national sources",
    "BX.KLT.DINV.WD.GD.ZS": "IMF IFS / Balance of Payments; World Bank and OECD GDP estimates",
    "NV.IND.MANF.ZS": "National statistical offices; central banks; World Bank staff estimates",
    "BN.CAB.XOKA.GD.ZS": "IMF Balance of Payments Statistics; World Bank; OECD",
    "TX.VAL.MRCH.CD.WT": "World Trade Organization (WTO)",
}
NOTES = {
    "NY.GDP.MKTP.CD": "Current US$: moves with exchange rates, not only real growth.",
    "NY.GDP.MKTP.KD.ZG": "2020 flagged for CZE and HUN (COVID contraction). Kept.",
    "NY.GDP.PCAP.CD": "Current US$ (exchange-rate sensitive). Level series: not flagged.",
    "NE.EXP.GNFS.CD": "Level series: not flagged (Poland is simply the largest economy).",
    "NE.EXP.GNFS.KD": "Constant 2015 US$ (base year 2015). Source of real export growth, CAGR and index.",
    "NE.IMP.GNFS.CD": "Level series: not flagged (size effect, Poland largest).",
    "NE.EXP.GNFS.ZS": "Equals Exports_current_USD / GDP_current_USD x 100 (verified). Trade intensity, not competitiveness.",
    "NE.IMP.GNFS.ZS": "Equals Imports_current_USD / GDP_current_USD x 100 (verified).",
    "NE.TRD.GNFS.ZS": "Equals Exports % + Imports % (verified, difference ~1e-13).",
    "BX.KLT.DINV.CD.WD": "Hungary swings between about -US$71bn and +US$167bn: BoP / special-purpose-entity effects. Flagged, kept.",
    "BX.KLT.DINV.WD.GD.ZS": "Hungary ranges from about -40% to +106% of GDP. Dominates any pooled FDI result. Flagged, kept; see sensitivity in section 6.",
    "NV.IND.MANF.ZS": "CZE 2015-2016 flagged on pooled IQR (highest manufacturing share). Kept.",
    "BN.CAB.XOKA.GD.ZS": "Not flagged by the workbook rule. HUN and SVK 2022 are the weakest years (about -8.8% and -9.6% of GDP).",
    "TX.VAL.MRCH.CD.WT": "WTO basis. Exceeds total goods-and-services exports for Czechia in 14 of 16 years (compilation basis differs from national accounts; cause not verified). Do not express as a share of total exports.",
}
dq0 = row + 1
for vi, v in enumerate(VARS):
    r = dq0 + vi
    name, code = v[0], v[1]
    put(S, f"A{r}", name, BLK); put(S, f"B{r}", f"={VCODE_CELL[name]}"); put(S, f"C{r}", v[3])
    put(S, f"D{r}", f"=ROWS({cl(name)})-COUNT({cl(name)})", BLK, "0")
    put(S, f"E{r}", f'=68-SUMPRODUCT(({RW}!$D$2:$D${RAW_LAST}=B{r})*ISNUMBER({RW}!$E$2:$U${RAW_LAST}))', BLK, "0")
    yr = f"{CL}!$C${R0}:$C${R1}"
    put(S, f"F{r}", f'=_xlfn.MINIFS({yr},{cl(name)},">-1E+300")&"-"&_xlfn.MAXIFS({yr},{cl(name)},">-1E+300")')
    put(S, f"G{r}", SRC[code], wrap=True)
    for ci in range(4):
        put(S, f"{L(8 + ci)}{r}", f"=16-COUNT({clb(name, ci)})", BLK, "0")
    put(S, f"M{r}", NOTES[code], wrap=True)
    # outlier count if a flag column exists
    flagmap = {"GDP_growth_pct": "K", "FDI_pct_GDP": "L", "Manufacturing_VA_pct_GDP": "M", "Trade_pct_GDP": "O"}
    if name in flagmap:
        put(S, f"L{r}", f'=COUNTIF({caall(flagmap[name])},"?*")-COUNTIF({caall(flagmap[name])},"MISSING")', BLK, "0")
    else:
        put(S, f"L{r}", "not flagged", NOTE)
r = dq0 + NV
put(S, f"A{r}", "TOTAL", BOLD); put(S, f"D{r}", f"=SUM(D{dq0}:D{r-1})", BOLD, "0"); put(S, f"E{r}", f"=SUM(E{dq0}:E{r-1})", BOLD, "0")
r += 1
put(S, f"A{r}", "Derived series flagged (04_CALCULATIONS):", BOLD)
put(S, f"D{r}", "Export growth", BLK); put(S, f"E{r}", f'=COUNTIF({caall("J")},"?*")-COUNTIF({caall("J")},"MISSING")', BLK, "0")
put(S, f"F{r}", "Trade balance % GDP", BLK); put(S, f"G{r}", f'=COUNTIF({caall("N")},"?*")-COUNTIF({caall("N")},"MISSING")', BLK, "0")
put(S, f"H{r}", "<- counts of flagged observations. All four 2010 export-growth values are tagged 'Rebound' (post-2009 recovery, per Design Lock) in 04_CALCULATIONS column J, in addition to statistical flags.", NOTE)
DQ_END = r
for rr in range(dq0, dq0 + NV):
    S.row_dimensions[rr].height = 40
row = r + 2

# ---- S2 integrity checks
put(S, f"A{row}", "2. INTEGRITY CHECKS", SEC); row += 1
header(S, row, ["Check", "Result", "Expected", "Status"], height=22); row += 1
gd, ex, im = cl("GDP_current_USD"), cl("Exports_current_USD"), cl("Imports_current_USD")
checks = [
    ("Observations in clean sheet", f"=COUNTA({CL}!$A${R0}:$A${R1})", 64, "eq"),
    ("Duplicate country-year keys", f"=SUMPRODUCT(--(COUNTIFS({CL}!$B${R0}:$B${R1},{CL}!$B${R0}:$B${R1},{CL}!$C${R0}:$C${R1},{CL}!$C${R0}:$C${R1})>1))", 0, "eq"),
    ("Max |Exports % GDP: computed - WDI|", f"=SUMPRODUCT(MAX(ABS({ex}/{gd}*100-{cl('Exports_pct_GDP')})))", 0, "tiny"),
    ("Max |Imports % GDP: computed - WDI|", f"=SUMPRODUCT(MAX(ABS({im}/{gd}*100-{cl('Imports_pct_GDP')})))", 0, "tiny"),
    ("Max |Trade openness: computed - WDI|", f"=MAX({caall('G')})-MIN({caall('G')})", 0, "tiny"),
    ("Max |Trade % - (Exports % + Imports %)|", f"=SUMPRODUCT(MAX(ABS({cl('Exports_pct_GDP')}+{cl('Imports_pct_GDP')}-{cl('Trade_pct_GDP')})))", 0, "tiny"),
    ("Max |FDI % GDP: computed - WDI|", f"=SUMPRODUCT(MAX(ABS({cl('FDI_inflows_USD')}/{gd}*100-{cl('FDI_pct_GDP')})))", 0, "tiny"),
    ("Obs where Merchandise exports > total G&S exports", f"=SUMPRODUCT(--({cl('Merchandise_exports_USD')}/{ex}>1))", 0, "info"),
    ("Total missing values (analysis window)", f"=D{dq0 + NV}", 0, "eq"),
]
for lab, f, exp, kind in checks:
    put(S, f"A{row}", lab); put(S, f"B{row}", f, BLK, "0.000000000000" if kind == "tiny" else "0"); put(S, f"C{row}", exp, BLUE)
    if kind == "eq":
        put(S, f"D{row}", f'=IF(B{row}=C{row},"OK","CHECK")')
    elif kind == "tiny":
        put(S, f"D{row}", f'=IF(ABS(B{row})<0.000001,"OK","CHECK")')
    else:
        put(S, f"D{row}", f'=IF(B{row}=C{row},"OK","FLAG (definitional - see notes)")')
    row += 1
row += 1

# ---- S3 descriptive statistics
put(S, f"A{row}", "3. DESCRIPTIVE STATISTICS PER COUNTRY (2010-2025). Mean shown next to median; nothing dropped.", SEC); row += 1
header(S, row, ["Variable", "Country", "Mean", "Median", "Min", "Max", "St. dev.", "2010 value", "Latest (2025)",
                "Change, latest - 2010 (own units / pp)", "% change (level/ratio series only)"], height=48); row += 1
STATV = [
    ("Exports % GDP", cl, "Exports_pct_GDP", True),
    ("Trade % GDP (openness)", cl, "Trade_pct_GDP", True),
    ("GDP growth %", cl, "GDP_growth_pct", False),
    ("Export growth, real %", None, "D", False),
    ("FDI net inflows % GDP", cl, "FDI_pct_GDP", False),
    ("Trade balance % GDP", None, "E", False),
    ("Manufacturing VA % GDP", cl, "Manufacturing_VA_pct_GDP", True),
    ("Current account % GDP", cl, "CurrentAccount_pct_GDP", False),
    ("GDP per capita, current US$", cl, "GDP_per_capita_USD", True),
]
for lab, fn, key, pc in STATV:
    for ci, (cn, cc) in enumerate(COUNTRIES):
        s, e = blk(ci)
        rg = clb(key, ci) if fn else cab(key, ci)
        src_sheet, src_col = (CL, VCOL[key]) if fn else (CA, key)
        fmt = "#,##0" if "US$" in lab else "0.00"
        put(S, f"A{row}", lab); put(S, f"B{row}", cc)
        put(S, f"C{row}", f"=AVERAGE({rg})", BLK, fmt); put(S, f"D{row}", f"=MEDIAN({rg})", BLK, fmt)
        put(S, f"E{row}", f"=MIN({rg})", BLK, fmt); put(S, f"F{row}", f"=MAX({rg})", BLK, fmt)
        put(S, f"G{row}", f"=STDEV({rg})", BLK, fmt)
        put(S, f"H{row}", f"={src_sheet}!{src_col}{s}", BLK, fmt); put(S, f"I{row}", f"={src_sheet}!{src_col}{e}", BLK, fmt)
        put(S, f"J{row}", f'=IF(OR(H{row}="",I{row}=""),"",I{row}-H{row})', BLK, fmt)
        if pc:
            put(S, f"K{row}", f'=IF(OR(H{row}="",I{row}=""),"",I{row}/H{row}-1)', BLK, "0.0%")
        else:
            put(S, f"K{row}", "n/a", NOTE)
        row += 1
put(S, f"A{row}", "Notes: 'Change' is in percentage points for ratio/growth series. Export growth '2010 value' is the rebound from the 2009 crisis (tagged Rebound). '% change' is shown only where it is meaningful.", NOTE)
row += 2

# ---- S4 CAGR
put(S, f"A{row}", "4. EXPORTS (CONSTANT 2015 US$): CAGR = (End/Begin)^(1/n) - 1", SEC); row += 1
yrow = row
put(S, f"A{yrow}", "Years (input):", BOLD)
put(S, f"B{yrow}", 2010, BLUE, fill=YFILL); put(S, f"C{yrow}", 2019, BLUE, fill=YFILL); put(S, f"D{yrow}", 2025, BLUE, fill=YFILL)
row += 1
header(S, row, ["Country", "Exports in year 1", "Exports in year 2", "Exports in year 3", "CAGR yr1-yr3 (full window)",
                "CAGR yr1-yr2 (pre-COVID)", "CAGR yr2-yr3 (2019 onward)", "Index in year 3 (2010=100)"], height=48); row += 1
kdc = VCOL["Exports_constant2015_USD"]
CAGR_ROWS = {}
for ci, (cn, cc) in enumerate(COUNTRIES):
    def at(ycell):
        return f"SUMIFS({CL}!${kdc}${R0}:${kdc}${R1},{CL}!$B${R0}:$B${R1},$A{row},{CL}!$C${R0}:$C${R1},{ycell})"
    put(S, f"A{row}", cc, BLUE)
    put(S, f"B{row}", "=" + at(f"$B${yrow}"), BLK, "#,##0"); put(S, f"C{row}", "=" + at(f"$C${yrow}"), BLK, "#,##0"); put(S, f"D{row}", "=" + at(f"$D${yrow}"), BLK, "#,##0")
    put(S, f"E{row}", f"=(D{row}/B{row})^(1/($D${yrow}-$B${yrow}))-1", BLK, "0.00%")
    put(S, f"F{row}", f"=(C{row}/B{row})^(1/($C${yrow}-$B${yrow}))-1", BLK, "0.00%")
    put(S, f"G{row}", f"=(D{row}/C{row})^(1/($D${yrow}-$C${yrow}))-1", BLK, "0.00%")
    put(S, f"H{row}", f"=D{row}/B{row}*100", BLK, "0.0")
    CAGR_ROWS[cc] = row
    row += 1
put(S, f"A{row}", "Caveat: the 2010 start year follows the 2009 crisis trough, so growth from 2010 includes rebound. CAGR is a single-number summary and hides the path.", NOTE)
row += 2

# ---- S5 period averages
put(S, f"A{row}", "5. PERIOD AVERAGES AND MEDIANS (pre-COVID 2010-2019 | COVID 2020-2021 | post-COVID 2022-2025)", SEC); row += 1
header(S, row, ["Variable", "Country", "Pre-COVID mean", "Pre-COVID median", "COVID mean", "COVID median", "Post-COVID mean",
                "Post-COVID median", "Pre-COVID mean excl. 2010 (sensitivity)"], height=48); row += 1
PERV = [
    ("Export growth, real %", None, "D"), ("GDP growth %", cl, "GDP_growth_pct"), ("Exports % GDP", cl, "Exports_pct_GDP"),
    ("Trade % GDP", cl, "Trade_pct_GDP"), ("FDI net inflows % GDP", cl, "FDI_pct_GDP"), ("Trade balance % GDP", None, "E"),
]
PRE_CELL = {}
for lab, fn, key in PERV:
    for ci, (cn, cc) in enumerate(COUNTRIES):
        s, e = blk(ci)
        sh, col = (CL, VCOL[key]) if fn else (CA, key)
        def sub(a, b):
            return f"{sh}!${col}${s + a}:${col}${s + b}"
        put(S, f"A{row}", lab); put(S, f"B{row}", cc)
        put(S, f"C{row}", f"=AVERAGE({sub(0, 9)})", BLK, "0.00"); put(S, f"D{row}", f"=MEDIAN({sub(0, 9)})", BLK, "0.00")
        put(S, f"E{row}", f"=AVERAGE({sub(10, 11)})", BLK, "0.00"); put(S, f"F{row}", f"=MEDIAN({sub(10, 11)})", BLK, "0.00")
        put(S, f"G{row}", f"=AVERAGE({sub(12, 15)})", BLK, "0.00"); put(S, f"H{row}", f"=MEDIAN({sub(12, 15)})", BLK, "0.00")
        put(S, f"I{row}", f"=AVERAGE({sub(1, 9)})", BLK, "0.00")
        PRE_CELL[(key, cc)] = f"C{row}"
        row += 1
put(S, f"A{row}", "COVID period has only 2 observations per country: the 'median' equals the mean. Treat period comparisons as descriptive.", NOTE)
row += 2

# ---- S6 correlation
put(S, f"A{row}", "6. CORRELATION (Pearson). Pooled = 64 country-year obs (not independent); within-country n = 16. Suggestive only.", SEC); row += 1
header(S, row, ["Pair", "Variable X", "Variable Y", "Pooled (n=64)", "HUN (n=16)", "POL (n=16)", "CZE (n=16)", "SVK (n=16)",
                "Sensitivity: pooled excl. HUN (n=48)"], height=48); row += 1
CV = [
    ("EG", "Export growth (real %)", CA, "D"),
    ("FDI", "FDI net inflows % GDP", CL, VCOL["FDI_pct_GDP"]),
    ("GDP", "GDP growth %", CL, VCOL["GDP_growth_pct"]),
    ("TRD", "Trade openness (Trade % GDP)", CL, VCOL["Trade_pct_GDP"]),
    ("MAN", "Manufacturing VA % GDP", CL, VCOL["Manufacturing_VA_pct_GDP"]),
    ("EXP", "Exports % GDP (added: needed by frozen H2 rule)", CL, VCOL["Exports_pct_GDP"]),
]
CVD = {k: (lab, sh, c) for k, lab, sh, c in CV}
CORR = {}
for a, b in itertools.combinations([k for k, *_ in CV], 2):
    la, sha, ca_ = CVD[a][0], CVD[a][1], CVD[a][2]
    lb, shb, cb_ = CVD[b][0], CVD[b][1], CVD[b][2]
    put(S, f"A{row}", f"{a} vs {b}"); put(S, f"B{row}", la); put(S, f"C{row}", lb)
    put(S, f"D{row}", f"=CORREL({sha}!${ca_}${R0}:${ca_}${R1},{shb}!${cb_}${R0}:${cb_}${R1})", BLK, "0.00")
    for ci in range(4):
        s, e = blk(ci)
        put(S, f"{L(5 + ci)}{row}", f"=CORREL({sha}!${ca_}${s}:${ca_}${e},{shb}!${cb_}${s}:${cb_}${e})", BLK, "0.00")
    put(S, f"I{row}", f"=CORREL({sha}!${ca_}$18:${ca_}${R1},{shb}!${cb_}$18:${cb_}${R1})", BLK, "0.00")
    CORR[(a, b)] = row
    row += 1
put(S, f"A{row}", "Rows 18-65 of the clean sheet = POL, CZE, SVK (HUN is the first country block). HUN FDI is extreme, so the ex-HUN column is a robustness check only; it does not replace the frozen pooled test.", NOTE)
row += 2

# ---- S7 frozen-rule checks
put(S, f"A{row}", "7. FROZEN HYPOTHESIS RULES (Phase1_Design_Lock.md, section 3) - MECHANICAL CHECK, NO INTERPRETATION", SEC); row += 1
put(S, f"A{row}", "Thresholds (inputs from the frozen rules):", BOLD); row += 1
put(S, f"A{row}", "H1: minimum years above POL (of 16)"); put(S, f"B{row}", 14, BLUE, fill=YFILL); T_H1 = f"$B${row}"; row += 1
put(S, f"A{row}", "H2: minimum pooled correlation"); put(S, f"B{row}", 0.3, BLUE, fill=YFILL); T_H2 = f"$B${row}"; row += 1
put(S, f"A{row}", "H3: minimum countries with positive within-country correlation (of 4)"); put(S, f"B{row}", 3, BLUE, fill=YFILL); T_H3 = f"$B${row}"; row += 1
put(S, f"A{row}", "H4: COVID year / recovery year"); put(S, f"B{row}", 2020, BLUE, fill=YFILL); put(S, f"C{row}", 2021, BLUE, fill=YFILL); Y20 = f"$B${row}"; Y21 = f"$C${row}"; row += 2

# H1
put(S, f"A{row}", "H1 - Smaller economies (HUN, SVK) have higher trade-to-GDP than POL", BOLD); row += 1
header(S, row, ["Measure", "HUN", "POL", "CZE (extra, not in test)", "SVK"], height=30); row += 1
trade = [clb("Trade_pct_GDP", i) for i in range(4)]
put(S, f"A{row}", "Mean Trade % GDP 2010-2025")
for ci, col in enumerate(["B", "C", "D", "E"]):
    put(S, f"{col}{row}", f"=AVERAGE({trade[ci]})", BLK, "0.00")
rm = row; row += 1
put(S, f"A{row}", "Years above POL (of 16)")
for ci, col in enumerate(["B", "C", "D", "E"]):
    if ci == 1:
        put(S, f"{col}{row}", "n/a", NOTE)
    else:
        put(S, f"{col}{row}", f"=SUMPRODUCT(--({trade[ci]}>{trade[1]}))", BLK, "0")
ry = row; row += 1
put(S, f"A{row}", "H1 result (HUN and SVK)", BOLD)
put(S, f"B{row}", f'=IF(AND(B{rm}>C{rm},E{rm}>C{rm},B{ry}>={T_H1},E{ry}>={T_H1}),"SUPPORTED","NOT SUPPORTED")', BOLD)
H1R = row; row += 2

# H2
put(S, f"A{row}", "H2 - Manufacturing-intensive economies show stronger export performance", BOLD); row += 1
header(S, row, ["Measure", "HUN", "POL", "CZE", "SVK"], height=22); row += 1
put(S, f"A{row}", "Mean Manufacturing VA % GDP")
for ci, col in enumerate("BCDE"):
    put(S, f"{col}{row}", f"=AVERAGE({clb('Manufacturing_VA_pct_GDP', ci)})", BLK, "0.00")
rmm = row; row += 1
put(S, f"A{row}", "Mean Exports % GDP")
for ci, col in enumerate("BCDE"):
    put(S, f"{col}{row}", f"=AVERAGE({clb('Exports_pct_GDP', ci)})", BLK, "0.00")
rme = row; row += 1
put(S, f"A{row}", "Rank by manufacturing (1 = highest)")
for col in "BCDE":
    put(S, f"{col}{row}", f"=RANK({col}{rmm},$B${rmm}:$E${rmm})", BLK, "0")
rrm = row; row += 1
put(S, f"A{row}", "Rank by exports % GDP (1 = highest)")
for col in "BCDE":
    put(S, f"{col}{row}", f"=RANK({col}{rme},$B${rme}:$E${rme})", BLK, "0")
rre = row; row += 1
put(S, f"A{row}", "Pooled correlation: manufacturing vs exports % GDP"); put(S, f"B{row}", f"=D{CORR[('MAN','EXP')]}", BLK, "0.00"); rc2 = row; row += 1
put(S, f"A{row}", "Rankings identical?")
put(S, f"B{row}", f'=IF(AND(B{rrm}=B{rre},C{rrm}=C{rre},D{rrm}=D{rre},E{rrm}=E{rre}),"YES","NO")'); rrk = row; row += 1
put(S, f"A{row}", "H2 result", BOLD)
put(S, f"B{row}", f'=IF(AND(B{rc2}>0,B{rc2}>={T_H2},B{rrk}="YES"),"SUPPORTED","NOT SUPPORTED")', BOLD); H2R = row; row += 2

# H3
put(S, f"A{row}", "H3 - Higher FDI inflows associated with stronger export performance (same year, no lag)", BOLD); row += 1
header(S, row, ["Measure", "Pooled", "HUN", "POL", "CZE", "SVK"], height=22); row += 1
cr = CORR[("EG", "FDI")]
put(S, f"A{row}", "Correlation: FDI % GDP vs export growth")
put(S, f"B{row}", f"=D{cr}", BLK, "0.00")
for ci, col in enumerate("CDEF"):
    put(S, f"{col}{row}", f"={L(5 + ci)}{cr}", BLK, "0.00")
r3 = row; row += 1
put(S, f"A{row}", "Countries with positive within-country correlation (of 4)"); put(S, f"B{row}", f'=COUNTIF(C{r3}:F{r3},">0")', BLK, "0"); rn3 = row; row += 1
put(S, f"A{row}", "Supplementary (not part of the frozen test): pooled excl. HUN"); put(S, f"B{row}", f"=I{cr}", BLK, "0.00"); row += 1
put(S, f"A{row}", "H3 result", BOLD)
put(S, f"B{row}", f'=IF(AND(B{r3}>0,B{rn3}>={T_H3}),"SUPPORTED","NOT SUPPORTED")', BOLD); H3R = row; row += 2

# H4
put(S, f"A{row}", "H4 - COVID-19 disruption followed by recovery (export growth, constant prices)", BOLD); row += 1
header(S, row, ["Measure", "HUN", "POL", "CZE", "SVK"], height=22); row += 1
put(S, f"A{row}", "Export growth in COVID year (2020), %")
for ci, col in enumerate("BCDE"):
    put(S, f"{col}{row}", f"=SUMIFS({caall('D')},{caall('B')},\"{COUNTRIES[ci][1]}\",{caall('C')},{Y20})", BLK, "0.00")
r20 = row; row += 1
put(S, f"A{row}", "Export growth in recovery year (2021), %")
for ci, col in enumerate("BCDE"):
    put(S, f"{col}{row}", f"=SUMIFS({caall('D')},{caall('B')},\"{COUNTRIES[ci][1]}\",{caall('C')},{Y21})", BLK, "0.00")
r21 = row; row += 1
put(S, f"A{row}", "Mean export growth 2010-2019 (incl. 2010 rebound, as frozen), %")
for ci, col in enumerate("BCDE"):
    put(S, f"{col}{row}", f"={PRE_CELL[('D', COUNTRIES[ci][1])]}", BLK, "0.00")
rpre = row; row += 1
put(S, f"A{row}", "2020 negative?")
for col in "BCDE":
    put(S, f"{col}{row}", f'=IF({col}{r20}<0,"YES","NO")')
rn = row; row += 1
put(S, f"A{row}", "2021 positive and above 2010-2019 mean?")
for col in "BCDE":
    put(S, f"{col}{row}", f'=IF(AND({col}{r21}>0,{col}{r21}>{col}{rpre}),"YES","NO")')
rr_ = row; row += 1
put(S, f"A{row}", "H4 result", BOLD)
put(S, f"B{row}", f'=IF(AND(COUNTIF(B{rn}:E{rn},"YES")=4,COUNTIF(B{rr_}:E{rr_},"YES")=4),"SUPPORTED","NOT SUPPORTED")', BOLD); H4R = row; row += 2

put(S, f"A{row}", "RULE RESULTS AT A GLANCE", SEC); row += 1
for lab, rr in (("H1", H1R), ("H2", H2R), ("H3", H3R), ("H4", H4R)):
    put(S, f"A{row}", lab, BOLD); put(S, f"B{row}", f"=B{rr}", BOLD); row += 1
put(S, f"A{row}", "These verdicts apply the pre-registered rules mechanically. They say nothing about causation; explanation and caveats come in Phase 4.", NOTE)
S.column_dimensions["A"].width = 46
for c, w in zip("BCDEFGHIJKLM", [20, 24, 16, 18, 16, 28, 20, 18, 22, 18, 22, 70]):
    S.column_dimensions[c].width = w
S.freeze_panes = "A4"

# ------------------------------------------------------------------ 01_README
R = ws1
put(R, "A1", "Export Competitiveness and Economic Performance in Central Europe", TITLE)
put(R, "A2", "A Comparative Analysis of Hungary, Poland, Czechia and Slovakia - independent research project (not employer work)", BOLD)
info = [
    ("Research question", "How has export competitiveness evolved across Hungary, Poland, Czechia and Slovakia since 2010, and what economic factors help explain differences in their trade performance?"),
    ("Countries", "Hungary (HUN), Poland (POL), Czechia (CZE), Slovakia (SVK). WDI names: Hungary, Poland, Czechia, Slovak Republic; standardised to Slovakia in the clean sheet."),
    ("Analysis window", "2010-2025 annual = 64 country-year observations. 2009 is downloaded as a base year only (for 2010 export growth)."),
    ("Author", "Ghulam Mustafa"),
    ("Source", "World Bank, World Development Indicators (databank.worldbank.org), downloaded as CSV by the author."),
    ("Raw file", "3ed9e304-4fec-4c09-ab92-21d2d709e1a1_Data.csv (copied unchanged into 02_RAW_DATA)."),
    ("WDI last updated", "10/08/2026 as printed in the file footer. The day/month order is not stated in the file; confirm on DataBank before citing."),
    ("Workbook last updated", "25 October 2026 (Phase 3)"),
    ("Missing data rule", "Missing values stay missing (blank) and are reported in 06_SUMMARY section 1. Nothing is estimated or filled. Outliers are flagged, never dropped."),
    ("Colour code", "Blue text = hard-coded input (raw values, keys, parameters). Black text = formula. Yellow fill = adjustable parameter."),
]
for i, (k, v) in enumerate(info):
    put(R, f"A{4 + i}", k, BOLD); put(R, f"B{4 + i}", v, wrap=True)
    R.merge_cells(f"B{4 + i}:G{4 + i}"); R.row_dimensions[4 + i].height = 30
put(R, "A15", "Sheet guide", SEC)
guide = [("01_README", "This sheet: scope, sources, variable dictionary, definitions."),
         ("02_RAW_DATA", "Original WDI download, untouched (values and footer exactly as in the CSV)."),
         ("03_CLEAN_DATA", "Long format, Country | Code | Year | 14 variables. Every cell is a formula that looks up 02_RAW_DATA; blank = missing."),
         ("04_CALCULATIONS", "Row-level indicators (export growth, trade balance, openness check, export index), period labels, outlier flags."),
         ("05_CHARTS", "Placeholder for Phase 4."),
         ("06_SUMMARY", "Data-quality table, integrity checks, descriptive statistics, CAGR, period averages, correlation, frozen-rule checks.")]
for i, (k, v) in enumerate(guide):
    put(R, f"A{16 + i}", k, BOLD); put(R, f"B{16 + i}", v); R.merge_cells(f"B{16 + i}:G{16 + i}")
put(R, "A23", "Calculated indicators (04_CALCULATIONS / 06_SUMMARY)", SEC)
put(R, "A24", "Export growth (real %) = (Exports_const_t / Exports_const_t-1 - 1) x 100, constant 2015 US$. | Trade balance % GDP = (Exports - Imports) / GDP x 100 (current US$). | "
              "Trade openness = (Exports + Imports) / GDP x 100, checked against WDI Trade % GDP. | CAGR = (End/Begin)^(1/n) - 1. | Export index = Exports_const_t / Exports_const_2010 x 100.", wrap=True)
R.merge_cells("A24:G24"); R.row_dimensions[24].height = 55
put(R, "A26", "#", HDR, fill=HFILL)
header(R, 26, ["#", "Clean-sheet variable", "WDI code", "WDI series name (as in file)", "Unit", "Role", "Tier"])
for i, v in enumerate(VARS):
    r = DICT0 + i
    put(R, f"A{r}", i + 1, BLK); put(R, f"B{r}", v[0], BLK); put(R, f"C{r}", v[1], BLUE)
    put(R, f"D{r}", v[2]); put(R, f"E{r}", v[3]); put(R, f"F{r}", v[4]); put(R, f"G{r}", v[5])
put(R, f"A{DICT0 + NV + 1}", "Codes in column C drive the lookups in 03_CLEAN_DATA. All 14 codes and names were matched against the Series metadata file (see Phase 3 log).", NOTE)
R.column_dimensions["A"].width = 22
for c, w in zip("BCDEFG", [28, 22, 56, 18, 28, 12]):
    R.column_dimensions[c].width = w

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = True
wb.save(OUT)
print("saved", OUT)
