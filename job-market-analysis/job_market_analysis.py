"""
Job Market Analysis Pipeline
============================
Loads job posting data into SQLite, runs SQL analysis queries,
performs statistical testing in Python, and generates publication-quality charts.

Skills demonstrated: SQL, Python (pandas, scipy), data visualization, database design
"""

import pandas as pd
import numpy as np
import sqlite3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# ---- Configuration ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'job_postings_2025.csv')
DB_PATH = os.path.join(BASE_DIR, 'job_market.db')
SQL_DIR = os.path.join(BASE_DIR, 'sql')
CHART_DIR = os.path.join(BASE_DIR, 'charts')
os.makedirs(CHART_DIR, exist_ok=True)

# ---- Style Configuration ----
COLORS = {
    'primary': '#2563EB',
    'secondary': '#7C3AED',
    'accent': '#059669',
    'warm': '#DC2626',
    'orange': '#EA580C',
    'slate': '#475569',
    'light_bg': '#F8FAFC',
}
PALETTE = [COLORS['primary'], COLORS['secondary'], COLORS['accent'],
           COLORS['warm'], COLORS['orange'], '#0891B2', '#CA8A04', '#BE185D']

sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['figure.facecolor'] = COLORS['light_bg']
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['font.family'] = 'sans-serif'

print("=" * 60)
print("  JOB MARKET ANALYSIS PIPELINE")
print("=" * 60)

# ==============================
# PHASE 1: Load Data into SQLite
# ==============================
print("\n[Phase 1] Loading data into SQLite...")

df = pd.read_csv(CSV_PATH)
print(f"  Loaded {len(df)} job postings from CSV")

# Create database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Run schema creation
with open(os.path.join(SQL_DIR, 'create_database.sql'), 'r') as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)

# Insert job postings
for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO job_postings
        (job_id, job_title, salary_usd, location, work_type, experience_level,
         industry, company_size, num_skills, post_date, applicants)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row['job_id'], row['job_title'], row['salary_usd'], row['location'],
          row['work_type'], row['experience_level'], row['industry'],
          row['company_size'], row['num_skills'], row['post_date'], row['applicants']))

# Insert normalized skills
for _, row in df.iterrows():
    skills = [s.strip() for s in row['skills_required'].split(',')]
    for skill in skills:
        cursor.execute("INSERT OR IGNORE INTO job_skills VALUES (?, ?)",
                      (row['job_id'], skill))

conn.commit()
print(f"  Database created: {DB_PATH}")
print(f"  job_postings: {cursor.execute('SELECT COUNT(*) FROM job_postings').fetchone()[0]} rows")
print(f"  job_skills: {cursor.execute('SELECT COUNT(*) FROM job_skills').fetchone()[0]} rows")


# ==============================
# PHASE 2: Run SQL Analysis
# ==============================
print("\n[Phase 2] Running SQL analysis queries...")

# Q1: Top paying skills
q1 = pd.read_sql_query("""
    SELECT js.skill, sc.category, COUNT(*) AS job_count,
           ROUND(AVG(jp.salary_usd)) AS avg_salary,
           ROUND(AVG(jp.salary_usd) - (SELECT AVG(salary_usd) FROM job_postings)) AS salary_premium
    FROM job_skills js
    JOIN job_postings jp ON js.job_id = jp.job_id
    JOIN skill_categories sc ON js.skill = sc.skill
    GROUP BY js.skill, sc.category
    HAVING COUNT(*) >= 30
    ORDER BY avg_salary DESC LIMIT 10
""", conn)
print("\n  Q1: Top 10 Highest-Paying Skills")
print(q1.to_string(index=False))

# Q2: Remote vs On-Site pay gap
q2 = pd.read_sql_query("""
    SELECT work_type, COUNT(*) AS posting_count,
           ROUND(AVG(salary_usd)) AS avg_salary,
           ROUND(AVG(applicants)) AS avg_applicants
    FROM job_postings GROUP BY work_type ORDER BY avg_salary DESC
""", conn)
print("\n  Q2: Pay by Work Type")
print(q2.to_string(index=False))

