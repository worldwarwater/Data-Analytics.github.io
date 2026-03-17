# Looker Studio Dashboard Setup — Job Market Analysis

## Step 1: Open Looker Studio

Go to [lookerstudio.google.com](https://lookerstudio.google.com) and sign in with your Google account.

Click **"Blank Report"** (the big + card) or **Create → Report**.

## Step 2: Upload Your Data

1. A "Add data to report" panel opens automatically
2. On the left sidebar, scroll down and click **"File Upload"**
3. Click **"Upload"** and select `job_market_dashboard_data.csv` from your `job-market-analysis` folder
4. Click **"Add"** in the bottom right
5. If it asks "Add to report?" click **"Add to Report"**

## Step 3: Set Up Your Fields

After the data loads, click **Resource → Manage added data sources → Edit** (pencil icon next to your CSV).

Set these field types:

| Field | Type | Aggregation |
|-------|------|-------------|
| salary_usd | Number | Average |
| applicants | Number | Average |
| competition_index | Number | Average |
| post_date | Date (YYYY-MM-DD) | None |
| num_skills | Number | Average |
| All `has_*` columns | Number | Sum |
| Everything else | Text | None |

Click **"Done"** then **"Close"**.

## Step 4: Set the Page Size & Title

1. Click anywhere on the blank canvas background
2. In the right panel under **"Layout"**, set canvas size to **1200 × 900**
3. Click **Insert → Text box**, type **"Data Job Market Analysis — 2025"**
4. Make it bold, size 24, and drag it to the top center

## Step 5: Add KPI Scorecards (Top Row)

You'll add 4 scorecards across the top. For each one:

1. Click **Insert → Scorecard**
2. Draw a rectangle at the top of the page
3. In the right **Data** panel, set the metric

**Scorecard 1 — Total Postings:**
- Metric: `job_id` → Aggregation: **Count Distinct**
- Label: "Total Postings"

**Scorecard 2 — Avg Salary:**
- Metric: `salary_usd` → Aggregation: **Average**
- Format: Currency (USD), 0 decimal places
- Label: "Avg Salary"

**Scorecard 3 — Remote %:**
- Metric: Create a calculated field:
  - Click the metric field → **"Create Field"**
  - Name: `Remote Percentage`
  - Formula: `COUNT_DISTINCT(CASE WHEN work_type = "Remote" THEN job_id ELSE NULL END) / COUNT_DISTINCT(job_id)`
  - Set type to **Percent**
- Label: "Remote %"

**Scorecard 4 — Avg Applicants:**
- Metric: `applicants` → Aggregation: **Average**
- Label: "Avg Applicants"

Space them evenly across the top row.

## Step 6: Add Filters (Below KPIs)

**Filter 1 — Work Type:**
1. Click **Insert → Drop-down list**
2. Draw it below the KPIs on the left
3. Control field: `work_type`
4. Metric: None needed

**Filter 2 — Experience Level:**
1. Insert → Drop-down list
2. Control field: `experience_level`

**Filter 3 — Industry:**
1. Insert → Drop-down list
2. Control field: `industry`

**Filter 4 — Job Title:**
1. Insert → Drop-down list
2. Control field: `job_title`

These filters will automatically control every chart on the page.

## Step 7: Bar Chart — Average Salary by Job Title

1. Click **Insert → Bar chart**
2. Draw a large rectangle on the left half of the page
3. **Data panel settings:**
   - Dimension: `job_title`
   - Metric: `salary_usd` (Aggregation: Average)
   - Sort: `salary_usd` descending
4. **Style panel:**
   - Set bar color to a blue (#2563EB)
   - Check "Show data labels"
   - Title: "Average Salary by Role"

## Step 8: Bar Chart — Top Skills by Demand

1. Insert → Bar chart (horizontal)
2. Draw it on the right half
3. **Data panel:**
   - Dimension: Create a calculated field — but this is tricky with the CSV format
   - Instead: **Add the `skills_summary.csv` as a second data source**
     - Click **Resource → Manage added data sources → Add a data source**
     - File Upload → Upload `skills_summary.csv`
     - Add to report
   - Now in your chart, switch data source to `skills_summary`
   - Dimension: `skill`
   - Metric: `job_count` (Sum)
   - Sort: `job_count` descending
   - Rows: 15
4. **Style:** Different color (#7C3AED), show data labels

## Step 9: Geo Map — Salary by City

1. Insert → **Google Maps** chart
2. **Data panel:**
   - Location field: `location`
   - Color metric: `salary_usd` (Average)
   - Size metric: `job_id` (Count Distinct)
3. **Style:**
   - Color range: Light blue → Dark blue
   - Title: "Salary by Location"

*If the map doesn't recognize cities well, use a plain bar chart with `location` as dimension instead.*

## Step 10: Pie Chart — Work Type Distribution

1. Insert → Pie chart
2. Dimension: `work_type`
3. Metric: `job_id` (Count Distinct)
4. Style: Use 3 distinct colors, show labels with percentages
5. Title: "Work Type Split"

## Step 11: Line Chart — Monthly Posting Trends

1. Insert → Time series (line chart)
2. Date dimension: `post_date`
3. Metric: `job_id` (Count Distinct)
4. Set date granularity to **Month** (click the date field → select "Year Month")
5. Title: "Monthly Posting Volume"

## Step 12: Table — Detailed Skill Breakdown

1. Insert → Table
2. Switch data source to `skills_summary`
3. Dimensions: `skill`, `category`
4. Metrics: `job_count` (Sum), `avg_salary` (Average)
5. Sort: `avg_salary` descending
6. Enable pagination (10 rows per page)
7. Style: Add alternating row colors

## Step 13: Final Polish

1. **Background:** Click canvas → Style → Background color: `#F8FAFC` (light gray)
2. **Borders:** Select each chart → Style → Add a light border
3. **Alignment:** Select all charts → Arrange → Distribute evenly
4. **Title bar:** Add a colored rectangle behind your title text (dark blue, `#1E3A5F`)
5. **Source note:** Add a text box at the bottom: "Data: 2,500 synthetic job postings | Analysis: Python + SQL + Looker Studio"

## Step 14: Share Your Dashboard

1. Click the blue **"Share"** button (top right)
2. Click **"Manage access"**
3. Change from "Restricted" to **"Anyone with the link can view"**
4. Copy the link
5. Click the 3 dots → **"Get report link"** to get the shareable URL

Paste that URL into your README where it says `*(link added after upload)*`.

## Layout Reference

```
┌─────────────────────────────────────────────────────────┐
│          Data Job Market Analysis — 2025                │
├──────────┬──────────┬──────────┬────────────────────────┤
│ Postings │ Avg Sal  │ Remote % │ Avg Applicants         │
│  2,500   │ $116.6K  │  33.1%   │    103                 │
├──────────┴──────────┴──────────┴────────────────────────┤
│ [Work Type ▼] [Experience ▼] [Industry ▼] [Title ▼]    │
├────────────────────────────┬────────────────────────────┤
│                            │                            │
│  Avg Salary by Role        │  Top Skills by Demand      │
│  (horizontal bar)          │  (horizontal bar)          │
│                            │                            │
├────────────────────────────┬──────────┬─────────────────┤
│                            │          │                 │
│  Salary by Location        │ Work Type│ Monthly Trends  │
│  (map or bar)              │ (pie)    │ (line chart)    │
│                            │          │                 │
├────────────────────────────┴──────────┴─────────────────┤
│  Skill Breakdown Table (skill, category, count, salary) │
└─────────────────────────────────────────────────────────┘
```
