"""UI for AI Business Intelligence Dashboard (Muhammad Faozan Mujtaba - Week 5)."""

import streamlit as st
import pandas as pd
from .engine import generate_sample_sales_data, generate_executive_insights


def render_ui() -> None:
    """Render the BI Dashboard UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">📈 AI Business Intelligence & Executive Dashboard</h2>
            <p style="margin: 0.5rem 0 0 0; color: #d1fae5;">
                Developer: <b>Muhammad Faozan Mujtaba</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox(
        "Select Target Business Domain:",
        ["E-Commerce & Digital Store", "SaaS Software Platform", "Retail Chain Network", "Consulting Agency"],
        index=0
    )

    df = generate_sample_sales_data(domain)

    # Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${df['Revenue ($)'].sum():,.2f}")
    c2.metric("Total Visitors", f"{df['Visitors'].sum():,}")
    c3.metric("Total Conversions", f"{df['Conversions'].sum():,}")
    c4.metric("Avg Order Value", f"${(df['Revenue ($)'].sum() / max(1, df['Conversions'].sum())):.2f}")

    # Charts
    st.subheader("📊 Revenue & Traffic Trends")
    st.line_chart(df.set_index("Date")[["Revenue ($)"]])

    # AI Plain English Summary
    st.subheader("🤖 AI Auto-Generated Weekly Insights")
    insights = generate_executive_insights(df, domain)
    st.markdown(insights)
