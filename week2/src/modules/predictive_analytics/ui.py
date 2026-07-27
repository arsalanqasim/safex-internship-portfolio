from __future__ import annotations

import pandas as pd
import streamlit as st

from src.modules.registry import MODULE_REGISTRY
from src.modules.predictive_analytics.engine import (
    CHURN_MODELS,
    DEMAND_MODELS,
    PredictiveAnalyticsEngine,
    PredictiveAnalyticsError,
)

_CSS = """
<style>
.st-key-pa-root [data-testid="stMetric"]{background:var(--card-bg);border:1px solid var(--card-border);
  border-radius:10px;padding:0.85rem;}
.st-key-pa-root [data-testid="stTab"] p{font-weight:600;}
.pa-note{font-size:12.5px;color:var(--text-muted);margin-top:-4px;}
</style>
"""


@st.cache_resource
def _get_engine() -> PredictiveAnalyticsEngine:
    return PredictiveAnalyticsEngine()


def render_ui() -> None:
    """Renders the Streamlit frontend tab for the Predictive Analytics Mini-Study."""
    metadata = MODULE_REGISTRY["week2"]["predictive_analytics"]
    engine = _get_engine()

    with st.container(key="pa-root"):
        st.markdown(_CSS, unsafe_allow_html=True)

        st.markdown(f'''
        <div class="hero-wrap">
            <div class="hero-badge">📈 Business Automation Suite</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Assigned to: <strong>{metadata["developer"]}</strong> ({metadata["role"]})
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.info(
            f"**Developer E-mail:** {metadata['email']}  \n"
            f"**Required Stack:** {', '.join(metadata['tech'])}"
        )

        st.subheader("Objective & Scope")
        st.write(metadata["description"])
        st.caption(
            "Both datasets below are synthetically generated sample data (no proprietary "
            "SafeX records were available for this internship prototype), built with realistic "
            "trend, seasonality, and behavioral structure so the models produce meaningful results."
        )

        st.markdown("---")

        tab_demand, tab_churn = st.tabs(["📈 Demand Forecasting", "👥 Churn Prediction"])

        with tab_demand:
            _render_demand_tab(engine)

        with tab_churn:
            _render_churn_tab(engine)


def _render_demand_tab(engine: PredictiveAnalyticsEngine) -> None:
    st.write(
        "Trains a regression model on 42 months of sample monthly demand history "
        "(marketing spend, price index, promotions, and seasonality) and forecasts "
        "demand for future months."
    )

    history = engine.load_demand_data()
    with st.expander("View raw demand history sample data"):
        st.dataframe(history, use_container_width=True, hide_index=True)

    col_model, col_periods, col_btn = st.columns([2, 1, 1])
    with col_model:
        model_label = st.selectbox(
            "Model", ["Linear Regression", "Random Forest Regressor"], key="demand_model_choice"
        )
        model_type = "linear" if model_label == "Linear Regression" else "random_forest"
    with col_periods:
        periods = st.number_input("Forecast months ahead", min_value=1, max_value=12, value=6, key="demand_periods")
    with col_btn:
        st.write("")
        train_clicked = st.button("Train & Forecast", type="primary", key="train_demand_btn", use_container_width=True)

    if train_clicked:
        try:
            metrics = engine.train_demand_model(model_type)
            forecast = engine.forecast_demand(int(periods))
            st.session_state["demand_metrics"] = metrics
            st.session_state["demand_forecast"] = forecast
        except PredictiveAnalyticsError as exc:
            st.error(str(exc))

    metrics = st.session_state.get("demand_metrics")
    forecast = st.session_state.get("demand_forecast")

    if metrics is None:
        st.info("Choose a model and click **Train & Forecast** to see results.")
        return

    st.markdown("#### Model Evaluation (last 6 months held out)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAE (units)", metrics["mae"])
    m2.metric("RMSE (units)", metrics["rmse"])
    m3.metric("R²", metrics["r2"])
    m4.metric("Train / Test rows", f"{metrics['n_train']} / {metrics['n_test']}")

    eval_df = pd.DataFrame({
        "Month": metrics["test_months"],
        "Actual": metrics["test_actual"],
        "Predicted": metrics["test_predicted"],
    }).set_index("Month")
    st.markdown("**Holdout: Actual vs Predicted demand**")
    st.line_chart(eval_df)

    st.markdown("#### Forecast")
    st.dataframe(forecast, use_container_width=True, hide_index=True)

    combined = pd.concat([
        history[["month_index", "demand_units"]].rename(columns={"demand_units": "Historical demand"}),
        forecast[["month_index", "forecast_demand"]].rename(columns={"forecast_demand": "Forecast demand"}),
    ]).set_index("month_index")
    st.markdown("**Historical demand + forecast**")
    st.line_chart(combined)

    st.download_button(
        "Download forecast as CSV",
        data=forecast.to_csv(index=False),
        file_name="demand_forecast.csv",
        mime="text/csv",
    )

    st.caption(
        "Note: Random Forest tends to under-extrapolate an ongoing upward trend "
        "(it can't predict beyond the range of values it saw in training), so "
        "Linear Regression generally forecasts the trend more accurately here — "
        "a useful, realistic finding for the case study write-up."
    )


def _render_churn_tab(engine: PredictiveAnalyticsEngine) -> None:
    st.write(
        "Trains a classification model on a sample of 300 customers (tenure, spend, "
        "support tickets, satisfaction, discount status) to flag customers at risk of churn."
    )

    churn_data = engine.load_churn_data()
    with st.expander("View raw customer churn sample data"):
        st.dataframe(churn_data, use_container_width=True, hide_index=True)

    col_model, col_btn = st.columns([2, 1])
    with col_model:
        model_label = st.selectbox(
            "Model", ["Logistic Regression", "Random Forest Classifier"], key="churn_model_choice"
        )
        model_type = "logistic" if model_label == "Logistic Regression" else "random_forest"
    with col_btn:
        st.write("")
        train_clicked = st.button("Train Churn Model", type="primary", key="train_churn_btn", use_container_width=True)

    if train_clicked:
        try:
            metrics = engine.train_churn_model(model_type)
            st.session_state["churn_metrics"] = metrics
        except PredictiveAnalyticsError as exc:
            st.error(str(exc))

    metrics = st.session_state.get("churn_metrics")

    if metrics is None:
        st.info("Choose a model and click **Train Churn Model** to see results.")
        return

    st.markdown("#### Model Evaluation (25% holdout, stratified)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", metrics["accuracy"])
    m2.metric("Precision", metrics["precision"])
    m3.metric("Recall", metrics["recall"])
    m4.metric("F1 score", metrics["f1"])

    cm = metrics["confusion_matrix"]
    cm_df = pd.DataFrame(
        cm, index=["Actual: Stayed", "Actual: Churned"], columns=["Predicted: Stayed", "Predicted: Churned"]
    )
    st.markdown("**Confusion Matrix**")
    st.dataframe(cm_df, use_container_width=True)

    st.markdown("**Feature importance**")
    importance_df = pd.DataFrame(
        sorted(metrics["feature_importance"].items(), key=lambda kv: kv[1], reverse=True),
        columns=["Feature", "Importance"],
    ).set_index("Feature")
    st.bar_chart(importance_df)

    st.markdown("---")
    st.markdown("#### Try it: score a single customer")

    with st.form("churn_predict_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=120, value=12)
            spend = st.number_input("Monthly spend ($)", min_value=0.0, value=75.0, step=5.0)
        with c2:
            tickets = st.number_input("Support tickets (recent)", min_value=0, max_value=20, value=1)
            satisfaction = st.slider("Satisfaction score (1-10)", 1, 10, 7)
        with c3:
            discount = st.checkbox("Active discount applied", value=False)
        predict_clicked = st.form_submit_button("Predict Churn Risk", type="primary")

    if predict_clicked:
        try:
            result = engine.predict_churn({
                "tenure_months": tenure,
                "monthly_spend": spend,
                "support_tickets": tickets,
                "satisfaction_score": satisfaction,
                "active_discount": int(discount),
            })
            if result["churn_probability"] >= 0.5:
                st.error(f"⚠️ {result['label']} — churn probability: {result['churn_probability']:.1%}")
            else:
                st.success(f"✅ {result['label']} — churn probability: {result['churn_probability']:.1%}")
        except PredictiveAnalyticsError as exc:
            st.error(str(exc))
