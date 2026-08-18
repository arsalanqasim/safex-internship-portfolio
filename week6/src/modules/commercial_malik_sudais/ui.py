"""UI for Retail BI Commercial Suite (Malik Sudais - Week 6)."""

import streamlit as st
from .engine import get_retail_bi_pricing


def render_ui() -> None:
    """Render Retail BI Commercial Suite."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #475569 0%, #334155 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🏬 Retail Multi-Store BI Commercial Deck</h2>
            <p style="margin: 0.5rem 0 0 0; color: #f1f5f9;">
                Developer: <b>Malik Sudais</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🛒 Retail Analytics Pricing Packages")
    tiers = get_retail_bi_pricing()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
