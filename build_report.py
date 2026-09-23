"""Build publishable PDF project report — SaaS Sprawl"""
import json, os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, ListFlowable, ListItem, KeepTogether)
from reportlab.lib.colors import HexColor

BASE = "/home/user/saas-sprawl-project"
IMG = BASE + "/images/"
with open(BASE+"/metrics.json") as f:
    M = json.load(f)

OUT = BASE + "/Mohammad_Ayan_Ansari_SaaS_Sprawl_Project_Report.pdf"

NAVY = HexColor("#1f4e79"); BLUE = HexColor("#2e75b6"); LIGHT = HexColor("#d9e2f3")
GREY = HexColor("#f2f2f2"); RED = HexColor("#c00000"); GREEN = HexColor("#375623")

styles = getSampleStyleSheet()
sTitle = ParagraphStyle("Title2", parent=styles["Title"], fontSize=26, leading=30, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
sSub = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=12, leading=16, textColor=HexColor("#404040"), alignment=TA_CENTER, spaceAfter=4)
sH1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=8, borderPadding=(0,0,4,0))
sH2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, leading=15, textColor=BLUE, spaceBefore=10, spaceAfter=6)
sBody = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
sBull = ParagraphStyle("Bull", parent=sBody, leftIndent=18, bulletIndent=8, alignment=TA_LEFT)
sCap = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=9, leading=12, textColor=HexColor("#595959"), alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
sCell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=8.5, leading=11)
sCellH = ParagraphStyle("CellH", parent=styles["Normal"], fontSize=8.5, leading=11, textColor=colors.white, fontName="Helvetica-Bold")
sCode = ParagraphStyle("Code", parent=styles["Code"], fontSize=7.5, leading=10, fontName="Courier", backColor=HexColor("#f5f5f5"))

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8); canvas.setFillColor(HexColor("#808080"))
    canvas.drawString(20*mm, 12*mm, "Cloud & SaaS Subscription Sprawl  |  Mohammad Ayan Ansari, IIT Madras")
    canvas.drawRightString(A4[0]-20*mm, 12*mm, f"Page {doc.page}")
    canvas.setStrokeColor(LIGHT); canvas.setLineWidth(0.6)
    canvas.line(20*mm, 14.5*mm, A4[0]-20*mm, 14.5*mm)
    canvas.restoreState()

def cover_header(canvas, doc):
    pass

def styled_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("BACKGROUND", (0,0), (-1,0), NAVY if header else GREY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white if header else colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, HexColor("#f7f9fc")]),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]
    t.setStyle(TableStyle(style))
    return t

def P(txt, style=sBody):
    return Paragraph(txt, style)

def img(path, w=6.4*inch, caption=""):
    elems = [Image(path, width=w, height=w*0.58, kind="proportional")]
    if caption:
        elems.append(P(f"<i>{caption}</i>", sCap))
    return elems

story = []

# ================= COVER =================
story += [Spacer(1, 0.7*inch)]
story.append(P("AICTE | IBM SkillsBuild", ParagraphStyle("top", parent=sSub, fontSize=11, textColor=BLUE, fontName="Helvetica-Bold")))
story.append(P("Data Analytics with AI — Internship Program 2026", ParagraphStyle("top2", parent=sSub, fontSize=11, textColor=BLUE)))
story.append(P("(17th August – 30th September 2026) · BharatCares", sSub))
story.append(HRFlowable(width="80%", thickness=1.5, color=NAVY, spaceAfter=14, spaceBefore=10, hAlign="CENTER"))
story.append(P("Cloud & SaaS<br/>Subscription Sprawl", sTitle))
story.append(P("An AI-Powered Business Intelligence Platform to Cut Waste,<br/>Kill Duplicate Tools & De-Risk Renewals", ParagraphStyle("tag", parent=sSub, fontSize=11, leading=15, textColor=HexColor("#333333"))))
story.append(Spacer(1, 0.25*inch))

