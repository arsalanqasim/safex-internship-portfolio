"""Streamlit UI for the BI Dashboard Monthly Reporting Service (Week 6).

Module owned by Muhammad Faozan Mujtaba. Page-level configuration stays in
``week6/src/app.py``; this file exposes a single self-contained ``render_ui()`` and holds
no business logic.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from .engine import (
    CURRENCY,
    DEMO_LINK,
    DEVELOPER,
    OUTAGE_EVIDENCE,
    PRICING_TIERS,
    SERVICE_NAME,
    STATUS_ORDER,
    STATUS_RESEARCHED,
    TARGET_MARKETS,
    calculate_client_roi,
    compute_tier_economics,
    export_outreach_excel_bytes,
    generate_cold_outreach_sequence,
    generate_proposal,
    load_outreach_data,
    pipeline_metrics,
    pricing_table,
    save_outreach_data,
)


def _render_header() -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">💼 Commercialization · Week 6</div>
            <div class="hero-title">BI Dashboard Monthly Reporting Service</div>
            <div class="hero-subtitle">
                {SERVICE_NAME}, sold as a monthly retainer to e-commerce operators in
                {', '.join(TARGET_MARKETS)}. Monetizes the Week 5 BI module.<br>
                Developer: <strong>{DEVELOPER}</strong> (Team Member)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_pricing_tab() -> None:
    st.markdown("#### Service tiers")
    columns = st.columns(len(PRICING_TIERS))
    for column, (name, tier) in zip(columns, PRICING_TIERS.items()):
        with column:
            st.markdown(f"##### {name}")
            st.markdown(f"### {CURRENCY} {tier['monthly_fee']:,}/mo")
            st.caption(f"+ {CURRENCY} {tier['setup_fee']:,} setup · {tier['reporting_cadence']}")
            st.caption(f"**Data sources:** {tier['data_sources']}")
            for feature in tier["features"]:
                st.markdown(f"- {feature}")

    st.divider()
    st.markdown("#### Unit economics")
    st.caption(
        "A price is only a price if you know what it costs to deliver. Each tier declares the "
        "delivery hours it consumes, so margin is computed rather than assumed."
    )

    col_a, col_b = st.columns(2)
    hourly_cost = col_a.slider("Internal delivery cost per hour", 5.0, 60.0, 18.0, 1.0, key="cf_hourly")
    infra_cost = col_b.slider("Infrastructure cost per client per month", 0.0, 100.0, 12.0, 1.0, key="cf_infra")

    table = pricing_table(hourly_cost=hourly_cost, infra_cost=infra_cost)
    display = table[
        ["tier", "monthly_fee", "delivery_hours", "delivery_cost", "gross_profit", "gross_margin_pct", "effective_hourly_rate", "break_even_hours"]
    ].rename(
        columns={
            "tier": "Tier",
            "monthly_fee": f"Fee ({CURRENCY})",
            "delivery_hours": "Hours/mo",
            "delivery_cost": "Delivery cost",
            "gross_profit": "Gross profit",
            "gross_margin_pct": "Margin %",
            "effective_hourly_rate": "Effective rate",
            "break_even_hours": "Break-even hrs",
        }
    )
    st.dataframe(display, width="stretch", hide_index=True)

    st.markdown("##### Margin risk: what happens when delivery overruns")
    st.caption(
        "The number that decides profitability is not the planned delivery time but the time "
        "actually spent once a client starts asking for extras. Raise the hours until margin "
        "goes negative to find where each tier stops being viable."
    )
    tier_name = st.selectbox("Tier", list(PRICING_TIERS), key="cf_risk_tier")
    rows = []
    planned = PRICING_TIERS[tier_name]["delivery_hours_monthly"]
    for multiplier in (1.0, 1.5, 2.0, 2.5, 3.0):
        hours = planned * multiplier
        economics = compute_tier_economics(tier_name, hourly_cost, infra_cost, hours_override=hours)
        rows.append(
            {
                "Delivery hours": f"{hours:.1f} ({multiplier:.1f}x planned)",
                "Gross profit": f"{CURRENCY} {economics.gross_profit:,.2f}",
                "Margin": f"{economics.gross_margin_pct:.1f}%",
                "Effective rate": f"{CURRENCY} {economics.effective_hourly_rate:,.2f}/hr",
                "Viable": "yes" if economics.gross_profit > 0 else "NO",
            }
        )
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def _render_roi_tab() -> dict[str, Any]:
    st.markdown("#### What the service is worth to a client")
    st.caption(
        "Two separate benefits, kept separate on purpose. Reporting time saved is the safe "
        "part of the claim. Faster incident detection is larger but rests on an assumption, so "
        "it is never blended into a single headline number."
    )

    col_a, col_b, col_c = st.columns(3)
    revenue = col_a.number_input(
        f"Client monthly revenue ({CURRENCY})", 10_000, 5_000_000, 250_000, 10_000, key="cf_rev"
    )
    hours = col_b.number_input("Analyst hours/month on reporting", 0.0, 80.0, 12.0, 1.0, key="cf_hours")
    rate = col_c.number_input(f"Analyst hourly rate ({CURRENCY})", 10.0, 200.0, 45.0, 5.0, key="cf_rate")

    col_d, col_e, col_f = st.columns(3)
    tier_name = col_d.selectbox("Plan", list(PRICING_TIERS), index=1, key="cf_roi_tier")
    incidents = col_e.slider("Assumed incidents per year", 0.0, 6.0, 2.0, 0.5, key="cf_incidents")
    days_saved = col_f.slider("Detection days saved per incident", 0.0, 7.0, 3.0, 0.5, key="cf_days")

    roi = calculate_client_roi(
        monthly_revenue_usd=float(revenue),
        analyst_hours_monthly=float(hours),
        analyst_hourly_rate=float(rate),
        tier_name=tier_name,
        incidents_per_year=float(incidents),
        detection_days_saved=float(days_saved),
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total monthly benefit", f"{CURRENCY} {roi['total_savings_monthly']:,.0f}")
    m2.metric("Net of fee", f"{CURRENCY} {roi['net_monthly_savings']:,.0f}")
    m3.metric("ROI", f"{roi['roi_percentage']:,.0f}%")
    m4.metric(
        "Payback on setup",
        f"{roi['payback_months']:.1f} mo" if roi["payback_months"] else "not reached",
    )

    st.markdown("##### Where the benefit comes from")
    st.dataframe(
        pd.DataFrame(
            [
                {"Source": "Reporting time recovered", "Monthly value": f"{CURRENCY} {roi['reporting_savings_monthly']:,.0f}", "Certainty": "High - measured hours x rate"},
                {"Source": "Faster incident detection", "Monthly value": f"{CURRENCY} {roi['incident_savings_monthly']:,.0f}", "Certainty": "Assumption-based - see below"},
            ]
        ),
        width="stretch",
        hide_index=True,
    )

    if roi["net_monthly_reporting_only"] > 0:
        st.success(
            f"Even discounting incident detection entirely, reporting time alone nets "
            f"{CURRENCY} {roi['net_monthly_reporting_only']:,.0f} per month. The case does not "
            "depend on the assumption."
        )
    else:
        st.warning(
            f"On reporting time alone this plan is {CURRENCY} "
            f"{abs(roi['net_monthly_reporting_only']):,.0f} per month short. The case rests "
            "entirely on the incident-detection assumption, which is worth saying out loud to "
            "the client rather than hiding in a total."
        )

    with st.expander("Where the incident figure comes from — measured, not an industry average"):
        st.markdown(
            f"""
