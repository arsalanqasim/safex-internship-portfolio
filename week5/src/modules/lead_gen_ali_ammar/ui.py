"""UI for B2B Sales Lead Qualification Agent (Ali Ammar Haider - Week 5)."""

import streamlit as st
from .engine import score_b2b_lead


def render_ui() -> None:
    """Render the B2B Lead Qualification UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">💼 B2B Sales Lead Qualification Agent</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ede9fe;">
                Developer: <b>Ali Ammar Haider</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Select Target B2B Niche:", ["B2B SaaS & Tech", "Consulting & Advisory", "Digital Marketing Agencies", "Custom B2B"])

    with st.form("ali_ammar_lead_form"):
        st.subheader("🎯 Lead Qualification Form")
        c1, c2 = st.columns(2)
        comp_size = c1.selectbox("Company Size", ["Enterprise (500+ employees)", "Mid-Market (50-500 employees)", "Small Business (< 50 employees)"])
        budget = c2.number_input("Monthly Marketing/Tech Budget ($)", min_value=500.0, max_value=50000.0, value=5000.0, step=500.0)
        dm = st.checkbox("Contact is a C-Level / Key Decision Maker", value=True)

        if st.form_submit_button("Run Lead Qualification"):
            res = score_b2b_lead(comp_size, budget, dm)
            st.success(f"Qualification Score: **{res['score']}/100** · **{res['priority_tier']}**")
            st.info(f"**AI Account Summary:** {res['summary']}")
