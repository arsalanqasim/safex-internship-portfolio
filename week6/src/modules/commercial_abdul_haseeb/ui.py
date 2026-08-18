"""UI for Marketing Agency BI Pitch (Abdul Haseeb - Week 6)."""

import streamlit as st
from .engine import get_marketing_bi_packages


def render_ui() -> None:
    """Render Marketing Agency BI Pitch UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #c026d3 0%, #a21caf 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">📊 Marketing Agency BI Commercial Deck</h2>
            <p style="margin: 0.5rem 0 0 0; color: #fae8ff;">
                Developer: <b>Abdul Haseeb</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("💡 Agency Analytics Packages")
    tiers = get_marketing_bi_packages()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
