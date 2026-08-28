"""Streamlit UI for Insurance Lead Qualifier Commercialization (Ali Zaib - Week 6)."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.engine import (
    PRICING_TIERS,
    calculate_client_roi,
    export_outreach_excel_bytes,
    generate_cold_outreach_sequence,
    load_outreach_data,
    save_outreach_data,
)


def render_ui() -> None:
    """Render the Insurance Lead Qualifier Commercialization Hub."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem; border-left: 5px solid #0d9488;">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800;">🛡️ Insurance Lead Scoring — Commercialization Hub</h2>
            <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                <b>Week 6: Sell Your Skills</b> · Ali Zaib · Turning the Week 5 Insurance & Finance Lead Qualifier
                into a sellable service offering for insurance agencies and brokers (USA, UK, Canada).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_pricing, tab_emails, tab_tracker, tab_social = st.tabs([
        "💎 Service Offering & Pricing",
        "✉️ Cold Outreach Generator",
        "📋 Outreach Pipeline",
        "📱 Social Media Marketing",
    ])

    with tab_pricing:
        _render_pricing_tab()
    with tab_emails:
        _render_outreach_generator_tab()
    with tab_tracker:
        _render_pipeline_tab()
    with tab_social:
        _render_social_tab()


def _render_pricing_tab() -> None:
    st.subheader("📦 Productized Service Packages & Tiered Pricing")
    st.info(
        "👉 *'We deploy a transparent, five-factor AI lead qualification service for insurance "
        "agencies and brokers that scores and prioritizes policy applicants instantly — cutting "
        "manual review time while keeping every decision explainable for underwriting.'*"
    )

    cols = st.columns(3)
    tier_styles = [
        ("#ffffff", "#dce3ec", "#e2e8f0", "#334155", "STARTER"),
        ("#f0fdfa", "#0d9488", "#0d9488", "#ffffff", "MOST POPULAR"),
        ("#ffffff", "#dce3ec", "#fef3c7", "#b45309", "ENTERPRISE"),
    ]
    for col, (name, tier), (bg, border, badge_bg, badge_color, badge_label) in zip(cols, PRICING_TIERS.items(), tier_styles):
        with col:
            features_html = "".join(f"<li>{f}</li>" for f in tier["features"])
            st.markdown(
                f"""
                <div style="background: {bg}; border: {'2px' if 'MOST' in badge_label else '1px'} solid {border}; border-radius: 10px; padding: 1.25rem; height: 100%;">
                    <span style="background: {badge_bg}; color: {badge_color}; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 99px;">{badge_label}</span>
                    <h3 style="margin: 0.5rem 0 0 0; font-size: 1.5rem; color: #0f172a;">{name}</h3>
                    <h4 style="margin: 0.25rem 0 0 0; font-size: 1.3rem; color: #0d9488;">${tier['monthly_fee']} <span style="font-size: 0.8rem; color: #64748b;">/ month</span></h4>
                    <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 1rem 0;">+ ${tier['setup_fee']} One-Time Setup Fee</p>
                    <p style="font-size: 0.85rem; color: #334155;"><b>{tier['lead_limit']}</b></p>
                    <p style="font-size: 0.8rem; color: #64748b;">{tier['channels']}</p>
                    <hr style="margin: 0.5rem 0 1rem 0;"/>
                    <ul style="font-size: 0.85rem; color: #334155; padding-left: 1.2rem; line-height: 1.6;">{features_html}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    st.subheader("🧮 Interactive Client Savings & ROI Modeler")
    st.write("Use this calculator live on discovery calls to quantify a prospective agency's exact monthly ROI.")

    c1, c2, c3, c4 = st.columns(4)
    monthly_leads = c1.number_input("Leads reviewed / month", min_value=10, max_value=5000, value=200, step=10)
    reviewer_rate = c2.number_input("Reviewer hourly rate ($)", min_value=10.0, max_value=200.0, value=35.0, step=5.0)
    review_time = c3.number_input("Manual review time / lead (min)", min_value=1.0, max_value=60.0, value=12.0, step=1.0)
    tier_choice = c4.selectbox("Pricing tier", list(PRICING_TIERS.keys()), index=1)

    if st.button("Calculate ROI", type="primary"):
        roi = calculate_client_roi(int(monthly_leads), reviewer_rate, review_time, tier_choice)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Hours Saved / mo", roi["hours_saved_monthly"])
        m2.metric("Manual Cost / mo", f"${roi['manual_cost_monthly']:,.0f}")
        m3.metric("Net Savings / mo", f"${roi['net_monthly_savings']:,.0f}")
        m4.metric("ROI", f"{roi['roi_percentage']:.0f}%")
        st.success(
            f"At {roi['monthly_leads']} leads/month, automating first-pass qualification saves "
            f"an estimated **${roi['annual_net_savings']:,.0f}/year** after subscription and setup costs "
            f"on the {roi['tier_name']} tier."
        )


def _render_outreach_generator_tab() -> None:
    st.subheader("✉️ Personalized Cold Outreach Sequence Generator")
    st.write("Generate a 3-step email sequence tailored to a specific insurance agency or brokerage prospect.")

    with st.form("outreach_gen_form"):
        c1, c2 = st.columns(2)
        prospect_name = c1.text_input("Prospect Contact Name", value="Sarah")
        agency_name = c2.text_input("Agency/Brokerage Name", value="Meridian Insurance Group")
        c3, c4 = st.columns(2)
        region = c3.selectbox("Target Region", ["USA", "UK", "Canada"])
        demo_link = c4.text_input("Live Demo Link", value="https://insurance-lead-qualifier.streamlit.app")
        observation = st.text_area(
            "Personalized observation (optional)",
            placeholder="e.g. I noticed your agency handles a high volume of commercial fleet applications...",
        )
        generate_clicked = st.form_submit_button("Generate Sequence", type="primary")

    if generate_clicked:
        sequence = generate_cold_outreach_sequence(prospect_name, agency_name, region, observation, demo_link)
        for step in [1, 2, 3]:
            with st.expander(f"Step {step}: {sequence[f'step_{step}_subject']}", expanded=(step == 1)):
                st.text_area(f"Step {step} body", value=sequence[f"step_{step}_body"], height=200, key=f"step_{step}_body_area")


def _render_pipeline_tab() -> None:
    st.subheader("📋 Live Outreach Pipeline")
    st.caption(
        "Tracks practice outreach for this module's own service pitch. Stored locally within this "
        "module's own data folder (not the shared team tracker) to avoid overwriting teammates' data."
    )

    leads = load_outreach_data()
    if leads:
        df = pd.DataFrame(leads)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Outreach Pipeline (Excel)",
            data=export_outreach_excel_bytes(),
            file_name="insurance_outreach_pipeline.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("No outreach entries yet — add one below.")

    with st.expander("➕ Add New Prospective Agency to Pipeline"):
        with st.form("add_lead_form"):
            c1, c2, c3 = st.columns(3)
            nl_agency = c1.text_input("Agency Name")
            nl_region = c2.selectbox("Region", ["USA", "UK", "Canada"])
            nl_web = c3.text_input("Website URL", value="https://")

            c4, c5, c6 = st.columns(3)
            nl_contact = c4.text_input("Contact Person & Title")
            nl_method = c5.selectbox("Contact Method", ["Cold Email", "LinkedIn Direct Message", "Broker Referral", "Contact Form"])
            nl_date = c6.date_input("Date Contacted")

            c7, c8 = st.columns(2)
            nl_resp = c7.selectbox("Response State", ["Awaiting Reply", "Replied - Interested", "Replied - Not Interested", "Replied - Requesting Demo"])
            nl_stat = c8.selectbox("Current Status", ["Initial Outreach", "Follow-up Sent", "Demo Link Shared", "Discovery Call Booked", "Proposal Sent", "Closed Won", "Closed Lost"])

            if st.form_submit_button("Save to Pipeline"):
                new_entry = {
                    "agency_name": nl_agency,
                    "region": nl_region,
                    "website": nl_web,
                    "contact_person": nl_contact,
                    "contact_method": nl_method,
                    "date_contacted": str(nl_date),
                    "service_offered": "Insurance Lead Qualifier (Broker Starter/Agency Pro/Enterprise)",
                    "response": nl_resp,
                    "followup_date": str(pd.Timestamp(nl_date) + pd.Timedelta(days=5)),
                    "result_status": nl_stat,
                }
                leads.append(new_entry)
                save_outreach_data(leads)
                st.success(f"✅ Added {nl_agency} to outreach pipeline.")
                st.rerun()


def _render_social_tab() -> None:
    st.subheader("📱 Social Media Campaign Assets")
    st.caption("Copy-and-paste assets for LinkedIn showcasing the insurance lead qualification service.")

    p1, p2 = st.tabs(["💼 LinkedIn Showcase Post", "🎬 60-Second Video Reel Script"])

    with p1:
        li_post = (
            "🚀 Excited to share my latest build from the SafeX Solutions AI/ML Internship!\n\n"
            "I designed and deployed a transparent AI Lead Qualification tool specifically for "
            "insurance agencies and brokers.\n\n"
            "💡 The Problem: Sales teams and underwriters manually review every incoming policy "
            "lead with no consistent prioritization — hot leads and poor-fit leads sit in the same queue.\n"
            "⚡ The Solution: A five-factor weighted scoring engine (policy value, budget fit, "
            "urgency, risk profile, engagement channel) that ranks leads instantly — with every "
            "score fully explainable, not a black box.\n\n"
            "🛠️ Key Features:\n"
            "• Single-lead and batch CSV scoring\n"
            "• Automatic risk/budget-mismatch flagging for underwriting review\n"
            "• Hot/Qualified/Nurture/Low Priority tiering\n\n"
            "🔗 Try the live demo: https://insurance-lead-qualifier.streamlit.app\n\n"
            "#SafeXSolutions #AI #InsurTech #MachineLearning #Automation #Python #Streamlit"
        )
        st.text_area("LinkedIn Post Content (Ready to Copy):", value=li_post, height=280)

    with p2:
        reel_script = (
            "🎬 [0:00-0:05] HOOK:\n"
            "\"Here's how this AI tool scores insurance leads in under a second...\"\n\n"
            "🎬 [0:05-0:20] PROBLEM & DEMO:\n"
            "\"Instead of manually reviewing every applicant, this scores five factors instantly — "
            "watch, I submit a high-value corporate applicant and it flags as a Hot Lead immediately.\"\n\n"
            "🎬 [0:20-0:40] TRANSPARENCY:\n"
            "\"Every score breaks down so underwriters see exactly why — no black box. And if the "
            "budget doesn't match the coverage requested, it flags that specifically.\"\n\n"
            "🎬 [0:40-0:55] CTA:\n"
            "\"Built during my SafeX Solutions AI/ML internship. Live demo link in my bio!\""
        )
        st.text_area("Video Reel Script:", value=reel_script, height=240)