# Q3: Remote vs On-Site by title
q3 = pd.read_sql_query("""
    SELECT jp.job_title,
           ROUND(AVG(CASE WHEN jp.work_type='Remote' THEN jp.salary_usd END)) AS avg_remote,
           ROUND(AVG(CASE WHEN jp.work_type='On-Site' THEN jp.salary_usd END)) AS avg_onsite,
           ROUND(AVG(CASE WHEN jp.work_type='Remote' THEN jp.salary_usd END) -
                 AVG(CASE WHEN jp.work_type='On-Site' THEN jp.salary_usd END)) AS remote_premium
    FROM job_postings jp GROUP BY jp.job_title
    HAVING COUNT(CASE WHEN jp.work_type='Remote' THEN 1 END) >= 10
       AND COUNT(CASE WHEN jp.work_type='On-Site' THEN 1 END) >= 10
    ORDER BY remote_premium DESC
""", conn)
print("\n  Q3: Remote Premium by Title")
print(q3.to_string(index=False))

# Q4: Salary by city
q4 = pd.read_sql_query("""
    SELECT location, COUNT(*) AS job_count, ROUND(AVG(salary_usd)) AS avg_salary,
           ROUND(AVG(applicants)) AS avg_applicants
    FROM job_postings GROUP BY location HAVING COUNT(*) >= 20
    ORDER BY avg_salary DESC
""", conn)
print("\n  Q4: Salary by City")
print(q4.to_string(index=False))

# Q5: Most in-demand skills
q5 = pd.read_sql_query("""
    SELECT js.skill, sc.category, COUNT(*) AS demand_count,
           ROUND(100.0 * COUNT(*) / (SELECT COUNT(DISTINCT job_id) FROM job_postings), 1) AS pct_of_postings,
           ROUND(AVG(jp.salary_usd)) AS avg_salary
    FROM job_skills js
    JOIN job_postings jp ON js.job_id = jp.job_id
    JOIN skill_categories sc ON js.skill = sc.skill
    GROUP BY js.skill ORDER BY demand_count DESC LIMIT 15
""", conn)
print("\n  Q5: Most In-Demand Skills")
print(q5.to_string(index=False))

# Q6: Salary by experience
q6 = pd.read_sql_query("""
    SELECT experience_level, COUNT(*) AS posting_count,
           ROUND(AVG(salary_usd)) AS avg_salary,
           ROUND(AVG(applicants)) AS avg_applicants
    FROM job_postings GROUP BY experience_level ORDER BY avg_salary
""", conn)
print("\n  Q6: Salary by Experience Level")
print(q6.to_string(index=False))

# Q7: Best skill pairs
q7 = pd.read_sql_query("""
    SELECT a.skill AS skill_1, b.skill AS skill_2,
           COUNT(*) AS pair_count, ROUND(AVG(jp.salary_usd)) AS avg_salary
    FROM job_skills a
    JOIN job_skills b ON a.job_id = b.job_id AND a.skill < b.skill
    JOIN job_postings jp ON a.job_id = jp.job_id
    GROUP BY a.skill, b.skill HAVING pair_count >= 20
    ORDER BY avg_salary DESC LIMIT 15
""", conn)
print("\n  Q7: Highest-Paying Skill Pairs")
print(q7.to_string(index=False))

# Q8: Industry comparison
q8 = pd.read_sql_query("""
    SELECT industry, COUNT(*) AS posting_count, ROUND(AVG(salary_usd)) AS avg_salary,
           ROUND(AVG(CASE WHEN experience_level='Entry (0-2 yrs)' THEN salary_usd END)) AS entry_salary,
           ROUND(1.0 * SUM(CASE WHEN work_type='Remote' THEN 1 ELSE 0 END)/COUNT(*)*100, 1) AS pct_remote
    FROM job_postings GROUP BY industry ORDER BY avg_salary DESC
""", conn)
print("\n  Q8: Industry Comparison")
print(q8.to_string(index=False))


