"""Streamlit UI for the Chinar Cart AI Business Intelligence & Forecasting Suite.

Week 5 module owned by Muhammad Faozan Mujtaba.

Page-level configuration stays in ``week5/src/app.py``. This file exposes a single
self-contained ``render_ui()`` and holds no business logic: every number it shows comes
from ``engine.py`` and every sentence from ``narrative.py``.
"""

from __future__ import annotations

from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from .engine import (
    COMPANY,
    CURRENCY,
    DEFAULT_FORECAST_DAYS,
    anomaly_summary,
    channel_performance,
    compute_kpis,
    dataset_summary,
    detect_anomalies,
    forecast_revenue,
    load_dataset,
)
from .narrative import build_insights, build_llm_prompt, compose_summary, provider

matplotlib.use("Agg")


# --------------------------------------------------------------------------------------
# Theming
# --------------------------------------------------------------------------------------


def _palette() -> dict[str, str]:
    """Match the shared shell's light/dark selection so charts do not glare."""
    dark = st.session_state.get("ui_theme_choice", "Light") == "Dark"
    if dark:
        return {
            "bg": "#151b24", "ink": "#f8fafc", "muted": "#a8b3c2",
            "grid": "#334155", "accent": "#2dd4bf", "accent2": "#f59e0b", "bad": "#f87171",
        }
    return {
        "bg": "#ffffff", "ink": "#172033", "muted": "#64748b",
        "grid": "#dce3ec", "accent": "#0f766e", "accent2": "#b45309", "bad": "#dc2626",
    }


