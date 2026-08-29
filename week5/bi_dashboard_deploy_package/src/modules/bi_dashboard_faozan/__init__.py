"""AI Business Intelligence & Forecasting Suite (Muhammad Faozan Mujtaba - Week 5)."""

from .engine import (
    anomaly_summary,
    channel_performance,
    compute_kpis,
    detect_anomalies,
    forecast_revenue,
    load_dataset,
)
from .narrative import build_insights, compose_summary
from .ui import render_ui

__all__ = [
    "anomaly_summary",
    "channel_performance",
    "compute_kpis",
    "detect_anomalies",
    "forecast_revenue",
    "load_dataset",
    "build_insights",
    "compose_summary",
    "render_ui",
]
