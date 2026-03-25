-- ============================================================
-- Marketing Campaign Analysis — SQL Queries
-- Dataset: ifood_df.csv (Kaggle - jackdaoud/marketing-data)
-- Author: Stephen Drani
-- Date: March 2026
-- ============================================================
-- NOTE: These queries assume the segmented data has been loaded
-- into a SQLite database table called 'customers'.
-- 
-- SETUP INSTRUCTIONS (run in Terminal first):
-- $ python3 setup_database.py
-- OR manually run this Python code:
--   import sqlite3, pandas as pd
--   df = pd.read_csv('data/processed/marketing_segmented.csv')
--   conn = sqlite3.connect('data/processed/marketing.db')
--   df.to_sql('customers', conn, if_exists='replace', index=False)
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- Query 1: Customer Demographic Summary by Education
-- Reconstructs education from one-hot columns, aggregates metrics
-- ────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN "education_PhD" = 1 THEN 'PhD'
        WHEN "education_Master" = 1 THEN 'Master'
        WHEN "education_Graduation" = 1 THEN 'Graduation'
        WHEN "education_2n Cycle" = 1 THEN '2n Cycle'
        WHEN "education_Basic" = 1 THEN 'Basic'
        ELSE 'Unknown'
    END AS Education,
    COUNT(*)                              AS customer_count,
    ROUND(AVG(Income), 2)                 AS avg_income,
    ROUND(AVG(MntTotal), 2)               AS avg_total_spent,
    ROUND(AVG(Total_Purchases), 2)        AS avg_total_purchases,
    ROUND(AVG(Total_Campaigns_Accepted), 2) AS avg_campaigns_accepted
FROM customers
GROUP BY Education
ORDER BY avg_income DESC;


-- ────────────────────────────────────────────────────────────
-- Query 2: Top 10 Highest-Spending Customers
-- Uses window function for spending rank
-- ────────────────────────────────────────────────────────────
SELECT
    ROWID AS customer_id,
    Income,
    MntTotal,
    Total_Purchases,
    Total_Campaigns_Accepted,
    RFM_Segment,
    RANK() OVER (ORDER BY MntTotal DESC) AS spending_rank
FROM customers
ORDER BY MntTotal DESC
LIMIT 10;


-- ────────────────────────────────────────────────────────────
-- Query 3: Campaign Acceptance Rates by Campaign
-- Calculates acceptance rate for each of the 6 campaigns
-- ────────────────────────────────────────────────────────────
SELECT
    'Campaign 1' AS campaign,
    ROUND(100.0 * SUM(AcceptedCmp1) / COUNT(*), 2) AS acceptance_rate_pct
FROM customers
UNION ALL
SELECT 'Campaign 2', ROUND(100.0 * SUM(AcceptedCmp2) / COUNT(*), 2) FROM customers
UNION ALL
SELECT 'Campaign 3', ROUND(100.0 * SUM(AcceptedCmp3) / COUNT(*), 2) FROM customers
UNION ALL
SELECT 'Campaign 4', ROUND(100.0 * SUM(AcceptedCmp4) / COUNT(*), 2) FROM customers
UNION ALL
SELECT 'Campaign 5', ROUND(100.0 * SUM(AcceptedCmp5) / COUNT(*), 2) FROM customers
UNION ALL
SELECT 'Last Campaign', ROUND(100.0 * SUM(Response) / COUNT(*), 2) FROM customers
ORDER BY acceptance_rate_pct DESC;


-- ────────────────────────────────────────────────────────────
-- Query 4: RFM Segment Distribution & Revenue Contribution
-- Shows customer count and total spend per RFM segment
-- ────────────────────────────────────────────────────────────
WITH segment_stats AS (
    SELECT
        RFM_Segment,
        COUNT(*)            AS segment_size,
        SUM(MntTotal)       AS total_revenue,
        AVG(MntTotal)       AS avg_revenue,
        AVG(Income)         AS avg_income
    FROM customers
    WHERE RFM_Segment IS NOT NULL
    GROUP BY RFM_Segment
),
total AS (
    SELECT SUM(MntTotal) AS grand_total FROM customers
)
SELECT
    s.RFM_Segment,
    s.segment_size,
    ROUND(s.avg_revenue, 2)                              AS avg_revenue_per_customer,
    ROUND(s.total_revenue, 2)                             AS segment_total_revenue,
    ROUND(100.0 * s.total_revenue / t.grand_total, 2)    AS revenue_share_pct,
    ROUND(s.avg_income, 2)                                AS avg_income
FROM segment_stats s
CROSS JOIN total t
ORDER BY segment_total_revenue DESC;


-- ────────────────────────────────────────────────────────────
-- Query 5: Purchase Channel Preference by Segment
-- Compares web, catalog, and store purchases across segments
-- ────────────────────────────────────────────────────────────
SELECT
    RFM_Segment,
    COUNT(*)                          AS n_customers,
    ROUND(AVG(NumWebPurchases), 2)    AS avg_web_purchases,
    ROUND(AVG(NumCatalogPurchases), 2) AS avg_catalog_purchases,
    ROUND(AVG(NumStorePurchases), 2)  AS avg_store_purchases,
    CASE
        WHEN AVG(NumWebPurchases) >= AVG(NumCatalogPurchases)
         AND AVG(NumWebPurchases) >= AVG(NumStorePurchases)
        THEN 'Web'
        WHEN AVG(NumCatalogPurchases) >= AVG(NumStorePurchases)
        THEN 'Catalog'
        ELSE 'Store'
    END AS preferred_channel
FROM customers
WHERE RFM_Segment IS NOT NULL
GROUP BY RFM_Segment
ORDER BY avg_web_purchases + avg_catalog_purchases + avg_store_purchases DESC;


