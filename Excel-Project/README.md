# 📊 Excel Project: Indian Cities' Electricity Consumption (2017-2019)

## 📂 Dataset Overview
This dataset contains electricity consumption data for Indian cities from 2017 to 2019.

## 🔍 Problem Statement
Stakeholders are interested in:  
- Electricity consumption for **commercial purposes** in **Indore City**.  
- The **total electricity consumption** across Indian cities.  
- Identifying **maximum and minimum** consumption.  
- Analyzing **overall trends** in electricity usage.  

---

## 🛠 Data Cleaning Process
1. **Conditional Formatting** – Highlighted cells containing “NA” values.  
2. **COUNTIF Function** – Found **7** occurrences of "NA".  
3. **Find and Replace** – Replaced "NA" values with **0**.  

---

## 📈 Analysis & Insights

### 1️⃣ Finding Electricity Consumption for Indore City
Used **VLOOKUP** to determine electricity consumption:  
```excel
=VLOOKUP(A13, A2:H48, 4, FALSE)
```
- `A13` – Lookup value (Indore City).  
- `A2:H48` – Data range.  
- `4` – Returns the value from the **4th column**.  
- `FALSE` – Ensures an **exact match**.  

### 2️⃣ Total Electricity Consumption Across Indian Cities
Used the **SUM function** to calculate total consumption:  
```excel
=SUM(H2:H48)
```
- This adds up all electricity consumption values in column `H`.  

### 3️⃣ Identifying Cities with Maximum & Minimum Consumption
Used **Pivot Tables & Conditional Formatting** to highlight:  
- **Top 10 cities with the highest electricity consumption** (Industry purpose).  
- **Cities with the highest consumption in Public Water Works & Street Lights**.  

---

## 📊 Key Findings & Trends
- The **top 10 cities with the highest electricity consumption** were identified, showing where reduction efforts could be focused.  
- **Total electricity consumption** has **decreased** over the years.  
- **Public Water Works & Street Lights** – Certain cities consume significantly more energy, requiring collaboration with local departments for energy-saving initiatives.  

---

## 📌 Conclusion & Next Steps
While this analysis provides valuable insights, further investigation is required to:  
- Identify the underlying factors driving electricity consumption differences among cities.  
- Develop energy-efficient strategies to **reduce consumption** in high-usage areas.  
- Implement policies for **upgrading infrastructure** and optimizing energy distribution.  

---

## 📥 Download the Excel File
🔗 [**Click here to download**](Excel%20Analysis.xlsm)
