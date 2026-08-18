"""UI for Logistics Bot Commercial Package (Hammad Abbas - Week 6)."""

import streamlit as st
from .engine import get_logistics_bot_tiers


def render_ui() -> None:
    """Render Logistics Bot Commercial Deck."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #d97706 0%, #b45309 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🚚 Logistics & Courier AI Bot Commercial Hub</h2>
            <p style="margin: 0.5rem 0 0 0; color: #fef3c7;">
                Developer: <b>Hammad Abbas</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📦 Courier & Logistics Automation Packages")
    tiers = get_logistics_bot_tiers()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
