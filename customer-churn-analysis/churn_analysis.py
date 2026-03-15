"""
Customer Churn Analysis & Prediction
Author: Stephen Drani
Dataset: IBM Telco Customer Churn (7,043 customers, 21 features)
Tools: Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
Goal: Identify churn drivers, predict at-risk customers, and provide
      actionable retention recommendations for business stakeholders.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
COLORS = {"Yes": "#e74c3c", "No": "#2ecc71"}

# ============================================================
# 1. DATA LOADING & CLEANING
# ============================================================
print("=" * 60)
print("STEP 1: Loading and Cleaning Data")
print("=" * 60)

df = pd.read_csv(os.path.join(OUTPUT_DIR, "telco_churn_raw.csv"))
print(f"Raw dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")

# TotalCharges has whitespace strings for new customers — convert to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
missing_tc = df["TotalCharges"].isna().sum()
print(f"Missing TotalCharges (new customers with tenure=0): {missing_tc}")
df["TotalCharges"].fillna(0, inplace=True)

# Create derived features
df["tenure_group"] = pd.cut(df["tenure"], bins=[0, 12, 24, 48, 72],
                            labels=["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"],
                            include_lowest=True)
df["avg_monthly_spend"] = np.where(df["tenure"] > 0,
                                   df["TotalCharges"] / df["tenure"],
                                   df["MonthlyCharges"])
df["churn_flag"] = (df["Churn"] == "Yes").astype(int)

# Count total services subscribed
service_cols = ["PhoneService", "MultipleLines", "InternetService",
                "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                "TechSupport", "StreamingTV", "StreamingMovies"]
df["num_services"] = df[service_cols].apply(
    lambda row: sum(1 for v in row if v in ["Yes", "DSL", "Fiber optic"]), axis=1
)

print(f"Cleaned dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Overall churn rate: {df['churn_flag'].mean():.1%}")
print()

# ============================================================
# 2. EXPLORATORY DATA ANALYSIS
# ============================================================
print("=" * 60)
print("STEP 2: Exploratory Data Analysis")
print("=" * 60)

# --- 2a. Churn Rate Overview ---
churn_counts = df["Churn"].value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    churn_counts, labels=["Retained", "Churned"],
    colors=["#2ecc71", "#e74c3c"], autopct="%1.1f%%",
    startangle=90, textprops={"fontsize": 14, "fontweight": "bold"},
    explode=(0, 0.05)
)
ax.set_title("Customer Churn Distribution", fontsize=16, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_churn_distribution.png"), dpi=150, bbox_inches="tight")
plt.close()
print(f"Churned: {churn_counts.get('Yes', 0):,} ({churn_counts.get('Yes', 0)/len(df):.1%})")
print(f"Retained: {churn_counts.get('No', 0):,} ({churn_counts.get('No', 0)/len(df):.1%})")

# --- 2b. Churn by Contract Type ---
contract_churn = df.groupby("Contract")["churn_flag"].agg(["mean", "count"]).reset_index()
contract_churn.columns = ["Contract", "Churn Rate", "Customers"]
contract_churn = contract_churn.sort_values("Churn Rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(contract_churn["Contract"], contract_churn["Churn Rate"],
              color=["#e74c3c", "#f39c12", "#2ecc71"], edgecolor="white", linewidth=2)
for bar, rate, count in zip(bars, contract_churn["Churn Rate"], contract_churn["Customers"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{rate:.0%}\n({count:,})", ha="center", fontsize=12, fontweight="bold")
ax.set_ylabel("Churn Rate", fontsize=13)
ax.set_title("Churn Rate by Contract Type", fontsize=16, fontweight="bold")
ax.set_ylim(0, max(contract_churn["Churn Rate"]) * 1.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_churn_by_contract.png"), dpi=150, bbox_inches="tight")
plt.close()
print("\nChurn by Contract:")
for _, row in contract_churn.iterrows():
    print(f"  {row['Contract']:20s} → {row['Churn Rate']:.1%} ({row['Customers']:,} customers)")

# --- 2c. Churn by Tenure Group ---
tenure_churn = df.groupby("tenure_group", observed=True)["churn_flag"].mean().reset_index()
tenure_churn.columns = ["Tenure Group", "Churn Rate"]

fig, ax = plt.subplots(figsize=(8, 5))
colors_tenure = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]
bars = ax.bar(tenure_churn["Tenure Group"], tenure_churn["Churn Rate"],
              color=colors_tenure, edgecolor="white", linewidth=2)
for bar, rate in zip(bars, tenure_churn["Churn Rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{rate:.0%}", ha="center", fontsize=13, fontweight="bold")
ax.set_ylabel("Churn Rate", fontsize=13)
ax.set_title("Churn Rate by Customer Tenure", fontsize=16, fontweight="bold")
ax.set_ylim(0, max(tenure_churn["Churn Rate"]) * 1.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_churn_by_tenure.png"), dpi=150, bbox_inches="tight")
plt.close()

# --- 2d. Monthly Charges Distribution: Churned vs Retained ---
fig, ax = plt.subplots(figsize=(10, 5))
for label, color in COLORS.items():
    subset = df[df["Churn"] == label]["MonthlyCharges"]
    ax.hist(subset, bins=40, alpha=0.6, label=f"{'Churned' if label == 'Yes' else 'Retained'}",
            color=color, edgecolor="white")
ax.set_xlabel("Monthly Charges ($)", fontsize=13)
ax.set_ylabel("Number of Customers", fontsize=13)
ax.set_title("Monthly Charges Distribution: Churned vs. Retained", fontsize=16, fontweight="bold")
ax.legend(fontsize=12, frameon=True)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "04_monthly_charges_dist.png"), dpi=150, bbox_inches="tight")
plt.close()

avg_churned = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
avg_retained = df[df["Churn"] == "No"]["MonthlyCharges"].mean()
print(f"\nAvg Monthly Charges — Churned: ${avg_churned:.2f} | Retained: ${avg_retained:.2f}")

# --- 2e. Internet Service Impact ---
internet_churn = df.groupby("InternetService")["churn_flag"].agg(["mean", "count"]).reset_index()
internet_churn.columns = ["Internet Service", "Churn Rate", "Customers"]
internet_churn = internet_churn.sort_values("Churn Rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
colors_int = ["#e74c3c", "#f39c12", "#2ecc71"]
bars = ax.bar(internet_churn["Internet Service"], internet_churn["Churn Rate"],
              color=colors_int, edgecolor="white", linewidth=2)
for bar, rate, count in zip(bars, internet_churn["Churn Rate"], internet_churn["Customers"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{rate:.0%}\n({count:,})", ha="center", fontsize=12, fontweight="bold")
ax.set_ylabel("Churn Rate", fontsize=13)
ax.set_title("Churn Rate by Internet Service Type", fontsize=16, fontweight="bold")
ax.set_ylim(0, max(internet_churn["Churn Rate"]) * 1.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "05_churn_by_internet.png"), dpi=150, bbox_inches="tight")
plt.close()

# --- 2f. Payment Method Impact ---
payment_churn = df.groupby("PaymentMethod")["churn_flag"].agg(["mean", "count"]).reset_index()
payment_churn.columns = ["Payment Method", "Churn Rate", "Customers"]
payment_churn = payment_churn.sort_values("Churn Rate", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
colors_pay = sns.color_palette("RdYlGn", len(payment_churn))
bars = ax.barh(payment_churn["Payment Method"], payment_churn["Churn Rate"],
               color=colors_pay, edgecolor="white", linewidth=2)
for bar, rate in zip(bars, payment_churn["Churn Rate"]):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f"{rate:.0%}", va="center", fontsize=12, fontweight="bold")
ax.set_xlabel("Churn Rate", fontsize=13)
ax.set_title("Churn Rate by Payment Method", fontsize=16, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "06_churn_by_payment.png"), dpi=150, bbox_inches="tight")
plt.close()

# --- 2g. Correlation Heatmap ---
numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen",
                "num_services", "avg_monthly_spend", "churn_flag"]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn_r",
            center=0, square=True, linewidths=1, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Feature Correlation Matrix", fontsize=16, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_correlation_heatmap.png"), dpi=150, bbox_inches="tight")
plt.close()

# --- 2h. Services Count vs Churn ---
services_churn = df.groupby("num_services")["churn_flag"].mean().reset_index()
services_churn.columns = ["Number of Services", "Churn Rate"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(services_churn["Number of Services"], services_churn["Churn Rate"],
        marker="o", linewidth=2.5, markersize=10, color="#3498db")
ax.fill_between(services_churn["Number of Services"], services_churn["Churn Rate"],
                alpha=0.15, color="#3498db")
ax.set_xlabel("Number of Services Subscribed", fontsize=13)
ax.set_ylabel("Churn Rate", fontsize=13)
ax.set_title("Does Bundling Services Reduce Churn?", fontsize=16, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "08_services_vs_churn.png"), dpi=150, bbox_inches="tight")
plt.close()

print("\n✓ All 8 EDA charts saved to charts/")
print()

# ============================================================
# 3. CHURN PREDICTION MODEL (Logistic Regression)
# ============================================================
print("=" * 60)
print("STEP 3: Churn Prediction Model")
print("=" * 60)

try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (classification_report, confusion_matrix,
                                 roc_auc_score, roc_curve)

    # Prepare features
    feature_cols = ["gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
                    "PhoneService", "InternetService", "Contract", "PaperlessBilling",
                    "PaymentMethod", "MonthlyCharges", "TotalCharges", "num_services"]

    df_model = df[feature_cols + ["churn_flag"]].copy()

    # Encode categorical variables
    cat_cols = df_model.select_dtypes(include="object").columns
    le_dict = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col])
        le_dict[col] = le

    X = df_model.drop("churn_flag", axis=1)
    y = df_model["churn_flag"]

    # Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train logistic regression
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # Metrics
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nModel Performance (Test Set):")
    print(f"  ROC-AUC Score: {auc:.3f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Retained", "Churned"]))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Retained", "Churned"],
                yticklabels=["Retained", "Churned"],
                annot_kws={"size": 16})
    ax.set_xlabel("Predicted", fontsize=13)
    ax.set_ylabel("Actual", fontsize=13)
    ax.set_title(f"Confusion Matrix (AUC: {auc:.3f})", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "09_confusion_matrix.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color="#3498db", linewidth=2.5, label=f"Logistic Regression (AUC = {auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random (AUC = 0.500)")
    ax.set_xlabel("False Positive Rate", fontsize=13)
    ax.set_ylabel("True Positive Rate", fontsize=13)
    ax.set_title("ROC Curve — Churn Prediction", fontsize=16, fontweight="bold")
    ax.legend(fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "10_roc_curve.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # Feature importance
    importance = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient": model.coef_[0]
    }).sort_values("Coefficient", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors_imp = ["#e74c3c" if c > 0 else "#2ecc71" for c in importance["Coefficient"]]
    ax.barh(importance["Feature"], importance["Coefficient"], color=colors_imp, edgecolor="white")
    ax.set_xlabel("Coefficient (→ increases churn | ← decreases churn)", fontsize=12)
    ax.set_title("Feature Importance: What Drives Churn?", fontsize=16, fontweight="bold")
    ax.axvline(x=0, color="black", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "11_feature_importance.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # Add churn probability to original dataframe
    X_all_scaled = scaler.transform(df_model.drop("churn_flag", axis=1))
    df["churn_probability"] = model.predict_proba(X_all_scaled)[:, 1]
    df["risk_segment"] = pd.cut(df["churn_probability"],
                                bins=[0, 0.3, 0.6, 1.0],
                                labels=["Low Risk", "Medium Risk", "High Risk"])

    print("✓ ML charts saved (confusion matrix, ROC curve, feature importance)")
    ML_AVAILABLE = True

except ImportError:
    print("⚠ scikit-learn not installed — skipping ML model.")
    print("  To run the full analysis: pip install scikit-learn")
    print("  EDA charts are still generated above.")
    df["churn_probability"] = np.nan
    df["risk_segment"] = "N/A"
    ML_AVAILABLE = False

print()

# ============================================================
# 4. KEY FINDINGS & BUSINESS RECOMMENDATIONS
# ============================================================
print("=" * 60)
print("STEP 4: Key Findings & Business Recommendations")
print("=" * 60)

print("""
KEY FINDINGS:
─────────────
1. MONTH-TO-MONTH CONTRACTS are the #1 churn driver
   → These customers churn at ~2-3x the rate of annual contracts

