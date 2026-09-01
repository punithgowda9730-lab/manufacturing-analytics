Manufacturing Production & Machine Performance Analysis

📌 Project Overview

This project analyzes manufacturing production data to identify machine-level performance, quality issues, downtime, and production trends.

The project combines **Python, Pandas, Matplotlib, and Power BI** to transform raw manufacturing data into useful operational insights.

🎯 Objectives

* Analyze overall production performance
* Identify machines with higher defect rates
* Analyze machine downtime
* Monitor production trends over time
* Measure overall manufacturing yield
* Build an interactive Power BI dashboard

📊 Dataset

The dataset contains the following fields:

| Column             | Description                 |
| ------------------ | --------------------------- |
| `date`             | Production date             |
| `machine`          | Machine identifier          |
| `shift`            | Production shift            |
| `produced_units`   | Number of units produced    |
| `defects`          | Number of defective units   |
| `downtime_minutes` | Machine downtime in minutes |
| `yield_rate`       | Production yield rate       |

🛠️ Technologies Used

Python
Pandas
Matplotlib
Power BI
Git & GitHub

📈 Key Performance Indicators

The Power BI dashboard tracks:

* **Total Production:** 64K units
* **Total Defects:** 5K
* **Defect Rate:** 8.53%
* **Total Downtime:** 2.5K minutes
* **Average Yield:** 90.44%

🔍 Key Findings

* **M-101** has the highest defect rate among the analyzed machines.
* **M-104** has the highest downtime.
* Overall average yield is **90.44%**.
* The dashboard allows production performance to be analyzed by **machine** and **shift**.

📊 Power BI Dashboard

### 📊 Dashboard Preview

![Manufacturing Production & Machine Performance Dashboard](dashboard.png)

The interactive dashboard contains:

* Production by Machine
* Defect Rate by Machine
* Downtime by Machine
* Production Trend Over Time
* Total Production KPI
* Total Defects KPI
* Defect Rate KPI
* Total Downtime KPI
* Average Yield KPI
* Machine and Shift filters

📁 Project Structure

```text
manufacturing-analytics/
│
├── data/
│   └── manufacturing_data.csv
│
├── notebooks/
│
├── src/
│
├── Manufacturing_Production_Analytics.pbix
│
├── README.md
└── .gitignore
```

🚀 Future Improvements

* Develop a machine failure prediction model
* Add predictive maintenance capabilities
* Analyze factors contributing to machine downtime
* Build machine health indicators
* Implement machine-learning based failure prediction
* Improve dashboard automation

👨‍💻 Project Focus

This project demonstrates practical skills in:

**Data Cleaning → Exploratory Data Analysis → Data Visualization → KPI Analysis → Business Insights → Power BI Dashboarding**
