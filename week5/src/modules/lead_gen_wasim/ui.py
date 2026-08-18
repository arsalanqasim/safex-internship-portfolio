"""UI for Lead Generation & Qualification Tool (MUHAMMAD WASIM - Week 5)."""

import streamlit as st
import pandas as pd
from .engine import score_lead


def render_ui() -> None:
    """Render the Lead Qualification UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🎯 AI-Powered Lead Generation & Qualification Tool</h2>
            <p style="margin: 0.5rem 0 0 0; color: #dbeafe;">
                Developer: <b>MUHAMMAD WASIM</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Domain Selection
    col_d, col_info = st.columns([2, 1])
    with col_d:
        domain = st.selectbox(
            "Selected Business Domain / Target Industry:",
            ["Real Estate Agencies", "B2B SaaS & Services", "Insurance Brokers", "Marketing Agencies", "Custom Domain"],
            index=0
        )
    with col_info:
        st.info(f"Targeting: **{domain}**")

    # Lead Scoring Form
    with st.form("wasim_lead_form"):
        st.subheader("📝 Lead Intake & Scoring Simulator")
        c1, c2 = st.columns(2)
        lead_name = c1.text_input("Lead Name / Contact", value="Sarah Jenkins")
        company_name = c2.text_input("Organization / Agency", value="Apex Property Group")
        
        c3, c4, c5 = st.columns(3)
        budget = c3.slider("Estimated Monthly Budget ($k)", 1.0, 50.0, 15.0, 0.5)
        urgency = c4.selectbox("Project Urgency", ["Immediate (< 1 month)", "Moderate (1-3 months)", "Low (> 3 months)"])
        fit_score = c5.slider("Ideal Customer Profile Fit (1-10)", 1, 10, 8)
        
        submit = st.form_submit_button("⚡ Qualify Lead")

    if submit:
        result = score_lead(lead_name, company_name, budget, urgency, fit_score)
        st.success(f"Lead Score: **{result['score']}/100** · Category: **{result['category']}**")
        st.write(f"**Recommended Next Action:** {result['recommended_action']}")
        st.info(f"**AI Lead Summary:** {result['summary']}")
