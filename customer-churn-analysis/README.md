# Customer Churn Analysis & Prediction

**Author:** Stephen Drani
**Tools:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn), Looker Studio
**Dataset:** IBM Telco Customer Churn — 7,043 customers, 21 features

## Business Question

A telecom company is losing customers and wants to understand **why customers leave** and **which customers are most likely to churn next month**, so the retention team can take proactive action before it's too late.

## Project Overview

This project walks through the full data analyst pipeline: data cleaning, exploratory analysis, predictive modeling, and actionable business recommendations — ending with an interactive Looker Studio dashboard for stakeholders.

## Key Findings

**1. Month-to-month contracts are the #1 churn driver.** These customers churn at 42%, compared to 17% for one-year and 9% for two-year contracts. Moving 10% of month-to-month customers onto annual contracts would keep about 100 more customers, worth roughly $6.5K/month in revenue (assuming they take on the one-year churn rate and keep the month-to-month average bill of $65.69).

**2. The first two years carry the most risk.** Customers with 0–24 months of tenure churn at 36–37%, versus 21–23% after that. This points to a need for a strong onboarding and early-retention program.

**3. Fiber optic customers churn more than DSL** (33% vs 27%), despite fiber being the premium service. This suggests a pricing/value mismatch rather than a quality problem.

**4. Churned customers pay more.** Their average monthly bill is $69.14, versus $64.42 for customers who stayed.

**5. Payment method and number of add-on services matter little.** Churn varies only between 27.5% and 31.9% across payment methods, and customers with more add-on services do not churn less. Contract and tenure are where retention effort should go.

## Visualizations

| Chart | Insight |
|-------|---------|
| ![Churn Distribution](charts/01_churn_distribution.png) | 29.4% of customers churned |
| ![Churn by Contract](charts/02_churn_by_contract.png) | Month-to-month = 42% churn |
| ![Churn by Tenure](charts/03_churn_by_tenure.png) | First two years churn most |
| ![Monthly Charges](charts/04_monthly_charges_dist.png) | Churned customers pay more |
| ![Internet Service](charts/05_churn_by_internet.png) | Fiber optic churn is highest |
| ![Payment Method](charts/06_churn_by_payment.png) | Payment method has little effect |
| ![Correlation Matrix](charts/07_correlation_heatmap.png) | Feature relationships |
| ![Services vs Churn](charts/08_services_vs_churn.png) | More services does not mean less churn |

## Prediction Model

A **logistic regression model** predicts which customers are likely to churn, achieving a ROC-AUC of ~0.74. Each customer is assigned a churn probability score and segmented into Low / Medium / High risk groups.

To run the model (requires scikit-learn):
```bash
pip install scikit-learn
python churn_analysis.py
```

The model generates three additional charts: confusion matrix, ROC curve, and feature importance coefficients.

## Interactive Dashboard

[**View the Live Dashboard on Looker Studio**](https://lookerstudio.google.com/s/ra8vaWVRUzQ)

The interactive dashboard includes KPI cards (total customers, churn rate, revenue at risk), churn breakdowns by contract type, tenure, internet service, and payment method, plus dropdown filters for stakeholder exploration.

## Project Structure

```
customer-churn-analysis/
├── churn_analysis.py          # Full analysis pipeline
├── telco_churn_raw.csv        # Raw dataset (7,043 rows)
├── churn_analysis.ipynb       # Notebook version of the analysis
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── charts/                    # All generated visualizations
    ├── 01_churn_distribution.png
    ├── 02_churn_by_contract.png
    ├── 03_churn_by_tenure.png
    ├── 04_monthly_charges_dist.png
    ├── 05_churn_by_internet.png
    ├── 06_churn_by_payment.png
    ├── 07_correlation_heatmap.png
    └── 08_services_vs_churn.png
```

## How to Run

```bash
# Clone the repo
git clone https://github.com/worldwarwater/Data-Analytics.github.io.git
cd Data-Analytics.github.io/customer-churn-analysis

# Install dependencies
pip install -r requirements.txt

# Run the full analysis
python churn_analysis.py
```

## Skills Demonstrated

- **Data Cleaning:** Handling missing values, type conversions, feature engineering
- **Exploratory Data Analysis:** Distribution analysis, group comparisons, correlation analysis
- **Data Visualization:** Publication-quality charts with Matplotlib and Seaborn
- **Machine Learning:** Logistic regression, train/test split, ROC-AUC evaluation
- **Business Acumen:** Translating statistical findings into actionable retention strategies
- **Dashboard Design:** Exporting analysis-ready data for Looker Studio