# ==============================
# PHASE 3: Statistical Analysis
# ==============================
print("\n[Phase 3] Statistical Analysis...")

# Test: Is remote pay significantly different from on-site?
remote_salaries = df[df['work_type'] == 'Remote']['salary_usd']
onsite_salaries = df[df['work_type'] == 'On-Site']['salary_usd']
hybrid_salaries = df[df['work_type'] == 'Hybrid']['salary_usd']

try:
    from scipy import stats

    # T-test: Remote vs On-Site
    t_stat, p_value = stats.ttest_ind(remote_salaries, onsite_salaries)
    print(f"\n  Remote vs On-Site T-Test:")
    print(f"    Remote mean: ${remote_salaries.mean():,.0f} | On-Site mean: ${onsite_salaries.mean():,.0f}")
    print(f"    Difference: ${remote_salaries.mean() - onsite_salaries.mean():,.0f}")
    print(f"    T-statistic: {t_stat:.3f} | P-value: {p_value:.6f}")
    print(f"    Significant at α=0.05? {'YES' if p_value < 0.05 else 'NO'}")

    # ANOVA: All three work types
    f_stat, anova_p = stats.f_oneway(remote_salaries, hybrid_salaries, onsite_salaries)
    print(f"\n  One-Way ANOVA (Remote vs Hybrid vs On-Site):")
    print(f"    F-statistic: {f_stat:.3f} | P-value: {anova_p:.6f}")
    print(f"    Significant? {'YES' if anova_p < 0.05 else 'NO'}")

    # Effect size (Cohen's d) for Remote vs On-Site
    pooled_std = np.sqrt(((len(remote_salaries)-1)*remote_salaries.std()**2 +
                          (len(onsite_salaries)-1)*onsite_salaries.std()**2) /
                         (len(remote_salaries) + len(onsite_salaries) - 2))
    cohens_d = (remote_salaries.mean() - onsite_salaries.mean()) / pooled_std
    print(f"\n  Effect Size (Cohen's d): {cohens_d:.3f}")
    effect_label = 'Small' if abs(cohens_d) < 0.5 else 'Medium' if abs(cohens_d) < 0.8 else 'Large'
    print(f"  Interpretation: {effect_label} effect")

    # Chi-square: Are certain industries more likely to offer remote?
    contingency = pd.crosstab(df['industry'], df['work_type'])
    chi2, chi_p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\n  Chi-Square Test: Industry × Work Type")
    print(f"    Chi² = {chi2:.2f} | P-value = {chi_p:.6f} | df = {dof}")
    print(f"    Significant? {'YES' if chi_p < 0.05 else 'NO'}")

    HAS_SCIPY = True

except ImportError:
    print("  scipy not available — skipping statistical tests")
    print("  Install with: pip install scipy")
    HAS_SCIPY = False

# Descriptive stats regardless
print(f"\n  Salary by Work Type (descriptive):")
for wt in ['Remote', 'Hybrid', 'On-Site']:
    subset = df[df['work_type'] == wt]['salary_usd']
    print(f"    {wt:8s}: mean=${subset.mean():>9,.0f}  median=${subset.median():>9,.0f}  std=${subset.std():>9,.0f}  n={len(subset)}")


# ==============================
# PHASE 4: Visualizations
# ==============================
print("\n[Phase 4] Generating visualizations...")


