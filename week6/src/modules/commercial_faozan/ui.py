"""UI for BI Commercial Deck (Muhammad Faozan Mujtaba - Week 6)."""

import streamlit as st
from .engine import get_bi_reporting_tiers


def render_ui() -> None:
    """Render BI Commercial Deck UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">📈 BI Dashboard Monetization & Retainer Deck</h2>
            <p style="margin: 0.5rem 0 0 0; color: #d1fae5;">
                Developer: <b>Muhammad Faozan Mujtaba</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("💼 Productized BI Reporting Retainers")
    tiers = get_bi_reporting_tiers()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
