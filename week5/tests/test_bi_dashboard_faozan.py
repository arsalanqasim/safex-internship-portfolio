"""Tests for the Chinar Cart BI & Forecasting module (Muhammad Faozan Mujtaba - Week 5).

Run from the week5 folder:

    pytest tests/test_bi_dashboard_faozan.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

WEEK5_DIR = Path(__file__).resolve().parents[1]
if str(WEEK5_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK5_DIR))

from src.modules.bi_dashboard_faozan.engine import (  # noqa: E402
    ANOMALY_THRESHOLD,
    anomaly_summary,
    channel_performance,
    compute_kpis,
    dataset_summary,
    detect_anomalies,
    forecast_revenue,
    load_dataset,
)
from src.modules.bi_dashboard_faozan.generate_dataset import build_dataset  # noqa: E402
from src.modules.bi_dashboard_faozan.narrative import (  # noqa: E402
    build_insights,
    build_llm_prompt,
    compose_summary,
    provider,
)


@pytest.fixture(scope="module")
def frame() -> pd.DataFrame:
    return load_dataset()


# -- dataset ---------------------------------------------------------------------------


def test_dataset_loads_with_expected_shape(frame: pd.DataFrame) -> None:
    assert len(frame) == 180
    for column in ("Date", "Revenue", "Orders", "Sessions", "Conversion_Rate", "AOV", "CAC"):
        assert column in frame.columns
    assert frame["Date"].is_monotonic_increasing


def test_generator_is_deterministic() -> None:
    """The scaffold regenerated data on every rerun, so totals changed while being read."""
    first = build_dataset()
    second = build_dataset()
    pd.testing.assert_frame_equal(first, second)


def test_derived_columns_are_internally_consistent(frame: pd.DataFrame) -> None:
    sample = frame.head(50)
    np.testing.assert_allclose(sample["Orders"] / sample["Sessions"], sample["Conversion_Rate"])
    np.testing.assert_allclose(sample["Revenue"] / sample["Orders"], sample["AOV"])
    np.testing.assert_allclose(sample["Revenue"] - sample["Refunds"], sample["Net_Revenue"])


def test_no_negative_or_missing_core_values(frame: pd.DataFrame) -> None:
    for column in ("Revenue", "Orders", "Sessions", "Marketing_Spend"):
        assert frame[column].notna().all()
        assert (frame[column] > 0).all()


def test_missing_dataset_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "absent.csv")


# -- KPIs ------------------------------------------------------------------------------


def test_kpis_compare_equal_length_windows(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame, window_days=30)
    labels = {k.label for k in kpis}
    assert {"Revenue", "Orders", "Conversion Rate", "Blended CAC", "ROAS"} <= labels

    revenue = next(k for k in kpis if k.label == "Revenue")
    assert revenue.value == pytest.approx(frame["Revenue"].tail(30).sum())
    assert revenue.previous == pytest.approx(frame["Revenue"].iloc[-60:-30].sum())


def test_cac_treats_an_increase_as_a_regression(frame: pd.DataFrame) -> None:
    """Direction of goodness is metric-specific: rising CAC is bad, rising revenue is good."""
    cac = next(k for k in compute_kpis(frame) if k.label == "Blended CAC")
    assert cac.higher_is_better is False
    assert cac.improved is (cac.delta_pct < 0)


def test_kpis_reject_a_window_longer_than_the_data(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        compute_kpis(frame, window_days=len(frame))


# -- forecasting -----------------------------------------------------------------------


def test_forecast_returns_the_requested_horizon(frame: pd.DataFrame) -> None:
    result = forecast_revenue(frame, forecast_days=21)
    assert len(result.forecast) == 21
    assert result.forecast["Date"].min() > frame["Date"].max()
    assert (result.forecast["Predicted_Revenue"] > 0).all()


def test_forecast_interval_brackets_the_prediction(frame: pd.DataFrame) -> None:
    result = forecast_revenue(frame)
    assert (result.forecast["Lower_Bound"] <= result.forecast["Predicted_Revenue"]).all()
    assert (result.forecast["Upper_Bound"] >= result.forecast["Predicted_Revenue"]).all()
    assert (result.forecast["Lower_Bound"] >= 0).all()


def test_backtest_is_measured_on_unseen_data(frame: pd.DataFrame) -> None:
    result = forecast_revenue(frame, holdout_days=30)
    assert len(result.backtest) == 30
    # The holdout must be the tail of the series, i.e. genuinely out of sample.
    assert result.backtest["Date"].max() == frame["Date"].max()


def test_forecast_accuracy_meets_the_documented_thresholds(frame: pd.DataFrame) -> None:
    """Guards the numbers published in README.md against silent regression.

    Before the robust/log model was adopted, this backtest scored R-squared -2.40 - worse
    than predicting the mean - because a promotion and an outage inside the training
    window bent the fitted trend.
    """
    result = forecast_revenue(frame)
    assert result.mape < 10.0
    assert result.r2 > 0.3


def test_forecast_rejects_a_holdout_larger_than_the_data(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        forecast_revenue(frame.head(20), holdout_days=30)


def test_forecast_is_reproducible(frame: pd.DataFrame) -> None:
    a = forecast_revenue(frame)
    b = forecast_revenue(frame)
    assert a.forecast_total == pytest.approx(b.forecast_total)
    assert a.mape == pytest.approx(b.mape)


# -- anomaly detection -----------------------------------------------------------------


def test_detector_recovers_the_checkout_outage(frame: pd.DataFrame) -> None:
    """The generator embeds a four-day conversion collapse; the detector must find it."""
    flagged = detect_anomalies(frame, "Conversion_Rate")
    hits = flagged[flagged["Is_Anomaly"]]
    outage = hits[(hits["Date"] >= "2026-07-08") & (hits["Date"] <= "2026-07-11")]
    assert len(outage) == 4
    assert (outage["Direction"] == "below normal").all()


def test_detector_recovers_the_promotion_spike(frame: pd.DataFrame) -> None:
    flagged = detect_anomalies(frame, "Revenue")
    hits = flagged[flagged["Is_Anomaly"]]
    promo = hits[(hits["Date"] >= "2026-06-06") & (hits["Date"] <= "2026-06-09")]
    assert len(promo) == 4
    assert (promo["Direction"] == "above normal").all()


def test_episodes_group_consecutive_days(frame: pd.DataFrame) -> None:
    """22 single-day alerts collapse to a handful of readable episodes."""
    summary = anomaly_summary(frame)
    assert summary["count"] < summary["flagged_days"]
    assert all(e.days >= 1 for e in summary["episodes"])
    assert all(e.start <= e.end for e in summary["episodes"])


def test_episodes_are_ranked_by_severity(frame: pd.DataFrame) -> None:
    episodes = anomaly_summary(frame)["episodes"]
    peaks = [abs(e.peak_z) for e in episodes]
    assert peaks == sorted(peaks, reverse=True)


def test_historical_episodes_are_separated_from_the_current_window(frame: pd.DataFrame) -> None:
    """All embedded events predate the last 30 days, so none should count as current."""
    summary = anomaly_summary(frame, window_days=30)
    assert summary["count"] > 0
    assert summary["in_window"] == []


def test_detector_rejects_an_unknown_column(frame: pd.DataFrame) -> None:
    with pytest.raises(KeyError):
        detect_anomalies(frame, "Not_A_Column")


def test_flat_series_produces_no_anomalies() -> None:
    flat = pd.DataFrame(
        {"Date": pd.date_range("2026-01-01", periods=40, freq="D"), "Conversion_Rate": [0.03] * 40}
    )
    flagged = detect_anomalies(flat, "Conversion_Rate")
    assert not flagged["Is_Anomaly"].any()


# -- channels --------------------------------------------------------------------------


def test_channel_shares_sum_to_one_hundred(frame: pd.DataFrame) -> None:
    table = channel_performance(frame)
    assert len(table) == 5
    assert table["Share_Pct"].sum() == pytest.approx(100.0, abs=0.01)
    assert table["Sessions"].is_monotonic_decreasing


# -- narrative -------------------------------------------------------------------------


def test_narrative_runs_offline_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    assert provider() == "mock"


def test_insights_surface_margin_erosion_behind_revenue_growth(frame: pd.DataFrame) -> None:
    """The point of the module: revenue is up, but AOV and CAC are moving the wrong way.

    The scaffold reported "strong upward momentum" whenever revenue rose, which is true
    here and useless.
    """
    kpis = compute_kpis(frame)
    insights = build_insights(kpis, forecast_revenue(frame), anomaly_summary(frame), channel_performance(frame))
    headlines = " ".join(i.headline for i in insights).lower()
    assert "volume, not basket size" in headlines
    assert "acquisition cost" in headlines


def test_every_insight_carries_evidence(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame)
    insights = build_insights(kpis, forecast_revenue(frame), anomaly_summary(frame), channel_performance(frame))
    assert insights
    for insight in insights:
        assert insight.evidence.strip()
        assert insight.severity in {"positive", "watch", "risk"}


def test_summary_quotes_the_real_revenue_figure(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame)
    result = forecast_revenue(frame)
    insights = build_insights(kpis, result, anomaly_summary(frame), channel_performance(frame))
    summary = compose_summary(insights, kpis, result, "Chinar Cart")
    revenue = next(k for k in kpis if k.label == "Revenue")
    assert f"{revenue.value:,.0f}" in summary
    assert "Chinar Cart" in summary


def test_summary_excludes_anomalies_outside_the_window(frame: pd.DataFrame) -> None:
    """A resolved July outage must not be reported as news in an August summary."""
    kpis = compute_kpis(frame, window_days=30)
    result = forecast_revenue(frame)
    anomalies = anomaly_summary(frame, window_days=30)
    insights = build_insights(kpis, result, anomalies, channel_performance(frame), window_days=30)
    summary = compose_summary(insights, kpis, result, "Chinar Cart", window_days=30)
    assert "Jul" not in summary


def test_llm_prompt_forbids_unsupported_claims(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame)
    insights = build_insights(kpis, forecast_revenue(frame), anomaly_summary(frame), channel_performance(frame))
    prompt = build_llm_prompt("Chinar Cart", kpis, insights)
    assert "Use only the figures and findings below" in prompt
    assert "Quote numbers exactly" in prompt


# -- summary ---------------------------------------------------------------------------


def test_dataset_summary_reports_totals(frame: pd.DataFrame) -> None:
    summary = dataset_summary(frame)
    assert summary["rows"] == 180
    assert summary["total_revenue"] == pytest.approx(frame["Revenue"].sum())
    assert 0 < summary["mean_conversion"] < 1
