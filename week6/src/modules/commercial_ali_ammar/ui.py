"""UI for B2B Lead Agency (Ali Ammar Haider - Week 6)."""

import streamlit as st
from .engine import get_b2b_agency_tiers


def render_ui() -> None:
    """Render B2B Lead Agency UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">💼 B2B Lead Qualification Commercial Agency</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ede9fe;">
                Developer: <b>Ali Ammar Haider</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 B2B Qualification Service Retainers")
    tiers = get_b2b_agency_tiers()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
