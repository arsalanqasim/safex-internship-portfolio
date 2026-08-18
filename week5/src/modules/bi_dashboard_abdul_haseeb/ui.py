"""UI for Marketing Agency BI Hub (Abdul Haseeb - Week 5)."""

import streamlit as st
import pandas as pd
from .engine import get_agency_metrics


def render_ui() -> None:
    """Render Marketing BI Dashboard."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #c026d3 0%, #a21caf 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">📊 Marketing Agency BI Analytics Hub</h2>
            <p style="margin: 0.5rem 0 0 0; color: #fae8ff;">
                Developer: <b>Abdul Haseeb</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Selected Client Agency Focus:", ["Performance Ad Agency", "SEO & Content Agency", "Influencer Media", "Custom Marketing Niche"])

    metrics = get_agency_metrics()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly Ad Spend", f"${metrics['ad_spend']:,.2f}")
    c2.metric("Total Conversions", f"{metrics['conversions']:,}")
    c3.metric("Avg CPA", f"${metrics['cpa']:.2f}")
    c4.metric("Blended ROAS", f"{metrics['roas']}x")

    st.subheader("💡 AI Optimization Recommendation")
    st.info(metrics["recommendation"])
