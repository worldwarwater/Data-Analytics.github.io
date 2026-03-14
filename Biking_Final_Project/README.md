# Divvy Bike-Share Analysis: Casual vs. Member Riders

## Overview
A comparative analysis of Chicago's Divvy bike-share program examining usage differences between casual riders and annual members across Q1 2019 and Q1 2020. This project was completed as part of the Google Data Analytics Professional Certificate capstone.

## Business Question
**How do annual members and casual riders use Divvy bikes differently?**

Understanding these differences helps the marketing team design strategies to convert casual riders into annual members.

## Key Findings
- **Members ride more frequently** but casual riders take **longer trips on average**
- Casual rider usage **peaks on weekends** while members ride consistently on weekdays, suggesting commuter vs. recreational patterns
- Ride duration for casual users is significantly higher, indicating leisure-oriented usage
- Q1 2020 data shows early impacts of COVID-19 on overall ridership

## Analysis Steps
1. **Data Wrangling** — Combined Q1 2019 and Q1 2020 datasets, standardized column names, and converted data types
2. **Data Cleaning** — Removed invalid records (negative ride lengths, HQ test stations), standardized user type labels
3. **Descriptive Analysis** — Calculated mean, median, max, and min ride lengths by user type and day of week
4. **Visualization** — Created bar charts comparing ride frequency and average duration by user type across weekdays

## Tools & Technologies
- R (tidyverse, lubridate, ggplot2, conflicted)
- R Markdown for reproducible reporting

## Data Source
[Divvy Trip Data](https://divvy-tripdata.s3.amazonaws.com/index.html) — Download Q1 2019 and Q1 2020 CSVs and place them in the project directory.

## How to Run
```r
# Install required packages
install.packages(c("tidyverse", "lubridate", "conflicted"))

# Open and knit the R Markdown file
rmarkdown::render("Biking Final Project.Rmd")
```

## Author
**Stephen Drani** — [LinkedIn](https://linkedin.com/in/stephen-drani-a58140232) | [GitHub](https://github.com/worldwarwater)
