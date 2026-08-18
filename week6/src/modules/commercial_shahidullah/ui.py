"""UI for Clinic Chatbot Commercial Deck (Shahidullah - Week 6)."""

import streamlit as st
from .engine import get_clinic_bot_pricing


def render_ui() -> None:
    """Render Clinic Chatbot Commercial Deck."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🏥 Healthcare & Clinic AI Chatbot Commercial Hub</h2>
            <p style="margin: 0.5rem 0 0 0; color: #e0f2fe;">
                Developer: <b>Shahidullah</b> · Week 6 Monetization
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("💊 Healthcare Clinic Automation Packages")
    tiers = get_clinic_bot_pricing()
    for name, desc in tiers.items():
        st.markdown(f"**{name}**: {desc}")
