"""UI for Retail Multi-Store BI Dashboard (Malik Sudais - Week 5)."""

import streamlit as st
from .engine import get_retail_kpis


def render_ui() -> None:
    """Render Retail BI Dashboard."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #475569 0%, #334155 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🏬 Retail Multi-Store BI Dashboard</h2>
            <p style="margin: 0.5rem 0 0 0; color: #f1f5f9;">
                Developer: <b>Malik Sudais</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Retail Format:", ["Fashion & Apparel Outlets", "Grocery Supermarkets", "Consumer Electronics", "Custom Retail"])

    kpis = get_retail_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Store Outlets", kpis["active_stores"])
    c2.metric("Daily Footfall", f"{kpis['daily_footfall']:,}")
    c3.metric("Inventory Turnover", f"{kpis['inventory_turnover']}x")
    c4.metric("Sell-Through Rate", f"{kpis['sell_through_rate']}%")

    st.subheader("⚠️ AI Inventory & Replenishment Alert")
    st.warning(kpis["replenishment_alert"])
