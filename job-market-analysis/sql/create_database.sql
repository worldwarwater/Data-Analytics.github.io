-- ============================================
-- Job Market Analysis - Database Schema
-- Creates normalized tables from raw CSV data
-- ============================================

-- Main job postings table
CREATE TABLE IF NOT EXISTS job_postings (
    job_id TEXT PRIMARY KEY,
    job_title TEXT NOT NULL,
    salary_usd INTEGER NOT NULL,
    location TEXT NOT NULL,
    work_type TEXT NOT NULL CHECK(work_type IN ('Remote', 'Hybrid', 'On-Site')),
    experience_level TEXT NOT NULL,
    industry TEXT NOT NULL,
    company_size TEXT NOT NULL,
    num_skills INTEGER,
    post_date DATE NOT NULL,
    applicants INTEGER
);

-- Normalized skills table (one row per job-skill pair)
CREATE TABLE IF NOT EXISTS job_skills (
    job_id TEXT NOT NULL,
    skill TEXT NOT NULL,
    PRIMARY KEY (job_id, skill),
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id)
);

-- Skill categories lookup
CREATE TABLE IF NOT EXISTS skill_categories (
    skill TEXT PRIMARY KEY,
    category TEXT NOT NULL
);

-- Populate skill categories
INSERT OR IGNORE INTO skill_categories VALUES
    ('Python', 'Programming'), ('R', 'Programming'), ('SQL', 'Programming'),
    ('Java', 'Programming'), ('Scala', 'Programming'),
    ('Tableau', 'Visualization'), ('Power BI', 'Visualization'),
    ('Looker', 'Visualization'), ('Excel', 'Visualization'),
    ('Google Sheets', 'Visualization'),
    ('AWS', 'Cloud'), ('Azure', 'Cloud'), ('GCP', 'Cloud'),
    ('Snowflake', 'Cloud'), ('Databricks', 'Cloud'),
    ('Scikit-learn', 'ML/AI'), ('TensorFlow', 'ML/AI'),
    ('PyTorch', 'ML/AI'), ('XGBoost', 'ML/AI'), ('Spark MLlib', 'ML/AI'),
    ('Airflow', 'Data Engineering'), ('dbt', 'Data Engineering'),
    ('Kafka', 'Data Engineering'), ('Docker', 'Data Engineering'),
    ('Git', 'Data Engineering'),
    ('PostgreSQL', 'Databases'), ('MySQL', 'Databases'),
    ('MongoDB', 'Databases'), ('BigQuery', 'Databases'),
    ('Redshift', 'Databases');
