# Marketing Campaign Segmentation & ROI Analysis

## Overview
End-to-end marketing analytics project analyzing 2,240 customers to identify high-value segments using RFM analysis and K-Means clustering, measure campaign ROI across channels, and validate findings with statistical tests. Built to demonstrate mid-level data analyst competencies in segmentation, predictive targeting, and data-driven budget optimization.

## Dataset
**Source:** [Kaggle — Marketing Campaign Dataset](https://www.kaggle.com/datasets/jackdaoud/marketing-data)
**Records:** 2,240 customers | **Features:** 28 columns
**Format:** Tab-separated CSV (`marketing_campaign.csv`)
**Raw Data:** Download from [Kaggle](https://www.kaggle.com/datasets/jackdaoud/marketing-data) and place in `data/raw/`

Key fields include demographics (income, education, marital status), product spending (wines, meat, fish, sweets, gold, fruits), purchase channels (web, catalog, store), campaign responses (6 campaigns), and enrollment date.

## Project Structure
```
marketing-campaign-analysis/
├── data/
│   ├── raw/                  # Original dataset (download from Kaggle: https://www.kaggle.com/datasets/jackdaoud/marketing-data)
│   └── processed/            # Cleaned CSV + SQLite database
├── notebooks/
│   ├── 01_cleaning_eda.ipynb         # Data cleaning & exploratory analysis
│   ├── 02_rfm_segmentation.ipynb     # RFM scoring & K-Means clustering
│   ├── 03_campaign_roi.ipynb         # Campaign ROI & channel analysis
│   └── 04_statistical_tests.ipynb    # Hypothesis testing & validation
├── sql/
│   └── analysis_queries.sql          # 10 SQL queries (CTEs, window functions)
├── visualizations/           # Saved charts (.png)
├── report/                   # Executive summary & statistical results
├── Looker_Studio_Dashboard_Guide.docx  # Step-by-step Looker Studio setup guide
└── README.md
```

## Setup Instructions
1. **Download the dataset** from [Kaggle](https://www.kaggle.com/datasets/jackdaoud/marketing-data) — place `marketing_campaign.csv` in `data/raw/`
3. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn scipy
   ```
4. Run notebooks in order (01 → 02 → 03 → 04) — each notebook saves output that the next one loads

## Analysis Phases

### Phase 1: Data Cleaning & EDA (Notebook 01)
- Handle 24 missing income values, remove outliers (income > $200K, age > 100)
- Engineer 7 features: Age, Total_Spent, Total_Purchases, Total_Campaigns_Accepted, Children, Customer_Tenure_Days, Conversion_Rate
- Generate 10 EDA visualizations (distributions, correlations, category breakdowns)

### Phase 2: RFM Segmentation & Clustering (Notebook 02)
- Calculate Recency, Frequency, Monetary scores using quintile-based scoring
- Map customers into 8 RFM segments (Champions, Loyal, At Risk, etc.)
- Apply K-Means clustering (K=4) with StandardScaler preprocessing
- Validate cluster selection with Elbow Method and Silhouette Score
- Visualize clusters with PCA 2D projection

### Phase 3: Campaign ROI Analysis (Notebook 03)
- Analyze acceptance rates across all 6 campaigns
- Compare channel performance (web, catalog, store) by segment
- Calculate ROI with simulated cost assumptions ($5 web, $15 catalog, $3 store)
- Produce budget reallocation recommendations based on segment-channel ROI

### Phase 4: Statistical Testing (Notebook 04)
- Chi-Square tests: segment vs. campaign response, education vs. acceptance
- ANOVA: income and spending differences across segments (with Bonferroni post-hoc)
- T-Test & Mann-Whitney U: responders vs. non-responders
- Correlation analysis: Pearson & Spearman with p-value matrix
- Effect size measurement with Cohen's d

### SQL Queries (10 queries)
- Customer demographic summary, top spenders with RANK()
- Campaign acceptance rates, RFM segment revenue contribution
- Channel preference by segment, monthly enrollment trends
- Pareto analysis of product categories, composite customer scoring
- Complaint impact analysis, cohort-based spending trends

## Key Skills Demonstrated
- **SQL:** CTEs, window functions (RANK, NTILE, running totals), UNION ALL, CASE
- **Python:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, SciPy
- **Statistics:** Chi-Square, ANOVA, T-Test, Mann-Whitney U, Pearson/Spearman correlation, Cohen's d
- **Machine Learning:** K-Means clustering, StandardScaler, Elbow Method, Silhouette Score, PCA
- **Visualization:** 10+ publication-quality charts, correlation heatmaps, PCA projections
- **Business Analysis:** RFM segmentation, campaign ROI, budget optimization, cohort analysis

## Interactive Dashboard

> **[View the Looker Studio Dashboard →](https://lookerstudio.google.com/s/sN0LOkumv0o)**

Explore the data interactively with filters by RFM segment, cluster, and education level. The dashboard includes 4 pages:
1. **Executive Overview** — KPI scorecards, RFM distribution, income distribution, spending by product category
2. **Customer Segmentation** — Average spending by RFM segment, cluster profiles table
3. **Campaign Performance** — Acceptance rates, channel performance by segment, ROI by channel
4. **Statistical Insights** — Test results summary, income vs. spending scatter plot, responder comparison

See `Looker_Studio_Dashboard_Guide.docx` for a complete step-by-step setup guide.

## Tools & Technologies
Python 3.x | Pandas | NumPy | Scikit-learn | SciPy | Matplotlib | Seaborn | SQLite | Looker Studio | Jupyter Notebook

## Author
**Stephen Drani**
[LinkedIn](https://linkedin.com/in/stephen-drani-a58140232) | [GitHub](https://github.com/worldwarwater/Data-Analytics.github.io)
