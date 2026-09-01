# Manufacturing Analytics

Manufacturing Production and Machine Performance Analysis using Python and Pandas.

## Overview
This project analyzes manufacturing data to study production trends, downtime, defects, and machine performance. It supports operational decision-making and helps identify machine reliability and efficiency opportunities.

## Project Goals
- Measure production volume by machine and shift
- Identify defect-prone machines and processes
- Understand production performance
- Identify bottlenecks and defects
- Visualize machine-level insights
- Analyze output efficiency and downtime drivers
- Visualize key manufacturing KPIs over time

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Project Structure
```text
manufacturing-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── manufacturing_data.csv
│   └── .gitkeep
├── src/
│   ├── analysis.py
│   └── visualize.py
└── visualizations/
    ├── production_by_machine.png
    ├── defects_by_machine.png
    └── output_trend.png
```

## Getting Started
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analysis pipeline:
   ```bash
   python src/analysis.py
   ```
4. Open the generated plots in the `visualizations/` folder.

## Sample Insights
- Highest-producing machines by total output
- Machines with the highest defect rates
- Production changes across shift and day segments

## Author
Punith Gowda