info = [
    [P("<b>Student</b>", sCellH), P("Mohammad Ayan Ansari", sCell)],
    [P("<b>Institution</b>", sCellH), P("Indian Institute of Technology, Madras", sCell)],
    [P("<b>Trainer</b>", sCellH), P("Mr. Kartik Hooda (BharatCares)", sCell)],
    [P("<b>Focus Area</b>", sCellH), P("Data Analytics with AI: Foundation to Implementation", sCell)],
    [P("<b>Submission</b>", sCellH), P("Final Project — Code (.py) + requirements.txt + README.md + Report + GitHub", sCell)],
    [P("<b>Date</b>", sCellH), P("September 2026", sCell)],
]
t = Table(info, colWidths=[1.7*inch, 4.3*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), NAVY), ("TEXTCOLOR", (0,0), (0,-1), colors.white),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (1,0), (1,-1), [colors.white, HexColor("#f7f9fc")]),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(Spacer(1, 0.25*inch))
# KPI strip
kpi = [[P(f"<b><font color='#1f4e79'>${M['total_monthly']:,.0f}</font></b><br/>Monthly Spend", sCap),
        P(f"<b><font color='#c00000'>${M['total_waste_m']:,.0f}</font></b><br/>Monthly Waste (39.7%)", sCap),
        P(f"<b><font color='#1f4e79'>{M['accuracy']*100:.1f}%</font></b><br/>AI Accuracy", sCap),
        P(f"<b><font color='#c00000'>{M['n_high_risk']}</font></b><br/>High-Risk Renewals", sCap)]]
kt = Table(kpi, colWidths=[1.5*inch]*4)
kt.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1, NAVY), ("INNERGRID", (0,0), (-1,-1), 0.5, LIGHT),
    ("BACKGROUND", (0,0), (-1,-1), HexColor("#eaf1fb")), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
story.append(kt)
story.append(Spacer(1, 0.2*inch))
story.append(P("Original work. Masterclass learning dataset NOT used. Dataset: synthetic SaaS subscriptions (600 rows) modelled on real-world patterns.", ParagraphStyle("note", parent=sCap, fontSize=8)))
story.append(PageBreak())

# ================= TOC =================
story.append(P("Table of Contents", sH1))
toc_items = ["1. Abstract", "2. Introduction — Problem, Objectives & Scope", "3. Dataset Description",
    "4. Methodology — BI Framework & Tools", "5. Implementation", "6. Results — Dashboard Outputs (with UI Evidence)",
    "7. AI Model Evaluation", "8. Business Insights — Risk, Opportunity & Action", "9. Code Snapshot (Single-File App)",
    "10. Conclusion & Future Scope", "11. References", "Appendix A — How to Run", "Appendix B — Submission Checklist & Declaration"]
for it in toc_items:
    story.append(P(f"• &nbsp;{it}", ParagraphStyle("toc", parent=sBody, leftIndent=12, spaceAfter=3, alignment=TA_LEFT)))
story.append(Spacer(1,0.15*inch))
story.append(P("List of Figures", sH2))
figs = ["Fig 1 — Monthly Spend by Category", "Fig 2 — Spend by Department", "Fig 3 — Utilization Distribution (waste zone)",
    "Fig 4 — Top 15 Tools by Waste", "Fig 5 — Renewal Risk Split", "Fig 6 — 12-Month Spend Trend",
    "Fig 7 — Utilization vs Waste Scatter", "Fig 8 — Tool Overlap (duplicate stacks)", "Fig 9 — Confusion Matrix (97.5% acc.)",
    "Fig 10 — Feature Importance (waste drivers)"]
for i,f in enumerate(figs,1):
    story.append(P(f"• &nbsp;{f}", ParagraphStyle("tof", parent=sBody, leftIndent=12, spaceAfter=2, alignment=TA_LEFT, fontSize=9.5)))

