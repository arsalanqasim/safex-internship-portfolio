"""UI for Insurance Lead Qualifier (Ali Zaib - Week 5)."""

import streamlit as st
from .engine import score_insurance_lead


def render_ui() -> None:
    """Render Insurance Lead Qualifier UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🛡️ Insurance & Finance Lead Qualifier</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ccfbf1;">
                Developer: <b>Ali Zaib</b> · Week 5 Assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    domain = st.selectbox("Insurance Focus Area:", ["Health & Medical Insurance", "Auto & Fleet Insurance", "Commercial Property", "Life & Annuity"])

    with st.form("ali_zaib_form"):
        st.subheader("📋 Policy Lead Qualification Form")
        c1, c2 = st.columns(2)
        pt = c1.selectbox("Policy Type", ["Comprehensive Corporate", "Individual Basic", "Fleet Commercial"])
        cov = c2.number_input("Desired Coverage ($)", min_value=10000.0, max_value=500000.0, value=75000.0, step=5000.0)
        timeframe = st.selectbox("Decision Timeframe", ["Immediate (< 14 days)", "Within 1 Month", "Exploratory"])

        if st.form_submit_button("Evaluate Applicant Lead"):
            res = score_insurance_lead(pt, cov, timeframe)
            st.success(f"Qualification Score: **{res['score']}/100** · Status: **{res['underwriting_tier']}**")
            st.info(res["summary"])
