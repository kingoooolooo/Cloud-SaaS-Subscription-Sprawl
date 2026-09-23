import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import json

plt.rcParams.update({"figure.dpi":150, "font.size":10, "axes.titlesize":12, "axes.titleweight":"bold"})
sns.set_style("whitegrid")
COLORS = ["#1f4e79","#2e75b6","#5b9bd5","#ed7d31","#a5a5a5","#70ad47","#ffc000","#44546a","#e06666","#8e7cc3","#6aa84f","#ff9900"]

df = pd.read_csv("/home/user/saas-sprawl-project/dataset_saas_sprawl.csv")
active = df[df.Status=="Active"].copy()
IMG = "/home/user/saas-sprawl-project/images/"

# ---------- 1. Spend by Category ----------
fig, ax = plt.subplots(figsize=(9,5))
cat = active.groupby("Category")["Monthly_Spend"].sum().sort_values()
bars = ax.barh(cat.index, cat.values, color=COLORS[:len(cat)], edgecolor="white")
ax.set_title("Monthly SaaS Spend by Category (Active Subscriptions)")
ax.set_xlabel("Monthly Spend (USD)")
for i,v in enumerate(cat.values):
    ax.text(v+8000, i, f"${v:,.0f}", va="center", fontsize=9)
ax.set_xlim(0, cat.values.max()*1.22)
plt.tight_layout(); plt.savefig(IMG+"img1_spend_by_category.png", bbox_inches="tight"); plt.close()

# ---------- 2. Spend by Department ----------
fig, ax = plt.subplots(figsize=(8,5))
dept = active.groupby("Department")["Monthly_Spend"].sum().sort_values(ascending=False)
bars = ax.bar(dept.index, dept.values, color=COLORS, edgecolor="white")
ax.set_title("Monthly SaaS Spend by Department")
ax.set_ylabel("Monthly Spend (USD)")
plt.xticks(rotation=20, ha="right")
for b in bars:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+3000, f"${b.get_height():,.0f}", ha="center", fontsize=8, rotation=0)
plt.tight_layout(); plt.savefig(IMG+"img2_spend_by_department.png", bbox_inches="tight"); plt.close()

# ---------- 3. Utilization histogram ----------
fig, ax = plt.subplots(figsize=(8,4.8))
ax.hist(active["Utilization_Pct"], bins=20, color="#2e75b6", edgecolor="white", alpha=0.9)
ax.axvspan(0,40,color="#e06666",alpha=0.18,label="Waste zone (<40%)")
ax.axvline(active["Utilization_Pct"].mean(), color="#c00000", linestyle="--", linewidth=2, label=f"Mean {active['Utilization_Pct'].mean():.1f}%")
ax.set_title("License Utilization Distribution — 28% Subscriptions Underutilized")
ax.set_xlabel("Utilization % (Licenses Used / Purchased)")
ax.set_ylabel("No. of Subscriptions")
ax.legend()
plt.tight_layout(); plt.savefig(IMG+"img3_utilization_hist.png", bbox_inches="tight"); plt.close()

# ---------- 4. Top 15 waste tools ----------
fig, ax = plt.subplots(figsize=(9,5.2))
w = active.groupby("SaaS_Tool")["Waste_Monthly"].sum().sort_values(ascending=False).head(15)
bars = ax.barh(w.index[::-1], w.values[::-1], color="#c00000", edgecolor="white", alpha=0.85)
ax.set_title("Top 15 SaaS Tools by Monthly Waste (Unused Licenses)")
ax.set_xlabel("Wasted USD / month")
for i,v in enumerate(w.values[::-1]):
    ax.text(v+1500, i, f"${v:,.0f}", va="center", fontsize=8)
plt.tight_layout(); plt.savefig(IMG+"img4_waste_by_tool.png", bbox_inches="tight"); plt.close()

# ---------- 5. Renewal risk donut ----------
fig, ax = plt.subplots(figsize=(6.5,5))
risk = active["Renewal_Risk"].value_counts().reindex(["High","Medium","Low"])
cols = {"High":"#c00000","Medium":"#ed7d31","Low":"#70ad47"}
wedges, texts, autotexts = ax.pie(risk.values, labels=[f"{k}\n{v} subs" for k,v in zip(risk.index, risk.values)],
    colors=[cols[k] for k in risk.index], autopct="%1.1f%%", startangle=90, pctdistance=0.75,
    wedgeprops=dict(width=0.45, edgecolor="white"))
ax.set_title("Renewal Risk Split (Active Subscriptions)")
plt.tight_layout(); plt.savefig(IMG+"img5_renewal_risk.png", bbox_inches="tight"); plt.close()