def _style_axes(ax: plt.Axes, colors: dict[str, str]) -> None:
    ax.set_facecolor(colors["bg"])
    ax.figure.set_facecolor(colors["bg"])
    ax.tick_params(colors=colors["muted"], labelsize=8)
    ax.grid(True, color=colors["grid"], linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(colors["grid"])
    ax.xaxis.label.set_color(colors["muted"])
    ax.yaxis.label.set_color(colors["muted"])
    ax.title.set_color(colors["ink"])


@st.cache_data(show_spinner=False)
def _load() -> pd.DataFrame:
    """Load once per process. The dataset is static, so caching is safe here."""
    return load_dataset()


# --------------------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------------------


def _render_header() -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">📈 BI &amp; Forecasting · Week 5 AI Products Suite</div>
            <div class="hero-title">AI Business Intelligence &amp; Forecasting Suite · {COMPANY}</div>
            <div class="hero-subtitle">
                Weekly executive reporting for a direct-to-consumer e-commerce store:
                KPIs against a like-for-like window, a backtested revenue forecast, anomaly
                detection, and a written summary that only states what the numbers support.<br>
                Developer: <strong>Muhammad Faozan Mujtaba</strong> (Team Member)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis(kpis: list[Any], window_days: int) -> None:
    st.markdown(f"#### Headline metrics · last {window_days} days vs previous {window_days}")
    for row_start in (0, 5):
        row = kpis[row_start : row_start + 5]
        if not row:
            continue
        for column, kpi in zip(st.columns(len(row)), row):
            column.metric(
                kpi.label,
                kpi.formatted(),
                f"{kpi.delta_pct:+.1f}%",
                delta_color="normal" if kpi.higher_is_better else "inverse",
            )
    st.caption(
        "Both windows are the same length so the comparison is like-for-like. This series has "
        "strong weekly seasonality, so an uneven window would show swings that are purely an "
        "artefact of which weekdays it contained."
    )


def _render_summary_tab(data: dict[str, Any]) -> None:
    st.markdown("#### Executive summary")
    st.markdown(data["summary"])

    st.caption(
        f"Generated offline (provider `{provider()}`) from the figures computed on this page. "
        "Every sentence is emitted by a rule that first checked a threshold against a real "
        "number, so the summary cannot describe a trend the data does not show."
    )

    st.divider()
    _render_kpis(data["kpis"], data["window_days"])

    st.divider()
    st.markdown("#### Findings")
    for insight in data["insights"]:
        st.markdown(insight.as_markdown(), unsafe_allow_html=True)


def _render_performance_tab(frame: pd.DataFrame, channels: pd.DataFrame) -> None:
    colors = _palette()

    st.markdown("#### Revenue and sessions")
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.plot(frame["Date"], frame["Revenue"], color=colors["accent"], linewidth=1.4, label="Daily revenue")
    ax.plot(
        frame["Date"],
        frame["Revenue"].rolling(7).mean(),
        color=colors["accent2"],
        linewidth=2.2,
        label="7-day average",
    )
    ax.set_ylabel(f"Revenue ({CURRENCY})")
    ax.legend(frameon=False, fontsize=8, labelcolor=colors["muted"])
    _style_axes(ax, colors)
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.caption(
        "The 7-day average is shown because daily revenue swings roughly 25% between a "
        "Tuesday and a Saturday. Reading the raw daily line as a trend is misleading."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Conversion rate")
        fig, ax = plt.subplots(figsize=(5, 2.8))
        ax.plot(frame["Date"], frame["Conversion_Rate"] * 100, color=colors["accent"], linewidth=1.3)
        ax.set_ylabel("%")
        _style_axes(ax, colors)
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with col_b:
        st.markdown("##### Average order value")
        fig, ax = plt.subplots(figsize=(5, 2.8))
        ax.plot(frame["Date"], frame["AOV"], color=colors["accent2"], linewidth=1.3)
        ax.set_ylabel(CURRENCY)
        _style_axes(ax, colors)
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    st.markdown("#### Channel mix")
    display = channels.copy()
    display["Sessions"] = display["Sessions"].map(lambda v: f"{v:,.0f}")
    display["Share_Pct"] = display["Share_Pct"].map(lambda v: f"{v:.1f}%")
    display["Change_Pct"] = display["Change_Pct"].map(lambda v: f"{v:+.1f}%")
    st.dataframe(
        display[["Channel", "Sessions", "Share_Pct", "Change_Pct"]].rename(
            columns={"Share_Pct": "Share", "Change_Pct": "Change vs prev window"}
        ),
        width="stretch",
        hide_index=True,
    )


def _render_forecast_tab(frame: pd.DataFrame, forecast_days: int) -> None:
    result = forecast_revenue(frame, forecast_days=forecast_days)
    colors = _palette()

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric(f"Next {result.forecast_days} days", f"{CURRENCY} {result.forecast_total:,.0f}")
    col_b.metric("Backtest MAPE", f"{result.mape:.2f}%")
    col_c.metric("Backtest R²", f"{result.r2:+.3f}")
    col_d.metric("Trend", f"{result.trend_per_day:+.2f}%/day")

    st.markdown("#### Forecast")
    fig, ax = plt.subplots(figsize=(10, 3.8))
    history = result.history.tail(90)
    ax.plot(history["Date"], history["Revenue"], color=colors["muted"], linewidth=1.2, label="Actual")
    ax.plot(
        result.forecast["Date"],
        result.forecast["Predicted_Revenue"],
        color=colors["accent"],
        linewidth=2.0,
        label="Forecast",
    )
    ax.fill_between(
        result.forecast["Date"],
        result.forecast["Lower_Bound"],
        result.forecast["Upper_Bound"],
        color=colors["accent"],
        alpha=0.18,
        label="95% interval",
    )
    ax.set_ylabel(f"Revenue ({CURRENCY})")
    ax.legend(frameon=False, fontsize=8, labelcolor=colors["muted"])
    _style_axes(ax, colors)
    st.pyplot(fig, width="stretch")
    plt.close(fig)

    st.markdown("#### Backtest: predictions against data the model never saw")
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(
        result.backtest["Date"],
        result.backtest["Actual_Revenue"],
        color=colors["muted"],
        linewidth=1.6,
        label="Actual",
    )
    ax.plot(
        result.backtest["Date"],
        result.backtest["Predicted_Revenue"],
        color=colors["accent"],
        linewidth=1.8,
        linestyle="--",
        label="Predicted",
    )
    ax.legend(frameon=False, fontsize=8, labelcolor=colors["muted"])
    _style_axes(ax, colors)
    st.pyplot(fig, width="stretch")
    plt.close(fig)

    st.markdown("#### Why the reported accuracy is the holdout figure")
    left, right = st.columns(2)
    left.metric("R² on unseen holdout", f"{result.r2:+.4f}", help="The number to trust.")
    right.metric("R² on training data", f"{result.in_sample_r2:+.4f}", help="Always flatters the model.")
    st.caption(
        f"MAE {CURRENCY} {result.mae:,.0f} · MAPE {result.mape:.2f}% · measured on the last "
        f"{result.holdout_days} days, which the model never trained on. "
        "The in-sample figure is shown only so the gap is visible; a client planning stock "
        "against a training fit would be misled."
    )
    for note in result.notes:
        st.caption(f"ℹ️ {note}")


def _render_anomaly_tab(frame: pd.DataFrame, anomalies: dict[str, Any]) -> None:
    colors = _palette()

    st.markdown("#### Detected episodes")
    st.caption(
        f"{anomalies['count']} episodes covering {anomalies['flagged_days']} flagged days across "
        "the full 180-day history. Detection uses the modified z-score (median and MAD) rather "
        "than mean and standard deviation, because the promotion spike would otherwise inflate "
        "the threshold enough to hide the checkout outage."
    )

    if not anomalies["episodes"]:
        st.success("No days in the history deviate far enough from normal to flag.")
        return

    rows = [
        {
            "Metric": e.metric,
            "From": e.start.strftime("%Y-%m-%d"),
            "To": e.end.strftime("%Y-%m-%d"),
            "Days": e.days,
            "Change vs normal": f"{e.change_pct:+.0f}%",
            "Peak z": f"{e.peak_z:+.1f}",
            "In current window": "yes" if e in anomalies.get("in_window", []) else "no",
        }
        for e in anomalies["episodes"]
    ]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    if not anomalies.get("in_window"):
        st.info(
            f"None of these fall inside the current {anomalies.get('window_days', 30)}-day "
            "reporting window, so they are historical. The executive summary deliberately "
            "excludes them rather than presenting a resolved incident as current news."
        )

    st.markdown("#### Conversion rate with flagged days")
    flagged = detect_anomalies(frame, "Conversion_Rate", anomalies["threshold"])
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(flagged["Date"], flagged["Conversion_Rate"] * 100, color=colors["accent"], linewidth=1.3)
    hits = flagged[flagged["Is_Anomaly"]]
    ax.scatter(
        hits["Date"], hits["Conversion_Rate"] * 100, color=colors["bad"], s=28, zorder=5, label="Flagged"
    )
    ax.set_ylabel("Conversion rate (%)")
    ax.legend(frameon=False, fontsize=8, labelcolor=colors["muted"])
    _style_axes(ax, colors)
    st.pyplot(fig, width="stretch")
    plt.close(fig)


def _render_method_tab(frame: pd.DataFrame, data: dict[str, Any]) -> None:
    summary = dataset_summary(frame)
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Days of history", summary["rows"])
    col_b.metric("Total revenue", f"{CURRENCY} {summary['total_revenue']:,.0f}")
    col_c.metric("Total orders", f"{summary['total_orders']:,}")
    col_d.metric("Mean conversion", f"{summary['mean_conversion'] * 100:.2f}%")
    st.caption(
        f"{summary['start']:%d %b %Y} to {summary['end']:%d %b %Y}. "
        "Synthetic data generated deterministically by `generate_dataset.py` and committed "
        "as CSV, so every figure on this page is reproducible."
    )

    st.markdown(
        """
#### Method

1. **Deterministic data.** The dataset is generated once from a fixed seed and read from
   disk. Generating it inside the render path, as the original scaffold did, meant every
   widget interaction reshuffled the numbers - totals changed while you read them, and no
   figure could be checked twice.
2. **Like-for-like KPI windows.** Two equal-length windows are compared. Weekly seasonality
   is strong enough that an uneven window shows swings which are purely an artefact of
   which weekdays it contained.
3. **Forecast.** Huber regression on log revenue, over a linear trend, weekday dummies and
   an annual Fourier pair. Log because revenue is sessions x conversion x order value, so
   its movements are multiplicative. Huber because the training window contains a
   promotion and an outage, and least squares bends the trend line to accommodate them.
4. **Honest accuracy.** Every reported figure comes from a holdout the model never trained
   on. The in-sample number is displayed beside it only so the gap is visible.
5. **Anomalies.** Modified z-score on median and MAD, grouped into episodes. Grouping turns
   22 individual day-alerts into 4 readable findings.
6. **Narrative.** Composed offline from computed facts. A language model handed a table
   will write a fluent paragraph whether or not the numbers support it, and that failure
   mode is exactly what a founder would act on.
        """
    )

    st.markdown("#### Prompt used when a hosted provider is configured")
    st.caption(
        "Rendered even in offline mode so the grounding rules can be reviewed without an API key."
    )
    st.code(build_llm_prompt(COMPANY, data["kpis"], data["insights"]), language="text")

    with st.expander("Browse the underlying data"):
        st.dataframe(frame.tail(60), width="stretch", hide_index=True)


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def render_ui() -> None:
    """Entry point called by the shared Week 5 Streamlit shell."""
    _render_header()

    try:
        frame = _load()
    except Exception as exc:
        st.error("The Chinar Cart dataset could not be loaded.")
        st.exception(exc)
        return

    with st.sidebar:
        st.markdown('<div class="side-heading">BI Dashboard Controls</div>', unsafe_allow_html=True)
        window_days = st.select_slider(
            "Reporting window (days)", options=[7, 14, 28, 30, 60], value=30, key="bi_window"
        )
        forecast_days = st.slider(
            "Forecast horizon (days)", 7, 60, DEFAULT_FORECAST_DAYS, key="bi_horizon"
        )

    try:
        kpis = compute_kpis(frame, window_days=window_days)
    except ValueError as exc:
        st.warning(str(exc))
        return

    result = forecast_revenue(frame)
    anomalies = anomaly_summary(frame, window_days=window_days)
    channels = channel_performance(frame, window_days=window_days)
    insights = build_insights(kpis, result, anomalies, channels, window_days=window_days)

    data = {
        "kpis": kpis,
        "insights": insights,
        "window_days": window_days,
        "summary": compose_summary(insights, kpis, result, COMPANY, window_days=window_days),
    }

    summary_tab, performance_tab, forecast_tab, anomaly_tab, method_tab = st.tabs(
        ["Executive summary", "Performance", "Forecast", "Anomalies", "Data & method"]
    )
    with summary_tab:
        _render_summary_tab(data)
    with performance_tab:
        _render_performance_tab(frame, channels)
    with forecast_tab:
        _render_forecast_tab(frame, forecast_days)
    with anomaly_tab:
        _render_anomaly_tab(frame, anomalies)
    with method_tab:
        _render_method_tab(frame, data)
