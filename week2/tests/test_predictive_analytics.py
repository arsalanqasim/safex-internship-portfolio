# ==============================================================================
# Predictive Analytics Mini-Study - Unit Tests
# ==============================================================================
import pandas as pd
import pytest

from src.modules.predictive_analytics.engine import (
    CHURN_FEATURE_COLS,
    PredictiveAnalyticsEngine,
    PredictiveAnalyticsError,
)


@pytest.fixture
def engine():
    # Uses the bundled sample CSVs (data/demand_history.csv, data/customer_churn.csv)
    # since this module's datasets are static reference data, not user-generated state.
    return PredictiveAnalyticsEngine()


# ------------------------------------------------------------------
# Demand forecasting
# ------------------------------------------------------------------
def test_load_demand_data_has_expected_columns(engine):
    df = engine.load_demand_data()
    assert not df.empty
    for col in ["month_index", "month_of_year", "marketing_spend", "price_index", "promo_flag", "demand_units"]:
        assert col in df.columns


def test_train_demand_model_rejects_unknown_model_type(engine):
    with pytest.raises(PredictiveAnalyticsError):
        engine.train_demand_model("prophet")


@pytest.mark.parametrize("model_type", ["linear", "random_forest"])
def test_train_demand_model_returns_metrics(engine, model_type):
    metrics = engine.train_demand_model(model_type)
    assert metrics["model_type"] == model_type
    assert metrics["n_test"] == 6
    assert metrics["mae"] >= 0
    assert metrics["rmse"] >= 0
    assert len(metrics["test_actual"]) == len(metrics["test_predicted"]) == 6


def test_forecast_demand_requires_trained_model(engine):
    with pytest.raises(PredictiveAnalyticsError):
        engine.forecast_demand(3)


def test_forecast_demand_returns_requested_periods(engine):
    engine.train_demand_model("linear")
    forecast = engine.forecast_demand(4)
    assert isinstance(forecast, pd.DataFrame)
    assert len(forecast) == 4
    assert list(forecast.columns) == ["month_index", "month_of_year", "forecast_demand"]
    # Forecast months should continue on from the last historical month.
    history = engine.load_demand_data()
    assert forecast.iloc[0]["month_index"] == history["month_index"].max() + 1


def test_forecast_demand_rejects_non_positive_periods(engine):
    engine.train_demand_model("linear")
    with pytest.raises(PredictiveAnalyticsError):
        engine.forecast_demand(0)


# ------------------------------------------------------------------
# Churn prediction
# ------------------------------------------------------------------
def test_load_churn_data_has_expected_columns(engine):
    df = engine.load_churn_data()
    assert not df.empty
    for col in CHURN_FEATURE_COLS + ["customer_id", "churned"]:
        assert col in df.columns


def test_train_churn_model_rejects_unknown_model_type(engine):
    with pytest.raises(PredictiveAnalyticsError):
        engine.train_churn_model("svm")


@pytest.mark.parametrize("model_type", ["logistic", "random_forest"])
def test_train_churn_model_returns_metrics(engine, model_type):
    metrics = engine.train_churn_model(model_type)
    assert metrics["model_type"] == model_type
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["f1"] <= 1.0
    assert len(metrics["confusion_matrix"]) == 2
    assert set(metrics["feature_importance"].keys()) == set(CHURN_FEATURE_COLS)


def test_predict_churn_requires_trained_model(engine):
    with pytest.raises(PredictiveAnalyticsError):
        engine.predict_churn({c: 0 for c in CHURN_FEATURE_COLS})


def test_predict_churn_rejects_missing_features(engine):
    engine.train_churn_model("logistic")
    with pytest.raises(PredictiveAnalyticsError):
        engine.predict_churn({"tenure_months": 12})


def test_predict_churn_high_risk_profile_scores_high(engine):
    engine.train_churn_model("logistic")
    result = engine.predict_churn({
        "tenure_months": 1,
        "monthly_spend": 40,
        "support_tickets": 8,
        "satisfaction_score": 1,
        "active_discount": 0,
    })
    assert result["label"] == "Likely to churn"
    assert result["churn_probability"] > 0.5


def test_predict_churn_low_risk_profile_scores_low(engine):
    engine.train_churn_model("logistic")
    result = engine.predict_churn({
        "tenure_months": 55,
        "monthly_spend": 90,
        "support_tickets": 0,
        "satisfaction_score": 10,
        "active_discount": 1,
    })
    assert result["label"] == "Likely to stay"
    assert result["churn_probability"] < 0.5
