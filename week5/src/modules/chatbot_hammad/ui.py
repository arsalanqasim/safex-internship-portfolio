"""UI for Logistics & Courier AI Support Bot (Hammad Abbas - Week 5)."""

import streamlit as st
from .engine import track_package


def render_ui() -> None:
    """Render Logistics Chatbot UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #d97706 0%, #b45309 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🚚 Logistics & Courier AI Support Bot</h2>
            <p style="margin: 0.5rem 0 0 0; color: #fef3c7;">
                Developer: <b>Hammad Abbas</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Selected Delivery Sector:", ["Last-Mile E-Commerce Courier", "Cross-Border Cargo Freight", "Same-Day Hyperlocal", "Custom Courier"])

    st.subheader("📦 Live Package Tracking & FAQ")
    track_id = st.text_input("Enter Tracking ID (e.g. SFX-998234-PK):", value="SFX-998234-PK")
    
    if st.button("Check Tracking Status"):
        res = track_package(track_id)
        st.success(f"Status: **{res['status']}**")
        st.write(f"Estimated Delivery: **{res['estimated_delivery']}** · Location: **{res['location']}**")