The Week 5 BI module's anomaly detection identified a genuine four-day checkout failure in
the Chinar Cart dataset (**{OUTAGE_EVIDENCE['window']}**):

| | |
|---|---|
| Conversion rate, normal | {OUTAGE_EVIDENCE['normal_conversion'] * 100:.2f}% |
| Conversion rate, during outage | {OUTAGE_EVIDENCE['outage_conversion'] * 100:.2f}% |
| Orders received | {OUTAGE_EVIDENCE['orders_actual']} |
| Orders expected at normal conversion | {OUTAGE_EVIDENCE['orders_expected']} |
| **Orders lost** | **{OUTAGE_EVIDENCE['orders_lost']}** |
| **Revenue lost** | **PKR {OUTAGE_EVIDENCE['revenue_lost_pkr']:,}** over {OUTAGE_EVIDENCE['days']} days |
| Recoverable if caught on day 1 | PKR {OUTAGE_EVIDENCE['recoverable_if_caught_day_one_pkr']:,} |

Traffic was unaffected throughout, which is why the incident is invisible on a revenue or
sessions chart and why it ran for four days.

That works out at **{roi['assumptions']['revenue_share_lost_per_undetected_day_pct']:.2f}% of
monthly revenue per undetected day**, which is the figure scaled to the prospect above.
Source: {roi['assumptions']['evidence']}.
            """
        )

    return roi


def _render_outreach_tab() -> None:
    rows = load_outreach_data()
    metrics = pipeline_metrics(rows)

    st.markdown("#### Prospect pipeline")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Prospects researched", metrics["total_prospects"])
    m2.metric("Contacted", metrics["contacted"])
    m3.metric("Replied", metrics["replied"])
    m4.metric("Calls booked", metrics["calls_booked"])

    if not metrics["any_outreach_sent"]:
        st.info(
            "Nothing has been sent yet, so the funnel rates below are zero rather than "
            "estimated. These metrics are computed from the pipeline file, not asserted - "
            "recording a reply before one arrives would make this tracker useless as "
            "submission evidence. Update a row's status as each message actually goes out."
        )

    st.caption(
        f"Regional split: " + " · ".join(f"{k}: {v}" for k, v in metrics["by_region"].items())
    )

    edited = st.data_editor(
        pd.DataFrame(rows),
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "status": st.column_config.SelectboxColumn("status", options=STATUS_ORDER, required=True),
            "notes": st.column_config.TextColumn("notes", width="large"),
        },
        key="cf_pipeline_editor",
    )

    col_a, col_b = st.columns(2)
    if col_a.button("Save pipeline", type="primary", key="cf_save"):
        if save_outreach_data(edited.to_dict(orient="records")):
            st.success("Pipeline saved.")
            st.rerun()
        else:
            st.error("Could not write the pipeline file.")

    col_b.download_button(
        "Download pipeline as Excel",
        data=export_outreach_excel_bytes(edited.to_dict(orient="records")),
        file_name="outreach_tracker_faozan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="cf_xlsx",
    )

    st.divider()
    st.markdown("#### Cold outreach sequence generator")
    st.caption(
        "A specific observation about the prospect is required, not optional. A sequence that "
        "cannot name something particular about the company is a template, and templates are "
        "what make cold outreach worthless."
    )

    col_a, col_b = st.columns(2)
    company = col_a.text_input("Company", value="Allbirds", key="cf_company")
    contact = col_b.text_input("Contact (first name or role)", value="Alex", key="cf_contact")
    industry = col_a.text_input("Segment", value="Footwear DTC", key="cf_industry")
    observation = col_b.text_input(
        "Specific observation",
        value="your last two quarterly updates show revenue growing while gross margin fell",
        key="cf_obs",
    )

    if observation.strip():
        sequence = generate_cold_outreach_sequence(contact, company, industry, observation)
        for step in (1, 2, 3):
            with st.expander(f"Step {step}: {sequence[f'step_{step}_subject']}", expanded=(step == 1)):
                st.code(sequence[f"step_{step}_body"], language="text")
    else:
        st.warning("Enter an observation to generate the sequence.")


def _render_proposal_tab(roi: dict[str, Any]) -> None:
    st.markdown("#### One-page client proposal")
    col_a, col_b, col_c = st.columns(3)
    company = col_a.text_input("Client company", value="Allbirds", key="cf_p_company")
    role = col_b.text_input("Recipient role", value="Director of Retail Analytics", key="cf_p_role")
    tier_name = col_c.selectbox("Plan", list(PRICING_TIERS), index=1, key="cf_p_tier")

    proposal = generate_proposal(company, role, tier_name, roi)
    st.download_button(
        "Download proposal (Markdown)",
        data=proposal,
        file_name=f"proposal_{company.lower().replace(' ', '_')}.md",
        mime="text/markdown",
        key="cf_p_download",
    )
    st.markdown("---")
    st.markdown(proposal)


def render_ui() -> None:
    """Entry point called by the shared Week 6 Streamlit shell."""
    _render_header()

    pricing_tab, roi_tab, outreach_tab, proposal_tab = st.tabs(
        ["Service & pricing", "Client ROI", "Outreach pipeline", "Proposal"]
    )

    with pricing_tab:
        _render_pricing_tab()
    with roi_tab:
        roi = _render_roi_tab()
    with outreach_tab:
        _render_outreach_tab()
    with proposal_tab:
        _render_proposal_tab(roi)

    st.divider()
    st.caption(f"Live product demo: {DEMO_LINK}")
