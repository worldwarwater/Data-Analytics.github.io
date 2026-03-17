"""
Job Market Dataset Generator
Creates a realistic synthetic dataset of 2,500 data-related job postings
with salary, skills, location, remote status, company size, and experience level.
"""

import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

N = 2500

# --- Job Titles with base salary ranges ---
job_titles = {
    'Data Analyst':          (55000, 85000),
    'Senior Data Analyst':   (80000, 120000),
    'Business Analyst':      (52000, 82000),
    'Data Scientist':        (90000, 140000),
    'Senior Data Scientist': (120000, 175000),
    'Data Engineer':         (95000, 145000),
    'Senior Data Engineer':  (130000, 180000),
    'BI Analyst':            (58000, 88000),
    'Analytics Engineer':    (90000, 135000),
    'ML Engineer':           (110000, 165000),
}

title_weights = [0.18, 0.08, 0.14, 0.12, 0.05, 0.10, 0.04, 0.12, 0.08, 0.09]

# --- Locations with cost-of-living multipliers ---
locations = {
    'San Francisco, CA': 1.35, 'New York, NY': 1.30, 'Seattle, WA': 1.25,
    'Austin, TX': 1.05, 'Chicago, IL': 1.05, 'Boston, MA': 1.20,
    'Denver, CO': 1.08, 'Atlanta, GA': 0.95, 'Dallas, TX': 0.98,
    'Portland, OR': 1.08, 'Miami, FL': 1.00, 'Minneapolis, MN': 0.97,
    'Phoenix, AZ': 0.93, 'Raleigh, NC': 0.95, 'Nashville, TN': 0.94,
    'Remote': 1.10,
}

# --- Skills pool ---
skills_pool = {
    'programming': ['Python', 'R', 'SQL', 'Java', 'Scala'],
    'visualization': ['Tableau', 'Power BI', 'Looker', 'Excel', 'Google Sheets'],
    'cloud': ['AWS', 'Azure', 'GCP', 'Snowflake', 'Databricks'],
    'ml_tools': ['Scikit-learn', 'TensorFlow', 'PyTorch', 'XGBoost', 'Spark MLlib'],
    'data_tools': ['Airflow', 'dbt', 'Kafka', 'Docker', 'Git'],
    'databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'BigQuery', 'Redshift'],
}

# Skill probability by title (which categories are common)
title_skill_profile = {
    'Data Analyst':          {'programming': 0.8, 'visualization': 0.9, 'cloud': 0.3, 'ml_tools': 0.15, 'data_tools': 0.3, 'databases': 0.5},
    'Senior Data Analyst':   {'programming': 0.9, 'visualization': 0.9, 'cloud': 0.5, 'ml_tools': 0.3, 'data_tools': 0.5, 'databases': 0.6},
    'Business Analyst':      {'programming': 0.5, 'visualization': 0.85, 'cloud': 0.2, 'ml_tools': 0.05, 'data_tools': 0.15, 'databases': 0.35},
    'Data Scientist':        {'programming': 0.95, 'visualization': 0.6, 'cloud': 0.5, 'ml_tools': 0.85, 'data_tools': 0.4, 'databases': 0.5},
    'Senior Data Scientist': {'programming': 0.98, 'visualization': 0.6, 'cloud': 0.7, 'ml_tools': 0.95, 'data_tools': 0.6, 'databases': 0.6},
    'Data Engineer':         {'programming': 0.9, 'visualization': 0.2, 'cloud': 0.85, 'ml_tools': 0.2, 'data_tools': 0.9, 'databases': 0.85},
    'Senior Data Engineer':  {'programming': 0.95, 'visualization': 0.2, 'cloud': 0.92, 'ml_tools': 0.3, 'data_tools': 0.95, 'databases': 0.9},
    'BI Analyst':            {'programming': 0.5, 'visualization': 0.95, 'cloud': 0.3, 'ml_tools': 0.05, 'data_tools': 0.2, 'databases': 0.5},
    'Analytics Engineer':    {'programming': 0.9, 'visualization': 0.5, 'cloud': 0.7, 'ml_tools': 0.2, 'data_tools': 0.8, 'databases': 0.8},
    'ML Engineer':           {'programming': 0.98, 'visualization': 0.2, 'cloud': 0.8, 'ml_tools': 0.98, 'data_tools': 0.7, 'databases': 0.5},
}

# --- Industries ---
industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Consulting',
              'Media', 'Manufacturing', 'Education', 'Insurance', 'Government']
industry_weights = [0.28, 0.18, 0.12, 0.10, 0.08, 0.06, 0.06, 0.05, 0.04, 0.03]

# --- Company sizes ---
company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Mid-Market (201-1000)',
                 'Large (1001-5000)', 'Enterprise (5000+)']
size_weights = [0.12, 0.18, 0.25, 0.22, 0.23]
size_salary_mult = [0.90, 0.95, 1.00, 1.05, 1.12]