# ================= ABSTRACT =================
story.append(P("1. Abstract", sH1))
story.append(P("Enterprises now run on dozens of SaaS and cloud subscriptions. Without governance this creates <b>subscription sprawl</b>: unused seats, duplicate tools doing the same job, forgotten auto-renewals and surprise bills. Industry studies estimate 30–35% of SaaS spend is wasted. This project builds an <b>AI-powered Business Intelligence platform</b> that converts 600 raw SaaS subscriptions into executive decisions.", sBody))
story.append(P(f"On our dataset the platform finds <b>${M['total_monthly']:,.0f}/month total spend</b> with <b>${M['total_waste_m']:,.0f}/month (39.7%) wasted</b> on {M['n_waste']} underutilized subscriptions, average utilization of only <b>{M['avg_util']:.1f}%</b>, and <b>{M['n_high_risk']} high-risk auto-renewals</b>. A <b>Random Forest classifier (97.5% accuracy)</b> predicts wasteful subscriptions before money is locked in. A 5-page Streamlit app (single <b>app.py</b> file) delivers KPIs, trends, risk tables and a 30-60-90-day savings playbook worth an estimated <b>${M['total_waste_m']*12*0.6:,.0f}/year</b> at 60% waste recovery.", sBody))
story.append(P("<b>Keywords:</b> SaaS sprawl, FinOps, business intelligence, churn/renewal risk, Random Forest, Streamlit, IBM SkillsBuild.", sBody))

# ================= INTRO =================
story.append(P("2. Introduction", sH1))
story.append(P("2.1 Background", sH2))
story.append(P("Data analytics, data science and visualization converge on one goal: converting data into <b>dashboards that drive actions</b>. With AI, we go further — AI cleans data, performs EDA, builds prediction models and generates full-stack apps (as learned with <b>IBM BOB</b> in Masterclass 4). This project applies that pipeline to a real FinOps pain: SaaS sprawl.", sBody))
story.append(P("Typical enterprise symptoms: (a) Engineering pays for Jira + Asana + Trello + Notion simultaneously; (b) Sales holds 200 Salesforce seats but uses 90; (c) auto-renew fires on a dormant $40k/yr contract; (d) nobody owns AWS dev servers left running. Finance sees the bill; nobody sees the <i>why</i>.", sBody))
story.append(P("2.2 Problem Statement", sH2))
story.append(P("<b>How can an organization identify, quantify and eliminate Cloud & SaaS subscription waste — and prevent risky renewals — using an AI-powered BI platform?</b> Sub-questions: What are the top KPIs? Which categories/departments/tools waste most? Which renewals are risky? Can AI predict waste at purchase time?", sBody))
story.append(P("2.3 Objectives", sH2))
for b in ["Define and track <b>Top KPIs</b>: Monthly/Annual Spend, Waste $, Utilization %, Active Subs, High-Risk Renewals.",
    "Reveal <b>trends & drivers</b>: spend growth, category/department hotspots, dormancy and over-licensing causes.",
    "Score every subscription for <b>renewal risk (High/Medium/Low)</b> and list ≤90-day actions.",
    "Build a <b>waste-prediction model (target ≥90% accuracy)</b> with explainable drivers.",
    "Deliver a <b>single-file BI app</b> (frontend + backend + ML) with Fact → Insight → Opportunity → Action board."]:
    story.append(P(f"• &nbsp;{b}", sBull))
story.append(P("2.4 Scope & Constraints", sH2))
story.append(P("In scope: 600-subscription synthetic dataset (12 categories, 8 departments); descriptive + predictive analytics; Streamlit decision app; savings playbook. Out of scope: real SSO/procurement integration, automated cancellation (human approval required). Constraint honoured: <b>masterclass learning dataset NOT used</b> — fully fresh data and analysis.", sBody))

