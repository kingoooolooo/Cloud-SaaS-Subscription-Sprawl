"""Generate synthetic Cloud & SaaS Subscription Sprawl dataset"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N = 600

tools = [
    ("Slack", "Communication", 8.75), ("Microsoft Teams", "Communication", 12.50),
    ("Zoom", "Communication", 15.99), ("Google Workspace", "Communication", 14.00),
    ("Jira", "Project Management", 10.50), ("Asana", "Project Management", 13.49),
    ("Trello", "Project Management", 6.00), ("Notion", "Project Management", 10.00),
    ("Monday.com", "Project Management", 16.00),
    ("AWS", "Cloud Infra", 450.00), ("Microsoft Azure", "Cloud Infra", 380.00),
    ("Google Cloud", "Cloud Infra", 320.00), ("DigitalOcean", "Cloud Infra", 95.00),
    ("Salesforce", "CRM & Sales", 165.00), ("HubSpot", "CRM & Sales", 89.00),
    ("Zoho CRM", "CRM & Sales", 45.00),
    ("Adobe Creative Cloud", "Design", 59.99), ("Figma", "Design", 15.00), ("Canva", "Design", 12.99),
    ("GitHub", "Engineering", 21.00), ("GitLab", "Engineering", 29.00),
    ("Jenkins", "Engineering", 0.00), ("Docker Hub", "Engineering", 9.00),
    ("Snowflake", "Data & Analytics", 220.00), ("Tableau", "Data & Analytics", 75.00),
    ("Power BI", "Data & Analytics", 20.00), ("Datadog", "Data & Analytics", 31.00),
    ("Workday", "HR & Finance", 55.00), ("BambooHR", "HR & Finance", 18.00),
    ("QuickBooks", "HR & Finance", 35.00), ("Expensify", "HR & Finance", 9.99),
    ("Dropbox", "Storage", 16.58), ("Box", "Storage", 18.00), ("OneDrive", "Storage", 6.99),
    ("1Password", "Security", 7.99), ("Okta", "Security", 12.00), ("Norton", "Security", 4.99),
    ("Coursera", "Learning", 49.00), ("Udemy Business", "Learning", 36.00),
]

departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Product", "Support", "Design"]
regions = ["North", "South", "East", "West"]

rows = []
start = datetime(2024, 1, 1)
for i in range(1, N+1):
    tool, cat, base_price = random.choice(tools)
    dept = random.choice(departments)
    region = random.choice(regions)
    plan = np.random.choice(["Monthly", "Annual", "Enterprise"], p=[0.35, 0.45, 0.20])
    # licenses
    lic_purchased = np.random.choice([5,10,15,20,25,30,50,75,100,150,200])
    # utilization - create sprawl: 30% low utilization
    if np.random.rand() < 0.30:
        util = round(np.random.uniform(5, 40), 1)  # wasteful
    else:
        util = round(np.random.uniform(55, 99), 1)
    lic_used = max(1, int(lic_purchased * util / 100))
    # price variation
    cost_pm = round(base_price * np.random.uniform(0.9, 1.15), 2) if base_price > 0 else 0.0
    # cloud infra is per-team not per-seat, adjust
    if cat == "Cloud Infra":
        monthly_spend = round(cost_pm * np.random.uniform(0.5, 2.0), 2)
        lic_purchased = 1
        lic_used = 1
    else:
        monthly_spend = round(cost_pm * lic_purchased, 2)
    annual_value = round(monthly_spend * 12 * (0.85 if plan=="Annual" else 1.0), 2)
    last_login = int(np.random.exponential(20)) if util > 40 else int(np.random.uniform(30, 120))
    last_login = min(last_login, 180)
    # renewal date in 2026
    renewal = datetime(2026, 1, 1) + timedelta(days=int(np.random.uniform(0, 365)))
    auto_renew = np.random.choice(["Yes", "No"], p=[0.72, 0.28])
    status = "Active" if np.random.rand() > 0.08 else np.random.choice(["Inactive", "Cancelled"])
    # duplicate flag: comm + pm tools duplicated
    owner = f"EMP{np.random.randint(1000,1200)}"
    rows.append([f"SUB{i:04d}", owner, dept, tool, cat, plan, cost_pm, lic_purchased, lic_used, util,
                 last_login, renewal.strftime("%Y-%m-%d"), annual_value, monthly_spend, auto_renew, status, region])

df = pd.DataFrame(rows, columns=["Subscription_ID","Owner_ID","Department","SaaS_Tool","Category","Plan_Type",
    "Cost_Per_License_Month","Licenses_Purchased","Licenses_Used","Utilization_Pct",
    "Last_Login_Days_Ago","Renewal_Date","Annual_Contract_Value","Monthly_Spend","Auto_Renew","Status","Region"])

# Waste flag
df["Unused_Licenses"] = df["Licenses_Purchased"] - df["Licenses_Used"]
df["Waste_Monthly"] = (df["Unused_Licenses"] * df["Cost_Per_License_Month"]).round(2)
df.loc[df["Category"]=="Cloud Infra","Waste_Monthly"] = 0
df["Waste_Flag"] = ((df["Utilization_Pct"]<40) & (df["Status"]=="Active")).astype(int)
# Renewal risk: high waste + auto-renew + renewal within 90 days from Sep 2026
ref = datetime(2026,9,23)
df["Renewal_Date_dt"] = pd.to_datetime(df["Renewal_Date"])
df["Days_to_Renewal"] = (df["Renewal_Date_dt"] - ref).dt.days
def risk(r):
    s=0
    if r["Utilization_Pct"]<40: s+=2
    elif r["Utilization_Pct"]<60: s+=1
    if r["Last_Login_Days_Ago"]>45: s+=1
    if r["Auto_Renew"]=="Yes" and r["Days_to_Renewal"]<=90 and r["Days_to_Renewal"]>=0: s+=2
    if r["Annual_Contract_Value"]>20000: s+=1
    if s>=4: return "High"
    if s>=2: return "Medium"
    return "Low"
df["Renewal_Risk"] = df.apply(risk, axis=1)
df.drop(columns=["Renewal_Date_dt"], inplace=True)

df.to_csv("/home/user/saas-sprawl-project/dataset_saas_sprawl.csv", index=False)
print(df.shape)
print(df.head(3).to_string())
print("\n--- KPIs ---")
print("Total Monthly Spend:", df[df.Status=="Active"]["Monthly_Spend"].sum())
print("Total Annual Value:", df[df.Status=="Active"]["Annual_Contract_Value"].sum())
print("Total Waste Monthly:", df[df.Status=="Active"]["Waste_Monthly"].sum())
print("Avg Utilization:", df[df.Status=="Active"]["Utilization_Pct"].mean())
print("Waste Flag %:", df["Waste_Flag"].mean()*100)
print(df["Renewal_Risk"].value_counts())
print(df["Category"].value_counts())