# --- Chart 1: Top 10 Highest-Paying Skills ---
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(q1['skill'][::-1], q1['avg_salary'][::-1], color=PALETTE[:len(q1)], edgecolor='white', height=0.7)
for bar, val in zip(bars, q1['avg_salary'][::-1]):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontweight='bold', fontsize=11)
ax.set_xlabel('Average Salary (USD)', fontsize=13)
ax.set_title('Top 10 Highest-Paying Skills in Data Roles', fontsize=16, fontweight='bold', pad=15)
ax.axvline(x=df['salary_usd'].mean(), color=COLORS['warm'], linestyle='--', alpha=0.7, label=f'Overall Avg: ${df["salary_usd"].mean():,.0f}')
ax.legend(fontsize=11)
ax.set_xlim(0, q1['avg_salary'].max() * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '01_top_paying_skills.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 01_top_paying_skills.png")


# --- Chart 2: Remote vs Hybrid vs On-Site Salary Distribution ---
fig, ax = plt.subplots(figsize=(12, 7))
work_order = ['Remote', 'Hybrid', 'On-Site']
work_colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
for wt, color in zip(work_order, work_colors):
    subset = df[df['work_type'] == wt]['salary_usd']
    ax.hist(subset, bins=40, alpha=0.5, label=f'{wt} (n={len(subset)}, avg=${subset.mean():,.0f})',
            color=color, edgecolor='white')
    ax.axvline(subset.mean(), color=color, linestyle='--', linewidth=2, alpha=0.8)
ax.set_xlabel('Annual Salary (USD)', fontsize=13)
ax.set_ylabel('Number of Postings', fontsize=13)
ax.set_title('Salary Distribution by Work Type', fontsize=16, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '02_salary_by_work_type.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 02_salary_by_work_type.png")


# --- Chart 3: Average Salary by City ---
fig, ax = plt.subplots(figsize=(12, 8))
city_data = q4.sort_values('avg_salary', ascending=True)
colors = [COLORS['primary'] if loc != 'Remote' else COLORS['accent'] for loc in city_data['location']]
bars = ax.barh(city_data['location'], city_data['avg_salary'], color=colors, edgecolor='white', height=0.7)
for bar, val in zip(bars, city_data['avg_salary']):
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontweight='bold', fontsize=10)
national_avg = df['salary_usd'].mean()
ax.axvline(x=national_avg, color=COLORS['warm'], linestyle='--', alpha=0.7,
           label=f'National Avg: ${national_avg:,.0f}')
ax.set_xlabel('Average Salary (USD)', fontsize=13)
ax.set_title('Average Data Role Salary by Location', fontsize=16, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.set_xlim(0, city_data['avg_salary'].max() * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '03_salary_by_city.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 03_salary_by_city.png")


# --- Chart 4: Most In-Demand Skills ---
fig, ax = plt.subplots(figsize=(12, 8))
demand_data = q5.sort_values('demand_count', ascending=True).tail(15)
cat_colors = {'Programming': COLORS['primary'], 'Visualization': COLORS['secondary'],
              'Cloud': COLORS['accent'], 'ML/AI': COLORS['warm'],
              'Data Engineering': COLORS['orange'], 'Databases': '#0891B2'}
bar_colors = [cat_colors.get(c, COLORS['slate']) for c in demand_data['category']]
bars = ax.barh(demand_data['skill'], demand_data['demand_count'], color=bar_colors, edgecolor='white', height=0.7)
for bar, pct in zip(bars, demand_data['pct_of_postings']):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f'{pct}%', va='center', fontweight='bold', fontsize=10)
ax.set_xlabel('Number of Job Postings', fontsize=13)
ax.set_title('Most In-Demand Skills (% of All Postings)', fontsize=16, fontweight='bold', pad=15)
# Legend for categories
from matplotlib.patches import Patch
legend_handles = [Patch(facecolor=cat_colors[c], label=c) for c in cat_colors]
ax.legend(handles=legend_handles, loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '04_most_in_demand_skills.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 04_most_in_demand_skills.png")


# --- Chart 5: Salary by Experience Level ---
fig, ax = plt.subplots(figsize=(12, 7))
exp_order = ['Entry (0-2 yrs)', 'Mid (3-5 yrs)', 'Senior (6-10 yrs)', 'Lead (10+ yrs)']
box_data = [df[df['experience_level'] == exp]['salary_usd'].values for exp in exp_order]
bp = ax.boxplot(box_data, patch_artist=True, labels=exp_order, widths=0.6,
                medianprops=dict(color='black', linewidth=2))
for patch, color in zip(bp['boxes'], [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warm']]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
# Add mean markers
means = [np.mean(d) for d in box_data]
ax.scatter(range(1, 5), means, color='black', marker='D', s=80, zorder=5, label='Mean')
for i, m in enumerate(means):
    ax.text(i + 1.15, m, f'${m:,.0f}', va='center', fontsize=10, fontweight='bold')
ax.set_ylabel('Annual Salary (USD)', fontsize=13)
ax.set_title('Salary Distribution by Experience Level', fontsize=16, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '05_salary_by_experience.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 05_salary_by_experience.png")


# --- Chart 6: Industry Salary & Remote % Bubble Chart ---
fig, ax = plt.subplots(figsize=(12, 8))
for i, (_, row) in enumerate(q8.iterrows()):
    ax.scatter(row['pct_remote'], row['avg_salary'],
               s=row['posting_count'] * 3, color=PALETTE[i % len(PALETTE)],
               alpha=0.7, edgecolors='white', linewidth=1.5)
    ax.annotate(row['industry'], (row['pct_remote'], row['avg_salary']),
                textcoords='offset points', xytext=(8, 5), fontsize=10, fontweight='bold')
ax.set_xlabel('% Remote Postings', fontsize=13)
ax.set_ylabel('Average Salary (USD)', fontsize=13)
ax.set_title('Industry: Salary vs Remote Availability\n(bubble size = # of postings)',
             fontsize=16, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '06_industry_salary_vs_remote.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 06_industry_salary_vs_remote.png")


# --- Chart 7: Top Skill Pairs Heatmap ---
fig, ax = plt.subplots(figsize=(12, 8))
pair_data = q7.head(12)
pair_labels = [f"{row['skill_1']} + {row['skill_2']}" for _, row in pair_data.iterrows()]
bars = ax.barh(pair_labels[::-1], pair_data['avg_salary'][::-1],
               color=[PALETTE[i % len(PALETTE)] for i in range(len(pair_data))],
               edgecolor='white', height=0.7)
for bar, (_, row) in zip(bars, pair_data[::-1].iterrows()):
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f'${row["avg_salary"]:,.0f} (n={row["pair_count"]})',
            va='center', fontsize=10, fontweight='bold')
ax.set_xlabel('Average Salary (USD)', fontsize=13)
ax.set_title('Highest-Paying Skill Combinations', fontsize=16, fontweight='bold', pad=15)
ax.set_xlim(0, pair_data['avg_salary'].max() * 1.18)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '07_top_skill_pairs.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 07_top_skill_pairs.png")


# --- Chart 8: Remote Premium by Job Title ---
fig, ax = plt.subplots(figsize=(12, 7))
premium_data = q3.sort_values('remote_premium', ascending=True)
colors = [COLORS['accent'] if v > 0 else COLORS['warm'] for v in premium_data['remote_premium']]
bars = ax.barh(premium_data['job_title'], premium_data['remote_premium'],
               color=colors, edgecolor='white', height=0.6)
for bar, val in zip(bars, premium_data['remote_premium']):
    offset = 500 if val > 0 else -500
    ha = 'left' if val > 0 else 'right'
    ax.text(bar.get_width() + offset, bar.get_y() + bar.get_height()/2,
            f'${val:+,.0f}', va='center', ha=ha, fontweight='bold', fontsize=11)
ax.axvline(x=0, color='black', linewidth=1)
ax.set_xlabel('Remote Salary Premium (USD)', fontsize=13)
ax.set_title('Remote vs On-Site Salary Premium by Role', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:+.0f}K'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '08_remote_premium_by_title.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 08_remote_premium_by_title.png")


# ==============================
# PHASE 5: Export for Looker Studio
# ==============================
print("\n[Phase 5] Exporting Looker Studio data...")

# Enrich the main dataset for dashboarding
export_df = df.copy()

# Add salary band
export_df['salary_band'] = pd.cut(export_df['salary_usd'],
    bins=[0, 60000, 80000, 100000, 130000, 170000, 500000],
    labels=['<$60K', '$60-80K', '$80-100K', '$100-130K', '$130-170K', '$170K+'])

# Add month/quarter
export_df['post_date'] = pd.to_datetime(export_df['post_date'])
export_df['post_month'] = export_df['post_date'].dt.strftime('%Y-%m')
export_df['post_quarter'] = export_df['post_date'].dt.to_period('Q').astype(str)

# Extract top skills as individual columns for filtering
top_skills = ['Python', 'SQL', 'Tableau', 'Power BI', 'Excel', 'AWS',
              'Snowflake', 'Scikit-learn', 'TensorFlow', 'dbt']
for skill in top_skills:
    export_df[f'has_{skill.lower().replace(" ", "_").replace("-", "_")}'] = \
        export_df['skills_required'].str.contains(skill, case=False).astype(int)

# Competition index (applicants relative to average)
avg_applicants = export_df['applicants'].mean()
export_df['competition_index'] = (export_df['applicants'] / avg_applicants * 100).round(0).astype(int)

export_path = os.path.join(BASE_DIR, 'job_market_dashboard_data.csv')
export_df.to_csv(export_path, index=False)
print(f"  Exported {len(export_df)} rows to {export_path}")

# Also export a skills summary for a second Looker table
skills_summary = pd.read_sql_query("""
    SELECT js.skill, sc.category, COUNT(*) AS job_count,
           ROUND(AVG(jp.salary_usd)) AS avg_salary,
           ROUND(AVG(jp.applicants)) AS avg_applicants
    FROM job_skills js
    JOIN job_postings jp ON js.job_id = jp.job_id
    JOIN skill_categories sc ON js.skill = sc.skill
    GROUP BY js.skill, sc.category
    ORDER BY job_count DESC
""", conn)
skills_path = os.path.join(BASE_DIR, 'skills_summary.csv')
skills_summary.to_csv(skills_path, index=False)
print(f"  Exported skills summary to {skills_path}")

conn.close()


# ==============================
# SUMMARY
# ==============================
print("\n" + "=" * 60)
print("  ANALYSIS COMPLETE — KEY FINDINGS")
print("=" * 60)

overall_avg = df['salary_usd'].mean()
remote_avg = remote_salaries.mean()
onsite_avg = onsite_salaries.mean()
top_skill = q1.iloc[0]
top_city = q4.iloc[0]

print(f"""
  1. REMOTE PAY GAP: Remote roles pay ${remote_avg - onsite_avg:,.0f} more than on-site
     (${remote_avg:,.0f} vs ${onsite_avg:,.0f})
     {'Statistically significant (p<0.05)' if HAS_SCIPY and p_value < 0.05 else ''}

  2. TOP PAYING SKILL: {top_skill['skill']} at ${top_skill['avg_salary']:,.0f} avg
     (${top_skill['salary_premium']:+,.0f} above overall average)

  3. TOP PAYING CITY: {top_city['location']} at ${top_city['avg_salary']:,.0f} avg

  4. EXPERIENCE PREMIUM: Lead roles earn ${df[df['experience_level']=='Lead (10+ yrs)']['salary_usd'].mean():,.0f}
     vs Entry at ${df[df['experience_level']=='Entry (0-2 yrs)']['salary_usd'].mean():,.0f}
     ({((df[df['experience_level']=='Lead (10+ yrs)']['salary_usd'].mean() / df[df['experience_level']=='Entry (0-2 yrs)']['salary_usd'].mean()) - 1) * 100:.0f}% premium)

  5. CAREER ADVICE: Entry-level analysts should focus on Python + SQL + a viz tool.
     The highest-paying entry path is through Data Engineering or ML roles.
""")

print(f"\n  Files generated:")
print(f"    📊 Database: job_market.db")
print(f"    📈 Charts: {len(os.listdir(CHART_DIR))} visualizations in charts/")
print(f"    📋 Dashboard data: job_market_dashboard_data.csv")
print(f"    📋 Skills summary: skills_summary.csv")
print(f"    📝 SQL queries: sql/analysis_queries.sql")
