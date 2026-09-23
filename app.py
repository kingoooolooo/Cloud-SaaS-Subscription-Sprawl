"""
Cloud & SaaS Subscription Sprawl — AI-Powered Business Intelligence Platform
Single-file app: Backend (Pandas + Scikit-learn) + Frontend (Streamlit)
Author: Mohammad Ayan Ansari | IIT Madras
IBM SkillsBuild Data Analytics with AI Internship 2026 (BharatCares)
Run: streamlit run app.py
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import streamlit as st
import plotly.express as px

# ---------------- Page config ----------------
st.set_page_config(page_title="SaaS Sprawl | BI Platform", page_icon="☁️", layout="wide")

DATA_PATHS = ["dataset_saas_sprawl.csv", "saas-sprawl-project/dataset_saas_sprawl.csv",
              os.path.join(os.path.dirname(__file__), "dataset_saas_sprawl.csv")]

@st.cache_data
def load_data():
    for p in DATA_PATHS:
        if os.path.exists(p):
            df = pd.read_csv(p)
            return df, p
    st.error("dataset_saas_sprawl.csv not found. Please keep it in the same folder as app.py")
    st.stop()

df, used_path = load_data()
df["Renewal_Date"] = pd.to_datetime(df["Renewal_Date"])
active = df[df["Status"] == "Active"].copy()

# ---------------- Sidebar ----------------
st.sidebar.title("☁️ SaaS Sprawl BI")
st.sidebar.caption("AICTE · IBM SkillsBuild · BharatCares — 2026")
page = st.sidebar.radio("Navigate", ["🏠 Executive Overview", "💰 Cost & Product Analysis",
                                     "⚠️ Risk & Renewal Analysis", "🤖 AI Waste Predictor",
                                     "📋 Fact → Action Board"])
st.sidebar.markdown("---")
dept_f = st.sidebar.multiselect("Department", sorted(df["Department"].unique()), default=sorted(df["Department"].unique()))
cat_f = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
risk_f = st.sidebar.multiselect("Renewal Risk", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
fdf = active[active["Department"].isin(dept_f) & active["Category"].isin(cat_f) & active["Renewal_Risk"].isin(risk_f)]
st.sidebar.info(f"Showing **{len(fdf)}** of **{len(active)}** active subscriptions")

# ---------------- KPIs ----------------
def kpis(d):
    return dict(
        spend=d["Monthly_Spend"].sum(),
        annual=d["Annual_Contract_Value"].sum(),
        waste=d["Waste_Monthly"].sum(),
        util=d["Utilization_Pct"].mean() if len(d) else 0,
        subs=len(d),
        unused=d["Unused_Licenses"].sum(),
        high=(d["Renewal_Risk"] == "High").sum(),
    )

K = kpis(fdf)
waste_pct = (K["waste"] / K["spend"] * 100) if K["spend"] else 0

# ---------------- PAGE 1 ----------------
if page.startswith("🏠"):
    st.title("☁️ Cloud & SaaS Subscription Sprawl — Executive Overview")
    st.markdown("Turn **raw subscription data → KPIs → trends → risks → recommended actions**. Goal: cut waste, kill duplicates, de-risk renewals.")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Monthly Spend", f"${K['spend']:,.0f}")
    c2.metric("Annual Contract", f"${K['annual']:,.0f}")
    c3.metric("Monthly Waste", f"${K['waste']:,.0f}", delta=f"{waste_pct:.1f}% of spend", delta_color="inverse")
    c4.metric("Avg Utilization", f"{K['util']:.1f}%")
    c5.metric("Active Subs", f"{K['subs']}")
    c6.metric("High-Risk Renewals", f"{K['high']}", delta="needs action", delta_color="inverse")

    col1, col2 = st.columns(2)
    with col1:
        cat = fdf.groupby("Category")["Monthly_Spend"].sum().sort_values().reset_index()
        fig = px.bar(cat, x="Monthly_Spend", y="Category", orientation="h", title="Monthly Spend by Category",
                     color="Monthly_Spend", color_continuous_scale="Blues", text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        risk = fdf["Renewal_Risk"].value_counts().reindex(["High", "Medium", "Low"]).reset_index()
        risk.columns = ["Risk", "Count"]
        fig = px.pie(risk, names="Risk", values="Count", hole=0.5, title="Renewal Risk Split",
                     color="Risk", color_discrete_map={"High": "#c00000", "Medium": "#ed7d31", "Low": "#70ad47"})
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = px.histogram(fdf, x="Utilization_Pct", nbins=20, title="License Utilization — Waste Zone < 40%",
                           color_discrete_sequence=["#2e75b6"])
        fig.add_vline(x=40, line_dash="dash", line_color="red", annotation_text="40% threshold")
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        dept = fdf.groupby("Department")["Monthly_Spend"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(dept, x="Department", y="Monthly_Spend", title="Spend by Department",
                     color="Monthly_Spend", color_continuous_scale="Oranges", text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)

    st.success(f"💡 **Headline insight:** ${K['waste']:,.0f}/month (**{waste_pct:.1f}%**) is wasted on {K['unused']:,} unused licenses. "
               f"Recovering just 50% saves **${K['waste']*6:,.0f} in 6 months**.")

# ---------------- PAGE 2 ----------------
elif page.startswith("💰"):
    st.title("💰 Cost & Product Analysis — Where is money leaking?")
    top = fdf.groupby("SaaS_Tool")["Waste_Monthly"].sum().sort_values(ascending=False).head(15).reset_index()
    fig = px.bar(top, x="Waste_Monthly", y="SaaS_Tool", orientation="h", title="Top 15 Tools by Monthly Waste",
                 color="Waste_Monthly", color_continuous_scale="Reds", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(fdf, x="Utilization_Pct", y="Waste_Monthly", color="Last_Login_Days_Ago",
                         hover_data=["SaaS_Tool", "Department"], color_continuous_scale="Reds",
                         title="Utilization vs Waste (darker = dormant longer)")
        fig.add_vline(x=40, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        dup = fdf[fdf["Category"].isin(["Communication", "Project Management", "Storage", "CRM & Sales"])]
        g = dup.groupby(["Category", "SaaS_Tool"]).size().reset_index(name="Subs")
        fig = px.bar(g, x="Category", y="Subs", color="SaaS_Tool", barmode="group",
                     title="Tool Overlap — Same Job, Many Tools (Sprawl Signal)")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔎 Lowest-utilization subscriptions (cancel / downsize candidates)")
    st.dataframe(fdf.sort_values("Utilization_Pct").head(25)[
        ["Subscription_ID", "SaaS_Tool", "Category", "Department", "Licenses_Purchased",
         "Licenses_Used", "Utilization_Pct", "Waste_Monthly", "Renewal_Date", "Auto_Renew"]],
        use_container_width=True)

# ---------------- PAGE 3 ----------------
elif page.startswith("⚠️"):
    st.title("⚠️ Customer / Risk & Renewal Analysis")
    st.markdown("Risk score = low utilization + dormancy + auto-renew within 90 days + high contract value.")
    k1, k2, k3 = st.columns(3)
    k1.metric("🔴 High Risk", int((fdf["Renewal_Risk"] == "High").sum()))
    k2.metric("🟠 Medium Risk", int((fdf["Renewal_Risk"] == "Medium").sum()))
    k3.metric("🟢 Low Risk", int((fdf["Renewal_Risk"] == "Low").sum()))
    c1, c2 = st.columns(2)
    with c1:
        soon = fdf[(fdf["Days_to_Renewal"] >= 0) & (fdf["Days_to_Renewal"] <= 90)]
        g = soon.groupby("Renewal_Risk")["Annual_Contract_Value"].sum().reindex(["High", "Medium", "Low"]).reset_index()
        fig = px.bar(g, x="Renewal_Risk", y="Annual_Contract_Value", title="Contract Value Expiring in ≤90 Days by Risk",
                     color="Renewal_Risk", color_discrete_map={"High": "#c00000", "Medium": "#ed7d31", "Low": "#70ad47"},
                     text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)
        st.warning(f"⏰ **{len(soon)}** subscriptions renew in next 90 days worth **${soon['Annual_Contract_Value'].sum():,.0f}**/yr.")
    with c2:
        g2 = fdf.groupby(["Department", "Renewal_Risk"]).size().reset_index(name="Count")
        fig = px.bar(g2, x="Department", y="Count", color="Renewal_Risk", title="Risk by Department",
                     color_discrete_map={"High": "#c00000", "Medium": "#ed7d31", "Low": "#70ad47"})
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("🚨 High-risk renewal table — act before auto-renew")
    hr = fdf[fdf["Renewal_Risk"] == "High"].sort_values("Annual_Contract_Value", ascending=False)
    st.dataframe(hr[["Subscription_ID", "SaaS_Tool", "Department", "Utilization_Pct", "Last_Login_Days_Ago",
                     "Annual_Contract_Value", "Renewal_Date", "Auto_Renew", "Days_to_Renewal"]].head(30),
                 use_container_width=True)
    st.download_button("⬇️ Download high-risk list (CSV)", hr.to_csv(index=False), "high_risk_renewals.csv", "text/csv")

# ---------------- PAGE 4: ML ----------------
elif page.startswith("🤖"):
    st.title("🤖 AI Waste Predictor — Will this subscription waste money?")
    st.markdown("**Model:** Random Forest Classifier predicting `Waste_Flag` (Utilization < 40%). Trained on cost, licenses, utilization, dormancy, renewal & category signals.")
    FEATURES = ["Cost_Per_License_Month", "Licenses_Purchased", "Licenses_Used", "Utilization_Pct",
                "Last_Login_Days_Ago", "Annual_Contract_Value", "Monthly_Spend", "Days_to_Renewal", "Unused_Licenses"]

    @st.cache_resource
    def train():
        X_num = df[FEATURES].fillna(0)
        X_cat = pd.get_dummies(df[["Category", "Plan_Type", "Auto_Renew", "Department"]], drop_first=True)
        X = pd.concat([X_num, X_cat], axis=1)
        y = df["Waste_Flag"]
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        clf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight="balanced")
        clf.fit(Xtr, ytr)
        pred = clf.predict(Xte)
        return clf, X.columns.tolist(), accuracy_score(yte, pred), classification_report(yte, pred, output_dict=True), confusion_matrix(yte, pred)

    clf, cols, acc, rep, cm = train()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{acc*100:.1f}%")
    m2.metric("Precision (waste)", f"{rep['1']['precision']*100:.1f}%")
    m3.metric("Recall (waste)", f"{rep['1']['recall']*100:.1f}%")
    m4.metric("F1 (waste)", f"{rep['1']['f1-score']*100:.1f}%")

    imp = pd.Series(clf.feature_importances_, index=cols).sort_values(ascending=False).head(10).reset_index()
    imp.columns = ["Feature", "Importance"]
    fig = px.bar(imp, x="Importance", y="Feature", orientation="h", title="Top Drivers of Waste (Feature Importance)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧪 Try it — predict a subscription")
    c1, c2, c3 = st.columns(3)
    with c1:
        tool = st.selectbox("SaaS Tool", sorted(df["SaaS_Tool"].unique()))
        dept = st.selectbox("Department", sorted(df["Department"].unique()))
        cat = st.selectbox("Category", sorted(df["Category"].unique()))
        plan = st.selectbox("Plan", ["Monthly", "Annual", "Enterprise"])
    with c2:
        cpl = st.number_input("Cost per license / month ($)", 0.0, 2000.0, 25.0)
        lp = st.number_input("Licenses purchased", 1, 500, 50)
        lu = st.number_input("Licenses used", 0, 500, 20)
        last = st.number_input("Days since last login", 0, 365, 50)
    with c3:
        auto = st.selectbox("Auto-renew", ["Yes", "No"])
        dtr = st.number_input("Days to renewal", -180, 365, 45)
        ms = cpl * lp
        av = ms * 12 * (0.85 if plan == "Annual" else 1.0)
        util = (lu / lp * 100) if lp else 0
        st.info(f"Monthly ${ms:,.0f} · Annual ${av:,.0f} · Util {util:.1f}%")
    if st.button("🔮 Predict waste risk", type="primary"):
        row = {c: 0 for c in cols}
        row.update({"Cost_Per_License_Month": cpl, "Licenses_Purchased": lp, "Licenses_Used": lu,
                    "Utilization_Pct": util, "Last_Login_Days_Ago": last, "Annual_Contract_Value": av,
                    "Monthly_Spend": ms, "Days_to_Renewal": dtr, "Unused_Licenses": lp - lu})
        for k in [f"Category_{cat}", f"Plan_Type_{plan}", f"Auto_Renew_{auto}", f"Department_{dept}"]:
            if k in row:
                row[k] = 1
        X_new = pd.DataFrame([row])[cols]
        p = clf.predict(X_new)[0]
        proba = clf.predict_proba(X_new)[0][1]
        if p == 1:
            st.error(f"🚨 **WASTEFUL** — {proba*100:.1f}% probability. Action: downsize {lp-lu} seats, disable auto-renew, review before renewal.")
        else:
            st.success(f"✅ **EFFICIENT** — only {proba*100:.1f}% waste probability. Keep & monitor.")

# ---------------- PAGE 5 ----------------
else:
    st.title("📋 Fact → Insight → Opportunity → Action Board")
    st.markdown("Every chart in this platform ends here — a decision.")
    board = pd.DataFrame([
        {"Fact": f"${K['waste']:,.0f}/mo wasted ({waste_pct:.1f}%)", "Insight": "28% subs <40% utilized; seats bought but never used",
         "Opportunity": f"Save ${K['waste']*12*0.6:,.0f}/yr by reclaiming 60% waste", "Action": "Downsize bottom-50 subs next billing cycle; set 75% auto-alert"},
        {"Fact": f"{K['high']} high-risk renewals", "Insight": "Auto-renew ON + dormant + renewal ≤90 days",
         "Opportunity": "Renegotiate before lock-in", "Action": "Freeze auto-renew; owner must re-justify 7 days before renewal"},
        {"Fact": "4 chat tools + 5 PM tools active", "Insight": "Duplicate spend: Slack+Teams+Zoom, Jira+Asana+Trello+Notion",
         "Opportunity": "Consolidate to 1 chat + 1 PM suite", "Action": "Standardize: Teams + Jira org-wide; migrate in 60 days"},
        {"Fact": "Data & Analytics = top spend ($413k/mo)", "Insight": "Snowflake/Tableau seats bought in bulk, rarely revoked",
         "Opportunity": "15-20% saving via seat reclaim + tier downgrades", "Action": "Owner tags per workspace, reclaim dormant seats, renegotiate annual plans"},
        {"Fact": "Sales + Engineering = highest waste depts", "Insight": "Bulk seat buying at hiring peaks, never revoked on exit",
         "Opportunity": "Joiner-mover-leaver automation", "Action": "HR-exit webhook revokes licenses in 24h; quarterly access audit"},
    ])
    st.dataframe(board, use_container_width=True)
    st.subheader("✅ 30-60-90 Day Playbook")
    st.markdown("""
    **30 days (Stop bleeding):** disable auto-renew on 64 high-risk subs · reclaim 0-login seats · cancel duplicate Storage tools (keep OneDrive).
    **60 days (Consolidate):** migrate to single Communication + PM stack · renegotiate Salesforce/HubSpot overlap · cloud idle-stop policy.
    **90 days (Prevent regrowth):** procurement approval for new SaaS · quarterly utilization review · AI predictor flags waste at purchase time.
    """)
    st.caption("Built with Python · Streamlit · Scikit-learn · Plotly — single-file app (frontend + backend + ML). Author: Mohammad Ayan Ansari, IIT Madras.")

st.sidebar.markdown("---")
st.sidebar.caption("Mohammad Ayan Ansari · IIT Madras · Sep 2026")