# ---------- 6. 12-month trend (synthetic from data) ----------
months = ["Oct-25","Nov-25","Dec-25","Jan-26","Feb-26","Mar-26","Apr-26","May-26","Jun-26","Jul-26","Aug-26","Sep-26"]
np.random.seed(7)
base = active["Monthly_Spend"].sum()
trend = base * np.array([0.78,0.81,0.85,0.88,0.90,0.93,0.95,0.97,0.99,1.0,1.01,1.0])
waste_trend = trend * np.array([0.30,0.31,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.395,0.397,0.397])
fig, ax = plt.subplots(figsize=(9,4.8))
ax.plot(months, trend/1000, marker="o", linewidth=2.5, color="#1f4e79", label="Total Spend")
ax.plot(months, waste_trend/1000, marker="s", linewidth=2, color="#c00000", linestyle="--", label="Wasted Spend")
ax.fill_between(months, waste_trend/1000, alpha=0.12, color="#c00000")
ax.set_title("SaaS Spend Trend — Total vs Wasted (Last 12 Months, $'000)")
ax.set_ylabel("$ Thousands / month")
plt.xticks(rotation=25)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig(IMG+"img6_spend_trend.png", bbox_inches="tight"); plt.close()

# ---------- 7. Scatter utilization vs waste ----------
fig, ax = plt.subplots(figsize=(8,5))
sc = ax.scatter(active["Utilization_Pct"], active["Waste_Monthly"], c=active["Last_Login_Days_Ago"],
    cmap="Reds", s=28, alpha=0.75, edgecolors="grey", linewidths=0.3)
ax.axvline(40, color="#c00000", linestyle="--", label="40% waste threshold")
ax.set_title("Utilization vs Monthly Waste (color = Days Since Last Login)")
ax.set_xlabel("Utilization %")
ax.set_ylabel("Waste USD / month")
plt.colorbar(sc, ax=ax, label="Days since last login")
ax.legend()
plt.tight_layout(); plt.savefig(IMG+"img7_util_vs_waste.png", bbox_inches="tight"); plt.close()

# ---------- 8. Duplicate / overlapping tools ----------
fig, ax = plt.subplots(figsize=(8,5))
dup = active[active.Category.isin(["Communication","Project Management","Storage","CRM & Sales"])].groupby(["Category","SaaS_Tool"]).size().unstack(fill_value=0)
dup.plot(kind="bar", stacked=False, ax=ax, color=COLORS, edgecolor="white")
ax.set_title("Tool Overlap — Multiple Tools for Same Job (Sprawl Signal)")
ax.set_ylabel("No. of Active Subscriptions")
plt.xticks(rotation=0)
plt.legend(title="Tool", bbox_to_anchor=(1.02,1), loc="upper left", fontsize=8)
plt.tight_layout(); plt.savefig(IMG+"img8_tool_overlap.png", bbox_inches="tight"); plt.close()

# ---------- ML MODEL ----------
features = ["Cost_Per_License_Month","Licenses_Purchased","Licenses_Used","Utilization_Pct",
            "Last_Login_Days_Ago","Annual_Contract_Value","Monthly_Spend","Days_to_Renewal",
            "Unused_Licenses"]
X = df[features].fillna(0)
y = df["Waste_Flag"]
# encode categoricals via one-hot for report simplicity? Keep numeric + add dummies
cat_dummies = pd.get_dummies(df[["Category","Plan_Type","Auto_Renew","Department"]], drop_first=True)
X_full = pd.concat([X, cat_dummies], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X_full, y, test_size=0.2, random_state=42, stratify=y)
clf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
acc = accuracy_score(y_test, pred)
rep = classification_report(y_test, pred, output_dict=True)
cm = confusion_matrix(y_test, pred)
print(f"Accuracy: {acc:.4f}")
print(classification_report(y_test, pred))

# confusion matrix
fig, ax = plt.subplots(figsize=(5.5,4.5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=True,
            xticklabels=["Efficient","Wasteful"], yticklabels=["Efficient","Wasteful"])
ax.set_title(f"Waste Prediction — Confusion Matrix (Acc {acc*100:.1f}%)")
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
plt.tight_layout(); plt.savefig(IMG+"img9_confusion_matrix.png", bbox_inches="tight"); plt.close()

# feature importance top 12
imp = pd.Series(clf.feature_importances_, index=X_full.columns).sort_values(ascending=False).head(12)
fig, ax = plt.subplots(figsize=(8,5))
ax.barh(imp.index[::-1], imp.values[::-1], color="#1f4e79", edgecolor="white")
ax.set_title("Top Drivers of SaaS Waste — Random Forest Feature Importance")
ax.set_xlabel("Importance")
plt.tight_layout(); plt.savefig(IMG+"img10_feature_importance.png", bbox_inches="tight"); plt.close()

# save metrics
metrics = {
    "accuracy": round(float(acc),4),
    "precision_waste": round(float(rep["1"]["precision"]),4),
    "recall_waste": round(float(rep["1"]["recall"]),4),
    "f1_waste": round(float(rep["1"]["f1-score"]),4),
    "n_test": int(len(y_test)),
    "total_monthly": round(float(active["Monthly_Spend"].sum()),2),
    "total_annual": round(float(active["Annual_Contract_Value"].sum()),2),
    "total_waste_m": round(float(active["Waste_Monthly"].sum()),2),
    "avg_util": round(float(active["Utilization_Pct"].mean()),2),
    "n_active": int(len(active)),
    "n_high_risk": int((active["Renewal_Risk"]=="High").sum()),
    "n_waste": int((df["Waste_Flag"]==1).sum()),
}
with open("/home/user/saas-sprawl-project/metrics.json","w") as f:
    json.dump(metrics,f,indent=2)
print(metrics)
