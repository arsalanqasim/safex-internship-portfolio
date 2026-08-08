"""Unit tests for the Predictive Dashboard Tutor module.

Verifies dataset loading, linear regression forecasts, metric calculations,
and dynamically evaluated business recommendations.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np
import pytest

from src.modules.predictive_dashboard_tutor.engine import PredictiveDashboardTutorEngine


@pytest.fixture
def engine() -> PredictiveDashboardTutorEngine:
    """Fixture to initialize the engine with the standard synthetic dataset."""
    return PredictiveDashboardTutorEngine()


def test_dataset_loading(engine: PredictiveDashboardTutorEngine) -> None:
    """Verify that the synthetic dataset is loaded and structured correctly."""
    df = engine.load_data()
    
    # Check length
    assert len(df) == 24
    
    # Check expected columns
    expected_cols = {
        "Month_Index",
        "Month_Label",
        "Enrollments",
        "Revenue",
        "Website_Visitors",
        "Marketing_Spend",
        "Social_Engagement",
        "Lead_Conversion_Rate"
    }
    assert set(df.columns) == expected_cols
    
    # Check data consistency
    assert df["Month_Index"].tolist() == list(range(1, 25))
    assert not df.isnull().any().any()
    assert not df.duplicated().any()
    assert not df["Month_Label"].duplicated().any()
    assert (df["Enrollments"] > 0).all()
    assert (df["Lead_Conversion_Rate"] > 0).all()
    assert (df["Revenue"] > 0).all()


def test_run_forecast(engine: PredictiveDashboardTutorEngine) -> None:
    """Verify the forecasting results dictionary structure and keys."""
    results = engine.run_forecast()
    
    # Verify expected output keys
    expected_keys = {
        "dataset",
        "slope",
        "intercept",
        "forecast_value",
        "forecast_raw",
        "r2_score",
        "mae",
        "latest_actual",
        "average_enrollment",
        "growth_absolute",
        "growth_percentage",
        "recommendations",
    }
    assert expected_keys.issubset(results.keys())
    
    # Check that predictions column was added to dataset
    assert "Predicted_Enrollments" in results["dataset"].columns
    
    # Basic value checks
    assert isinstance(results["forecast_value"], int)
    assert 0.0 <= results["r2_score"] <= 1.0
    assert results["mae"] > 0
    assert results["latest_actual"] == results["dataset"]["Enrollments"].iloc[-1]
    assert results["average_enrollment"] == results["dataset"]["Enrollments"].mean()


def test_recommendation_count(engine: PredictiveDashboardTutorEngine) -> None:
    """Ensure exactly 3 data-driven recommendations are returned."""
    results = engine.run_forecast()
    recs = results["recommendations"]
    assert len(recs) == 3
    assert all(isinstance(r, str) for r in recs)


def test_dynamic_recommendation_conditions() -> None:
    """Verify that business recommendations adapt dynamically to dataset conditions."""
    # Create a temporary dummy CSV path to isolate tests
    temp_csv_path = Path(__file__).resolve().parent / "temp_test_data.csv"
    
    try:
        # Scenario A: Rising trend, conversion rate dropping recently, forecast exceeding max
        # Max enrollments is 100, forecast will be > 100 due to sharp rise
        data_a = {
            "Month_Index": list(range(1, 25)),
            "Month_Label": [f"2024-{m:02d}" for m in range(1, 25)],
            "Enrollments": [50 + 2 * x for x in range(1, 25)], # rising: slope > 0, max is 98
            "Revenue": [120.0] * 24,
            "Website_Visitors": [1000] * 24,
            "Marketing_Spend": [100.0] * 24,
            "Social_Engagement": [50] * 24,
            "Lead_Conversion_Rate": [4.0] * 21 + [2.0] * 3 # recent 3-month (2.0%) is below 24-month avg (~3.75%)
        }
        pd.DataFrame(data_a).to_csv(temp_csv_path, index=False)
        
        engine_a = PredictiveDashboardTutorEngine(data_path=temp_csv_path)
        results_a = engine_a.run_forecast()
        recs_a = results_a["recommendations"]
        
        # Test Case 1: Rising slope recommendation is triggered
        assert "Prepare to recruit additional tutors" in recs_a[0]
        # Test Case 2: Conversion funnel warning is triggered
        assert "Optimize registration funnel" in recs_a[1]
        assert "2.00%" in recs_a[1]
        # Test Case 3: Administrative capacity audit warning is triggered (forecast Month 25 is ~102, which is > max 98)
        assert "Audit administrative capacity" in recs_a[2]
        
        # Scenario B: Declining trend, conversion rate improving recently, forecast within limits
        # Max enrollments is 100, forecast will be low (around 48, which is < max 100)
        data_b = {
            "Month_Index": list(range(1, 25)),
            "Month_Label": [f"2024-{m:02d}" for m in range(1, 25)],
            "Enrollments": [100 - 2 * x for x in range(1, 25)], # declining: slope < 0, max is 98
            "Revenue": [120.0] * 24,
            "Website_Visitors": [1000] * 24,
            "Marketing_Spend": [100.0] * 24,
            "Social_Engagement": [50] * 24,
            "Lead_Conversion_Rate": [2.0] * 21 + [4.0] * 3 # recent 3-month (4.0%) is above 24-month avg (~2.25%)
        }
        pd.DataFrame(data_b).to_csv(temp_csv_path, index=False)
        
        engine_b = PredictiveDashboardTutorEngine(data_path=temp_csv_path)
        results_b = engine_b.run_forecast()
        recs_b = results_b["recommendations"]
        
        # Test Case 1: Declining slope retention audit is triggered
        assert "Audit student retention" in recs_b[0]
        # Test Case 2: Conversion funnel success is triggered
        assert "Capitalize on conversion health" in recs_b[1]
        # Test Case 3: Maintenance recommendation is triggered (forecast Month 25 is ~48, which is <= max 98)
        assert "Maintain standard capacity limits" in recs_b[2]

    finally:
        # Clean up temporary test file
        if temp_csv_path.exists():
            temp_csv_path.unlink()