-- ────────────────────────────────────────────────────────────
-- Query 6: Customer Tenure Analysis
-- Groups by Customer_Days buckets and tracks spending patterns
-- ────────────────────────────────────────────────────────────
WITH tenure_buckets AS (
    SELECT
        CASE
            WHEN Customer_Days < 2300 THEN 'Newer (<2300 days)'
            WHEN Customer_Days < 2500 THEN 'Mid (2300-2500 days)'
            ELSE 'Veteran (2500+ days)'
        END AS tenure_group,
        Income,
        MntTotal,
        Total_Purchases,
        Total_Campaigns_Accepted
    FROM customers
)
SELECT
    tenure_group,
    COUNT(*)                                AS customer_count,
    ROUND(AVG(Income), 2)                   AS avg_income,
    ROUND(AVG(MntTotal), 2)                 AS avg_spent,
    ROUND(AVG(Total_Purchases), 2)          AS avg_purchases,
    ROUND(AVG(Total_Campaigns_Accepted), 2) AS avg_campaigns
FROM tenure_buckets
GROUP BY tenure_group
ORDER BY tenure_group;


-- ────────────────────────────────────────────────────────────
-- Query 7: Product Category Spending — Pareto Analysis
-- Identifies which product categories drive 80% of revenue
-- ────────────────────────────────────────────────────────────
WITH category_totals AS (
    SELECT 'Wines'    AS category, SUM(MntWines)          AS total_spent FROM customers
    UNION ALL
    SELECT 'Meat',    SUM(MntMeatProducts)    FROM customers
    UNION ALL
    SELECT 'Gold',    SUM(MntGoldProds)       FROM customers
    UNION ALL
    SELECT 'Fish',    SUM(MntFishProducts)    FROM customers
    UNION ALL
    SELECT 'Sweet',   SUM(MntSweetProducts)   FROM customers
    UNION ALL
    SELECT 'Fruits',  SUM(MntFruits)          FROM customers
),
ranked AS (
    SELECT
        category,
        total_spent,
        ROUND(100.0 * total_spent / SUM(total_spent) OVER (), 2) AS pct_of_total,
        SUM(total_spent) OVER (ORDER BY total_spent DESC) AS running_total,
        SUM(total_spent) OVER ()                           AS grand_total
    FROM category_totals
)
SELECT
    category,
    total_spent,
    pct_of_total,
    ROUND(100.0 * running_total / grand_total, 2) AS cumulative_pct
FROM ranked
ORDER BY total_spent DESC;


-- ────────────────────────────────────────────────────────────
-- Query 8: High-Value Customer Identification
-- CTE-based scoring combining spending, frequency, and
-- campaign responsiveness
-- ────────────────────────────────────────────────────────────
WITH scored AS (
    SELECT
        ROWID AS customer_id,
        Income,
        MntTotal,
        Total_Purchases,
        Total_Campaigns_Accepted,
        RFM_Segment,
        NTILE(5) OVER (ORDER BY MntTotal)                 AS spend_quintile,
        NTILE(5) OVER (ORDER BY Total_Purchases)          AS purchase_quintile,
        NTILE(5) OVER (ORDER BY Total_Campaigns_Accepted) AS campaign_quintile
    FROM customers
),
composite AS (
    SELECT
        *,
        spend_quintile + purchase_quintile + campaign_quintile AS composite_score
    FROM scored
)
SELECT
    customer_id,
    Income,
    MntTotal,
    Total_Purchases,
    Total_Campaigns_Accepted,
    RFM_Segment,
    composite_score,
    CASE
        WHEN composite_score >= 13 THEN 'Platinum'
        WHEN composite_score >= 10 THEN 'Gold'
        WHEN composite_score >= 7  THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM composite
ORDER BY composite_score DESC
LIMIT 20;


-- ────────────────────────────────────────────────────────────
-- Query 9: Complaint Analysis — Spending & Engagement Impact
-- Compares metrics between customers who complained vs not
-- ────────────────────────────────────────────────────────────
SELECT
    CASE WHEN Complain = 1 THEN 'Complained' ELSE 'No Complaint' END AS complaint_status,
    COUNT(*)                                AS customer_count,
    ROUND(AVG(Income), 2)                   AS avg_income,
    ROUND(AVG(MntTotal), 2)                 AS avg_spent,
    ROUND(AVG(Total_Purchases), 2)          AS avg_purchases,
    ROUND(AVG(NumWebVisitsMonth), 2)        AS avg_web_visits,
    ROUND(AVG(Total_Campaigns_Accepted), 2) AS avg_campaigns_accepted,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS last_campaign_acceptance_pct
FROM customers
GROUP BY Complain;


-- ────────────────────────────────────────────────────────────
-- Query 10: Marital Status Analysis
-- Reconstructs marital status from one-hot, compares segments
-- ────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN marital_Married = 1 THEN 'Married'
        WHEN marital_Single = 1 THEN 'Single'
        WHEN marital_Together = 1 THEN 'Together'
        WHEN marital_Divorced = 1 THEN 'Divorced'
        WHEN marital_Widow = 1 THEN 'Widow'
        ELSE 'Unknown'
    END AS Marital_Status,
    COUNT(*)                                AS customer_count,
    ROUND(AVG(Income), 2)                   AS avg_income,
    ROUND(AVG(MntTotal), 2)                 AS avg_spent,
    ROUND(AVG(Children), 2)                 AS avg_children,
    ROUND(AVG(Total_Purchases), 2)          AS avg_purchases,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS campaign_response_pct
FROM customers
GROUP BY Marital_Status
ORDER BY avg_spent DESC;
