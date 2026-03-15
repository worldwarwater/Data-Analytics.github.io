# Looker Studio Dashboard Setup Guide

Follow these steps to create an interactive churn dashboard using the exported data.

## Step 1: Upload Data

1. Go to [Looker Studio](https://lookerstudio.google.com/)
2. Click **Create → Report**
3. Click **Add data → File Upload**
4. Upload `churn_dashboard_data.csv` from this project
5. Click **Add** to connect the data

## Step 2: Create KPI Cards (Top Row)

Add four **Scorecard** components across the top:

| KPI | Metric | Configuration |
|-----|--------|---------------|
| Total Customers | Record Count | Default |
| Churn Rate | churn_flag | Change to AVG, format as % |
| Avg Monthly Revenue | MonthlyCharges | Change to AVG, format as $ |
| Revenue at Risk | MonthlyCharges | Add filter: Churn = "Yes", use SUM |

**Styling:** Use a dark header bar (#1F4E79), white text, large font (32pt).

## Step 3: Add Charts

### Chart 1: Churn by Contract Type (Bar Chart)
- Dimension: `Contract`
- Metric: `churn_flag` (AVG)
- Sort: Descending by metric
- Colors: Red for month-to-month, yellow for one year, green for two year

### Chart 2: Churn by Tenure Group (Bar Chart)
- Dimension: `tenure_group`
- Metric: `churn_flag` (AVG)
- Sort: By dimension ascending

### Chart 3: Churn by Internet Service (Pie Chart)
- Dimension: `InternetService`
- Metric: Record Count
- Add filter: Churn = "Yes"

### Chart 4: Monthly Charges Distribution (Histogram/Scatter)
- Dimension: `MonthlyCharges`
- Metric: Record Count
- Breakdown: `Churn`

### Chart 5: Payment Method Comparison (Horizontal Bar)
- Dimension: `PaymentMethod`
- Metric: `churn_flag` (AVG)
- Sort: Descending

## Step 4: Add Filters

Add dropdown filter controls at the top for:
- `Contract` — lets stakeholders focus on a specific contract type
- `InternetService` — filter by internet tier
- `risk_segment` — High / Medium / Low risk (if ML model was run)
- `tenure_group` — filter by customer tenure

## Step 5: Styling

- **Theme:** Use a clean blue theme (#1F4E79 header, white background)
- **Font:** Roboto or Arial
- **Layout:** 2 columns, KPIs across top, charts below
- **Page size:** US Letter landscape (11" × 8.5")

## Step 6: Share

1. Click **Share** in the top right
2. Set to "Anyone with the link can view"
3. Copy the link for your portfolio README

## Final Result

Your dashboard should have:
- 4 KPI cards summarizing the business impact
- 5 interactive charts showing churn drivers
- 4 filter controls for stakeholder exploration
- Clean, professional styling matching your portfolio theme
