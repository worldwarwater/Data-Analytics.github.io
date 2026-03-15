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

### 1. Data Wrangling
- Combined Q1 2019 and Q1 2020 datasets using `bind_rows()`
- Standardized column names across datasets (e.g., `trip_id` → `ride_id`, `usertype` → `member_casual`)
- Converted data types (`ride_id` and `rideable_type` to character, timestamps to datetime)
- Dropped unnecessary columns (`start_lat`, `start_lng`, `birthyear`, `gender`, `tripduration`)

### 2. Data Cleaning
- Reclassified user labels: "Subscriber" → "member", "Customer" → "casual"
- Added derived date fields: month, day, year, day_of_week
- Calculated `ride_length` from start/end timestamps
- Removed invalid records (negative ride lengths, HQ QR test station entries)

### 3. Descriptive Analysis
- Computed summary statistics (mean, median, max, min) for ride length
- Compared ride duration by user type and day of week
- Ordered weekdays chronologically for meaningful trend comparison

### 4. Visualizations

**Chart 1: Number of Rides by Day of Week (Casual vs. Member)**
A grouped bar chart comparing total ride count by weekday for each user type. Shows that members ride consistently throughout the week while casual riders peak on weekends.

![Number of Rides by Weekday](images/rides_by_weekday.png)

```r
all_trips_v2 %>%
  mutate(weekday = wday(started_at, label = TRUE)) %>%
  group_by(member_casual, weekday) %>%
  summarise(number_of_rides = n(), .groups = "drop") %>%
  ggplot(aes(x = weekday, y = number_of_rides, fill = member_casual)) +
  geom_col(position = "dodge")
```

**Chart 2: Average Ride Duration by Day of Week (Casual vs. Member)**
A grouped bar chart comparing average ride length (seconds) by weekday. Demonstrates that casual riders consistently take longer trips than members across all days.

![Average Ride Duration by Weekday](images/avg_duration_by_weekday.png)

```r
all_trips_v2 %>%
  mutate(weekday = wday(started_at, label = TRUE)) %>%
  group_by(member_casual, weekday) %>%
  summarise(average_duration = mean(ride_length), .groups = "drop") %>%
  ggplot(aes(x = weekday, y = average_duration, fill = member_casual)) +
  geom_col(position = "dodge")
```

> **Note:** To generate the chart images, knit the R Markdown file or run the code chunks in RStudio. The charts will render inline.

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
