# Predictive Analytics Mini-Study

**Module:** `week2/src/modules/predictive_analytics/`
**Developer:** Ali Zaib (AI/ML Intern)
**Part of:** SafeX Solutions — Business Automation Research, Week 2

## What this is

A small predictive-analytics prototype with two independent forecasting
workflows, built on sample data since no proprietary SafeX production
data was available for this internship task:

1. **Demand forecasting** — predicts next-month business demand from a
   sample of 42 months of historical data (marketing spend, price,
   promotions, seasonality).
2. **Churn prediction** — predicts whether a customer is likely to churn,
   from a sample of 300 customers (tenure, spend, support tickets,
   satisfaction, discount status).

Both are exposed through one `PredictiveAnalyticsEngine` class
(`engine.py`) and a Streamlit tab (`ui.py`) in the shared automation
suite.

## How it works

### Demand forecasting
- **Features engineered:** lag-1 and lag-2 demand, 3-month rolling mean,
  and sine/cosine encodings of month-of-year (to represent seasonality
  without a hard 1–12 category boundary).
- **Models:** Linear Regression or Random Forest Regressor (user-selectable
  in the UI).
- **Evaluation:** the **last 6 months** are held out as a test set — a
  time-based split, not a random shuffle, since shuffling a time series
  would leak future values into training. Reported as MAE, RMSE, and R².
- **Forecasting:** `forecast_demand(periods)` iteratively predicts one
  month at a time, feeding each prediction back in as the next month's
  lag feature, so it can forecast arbitrarily far ahead from the trained
  model.
- **Finding worth noting:** Random Forest consistently underperforms
  Linear Regression here because tree-based models can't extrapolate
  past the range of values seen in training — they flatten out instead
  of continuing an upward trend. Linear Regression captures the trend
  term directly and extrapolates it correctly. See the notebook for the
  side-by-side comparison.

### Churn prediction
- **Features:** tenure (months), monthly spend, recent support tickets,
  satisfaction score (1–10), and whether a discount is active.
- **Models:** Logistic Regression or Random Forest Classifier
  (user-selectable).
- **Evaluation:** a 75/25 stratified train/test split (stratified so the
  ~20% churn rate is preserved in both splits). Reported as accuracy,
  precision, recall, F1, and a confusion matrix.
- **Feature importance:** absolute logistic-regression coefficients, or
  Random Forest's built-in feature importances, whichever model was
  last trained.
- **Single-customer scoring:** `predict_churn(features)` returns a churn
  probability and a plain-language label for one customer's profile —
  this powers the "Try it" form in the UI.

## Files

| File | Purpose |
|---|---|
| `engine.py` | All model logic: data loading, feature engineering, training, evaluation, forecasting, and single-record prediction. No Streamlit code. |
| `ui.py` | Streamlit tab: model selection, training buttons, metrics, charts, forecast table, CSV download, and a form to score one customer's churn risk. |
| `data/demand_history.csv` | Sample demand dataset (42 months, synthetically generated with trend + seasonality + noise). |
| `data/customer_churn.csv` | Sample customer dataset (300 rows, ~20% churn rate, synthetically generated). |
| `predictive_analytics_mini_study.ipynb` | Notebook walkthrough of both tasks with sample input/output, plots, and written observations — the case-study companion to this doc. |
| `../../../tests/test_predictive_analytics.py` | 15 unit tests covering both models' training, evaluation, forecasting, and error handling. |

## How to run

**Unit tests:**
```bash
cd week2
python -m pytest tests/test_predictive_analytics.py -v
```

**Notebook:**
Open `predictive_analytics_mini_study.ipynb` in Jupyter/VS Code and run
all cells (repo root must be on `sys.path`; the first code cell handles
this automatically).

**Full Streamlit suite** (this module is one tab inside it):
```bash
cd week2
pip install -r requirements.txt
streamlit run src/app.py
```
Then select **"Predictive Analytics Mini-Study"** from the sidebar,
pick a model in either tab, and click **Train & Forecast** /
**Train Churn Model**.

## Known limitations

- Both datasets are **synthetic sample data**, generated to have
  realistic trend/seasonality/behavioral structure — the specific
  numbers illustrate the *method*, not real SafeX KPIs. Swapping in
  real historical sales/CRM data requires no code changes beyond
  matching the expected column names (see `engine.py`'s `*_FEATURE_COLS`
  / dataset loaders).
- The demand forecast assumes marketing spend and price stay near their
  recent 6-month average going forward; it doesn't model planned future
  changes to either.
- Churn model performance is bounded by the sample size (300 rows,
  ~60 churners) — recall on the minority class is modest, which is
  expected and called out in the notebook's evaluation section.
