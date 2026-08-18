"""UI for Healthcare & Clinic AI Chatbot (Shahidullah - Week 5)."""

import streamlit as st
from .engine import match_clinic_query


def render_ui() -> None:
    """Render the Healthcare Chatbot UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🏥 Healthcare & Clinic AI Support Chatbot</h2>
            <p style="margin: 0.5rem 0 0 0; color: #e0f2fe;">
                Developer: <b>Shahidullah</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Selected Clinic / Healthcare Setting:", ["General Medical Clinic", "Dental Care Center", "Diagnostic Laboratory", "Custom Health Service"])
    
    st.subheader("💬 Patient Query Simulator")
    query = st.text_input("Ask a clinic question (e.g., 'What are your clinic hours?' or 'Do you accept insurance?'):")
    
    if st.button("Submit Inquiry"):
        if query:
            res = match_clinic_query(query)
            st.success(f"**Bot Response:** {res['answer']}")
            st.caption(f"Confidence Score: {int(res['confidence']*100)}%")
        else:
            st.warning("Please enter a question.")