# ================= DATASET =================
story.append(P("3. Dataset Description", sH1))
story.append(P("<b>Source:</b> <i>dataset_saas_sprawl.csv</i> — synthetic dataset generated for this project, modelling real-world SaaS patterns (seat-based pricing, annual discounts, cloud usage billing, dormancy). 600 rows × 22 columns. Patterns inspired by public Kaggle SaaS/subscription datasets. Dataset link is provided in README.md and the GitHub repository.", sBody))
cols_data = [
    ["Column", "Type", "Example", "Business Meaning"],
    ["Subscription_ID", "ID", "SUB0001", "Unique subscription"],
    ["Owner_ID / Department / Region", "Cat", "EMP1130 / Sales / West", "Who owns & where"],
    ["SaaS_Tool / Category", "Cat", "Slack / Communication", "What tool & job family"],
    ["Plan_Type", "Cat", "Annual", "Monthly / Annual / Enterprise"],
    ["Cost_Per_License_Month", "Num", "$25.00", "Seat price"],
    ["Licenses_Purchased / Used", "Num", "50 / 20", "Bought vs actually used"],
    ["Utilization_Pct", "Num", "40.0%", "Used ÷ Purchased — core KPI"],
    ["Last_Login_Days_Ago", "Num", "50", "Dormancy signal"],
    ["Renewal_Date / Days_to_Renewal", "Date/Num", "2026-11-02 / 40", "When money locks in"],
    ["Monthly_Spend / Annual_Contract_Value", "Num", "$1,250 / $12,750", "Spend KPIs"],
    ["Auto_Renew / Status", "Cat", "Yes / Active", "Risk flags"],
    ["Unused_Licenses / Waste_Monthly", "Num", "30 / $750", "Waste quantification"],
    ["Waste_Flag (target)", "0/1", "1", "1 if Util<40% & Active"],
    ["Renewal_Risk", "Cat", "High", "Rule score: util+dormancy+renewal+value"],
]
# wrap
wrapped = [[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate([["Column","Type","Example","Business Meaning"]] + cols_data[1:])]
# fix: cols_data already includes header; rebuild properly
hdr = ["Column","Type","Example","Business Meaning"]
body = cols_data[1:]
data_w = [[P(c, sCellH) for c in hdr]] + [[P(c, sCell) for c in row] for row in body]
story.append(styled_table(data_w, col_widths=[2.0*inch, 0.9*inch, 1.5*inch, 1.9*inch]))
story.append(P("Table 1 — Data dictionary (key columns).", sCap))
story.append(P("Descriptive snapshot (Active = 544 subs): 12 categories led by Project Management (86) and Data & Analytics (76); 8 departments; 72% auto-renew ON; 168 waste-flagged (28%). Full EDA is in Section 6.", sBody))

# ================= METHODOLOGY =================
story.append(P("4. Methodology — BI Framework & Tools", sH1))
story.append(P("4.1 Business Intelligence Process (taught framework)", sH2))
story.append(P("We move strictly <b>left → right: Data → Information → Insights → Decision → Action</b>. Every chart must end in an action; a simple project with a better decision beats a complex one with 50 charts. Hierarchy followed:", sBody))
hier = [["Level","Question","This Project"],
    ["L1 KPIs","What is happening?","Spend, Waste, Utilization, Active Subs, High-Risk count"],
    ["L2 Trends","Where is it going?","12-month spend vs waste growth; category/dept bars"],
    ["L3 Drivers","Why?","Over-licensing, dormancy, duplicate stacks, bulk hiring buys"],
    ["L4 Risk & Opportunity","What could go wrong / grow?","Risk score; consolidation & renegotiation upside"],
    ["L5 Action","What should mgmt do?","30-60-90 playbook + per-subscription next step"]]
story.append(styled_table([[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate(hier)], col_widths=[0.9*inch,1.7*inch,3.7*inch]))
story.append(P("Table 2 — BI hierarchy mapped to SaaS sprawl.", sCap))
story.append(P("4.2 Tools & Workflow", sH2))
story.append(P("Python + Pandas (cleaning/EDA) + Scikit-learn (Random Forest) + Streamlit/Plotly (app) + Matplotlib/Seaborn (report figures). Workflow mirrors the IBM BOB method: <b>plan KPIs → craft prompt → generate code → approve each step → combine into ONE file → generate report with UI evidence</b>. All libraries are pinned in <i>requirements.txt</i> so any evaluator can reproduce with <i>pip install -r requirements.txt; streamlit run app.py</i>.", sBody))
story.append(P("4.3 Risk Scoring & Waste Definition", sH2))
story.append(P("<b>Waste_Flag = 1</b> if Utilization &lt; 40% and Status = Active (standard FinOps shelfware threshold). <b>Renewal_Risk</b> rule score: +2 if util&lt;40 (+1 if &lt;60), +1 if dormant &gt;45 days, +2 if auto-renew=Yes and 0≤days-to-renewal≤90, +1 if annual value &gt;$20k. Total ≥4 → High, ≥2 → Medium, else Low. Transparent, auditable, and explainable to Finance.", sBody))

# ================= IMPLEMENTATION =================
story.append(P("5. Implementation", sH1))
story.append(P("5.1 Data Cleaning (AI-assisted)", sH2))
story.append(P("Parsed Renewal_Date to datetime; derived Days_to_Renewal vs 23-Sep-2026, Unused_Licenses, Waste_Monthly, Waste_Flag, Renewal_Risk; treated Cloud Infra as usage-billed (1 license, spend = metered); capped Last_Login at 180 days; no nulls in final set. Result: analysis-ready 600 × 22 table.", sBody))
story.append(P("5.2 Exploratory Analysis", sH2))
story.append(P("Grouped spend/waste by Category, Department, Tool; plotted utilization histogram with 40% waste zone; built 12-month trend (total vs wasted); mapped duplicate stacks (Communication, PM, Storage, CRM); scatter of utilization vs waste coloured by dormancy. Key outputs are Figures 1–8.", sBody))
story.append(P("5.3 Prediction Model", sH2))
story.append(P("Target Waste_Flag; 9 numeric + one-hot(Category, Plan_Type, Auto_Renew, Department) features; 80/20 stratified split (seed 42); <b>RandomForestClassifier (200 trees, max_depth 12, class_weight=balanced)</b>. Chosen for tabular data, imbalance handling and feature importance. Metrics in Section 7.", sBody))
story.append(P("5.4 Dashboard (Single-File App)", sH2))
story.append(P("<b>app.py</b> (~300 lines) contains backend + frontend + ML. Five pages: (1) Executive Overview — 6 KPI cards + 4 charts; (2) Cost & Product — top-waste tools, overlap map, bottom-25 action table; (3) Risk & Renewal — ≤90-day exposure, high-risk table + CSV download; (4) AI Predictor — live form + probability + recommendation; (5) Fact → Action Board — 5 decisions + 30-60-90 playbook. Sidebar filters (Department/Category/Risk) drive every page — each audience finds its answer fast.", sBody))

# ================= RESULTS =================
story.append(P("6. Results — Dashboard Outputs", sH1))
story.append(P("Headline KPIs (Active subscriptions, filters = All):", sH2))
kpi_rows = [["KPI","Value","Reading"],
    ["Monthly Spend", f"${M['total_monthly']:,.0f}", "Burn rate; ~$13.5M annualized run-rate"],
    ["Annual Contract Value", f"${M['total_annual']:,.0f}", "Committed contract base"],
    ["Monthly Waste", f"${M['total_waste_m']:,.0f} (39.7%)", "Unused seats — #1 savings lever"],
    ["Avg Utilization", f"{M['avg_util']:.1f}%", "10 pts below 70% healthy benchmark"],
    ["Active Subscriptions", f"{M['n_active']}", "544 of 600; rest inactive/cancelled"],
    ["High-Risk Renewals", f"{M['n_high_risk']}", "Auto-renew + dormant + ≤90 days"],
    ["Waste-flagged Subs", f"{M['n_waste']} (28%)", "Util <40% — downsize/cancel list"]]
story.append(styled_table([[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate(kpi_rows)], col_widths=[1.8*inch,1.7*inch,2.8*inch]))
story.append(P("Table 3 — Executive KPIs.", sCap))

for fname, title, desc in [
    ("img1_spend_by_category.png", "Fig 1 — Monthly Spend by Category", "Data & Analytics dominates at $412,852/mo (Snowflake/Tableau/Power BI seats at scale), followed by CRM & Sales ($173,870) and HR & Finance ($138,290). Seat-based categories dwarf metered Cloud Infra ($19,464) — so empty seats, not servers, are the #1 leak to fix first."),
    ("img2_spend_by_department.png", "Fig 2 — Spend by Department", "Engineering and Sales are the largest spenders — expected (dev tools + Salesforce seats) but also the largest wasters. HR/Finance are leanest. Chargeback by department makes owners accountable."),
    ("img3_utilization_hist.png", "Fig 3 — Utilization Distribution", "Bimodal: a healthy cluster at 70–99% and a waste spike at 5–40%. Mean 59.8%. The red zone (<40%) = 168 shelfware subscriptions. Anything left of the line is a downsize/cancel candidate."),
    ("img4_waste_by_tool.png", "Fig 4 — Top 15 Tools by Monthly Waste", "High seat-price × bulk buying = biggest leaks (Salesforce, Service suites, Adobe CC). Renegotiating top-5 tools alone recovers six figures monthly."),
    ("img5_renewal_risk.png", "Fig 5 — Renewal Risk Split", "High + Medium = majority of active subs. Only a minority is truly safe (Low). Risk is systemic, not a few bad buys — governance, not blame, is the fix."),
    ("img6_spend_trend.png", "Fig 6 — 12-Month Spend Trend", "Total spend +28% in 12 months; wasted spend grew faster (+32%), now ~40% of every dollar. Without action, waste compounds with growth — the core sprawl trap."),
    ("img7_util_vs_waste.png", "Fig 7 — Utilization vs Waste", "Classic L-shape: waste explodes below 40% utilization, and darker dots (dormant 60–180 days) sit exactly there. Dormancy + low util = certain waste — the model's two strongest signals."),
    ("img8_tool_overlap.png", "Fig 8 — Tool Overlap (Duplicates)", "Communication: Slack + Teams + Zoom + Workspace in parallel. PM: Jira + Asana + Trello + Notion + Monday. Storage: Dropbox + Box + OneDrive. Each overlap = double licences + split knowledge. Consolidation to one stack per job family is the structural fix."),
]:
    story.append(P(title, sH2))
    for el in img(IMG+fname, caption=title):
        story.append(el)
    story.append(P(desc, sBody))

# ================= MODEL EVAL =================
story.append(P("7. AI Model Evaluation", sH1))
story.append(P("Random Forest waste classifier — test set (n=120, stratified 20% holdout):", sBody))
met = [["Metric (Waste class)","Score","Interpretation"],
    ["Accuracy", f"{M['accuracy']*100:.1f}%", "Overall correctness — exceeds 90% target"],
    ["Precision", f"{M['precision_waste']*100:.1f}%", "When flagged wasteful, right 94% of time (few false alarms)"],
    ["Recall", f"{M['recall_waste']*100:.1f}%", "Catches 97% of all real waste (almost nothing slips)"],
    ["F1-Score", f"{M['f1_waste']*100:.1f}%", "Balanced excellence"]]
story.append(styled_table([[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate(met)], col_widths=[1.7*inch,1.1*inch,3.5*inch]))
story.append(P("Table 4 — Model metrics.", sCap))
story.append(P("Fig 9 — Confusion Matrix", sH2))
for el in img(IMG+"img9_confusion_matrix.png", w=4.6*inch, caption="Fig 9 — Confusion matrix: only ~3 errors in 120 test cases."):
    story.append(el)
story.append(P("The matrix shows near-perfect separation: efficient vs wasteful subscriptions are distinguished by utilization, unused seats and dormancy — exactly the signals Finance can act on.", sBody))
story.append(P("Fig 10 — Feature Importance (Why Waste Happens)", sH2))
for el in img(IMG+"img10_feature_importance.png", caption="Fig 10 — Top waste drivers: Utilization_Pct, Unused_Licenses, Licenses_Used dominate."):
    story.append(el)
story.append(P("Explainability matters: the model's top drivers are the same levers management controls (buy fewer seats, revoke dormant ones). This alignment is why the predictor is trusted — and why Page 4 of the app shows probability + recommended action for every new purchase.", sBody))

# ================= INSIGHTS =================
story.append(P("8. Business Insights — Risk, Opportunity & Action", sH1))
story.append(P("Following the taught mantra — <b>start from Fact, end on Action</b> — the platform's five board decisions:", sBody))
board = [
    ["#","Fact","Insight","Opportunity","Action"],
    ["1", f"${M['total_waste_m']:,.0f}/mo wasted (39.7%)", "28% subs <40% utilized; seats bought, never used", f"Save ${M['total_waste_m']*12*0.6:,.0f}/yr at 60% recovery", "Downsize bottom-50 subs next cycle; 75% util auto-alert"],
    ["2", f"{M['n_high_risk']} high-risk renewals", "Auto-renew ON + dormant + ≤90 days", "Renegotiate before lock-in", "Freeze auto-renew; owner re-justifies 7 days prior"],
    ["3", "4 chat + 5 PM tools live", "Slack+Teams+Zoom; Jira+Asana+Trello+Notion", "One suite per job family", "Standardize Teams + Jira; 60-day migration"],
    ["4", "Data & Analytics = top spend ($413k/mo)", "Snowflake/Tableau/Power BI seats bought in bulk; rarely revoked", "15–20% saving via seat reclaim + tier downgrades", "Owner tags per workspace; reclaim dormant analyst seats; annual-plan renegotiation"],
    ["5", "Sales+Eng waste most", "Bulk buys at hiring peaks; exit revokes missed", "Joiner-mover-leaver automation", "HR-exit webhook revokes in 24h; quarterly audit"],
]
bw = [0.25*inch, 1.25*inch, 1.5*inch, 1.35*inch, 1.95*inch]
story.append(styled_table([[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate(board)], col_widths=bw))
story.append(P("Table 5 — Fact → Insight → Opportunity → Action board (app Page 5).", sCap))
story.append(P("30-60-90-Day Playbook", sH2))
story.append(P("<b>30 days — Stop bleeding:</b> disable auto-renew on high-risk subs; reclaim zero-login seats; cancel duplicate Storage (keep OneDrive). <b>60 days — Consolidate:</b> single Communication + PM stack; resolve Salesforce/HubSpot overlap; cloud idle-stop policy. <b>90 days — Prevent regrowth:</b> procurement gate for new SaaS; quarterly utilization review; AI predictor scores every purchase request.", sBody))

# ================= CODE =================
story.append(P("9. Code Snapshot (Single-File App)", sH1))
story.append(P("Full code in <b>app.py</b> (single file: backend + frontend + ML, ~300 lines). Key excerpts:", sBody))
snippets = [
    ("a) KPI engine + filters (backend)", "fdf = active[active['Department'].isin(dept_f) & active['Category'].isin(cat_f)]\nK = dict(spend=fdf['Monthly_Spend'].sum(), waste=fdf['Waste_Monthly'].sum(),\n           util=fdf['Utilization_Pct'].mean(), high=(fdf['Renewal_Risk']=='High').sum())"),
    ("b) Model training (AI backend)", "X = pd.concat([df[FEATURES], pd.get_dummies(df[['Category','Plan_Type',\n    'Auto_Renew','Department']], drop_first=True)], axis=1)\nclf = RandomForestClassifier(n_estimators=200, max_depth=12,\n    random_state=42, class_weight='balanced')\nclf.fit(X_train, y_train)  # Accuracy 97.5%"),
    ("c) Frontend KPI cards (Streamlit)", "c1.metric('Monthly Spend', f\"${K['spend']:,.0f}\")\nc3.metric('Monthly Waste', f\"${K['waste']:,.0f}\", delta=f\"{waste_pct:.1f}% of spend\")\nfig = px.bar(cat, x='Monthly_Spend', y='Category', orientation='h')\nst.plotly_chart(fig, use_container_width=True)"),
    ("d) Live prediction (AI frontend)", "proba = clf.predict_proba(X_new)[0][1]\nif pred==1: st.error(f'WASTEFUL — {proba*100:.1f}%. Downsize {lp-lu} seats.')\nelse: st.success(f'EFFICIENT — {proba*100:.1f}% waste probability.')"),
]
for title, code in snippets:
    story.append(P(title, sH2))
    for line in code.split("\n"):
        story.append(P(line.replace(" ", "&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;", sCode))
    story.append(Spacer(1, 0.08*inch))
story.append(P("Reproduce: <i>pip install -r requirements.txt</i> then <i>streamlit run app.py → http://localhost:8501</i>. Dependencies pinned in requirements.txt; dataset beside app.py.", sBody))

# ================= CONCLUSION =================
story.append(P("10. Conclusion & Future Scope", sH1))
story.append(P("This project proves the masterclass thesis: <b>raw data → BI discipline → action</b>. With a simple 5-level framework, fresh data, and one Python file, we quantified a 39.7% SaaS waste leak, scored every renewal, predicted waste at 97.5% accuracy, and produced a board-ready savings playbook — favouring <b>clear decisions over complex charts</b>, exactly as taught.", sBody))
story.append(P("Future scope: (1) live connectors (Google Workspace / Azure AD / AWS Cost Explorer APIs); (2) renewal-date forecasting + price-benchmarking; (3) NLP on invoices to auto-detect shadow IT; (4) anomaly alerts (spend spike → Slack); (5) multi-tenant SaaS with role-based views; (6) LLM copilot answering 'why did Design spend jump 22%?' in plain English.", sBody))

# ================= REFERENCES =================
story.append(P("11. References", sH1))
refs = [
    "IBM SkillsBuild + BharatCares masterclasses 1–4 & project discussion (Aug–Sep 2026) — BI process, EDA, AI modelling, IBM BOB app building.",
    "Gartner / Flexera State of FinOps & SaaS Management reports — 30–35% SaaS waste benchmarks; shelfware and duplicate-tool patterns.",
    "Kaggle public SaaS / subscription / customer-churn datasets — pattern inspiration for synthetic data design (no masterclass data reused).",
    "Scikit-learn documentation — RandomForestClassifier, train_test_split, classification metrics.",
    "Streamlit & Plotly documentation — single-file BI app and interactive figures.",
]
for i,r in enumerate(refs,1):
    story.append(P(f"[{i}] &nbsp;{r}", sBull))

# ================= APPENDIX =================
story.append(P("Appendix A — How to Run (Evaluator Quick Start)", sH1))
steps = ["Download / clone the GitHub repo (contains app.py, requirements.txt, README.md, dataset_saas_sprawl.csv, this PDF).",
    "Install: <b>pip install -r requirements.txt</b> (Python 3.10+ recommended).",
    "Run: <b>streamlit run app.py</b> → open <b>http://localhost:8501</b>.",
    "Try: sidebar filters → Page 1 KPIs → Page 3 download high-risk CSV → Page 4 predict a new subscription.",
    "No internet / API keys needed. All 10 report figures regenerate via <i>python generate_images.py</i>."]
for s in steps:
    story.append(P(f"• &nbsp;{s}", sBull))
story.append(P("Appendix B — Submission Checklist & Declaration", sH1))
chk = [["Deliverable","File / Link","Status"],
    ["1. Code file (.py)", "app.py — single file, frontend+backend+ML", "✅ Ready"],
    ["2. Requirements (.txt)", "requirements.txt — 9 pinned libs", "✅ Ready"],
    ["3. Project report (.pdf)", "Mohammad_Ayan_Ansari_SaaS_Sprawl_Project_Report.pdf (this file)", "✅ Ready"],
    ["4. README (.md)", "README.md — overview + dataset link + run guide", "✅ Ready"],
    ["5. GitHub repo link", "Paste repo URL in form (all 4 files + dataset uploaded)", "⬜ Paste before submit"],
    ["Dataset link in README", "Repo path to dataset_saas_sprawl.csv", "⬜ Paste after upload"]]
story.append(styled_table([[P(c, sCellH if r==0 else sCell) for c in row] for r,row in enumerate(chk)], col_widths=[1.9*inch,2.9*inch,1.5*inch]))
story.append(P("Table 6 — Submission checklist.", sCap))
story.append(P("Declaration: I, <b>Mohammad Ayan Ansari (IIT Madras)</b>, declare this project is my original work for the IBM SkillsBuild Data Analytics with AI Internship 2026. The masterclass learning dataset was NOT used. All analysis, modelling, app code and documentation were produced for this submission with AI-assisted workflow guidance.", sBody))
story.append(Spacer(1,0.2*inch))
story.append(P("____________________________ &nbsp;&nbsp;&nbsp;&nbsp; Date: 23 September 2026<br/>Mohammad Ayan Ansari · IIT Madras", ParagraphStyle("sig", parent=sBody, alignment=TA_LEFT)))
story.append(Spacer(1,0.15*inch))
story.append(P("Acknowledgement: Thanks to Mr. Kartik Hooda, Mr. Himanshu Souda and the BharatCares / IBM SkillsBuild team for the BI framework, IBM BOB training and project guidance.", sBody))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm,
                        title="SaaS Subscription Sprawl — Project Report — Mohammad Ayan Ansari",
                        author="Mohammad Ayan Ansari, IIT Madras")
# build with footer on all pages except we accept cover also has footer (fine)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("PDF saved:", OUT, os.path.getsize(OUT)//1024, "KB")
