-- ============================================
-- Job Market Analysis - SQL Queries
-- Business questions answered through data
-- ============================================


-- ============================================
-- Q1: Top 10 Highest-Paying Skills
-- Which individual skills correlate with the highest salaries?
-- ============================================
SELECT
    js.skill,
    sc.category,
    COUNT(*) AS job_count,
    ROUND(AVG(jp.salary_usd)) AS avg_salary,
    ROUND(MIN(jp.salary_usd)) AS min_salary,
    ROUND(MAX(jp.salary_usd)) AS max_salary,
    ROUND(AVG(jp.salary_usd) - (SELECT AVG(salary_usd) FROM job_postings)) AS salary_premium
FROM job_skills js
JOIN job_postings jp ON js.job_id = jp.job_id
JOIN skill_categories sc ON js.skill = sc.skill
GROUP BY js.skill, sc.category
HAVING COUNT(*) >= 30
ORDER BY avg_salary DESC
LIMIT 10;


-- ============================================
-- Q2: Remote vs Hybrid vs On-Site Pay Gap
-- Is there a measurable salary difference by work type?
-- ============================================
SELECT
    work_type,
    COUNT(*) AS posting_count,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(AVG(salary_usd) * 100.0 / (SELECT AVG(salary_usd) FROM job_postings), 1) AS pct_of_overall,
    ROUND(AVG(applicants)) AS avg_applicants
FROM job_postings
GROUP BY work_type
ORDER BY avg_salary DESC;


-- ============================================
-- Q3: Remote vs On-Site by Job Title (Controlled Comparison)
-- Controlling for title to isolate the remote effect
-- ============================================
SELECT
    jp.job_title,
    ROUND(AVG(CASE WHEN jp.work_type = 'Remote' THEN jp.salary_usd END)) AS avg_remote_salary,
    ROUND(AVG(CASE WHEN jp.work_type = 'On-Site' THEN jp.salary_usd END)) AS avg_onsite_salary,
    ROUND(AVG(CASE WHEN jp.work_type = 'Remote' THEN jp.salary_usd END) -
          AVG(CASE WHEN jp.work_type = 'On-Site' THEN jp.salary_usd END)) AS remote_premium,
    COUNT(CASE WHEN jp.work_type = 'Remote' THEN 1 END) AS remote_count,
    COUNT(CASE WHEN jp.work_type = 'On-Site' THEN 1 END) AS onsite_count
FROM job_postings jp
GROUP BY jp.job_title
HAVING remote_count >= 10 AND onsite_count >= 10
ORDER BY remote_premium DESC;


-- ============================================
-- Q4: Average Salary by City (Top 15)
-- Which metro areas pay the most for data roles?
-- ============================================
SELECT
    location,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(AVG(salary_usd) - (SELECT AVG(salary_usd) FROM job_postings)) AS vs_national_avg,
    ROUND(AVG(applicants)) AS avg_applicants,
    ROUND(1.0 * SUM(CASE WHEN work_type = 'Remote' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_remote
FROM job_postings
GROUP BY location
HAVING COUNT(*) >= 20
ORDER BY avg_salary DESC;


-- ============================================
-- Q5: Most In-Demand Skills by Volume
-- What skills appear in the most job postings?
-- ============================================
SELECT
    js.skill,
    sc.category,
    COUNT(*) AS demand_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(DISTINCT job_id) FROM job_postings), 1) AS pct_of_postings,
    ROUND(AVG(jp.salary_usd)) AS avg_salary_with_skill
FROM job_skills js
JOIN job_postings jp ON js.job_id = jp.job_id
JOIN skill_categories sc ON js.skill = sc.skill
GROUP BY js.skill, sc.category
ORDER BY demand_count DESC
LIMIT 15;


-- ============================================
-- Q6: Salary by Experience Level
-- How much does experience actually affect pay?
-- ============================================
SELECT
    experience_level,
    COUNT(*) AS posting_count,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(MIN(salary_usd)) AS min_salary,
    ROUND(MAX(salary_usd)) AS max_salary,
    ROUND(AVG(applicants)) AS avg_applicants
FROM job_postings
GROUP BY experience_level
ORDER BY avg_salary;


-- ============================================
-- Q7: Best Skill Combinations (2-skill pairs)
-- Which pairs of skills command the highest salaries?
-- ============================================
SELECT
    a.skill AS skill_1,
    b.skill AS skill_2,
    COUNT(*) AS pair_count,
    ROUND(AVG(jp.salary_usd)) AS avg_salary
FROM job_skills a
JOIN job_skills b ON a.job_id = b.job_id AND a.skill < b.skill
JOIN job_postings jp ON a.job_id = jp.job_id
GROUP BY a.skill, b.skill
HAVING pair_count >= 20
ORDER BY avg_salary DESC
LIMIT 15;


-- ============================================
-- Q8: Industry Salary Comparison
-- Which industries pay the most for data talent?
-- ============================================
SELECT
    industry,
    COUNT(*) AS posting_count,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(AVG(CASE WHEN experience_level = 'Entry (0-2 yrs)' THEN salary_usd END)) AS avg_entry_salary,
    ROUND(AVG(CASE WHEN experience_level = 'Lead (10+ yrs)' THEN salary_usd END)) AS avg_lead_salary,
    ROUND(1.0 * SUM(CASE WHEN work_type = 'Remote' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_remote
FROM job_postings
GROUP BY industry
ORDER BY avg_salary DESC;


-- ============================================
-- Q9: Hiring Trends by Month
-- When do companies post the most data roles?
-- ============================================
SELECT
    strftime('%m', post_date) AS month_num,
    CASE strftime('%m', post_date)
        WHEN '01' THEN 'January' WHEN '02' THEN 'February'
        WHEN '03' THEN 'March' WHEN '04' THEN 'April'
        WHEN '05' THEN 'May' WHEN '06' THEN 'June'
        WHEN '07' THEN 'July' WHEN '08' THEN 'August'
        WHEN '09' THEN 'September' WHEN '10' THEN 'October'
        WHEN '11' THEN 'November' WHEN '12' THEN 'December'
    END AS month_name,
    COUNT(*) AS postings,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(AVG(applicants)) AS avg_applicants
FROM job_postings
GROUP BY month_num
ORDER BY month_num;


-- ============================================
-- Q10: Competition Analysis - Applicants per Posting
-- Which roles/locations have the least competition?
-- ============================================
SELECT
    job_title,
    work_type,
    COUNT(*) AS postings,
    ROUND(AVG(applicants)) AS avg_applicants,
    ROUND(AVG(salary_usd)) AS avg_salary,
    ROUND(AVG(salary_usd) * 1.0 / AVG(applicants)) AS salary_per_applicant_ratio
FROM job_postings
GROUP BY job_title, work_type
HAVING postings >= 15
ORDER BY salary_per_applicant_ratio DESC
LIMIT 15;
