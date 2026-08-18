"""UI for Lead Gen Commercial Deck (MUHAMMAD WASIM - Week 6)."""

import streamlit as st
from .engine import get_lead_gen_pricing


def render_ui() -> None:
    """Render Lead Gen Commercial Deck UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🎯 Lead Generation Agency Commercialization</h2>
            <p style="margin: 0.5rem 0 0 0; color: #dbeafe;">
                Developer: <b>MUHAMMAD WASIM</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📦 Pricing & Service Packages")
    tiers = get_lead_gen_pricing()
    for t_name, t_desc in tiers.items():
        st.markdown(f"**{t_name}**: {t_desc}")
