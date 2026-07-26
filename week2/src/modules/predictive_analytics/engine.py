# Predictive Analytics Mini-Study - Engine
# Developer: Ali Zaib (Group Member)
# For SafeX Solutions Business Automation Research
#
# Two prototype forecasting workflows for a small business automation
# suite:
#   1. Demand forecasting  - regression model trained on monthly demand
#      history (trend + seasonality + marketing/price effects) that
#      forecasts demand for the next N months.
#   2. Churn prediction    - classification model trained on a sample
#      customer dataset (tenure, spend, support tickets, satisfaction)
#      that scores the probability a given customer will churn.
#
# Data is read from CSV files bundled under this module's data/
# directory so the prototype has no external service dependency and no
# proprietary SafeX data is required. Each engine instance can be
# pointed at its own data directory, which keeps it easy to unit test.

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    r2_score,
)
from sklearn.model_selection import train_test_split

DEFAULT_DATA_DIR = Path(__file__).parent / "data"

DEMAND_FILE = "demand_history.csv"
CHURN_FILE = "customer_churn.csv"

DEMAND_MODELS = {
    "linear": lambda: LinearRegression(),
    "random_forest": lambda: RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42),
}
CHURN_MODELS = {
    "logistic": lambda: LogisticRegression(max_iter=1000),
    "random_forest": lambda: RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42),
}

DEMAND_TEST_MONTHS = 6  # holdout window for time-based evaluation
CHURN_TEST_SIZE = 0.25

CHURN_FEATURE_COLS = [
    "tenure_months",
    "monthly_spend",
    "support_tickets",
    "satisfaction_score",
    "active_discount",
]


class PredictiveAnalyticsError(ValueError):
    """Raised for invalid predictive-analytics inputs (bad model type, unfitted model, etc.)."""


