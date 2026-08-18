"""Streamlit UI for AI Model Comparison & Recommendation Report (Malik Sudais - Week 4)."""

import streamlit as st
import pandas as pd
from .engine import get_comparison_dataframe, evaluate_careem_scenario


def render_ui() -> None:
    """Render the AI Model Comparison & Recommendation Report for Careem."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f766e 0%, #115e59 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem; border-left: 5px solid #2dd4bf;">
            <h2 style="margin: 0; color: #ffffff;">📊 AI Model Comparison & Recommendation Report</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ccfbf1; font-size: 0.95rem;">
                Target Enterprise: <b>Careem (Ride-Hailing & Super App)</b> · Developer: <b>Malik Sudais</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Live Deployment Launchpad Card
    st.markdown(
        """
        <div style="background: #f0fdfa; border: 2px solid #0d9488; border-radius: 10px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: center;">
            <h3 style="margin: 0; color: #0f766e;">🚀 Live Standalone Deployed Application</h3>
            <p style="margin: 0.5rem 0 1rem 0; color: #134e4a; font-size: 0.95rem;">
                Malik Sudais has deployed the full interactive Careem Model Evaluation app live on Streamlit Community Cloud.
            </p>
            <a href="https://cxyaqlr4q4jdwtm7dadw8v.streamlit.app/" target="_blank" style="background: #0d9488; color: white; padding: 0.6rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1rem; display: inline-block;">
                🌐 Launch Malik Sudais's Live Deployed App →
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # In-App Evaluation Matrix
    st.subheader("📈 Multi-Model Comparative Benchmark Matrix")
    df = get_comparison_dataframe()
    st.dataframe(
        df[["model", "accuracy_pct", "avg_latency_ms", "cost_per_1m_input", "cost_per_1m_output", "careem_fit_score"]],
        column_config={
            "model": "Evaluated AI Model",
            "accuracy_pct": st.column_config.ProgressColumn("Accuracy (%)", min_value=80, max_value=100, format="%.1f%%"),
            "avg_latency_ms": "Avg Latency (ms)",
            "cost_per_1m_input": "Input Cost (1M Tokens)",
            "cost_per_1m_output": "Output Cost (1M Tokens)",
            "careem_fit_score": st.column_config.NumberColumn("Careem Fit Score (/10)", format="%.1f")
        },
        use_container_width=True,
        hide_index=True
    )

    # Interactive Scenario Tester
    st.subheader("🧪 Live Careem Customer Support Scenario Evaluation")
    selected_scenario = st.selectbox(
        "Select Careem Support Scenario to Compare",
        ["Lost Item in Captain's Vehicle", "Overcharged Fare / Toll Dispute"]
    )

    responses = evaluate_careem_scenario(selected_scenario)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Google Gemini 1.5 Flash** `(Recommended)`")
        st.info(responses["gemini"])
        st.caption("⚡ Latency: 320ms | Cost: $0.075/1M | CSAT Fit: 9.6/10")
    with col2:
        st.markdown("**OpenAI GPT-4o-mini**")
        st.info(responses["gpt4"])
        st.caption("⚡ Latency: 410ms | Cost: $0.15/1M | CSAT Fit: 9.1/10")
    with col3:
        st.markdown("**Anthropic Claude 3.5 Haiku**")
        st.info(responses["claude"])
        st.caption("⚡ Latency: 480ms | Cost: $0.25/1M | CSAT Fit: 8.7/10")

    # Executive Recommendation
    st.markdown("### 🏆 Executive Recommendation Memo for Careem Operations")
    st.success(
        """
        **Primary Architecture Recommendation: Google Gemini 1.5 Flash**
        * **Cost Efficiency:** Lowest token pricing for high-volume inquiries (75% cheaper than Claude Haiku).
        * **Speed:** 320ms average response time fits live in-ride mobile chat expectations.
        * **Multilingual Accuracy:** Superior localized comprehension of mixed English, Urdu, and Arabic terms used in MENA and Pakistan ride-hailing markets.
        """
    )