# --- Experience levels ---
exp_levels = ['Entry (0-2 yrs)', 'Mid (3-5 yrs)', 'Senior (6-10 yrs)', 'Lead (10+ yrs)']

# Map titles to likely experience
title_exp_dist = {
    'Data Analyst':          [0.40, 0.40, 0.15, 0.05],
    'Senior Data Analyst':   [0.05, 0.25, 0.50, 0.20],
    'Business Analyst':      [0.35, 0.40, 0.20, 0.05],
    'Data Scientist':        [0.20, 0.45, 0.25, 0.10],
    'Senior Data Scientist': [0.02, 0.15, 0.50, 0.33],
    'Data Engineer':         [0.15, 0.40, 0.30, 0.15],
    'Senior Data Engineer':  [0.02, 0.15, 0.48, 0.35],
    'BI Analyst':            [0.35, 0.40, 0.20, 0.05],
    'Analytics Engineer':    [0.15, 0.45, 0.30, 0.10],
    'ML Engineer':           [0.10, 0.40, 0.35, 0.15],
}

exp_salary_mult = {'Entry (0-2 yrs)': 0.85, 'Mid (3-5 yrs)': 1.0,
                   'Senior (6-10 yrs)': 1.18, 'Lead (10+ yrs)': 1.35}

# --- Work type ---
work_types = ['Remote', 'Hybrid', 'On-Site']

# --- Post dates ---
date_range = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')

# ============================
# GENERATE DATA
# ============================
records = []

for i in range(N):
    # Title
    title = random.choices(list(job_titles.keys()), weights=title_weights, k=1)[0]
    base_low, base_high = job_titles[title]

    # Location
    loc = random.choices(list(locations.keys()), k=1)[0]
    col_mult = locations[loc]

    # Work type (Remote locations forced to Remote)
    if loc == 'Remote':
        work_type = 'Remote'
    else:
        work_type = random.choices(work_types, weights=[0.30, 0.40, 0.30], k=1)[0]

    # Company size
    size_idx = random.choices(range(5), weights=size_weights, k=1)[0]
    company_size = company_sizes[size_idx]
    size_mult = size_salary_mult[size_idx]

    # Experience
    exp = random.choices(exp_levels, weights=title_exp_dist[title], k=1)[0]
    exp_mult = exp_salary_mult[exp]

    # Industry
    industry = random.choices(industries, weights=industry_weights, k=1)[0]

    # Remote premium
    remote_premium = 1.03 if work_type == 'Remote' else 1.0

    # Calculate salary with noise
    base_salary = np.random.uniform(base_low, base_high)
    salary = base_salary * col_mult * size_mult * exp_mult * remote_premium
    salary = int(round(salary / 1000) * 1000)  # Round to nearest 1000
    salary = max(salary, 40000)  # Floor

    # Skills (2-5 per posting based on profile)
    profile = title_skill_profile[title]
    posting_skills = []
    for cat, prob in profile.items():
        if random.random() < prob:
            # Pick 1-2 skills from this category
            n_skills = random.choices([1, 2], weights=[0.6, 0.4], k=1)[0]
            posting_skills.extend(random.sample(skills_pool[cat], min(n_skills, len(skills_pool[cat]))))
    # Ensure at least 2 skills
    if len(posting_skills) < 2:
        posting_skills.extend(random.sample(skills_pool['programming'], 2))
    posting_skills = list(set(posting_skills))  # Dedupe
    random.shuffle(posting_skills)

    # Post date
    post_date = random.choice(date_range)

    # Number of applicants (correlated with title popularity and remote)
    base_applicants = np.random.poisson(80)
    if work_type == 'Remote':
        base_applicants = int(base_applicants * 1.6)
    if 'Entry' in exp:
        base_applicants = int(base_applicants * 1.4)

    records.append({
        'job_id': f'JP-{10000 + i}',
        'job_title': title,
        'salary_usd': salary,
        'location': loc,
        'work_type': work_type,
        'experience_level': exp,
        'industry': industry,
        'company_size': company_size,
        'skills_required': ', '.join(posting_skills),
        'num_skills': len(posting_skills),
        'post_date': post_date.strftime('%Y-%m-%d'),
        'applicants': base_applicants,
    })

df = pd.DataFrame(records)

# Save
output_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(output_dir, 'job_postings_2025.csv')
df.to_csv(csv_path, index=False)

print(f"Dataset generated: {len(df)} job postings")
print(f"Saved to: {csv_path}")
print(f"\nSample:")
print(df.head(3).to_string(index=False))
print(f"\nTitle distribution:")
print(df['job_title'].value_counts().to_string())
print(f"\nSalary stats:")
print(df['salary_usd'].describe().to_string())
print(f"\nWork type distribution:")
print(df['work_type'].value_counts().to_string())