2. FIRST 12 MONTHS are critical
   → New customers churn at the highest rate; retention drops significantly after year 1

3. FIBER OPTIC customers churn more than DSL
   → Likely a pricing/value perception issue, not a quality issue

4. ELECTRONIC CHECK payers churn most
   → Less "sticky" payment method; auto-pay reduces churn

5. HIGHER MONTHLY CHARGES correlate with higher churn
   → Customers paying more need to perceive more value

RECOMMENDATIONS:
────────────────
1. OFFER INCENTIVES to convert month-to-month → annual contracts
   (e.g., 15% discount for 1-year commitment)

2. CREATE A 90-DAY ONBOARDING PROGRAM for new customers
   to reduce early-stage churn

3. REVIEW FIBER OPTIC PRICING — may need value-adds or
   price adjustments to match customer expectations

4. ENCOURAGE AUTO-PAY enrollment with a small discount
   ($2-5/mo) to increase payment stickiness

5. BUNDLE SERVICES — customers with 4+ services churn less;
   create attractive bundle packages
""")

# ============================================================
# 5. EXPORT DATA FOR LOOKER STUDIO DASHBOARD
# ============================================================
print("=" * 60)
print("STEP 5: Exporting Data for Looker Studio")
print("=" * 60)

# Main dataset with all features + predictions
export_cols = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
               "tenure", "tenure_group", "PhoneService", "InternetService",
               "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
               "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
               "PaymentMethod", "MonthlyCharges", "TotalCharges", "num_services",
               "Churn", "churn_flag", "churn_probability", "risk_segment"]

df_export = df[export_cols].copy()
df_export.to_csv(os.path.join(OUTPUT_DIR, "churn_dashboard_data.csv"), index=False)
print(f"Exported: churn_dashboard_data.csv ({len(df_export):,} rows)")

# Summary stats for dashboard KPIs
summary = {
    "Total Customers": len(df),
    "Churned Customers": int(df["churn_flag"].sum()),
    "Churn Rate": f"{df['churn_flag'].mean():.1%}",
    "Avg Monthly Revenue": f"${df['MonthlyCharges'].mean():.2f}",
    "Revenue at Risk (monthly)": f"${df[df['Churn']=='Yes']['MonthlyCharges'].sum():,.0f}",
}
for k, v in summary.items():
    print(f"  {k}: {v}")

print(f"\n✓ Project complete! Files in: {OUTPUT_DIR}")
print(f"  → churn_analysis.py (this script)")
print(f"  → telco_churn_raw.csv (raw data)")
print(f"  → churn_dashboard_data.csv (Looker Studio ready)")
print(f"  → charts/ (all visualizations)")
