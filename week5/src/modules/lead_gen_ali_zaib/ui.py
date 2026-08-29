"""UI for Insurance & Finance Lead Qualifier (Ali Zaib - Week 5)."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from .engine import (
    CONTACT_CHANNELS,
    OCCUPATION_RISK_LEVELS,
    POLICY_TYPES,
    TIMELINES,
    LeadQualifierError,
    load_sample_leads,
    score_insurance_lead,
    score_leads_batch,
)


def render_ui() -> None:
    """Render the Insurance & Finance Lead Qualifier UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; color: #ffffff;">🛡️ Insurance & Finance Lead Qualifier</h2>
            <p style="margin: 0.5rem 0 0 0; color: #ccfbf1;">
                Developer: <b>Ali Zaib</b> · Week 5 Assignment · Insurance & Wealth Management
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "A transparent, rubric-based lead scoring model — not a black-box classifier. "
        "Every score breaks down into five weighted factors so a sales rep or underwriter "
        "can see exactly *why* a lead scored the way it did."
    )

    tab_single, tab_batch, tab_about = st.tabs(
        ["📋 Qualify a Single Lead", "📊 Batch Lead Scoring", "ℹ️ How Scoring Works"]
    )

    with tab_single:
        _render_single_lead_tab()
    with tab_batch:
        _render_batch_tab()
    with tab_about:
        _render_about_tab()


def _render_single_lead_tab() -> None:
    with st.form("ali_zaib_lead_form"):
        st.subheader("Policy Lead Qualification Form")
        c1, c2 = st.columns(2)
        policy_type = c1.selectbox("Policy Type", POLICY_TYPES)
        coverage = c2.number_input("Desired Coverage ($)", min_value=5000.0, max_value=500000.0, value=75000.0, step=5000.0)

        c3, c4 = st.columns(2)
        timeline = c3.selectbox("Decision Timeframe", TIMELINES)
        budget = c4.number_input("Stated Monthly Budget ($)", min_value=10.0, max_value=2000.0, value=200.0, step=10.0)

        c5, c6, c7 = st.columns(3)
        claims = c5.number_input("Prior Claims (count)", min_value=0, max_value=10, value=0, step=1)
        age = c6.number_input("Applicant Age", min_value=18, max_value=90, value=35, step=1)
        occupation = c7.selectbox("Occupation Risk", OCCUPATION_RISK_LEVELS)

        channel = st.selectbox("Contact Channel", CONTACT_CHANNELS)

        submitted = st.form_submit_button("Evaluate Applicant Lead", type="primary")

    if submitted:
        try:
            result = score_insurance_lead(
                policy_type=policy_type,
                coverage_amount=coverage,
                decision_timeline=timeline,
                prior_claims_count=int(claims),
                applicant_age=int(age),
                occupation_risk=occupation,
                stated_monthly_budget=budget,
                contact_channel=channel,
            )
        except LeadQualifierError as exc:
            st.error(str(exc))
            return

        score_color = "success" if result.total_score >= 60 else ("warning" if result.total_score >= 40 else "error")
        getattr(st, score_color)(f"**{result.total_score}/100** — {result.tier}")
        st.write(result.summary)

        st.markdown("#### Score Breakdown")
        breakdown_df = pd.DataFrame(
            [{"Factor": k, "Points": v} for k, v in result.sub_scores.items()]
        ).set_index("Factor")
        st.bar_chart(breakdown_df)

        if result.flags:
            st.markdown("#### Flags for Review")
            for flag in result.flags:
                st.warning(flag)
        else:
            st.info("No risk flags — clean lead profile.")


