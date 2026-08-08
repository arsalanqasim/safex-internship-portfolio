# Predictive Dashboard for a Small Business (LearnHub Academy)

This module implements a client-ready forecasting dashboard designed for **LearnHub Academy**, an online tutoring platform. It uses historical enrollment data to project student recruitment metrics and provides dynamically calculated business insights.

## Developer Metadata
- **Developer**: Ali Ammar Haider
- **Role**: Group Member (Group 54)
- **Sprint**: Week 4 Client-Ready Sprint

## Tech Stack
- **Python** (v3.9+)
- **scikit-learn** (for Linear Regression OLS modeling)
- **Pandas** & **NumPy** (for operational data manipulation)
- **Matplotlib** (for high-fidelity visualizations matching light/dark themes)
- **Streamlit** (for the shared dashboard interface)

## Dataset Specifications
The dashboard operates on a synthetic 24-month historical operational dataset (`data/learnhub_enrollment_data.csv`) that contains the following indicators:
1. `Month_Index`: Sequential identifier (`1` to `24`).
2. `Month_Label`: Chronological date strings in `YYYY-MM` format.
3. `Enrollments` (Target): Total active monthly student count.
4. `Revenue` (Context): Monthly gross revenue included as a supporting business indicator; it is not used as a forecasting target.
5. `Website_Visitors` (Context): Monthly web traffic unique visitors.
6. `Marketing_Spend` (Context): Monthly promotional ad expenditure.
7. `Social_Engagement` (Context): Monthly social media interactions (likes, clicks, views).
8. `Lead_Conversion_Rate` (Context): Monthly lead-to-signup conversion rate percentage.

*Disclaimer: All data inside this file is synthetically generated for demonstration purposes during the SafeX internship.*

## Model & Forecasting Methodology
- **Target Variable**: `Enrollments`
- **Features**: `Month_Index`
- **Algorithm**: Ordinary Least Squares (OLS) Linear Regression model from `scikit-learn`.
- **Seasonality Policy**: The model focuses entirely on forecasting linear growth trends and month-to-month variation. It does not attempt to isolate or model seasonal patterns.

## Dynamic Business Recommendations
The engine dynamically calculates the following conditions to display exactly three targeted operational recommendations:
1. **Tutor Recruiting**: Triggers staffing instructions based on whether the regression slope coefficient $\beta_1$ is positive (growth) or negative/flat (retention audit).
2. **Funnel UX Optimization**: Triggers audit alerts if the mean conversion rate of the most recent 3 months falls below the 24-month historical baseline.
3. **Administrative Load Planning**: Triggers resource capacity warnings if the next-month forecast exceeds the historical 24-month maximum enrollment peak.

## Verification & Execution

### Run the Shared Application
Launch Streamlit from the root `week4/` directory:
```bash
streamlit run src/app.py
```

### Run Automated Tests
Execute the pytest suite targeting the module tests:
```bash
pytest src/modules/predictive_dashboard_tutor/
```
