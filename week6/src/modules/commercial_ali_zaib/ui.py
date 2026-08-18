"""UI for Insurance Lead Qualifier Commercial Hub (Ali Zaib - Week 6)."""

import streamlit as st
from .engine import get_insurance_scoring_tiers


def render_ui() -> None:
    """Render Insurance Qualifier Commercial Hub."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🛡️ Insurance Lead Scoring Commercial Agency</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ccfbf1;">
                Developer: <b>Ali Zaib</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📋 Policy Lead Scoring Retainers")
    tiers = get_insurance_scoring_tiers()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