def _render_batch_tab() -> None:
    st.write(
        "Score a batch of leads at once. Use the bundled sample dataset, or upload your own "
        "CSV with the same columns."
    )

    uploaded = st.file_uploader("Upload a leads CSV (optional)", type=["csv"])
    use_sample = st.button("Use Sample Dataset (40 leads)", type="primary")

    df = None
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
        except Exception as exc:
            st.error(f"Could not read uploaded file: {exc}")
            return
    elif use_sample:
        df = load_sample_leads()

    if df is None:
        st.info("Upload a CSV or click **Use Sample Dataset** to see batch scoring in action.")
        return

    try:
        scored = score_leads_batch(df)
    except LeadQualifierError as exc:
        st.error(str(exc))
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Leads", len(scored))
    m2.metric("Hot Leads", int((scored["tier"] == "Hot Lead — Fast-Track Underwriting").sum()))
    m3.metric("Avg Score", round(scored["total_score"].mean(), 1))
    m4.metric("Leads w/ Flags", int((scored["flag_count"] > 0).sum()))

    st.markdown("#### Tier Distribution")
    tier_counts = scored["tier"].value_counts().reindex([
        "Hot Lead — Fast-Track Underwriting",
        "Qualified — Standard Underwriting",
        "Nurture — Needs More Information",
        "Low Priority — Manual Review Likely",
    ]).fillna(0).astype(int)
    st.bar_chart(tier_counts)

    st.markdown("#### Ranked Leads (hottest first)")
    st.caption("🟢 Hot Lead · 🟡 Qualified · 🟠 Nurture · 🔴 Low Priority")

    def _tier_row_color(row):
        colors = {
"Hot Lead — Fast-Track Underwriting": "background-color: #15803d; color: white",
"Qualified — Standard Underwriting": "background-color: #a16207; color: white",
"Nurture — Needs More Information": "background-color: #c2410c; color: white",
"Low Priority — Manual Review Likely": "background-color: #b91c1c; color: white",
        }
        color = colors.get(row["tier"], "")
        return [color] * len(row)

    styled = scored.style.apply(_tier_row_color, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.download_button(
        "Download scored leads as CSV",
        data=scored.to_csv(index=False),
        file_name="scored_leads.csv",
        mime="text/csv",
    )


def _render_about_tab() -> None:
    st.markdown("#### Why a rubric, not a black-box model?")
    st.write(
        "For an underwriting-adjacent use case, a sales rep or underwriter needs to see "
        "*why* a lead scored the way it did — a black-box ML classifier can't explain "
        "itself the way a transparent, weighted rubric can. Each factor below is visible "
        "in the score breakdown for every lead."
    )
    st.markdown("#### The five scoring factors (0-100 total)")
    st.markdown(
        "- **Policy Value Fit (0-25):** how valuable/complex the requested product is "
        "(Comprehensive Corporate > Fleet Commercial > Individual Basic).\n"
        "- **Coverage/Budget Fit (0-20):** does the stated monthly budget realistically "
        "support the requested coverage, using an industry rule-of-thumb premium rate "
        "(~1.5% of coverage annually)? A mismatch flags a budget conversation before quoting.\n"
        "- **Urgency/Timeline (0-20):** how soon the applicant wants to decide.\n"
        "- **Risk Profile (0-20):** prior claims count, applicant age band, and occupation "
        "risk level — fewer/lower risk factors score higher.\n"
        "- **Engagement/Channel (0-15):** referrals and broker partners tend to convert "
        "better than cold outreach, so channel quality contributes to the score."
    )
    st.markdown("#### Tiers")
    st.markdown(
        "- **80-100 — Hot Lead:** fast-track to underwriting.\n"
        "- **60-79 — Qualified:** standard underwriting process.\n"
        "- **40-59 — Nurture:** needs more information before proceeding.\n"
        "- **Below 40 — Low Priority:** likely needs a budget/coverage conversation or manual review."
    )
    st.markdown("#### Known limitations")
    st.markdown(
        "- The budget-fit check uses a **rough industry rule-of-thumb premium rate**, not a "
        "real underwriting quote — actual premiums vary by insurer, region, and applicant "
        "specifics.\n"
        "- This is a **lead prioritization tool**, not a final underwriting decision — every "
        "lead should still go through proper underwriting review regardless of score.\n"
        "- The rubric weights were set based on reasonable sales/underwriting judgment for "
        "this exercise, not fitted to real historical conversion data — a production version "
        "would validate/tune these weights against actual close rates."
    )
