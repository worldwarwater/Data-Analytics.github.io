# Stephen Drani — Data Analytics Portfolio

**Live site with interactive charts: https://worldwarwater.github.io/Data-Analytics.github.io/**

Data analytics, visualization, and automation projects using Python, SQL, R, Excel, and BI tools.

---

## Projects

### Marketing Campaign Segmentation & ROI Analysis | Python, SQL, Scikit-learn, Looker Studio

Analyzed 2,240 customers (2,205 after cleaning) to identify high-value segments using RFM analysis and K-Means clustering (K=4), then measured campaign ROI across web, catalog, and store channels. Applied Chi-Square, ANOVA, T-Test, and Mann-Whitney U tests to validate segment differences. Produced 30+ visualizations and data-driven budget reallocation recommendations.

**Key Finding:** Loyal customers are 10% of the base but 21% of spend, and Champions respond to campaigns at 48% versus 11% for Hibernating customers. Store purchases showed the highest ROI under the assumed contact costs ($5 web, $15 catalog, $3 store).

[View Code](marketing-campaign-analysis/) | [View Dashboard](https://lookerstudio.google.com/s/sN0LOkumv0o)

---

### Job Market Analysis Pipeline | Python, SQL, SQLite, Looker Studio

Built an end-to-end data pipeline analyzing 2,500 synthetic data-role job postings (generated with `generate_dataset.py`) to uncover salary trends, in-demand skills, and the remote work pay gap. Designed a normalized SQLite database, wrote 10 SQL analysis queries, and validated findings with statistical tests (T-tests, ANOVA, Chi-square, Cohen's d). Generated 8 publication-quality visualizations.

**Key Finding:** ML/AI skills (TensorFlow, Spark MLlib) command $20-30K salary premiums, while remote roles pay ~$4,400 more on average but attract 59% more applicants.

[View Code](job-market-analysis/) | [View Dashboard](https://lookerstudio.google.com/s/g3VbO0T8B4c)

---

### Customer Churn Analysis & Prediction | Python, Scikit-learn, Looker Studio

Analyzed 7,043 telecom customers to identify churn drivers and built a logistic regression model (ROC-AUC ~0.74) to predict at-risk customers. Engineered features from contract type, tenure, payment method, and service bundles. Created an interactive Looker Studio dashboard for stakeholder exploration.

**Key Finding:** Month-to-month contracts churn at 42% versus 17% for one-year contracts. Moving 10% of them to annual contracts would retain about $6.5K/month in revenue.

[View Code](customer-churn-analysis/) | [View Dashboard](https://lookerstudio.google.com/s/ra8vaWVRUzQ)

---

### Electricity Consumption Trend Analysis | Excel

Analyzed electricity consumption across Indian cities (2016–2019) by purpose using Pivot Tables, VLOOKUP, conditional formatting, and trend analysis. Identified the top 10 highest-consuming cities and the sectors driving usage.

[View Project Files](Excel-Project/)

---

### Fiction Book Web Scraper | Python (BeautifulSoup, Requests)

Built a scraper that walks the paginated fiction category of a practice bookstore site and extracts title, price, availability, and star rating into an analysis-ready CSV, with polite rate limiting.

[View Code](book_scraper/) | [View Data](book_scraper/fiction_books.csv)

---

### Divvy Bike-Share Analysis | R (tidyverse, ggplot2)

Comparative analysis of Divvy bike-share usage between Q1 2019 and Q1 2020, examining differences in ride behavior between casual riders and annual members. Includes data wrangling, descriptive statistics, and visualizations.

[View R Markdown](Biking_Final_Project/Biking%20Final%20Project.Rmd) | [View README](Biking_Final_Project/README.md)

---

## Tools & Technologies

- **Languages:** Python, SQL, R
- **Analysis:** Pandas, NumPy, SciPy, Scikit-learn
- **Visualization:** Matplotlib, Seaborn, Tableau, Looker Studio, Excel
- **Databases:** SQLite, Microsoft SQL Server
- **Other:** Git/GitHub, Jupyter Notebooks, BeautifulSoup

## About Me

Data Analytics professional based in Edmonton, AB with expertise in SQL, Python, and business intelligence tools. Currently completing a Bachelor of Finance at NAIT. Google certified in Data Analytics and Business Intelligence.

[LinkedIn](https://linkedin.com/in/stephen-drani-a58140232) | [GitHub](https://github.com/worldwarwater)