class PredictiveAnalyticsEngine:
    """
    Demand forecasting + churn prediction mini-study.

    Loads sample CSV datasets bundled with this module, trains a
    regression model to forecast future demand and a classification
    model to score customer churn risk, and exposes evaluation metrics
    for both so results can be reported in the UI / case study.
    """

    def __init__(self, data_dir: Path | str = DEFAULT_DATA_DIR):
        self.data_dir = Path(data_dir)

        # Demand forecasting state
        self.demand_model = None
        self.demand_model_type: str | None = None
        self.demand_feature_cols: list[str] = []
        self._demand_features: pd.DataFrame | None = None

        # Churn prediction state
        self.churn_model = None
        self.churn_model_type: str | None = None

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    def _path(self, filename: str) -> Path:
        return self.data_dir / filename

    # ------------------------------------------------------------------
    # Demand forecasting
    # ------------------------------------------------------------------
    def load_demand_data(self) -> pd.DataFrame:
        path = self._path(DEMAND_FILE)
        if not path.exists():
            raise PredictiveAnalyticsError(f"Demand dataset not found at {path}")
        return pd.read_csv(path)

    @staticmethod
    def _build_demand_features(df: pd.DataFrame) -> pd.DataFrame:
        """Add lag/rolling/seasonal features used by the demand model."""
        out = df.copy().sort_values("month_index").reset_index(drop=True)
        out["lag_1"] = out["demand_units"].shift(1)
        out["lag_2"] = out["demand_units"].shift(2)
        out["rolling_mean_3"] = out["demand_units"].shift(1).rolling(3).mean()
        out["month_sin"] = np.sin(2 * np.pi * out["month_of_year"] / 12)
        out["month_cos"] = np.cos(2 * np.pi * out["month_of_year"] / 12)
        return out

    def train_demand_model(self, model_type: str = "linear") -> dict:
        """Train a demand-forecasting regressor and evaluate it on the
        last DEMAND_TEST_MONTHS months (a time-based holdout, not a
        random split, since this is a time series)."""
        if model_type not in DEMAND_MODELS:
            raise PredictiveAnalyticsError(f"model_type must be one of {list(DEMAND_MODELS)}")

        raw = self.load_demand_data()
        features = self._build_demand_features(raw).dropna().reset_index(drop=True)

        feature_cols = [
            "month_index", "marketing_spend", "price_index", "promo_flag",
            "lag_1", "lag_2", "rolling_mean_3", "month_sin", "month_cos",
        ]
        target_col = "demand_units"

        if len(features) <= DEMAND_TEST_MONTHS + 5:
            raise PredictiveAnalyticsError("Not enough rows to train/test the demand model.")

        train = features.iloc[: -DEMAND_TEST_MONTHS]
        test = features.iloc[-DEMAND_TEST_MONTHS:]

        model = DEMAND_MODELS[model_type]()
        model.fit(train[feature_cols], train[target_col])
        preds = model.predict(test[feature_cols])

        self.demand_model = model
        self.demand_model_type = model_type
        self.demand_feature_cols = feature_cols
        self._demand_features = features

        return {
            "model_type": model_type,
            "n_train": len(train),
            "n_test": len(test),
            "mae": round(float(mean_absolute_error(test[target_col], preds)), 2),
            "rmse": round(float(np.sqrt(mean_squared_error(test[target_col], preds))), 2),
            "r2": round(float(r2_score(test[target_col], preds)), 3),
            "test_months": test["month_index"].tolist(),
            "test_actual": test[target_col].tolist(),
            "test_predicted": [round(float(p), 1) for p in preds],
        }

    def forecast_demand(self, periods: int = 6) -> pd.DataFrame:
        """Iteratively forecast demand for the next `periods` months
        using the most recently trained model, feeding each month's
        prediction back in as next month's lag feature."""
        if self.demand_model is None or self._demand_features is None:
            raise PredictiveAnalyticsError("Train a demand model before forecasting.")
        if periods < 1:
            raise PredictiveAnalyticsError("periods must be at least 1.")

        history = self._demand_features.copy()
        last_row = history.iloc[-1]
        last_marketing = history["marketing_spend"].tail(6).mean()
        last_price = history["price_index"].tail(6).mean()

        forecasts = []
        lag_1 = last_row["demand_units"]
        lag_2 = history.iloc[-2]["demand_units"]
        rolling_window = history["demand_units"].tail(3).tolist()
        month_index = int(last_row["month_index"])
        month_of_year = int(last_row["month_of_year"])

        for _ in range(periods):
            month_index += 1
            month_of_year = (month_of_year % 12) + 1
            rolling_mean_3 = float(np.mean(rolling_window[-3:])) if rolling_window else lag_1

            row = pd.DataFrame([{
                "month_index": month_index,
                "marketing_spend": last_marketing,
                "price_index": last_price,
                "promo_flag": 0,
                "lag_1": lag_1,
                "lag_2": lag_2,
                "rolling_mean_3": rolling_mean_3,
                "month_sin": np.sin(2 * np.pi * month_of_year / 12),
                "month_cos": np.cos(2 * np.pi * month_of_year / 12),
            }])
            pred = float(self.demand_model.predict(row[self.demand_feature_cols])[0])

            forecasts.append({
                "month_index": month_index,
                "month_of_year": month_of_year,
                "forecast_demand": round(pred, 1),
            })

            lag_2 = lag_1
            lag_1 = pred
            rolling_window.append(pred)

        return pd.DataFrame(forecasts)

    # ------------------------------------------------------------------
    # Churn prediction
    # ------------------------------------------------------------------
    def load_churn_data(self) -> pd.DataFrame:
        path = self._path(CHURN_FILE)
        if not path.exists():
            raise PredictiveAnalyticsError(f"Churn dataset not found at {path}")
        return pd.read_csv(path)

    def train_churn_model(self, model_type: str = "logistic") -> dict:
        """Train a churn classifier on a stratified train/test split and
        return evaluation metrics plus feature importance/coefficients."""
        if model_type not in CHURN_MODELS:
            raise PredictiveAnalyticsError(f"model_type must be one of {list(CHURN_MODELS)}")

        df = self.load_churn_data()
        X = df[CHURN_FEATURE_COLS]
        y = df["churned"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=CHURN_TEST_SIZE, random_state=42, stratify=y
        )

        model = CHURN_MODELS[model_type]()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        self.churn_model = model
        self.churn_model_type = model_type

        cm = confusion_matrix(y_test, preds).tolist()

        if model_type == "random_forest":
            importance = dict(zip(CHURN_FEATURE_COLS, model.feature_importances_.round(3).tolist()))
        else:
            importance = dict(zip(CHURN_FEATURE_COLS, np.abs(model.coef_[0]).round(3).tolist()))

        return {
            "model_type": model_type,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "accuracy": round(float(accuracy_score(y_test, preds)), 3),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 3),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 3),
            "f1": round(float(f1_score(y_test, preds, zero_division=0)), 3),
            "confusion_matrix": cm,
            "feature_importance": importance,
        }

    def predict_churn(self, features: dict) -> dict:
        """Score a single customer's churn probability with the most
        recently trained churn model."""
        if self.churn_model is None:
            raise PredictiveAnalyticsError("Train a churn model before predicting.")
        missing = [c for c in CHURN_FEATURE_COLS if c not in features]
        if missing:
            raise PredictiveAnalyticsError(f"Missing required feature(s): {missing}")

        row = pd.DataFrame([{c: features[c] for c in CHURN_FEATURE_COLS}])
        probability = float(self.churn_model.predict_proba(row)[0][1])
        label = "Likely to churn" if probability >= 0.5 else "Likely to stay"
        return {"churn_probability": round(probability, 3), "label": label}
