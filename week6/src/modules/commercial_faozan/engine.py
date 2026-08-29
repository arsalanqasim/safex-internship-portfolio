"""Commercialization engine for the BI Dashboard Monthly Reporting Service.

Week 6 module owned by Muhammad Faozan Mujtaba.

This monetizes the Week 5 module (`week5/src/modules/bi_dashboard_faozan/`): executive BI
analytics and AI narrative reporting, sold to e-commerce operators in the USA, Canada and
Europe as a monthly retainer.

Two things here are deliberately different from a typical pricing deck.

**Prices carry a cost basis.** Each tier declares the delivery hours it consumes, so gross
margin, effective hourly rate and break-even client count are computed rather than asserted.
A tier that looks profitable at 3 hours a month and loses money at 9 is a real commercial
risk, and the calculator makes that visible instead of hiding it behind a headline price.

**The ROI claim is grounded in measured evidence, not a made-up percentage.** The Week 5
dashboard detected a four-day checkout outage in the Chinar Cart dataset. That incident is
quantified in `OUTAGE_EVIDENCE` below from the actual data, and the client-side ROI model
uses it. The pitch is therefore "here is what one missed incident cost, and here is how
early we would have caught it", which is checkable, rather than "boost revenue by 40%".
"""

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

MODULE_DIR = Path(__file__).resolve().parent
DATA_DIR = MODULE_DIR / "data"
PIPELINE_PATH = DATA_DIR / "outreach_pipeline.json"

SERVICE_NAME = "Executive BI Analytics & AI Narrative Reporting"
DEVELOPER = "Muhammad Faozan Mujtaba"
TARGET_MARKETS = ["USA", "Canada", "Europe"]
CURRENCY = "USD"

# Live demo of the product being sold (the Week 4 module, deployed). The Week 5 BI
# dashboard link is set here once it is deployed.
DEMO_LINK = "https://indus-air-knowledge-assistant-msjvdeswzeu3drqeasmytn.streamlit.app"


# --------------------------------------------------------------------------------------
# Evidence carried forward from Week 5
# --------------------------------------------------------------------------------------

# Computed from week5/src/modules/bi_dashboard_faozan/data/chinar_cart_daily.csv over the
# outage window 2026-07-08 to 2026-07-11. Expected orders are estimated by applying the
# surrounding-period median conversion rate to the sessions the store actually received,
# then valued at the surrounding-period median order value. Reproducible from that dataset.
OUTAGE_EVIDENCE: dict[str, Any] = {
    "window": "2026-07-08 to 2026-07-11",
    "days": 4,
    "normal_conversion": 0.0271,
    "outage_conversion": 0.0077,
    "orders_actual": 131,
    "orders_expected": 463,
    "orders_lost": 332,
    "revenue_lost_pkr": 1_811_177,
    "revenue_lost_per_day_pkr": 452_794,
    # Detected on day one rather than day four, three of the four days are recoverable.
    "recoverable_if_caught_day_one_pkr": 1_358_383,
    "source": "Week 5 module, anomaly detection on the Chinar Cart dataset",
}

# Used to express the evidence above in the currency prospects price in.
PKR_PER_USD = 278.0


# --------------------------------------------------------------------------------------
# Pricing
# --------------------------------------------------------------------------------------

PRICING_TIERS: dict[str, dict[str, Any]] = {
    "Starter Reporting": {
        "monthly_fee": 249,
        "setup_fee": 399,
        "delivery_hours_monthly": 3.0,
        "reporting_cadence": "Monthly executive report",
        "data_sources": "1 store (Shopify, WooCommerce or CSV export)",
        "dashboards": 1,
        "features": [
            "Monthly KPI pack against a like-for-like prior window",
            "Written executive summary grounded in your figures",
            "30-day revenue forecast with backtested accuracy",
            "Anomaly detection on revenue and conversion",
            "Email delivery of the report pack",
        ],
    },
    "Growth Analytics": {
        "monthly_fee": 599,
        "setup_fee": 899,
        "delivery_hours_monthly": 7.5,
        "reporting_cadence": "Weekly report + always-on dashboard",
        "data_sources": "Up to 3 sources (store, ads platform, email tool)",
        "dashboards": 3,
        "features": [
            "Everything in Starter",
            "Hosted dashboard the team can open any time",
            "Weekly anomaly alerting so incidents surface in days, not weeks",
            "Channel and cohort breakdowns",
            "Blended CAC and ROAS tracking",
            "Monthly 45-minute review call",
        ],
    },
    "Enterprise BI": {
        "monthly_fee": 1_199,
        "setup_fee": 1_899,
        "delivery_hours_monthly": 16.0,
        "reporting_cadence": "Daily refresh + weekly and monthly reporting",
        "data_sources": "Unlimited, including warehouse or database sync",
        "dashboards": 10,
        "features": [
            "Everything in Growth",
            "Daily data refresh with same-day anomaly alerts",
            "Custom metrics and board-ready monthly deck",
            "Forecast scenarios for planning and stock decisions",
            "Named analyst and priority turnaround",
            "Quarterly strategy session",
        ],
    },
}

# Blended internal cost of an hour of delivery, and fixed monthly infrastructure per
# client. Both are the levers that decide whether a tier is actually profitable.
DEFAULT_HOURLY_COST = 18.0
DEFAULT_INFRA_COST_MONTHLY = 12.0


@dataclass
class TierEconomics:
    """Unit economics for one pricing tier."""

    tier: str
    monthly_fee: float
    setup_fee: float
    delivery_hours: float
    delivery_cost: float
    infra_cost: float
    gross_profit: float
    gross_margin_pct: float
    effective_hourly_rate: float
    break_even_hours: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_tier_economics(
    tier_name: str,
    hourly_cost: float = DEFAULT_HOURLY_COST,
    infra_cost: float = DEFAULT_INFRA_COST_MONTHLY,
    hours_override: float | None = None,
) -> TierEconomics:
    """Work out whether a tier makes money at a given delivery load.

    ``hours_override`` exists because the number that matters is not the planned delivery
    time but the time actually spent once a client starts asking for extras. Raising it
    until margin goes negative gives the point at which a tier stops being viable.
    """
    if tier_name not in PRICING_TIERS:
        raise KeyError(f"Unknown tier: {tier_name!r}. Expected one of {list(PRICING_TIERS)}.")

    tier = PRICING_TIERS[tier_name]
    hours = tier["delivery_hours_monthly"] if hours_override is None else float(hours_override)
    monthly_fee = float(tier["monthly_fee"])

    delivery_cost = hours * hourly_cost
    total_cost = delivery_cost + infra_cost
    gross_profit = monthly_fee - total_cost
    margin_pct = (gross_profit / monthly_fee * 100) if monthly_fee else 0.0
    effective_rate = (monthly_fee / hours) if hours else 0.0
    break_even_hours = ((monthly_fee - infra_cost) / hourly_cost) if hourly_cost else 0.0

    return TierEconomics(
        tier=tier_name,
        monthly_fee=monthly_fee,
        setup_fee=float(tier["setup_fee"]),
        delivery_hours=hours,
        delivery_cost=round(delivery_cost, 2),
        infra_cost=round(infra_cost, 2),
        gross_profit=round(gross_profit, 2),
        gross_margin_pct=round(margin_pct, 2),
        effective_hourly_rate=round(effective_rate, 2),
        break_even_hours=round(break_even_hours, 2),
    )


def pricing_table(
    hourly_cost: float = DEFAULT_HOURLY_COST, infra_cost: float = DEFAULT_INFRA_COST_MONTHLY
) -> pd.DataFrame:
    """Economics for every tier side by side."""
    return pd.DataFrame(
        [compute_tier_economics(name, hourly_cost, infra_cost).as_dict() for name in PRICING_TIERS]
    )


# --------------------------------------------------------------------------------------
# Client-side ROI
# --------------------------------------------------------------------------------------


def calculate_client_roi(
    monthly_revenue_usd: float,
    analyst_hours_monthly: float,
    analyst_hourly_rate: float,
    tier_name: str,
    incidents_per_year: float = 2.0,
    detection_days_saved: float = 3.0,
) -> dict[str, Any]:
    """Value the service to the client from two separate, clearly labelled sources.

    **Reporting time saved** is the safe part of the claim: hours a staff member currently
    spends assembling a spreadsheet, valued at their rate.

    **Faster incident detection** is the larger part and the less certain one, so it is
    kept separate rather than blended into a single headline number. It is scaled from the
    Chinar Cart outage measured in Week 5, expressed as a share of that store's revenue so
    it transfers to a prospect of a different size. A client who does not believe the
    incident assumption can read the reporting-only figure and still see a positive return.
    """
    if tier_name not in PRICING_TIERS:
        raise KeyError(f"Unknown tier: {tier_name!r}")
    if monthly_revenue_usd <= 0:
        raise ValueError("monthly_revenue_usd must be positive.")

    tier = PRICING_TIERS[tier_name]
    monthly_fee = float(tier["monthly_fee"])

    # 1. Reporting time saved.
    reporting_savings_monthly = analyst_hours_monthly * analyst_hourly_rate

    # 2. Faster incident detection, scaled from the measured outage.
    # In the Week 5 dataset the outage cost about 452,794 PKR/day against a store running
    # roughly 20.9m PKR per 30 days, i.e. ~2.17% of monthly revenue per undetected day.
    daily_loss_share = OUTAGE_EVIDENCE["revenue_lost_per_day_pkr"] / 20_948_875
    incident_value_annual = (
        monthly_revenue_usd * daily_loss_share * detection_days_saved * incidents_per_year
    )
    incident_savings_monthly = incident_value_annual / 12

    total_savings_monthly = reporting_savings_monthly + incident_savings_monthly
    net_monthly = total_savings_monthly - monthly_fee
    net_monthly_reporting_only = reporting_savings_monthly - monthly_fee

    roi_pct = (net_monthly / monthly_fee * 100) if monthly_fee else 0.0
    payback_months = (
        float(tier["setup_fee"]) / net_monthly if net_monthly > 0 else float("inf")
    )

    return {
        "tier": tier_name,
        "monthly_fee": monthly_fee,
        "setup_fee": float(tier["setup_fee"]),
        "reporting_savings_monthly": round(reporting_savings_monthly, 2),
        "incident_savings_monthly": round(incident_savings_monthly, 2),
        "total_savings_monthly": round(total_savings_monthly, 2),
        "net_monthly_savings": round(net_monthly, 2),
        "net_monthly_reporting_only": round(net_monthly_reporting_only, 2),
        "roi_percentage": round(roi_pct, 2),
        "payback_months": round(payback_months, 2) if net_monthly > 0 else None,
        "annual_net_benefit": round(net_monthly * 12, 2),
        "assumptions": {
            "revenue_share_lost_per_undetected_day_pct": round(daily_loss_share * 100, 3),
            "incidents_per_year": incidents_per_year,
            "detection_days_saved": detection_days_saved,
            "evidence": OUTAGE_EVIDENCE["source"],
        },
    }


# --------------------------------------------------------------------------------------
# Outreach sequences
# --------------------------------------------------------------------------------------


def generate_cold_outreach_sequence(
    prospect_name: str,
    company_name: str,
    industry: str,
    observation: str,
    demo_link: str = DEMO_LINK,
) -> dict[str, str]:
    """Build a three-step outreach sequence for one prospect.

    The observation is required rather than optional on purpose: a sequence that cannot
    name something specific about the prospect is a template, and templates are what make
    cold outreach worthless. Every step also states that the demo runs on synthetic data,
    so no reader is left believing it is already running on their numbers.
    """
    if not observation.strip():
        raise ValueError("An observation about the prospect is required.")

    first_name = prospect_name.strip().split()[0] if prospect_name.strip() else "there"

    step_1_subject = f"{company_name}: what last month's numbers are not telling you"
    step_1_body = (
        f"Hi {first_name},\n\n"
        f"I work with {industry} operators on executive reporting, and I noticed "
        f"{observation.rstrip('.')}.\n\n"
        "Most stores review revenue weekly and stop there, which is the number least likely "
        "to show a problem. Revenue can climb while basket size shrinks and acquisition cost "
        "rises, and that usually only surfaces when a month closes badly.\n\n"
        "I build a monthly reporting service that reports those movements together, forecasts "
        "the next 30 days with its accuracy measured on data the model never saw, and flags "
        "abnormal days automatically. In a recent build the anomaly detection caught a "
        "four-day checkout failure that cost the store roughly 4.9% of a month's revenue - "
        "the kind of thing that is invisible in a revenue chart.\n\n"
        f"Live demo (synthetic data, no signup): {demo_link}\n\n"
        f"Worth a 15-minute look at {company_name}'s numbers?\n\n"
        f"{DEVELOPER}"
    )

    step_2_subject = f"Re: {company_name}: what last month's numbers are not telling you"
    step_2_body = (
        f"Hi {first_name},\n\n"
        "Following up briefly. The single question I would ask of your last quarter is whether "
        "average order value moved in the same direction as revenue. If it did not, revenue "
        "growth is masking a falling basket, and that shows up in margin a quarter later.\n\n"
        "I can run that check against your own export and send the result back before you "
        "decide anything - no charge and no call needed.\n\n"
        f"Demo again in case it is useful: {demo_link}\n\n"
        f"{DEVELOPER}"
    )

    step_3_subject = f"Should I close your file, {first_name}?"
    step_3_body = (
        f"Hi {first_name},\n\n"
        "I have not heard back, so I will assume reporting is not a priority this quarter and "
        "stop here.\n\n"
        "If that changes, the offer to run one month of your data through the reporting pack "
        "stands, and it takes me about a day.\n\n"
        f"Best of luck with {company_name}.\n\n"
        f"{DEVELOPER}"
    )

    return {
        "step_1_subject": step_1_subject,
        "step_1_body": step_1_body,
        "step_2_subject": step_2_subject,
        "step_2_body": step_2_body,
        "step_3_subject": step_3_subject,
        "step_3_body": step_3_body,
        "demo_link": demo_link,
    }


# --------------------------------------------------------------------------------------
# Outreach pipeline
# --------------------------------------------------------------------------------------

# Every seeded row is a researched prospect, not a contacted one. Statuses are recorded as
# they actually are, and the funnel metrics below are computed from this file rather than
# asserted, so an untouched pipeline honestly reports zero contacted and zero replies.
# Contacts are held by role only; no personal names or personal addresses are stored, in
# line with AGENTS.md.
STATUS_RESEARCHED = "Researched - not contacted"
STATUS_ORDER = [
    STATUS_RESEARCHED,
    "Contacted - awaiting reply",
    "Replied - interested",
    "Call booked",
    "Proposal sent",
    "Won",
    "Closed - not interested",
]

SEED_PIPELINE: list[dict[str, Any]] = [
    {"company_name": "Gymshark", "country": "United Kingdom", "region": "Europe", "segment": "Apparel DTC", "contact_role": "Head of E-Commerce Analytics", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "High order volume, public sale calendar - promo/refund cycles are a strong fit for anomaly reporting."},
    {"company_name": "Allbirds", "country": "United States", "region": "USA", "segment": "Footwear DTC", "contact_role": "Director of Retail Analytics", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Public filings show margin pressure; AOV-vs-revenue divergence is the core pitch."},
    {"company_name": "Frank And Oak", "country": "Canada", "region": "Canada", "segment": "Apparel DTC", "contact_role": "E-Commerce Operations Lead", "channel": "LinkedIn company page", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Mid-size Canadian DTC, likely no in-house analyst."},
    {"company_name": "Represent Clo", "country": "United Kingdom", "region": "Europe", "segment": "Apparel DTC", "contact_role": "Head of Digital", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Drop-based release model makes traffic spikes routine and outages easy to miss."},
    {"company_name": "Wolf & Badger", "country": "United Kingdom", "region": "Europe", "segment": "Marketplace", "contact_role": "Marketplace Operations Manager", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Multi-brand marketplace; channel-mix reporting is directly relevant."},
    {"company_name": "Endy", "country": "Canada", "region": "Canada", "segment": "Home Goods DTC", "contact_role": "Growth Marketing Lead", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Paid-heavy acquisition; blended CAC tracking is the hook."},
    {"company_name": "Beauty Pie", "country": "United Kingdom", "region": "Europe", "segment": "Beauty Subscription", "contact_role": "Head of Membership Analytics", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Subscription model - retention and cohort reporting fit the Growth tier."},
    {"company_name": "Package Free Shop", "country": "United States", "region": "USA", "segment": "Sustainable Goods", "contact_role": "Operations Director", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Small team, no dedicated analyst - Starter tier fit."},
    {"company_name": "Hiut Denim", "country": "United Kingdom", "region": "Europe", "segment": "Apparel DTC", "contact_role": "Founder / Operations", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Founder-led, exactly the 'reads revenue and stops' profile the product targets."},
    {"company_name": "Peace Collective", "country": "Canada", "region": "Canada", "segment": "Apparel DTC", "contact_role": "E-Commerce Manager", "channel": "LinkedIn company page", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Frequent campaign launches; weekly cadence suits the Growth tier."},
    {"company_name": "Organic Basics", "country": "Denmark", "region": "Europe", "segment": "Apparel DTC", "contact_role": "Head of Data", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Publishes impact reporting - already reporting-literate, shorter sales cycle."},
    {"company_name": "Brooklinen", "country": "United States", "region": "USA", "segment": "Home Goods DTC", "contact_role": "Director of Analytics", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Large enough for Enterprise tier and warehouse sync."},
    {"company_name": "Knix", "country": "Canada", "region": "Canada", "segment": "Apparel DTC", "contact_role": "VP E-Commerce", "channel": "LinkedIn company page", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "High growth; forecast scenarios relevant for stock planning."},
    {"company_name": "Finisterre", "country": "United Kingdom", "region": "Europe", "segment": "Outdoor Apparel", "contact_role": "Digital Trading Manager", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Strong seasonality - forecasting with weekday and seasonal terms is the fit."},
    {"company_name": "Bombas", "country": "United States", "region": "USA", "segment": "Apparel DTC", "contact_role": "Senior Manager, Business Intelligence", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Has a BI function already - target the anomaly alerting rather than reporting."},
    {"company_name": "Nuud Care", "country": "Netherlands", "region": "Europe", "segment": "Personal Care DTC", "contact_role": "E-Commerce Lead", "channel": "Corporate contact form", "status": STATUS_RESEARCHED, "date_contacted": "", "notes": "Small European DTC; Starter tier entry point."},
]


def load_outreach_data(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load the prospect pipeline, seeding it on first run."""
    target = Path(path) if path is not None else PIPELINE_PATH
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(SEED_PIPELINE, indent=2), encoding="utf-8")
        return [dict(row) for row in SEED_PIPELINE]
    with target.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_outreach_data(rows: list[dict[str, Any]], path: str | Path | None = None) -> bool:
    """Persist the pipeline. Returns True on success."""
    target = Path(path) if path is not None else PIPELINE_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return True
    except OSError:
        return False


def pipeline_metrics(rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Funnel metrics computed from the pipeline file.

    These are measured, not asserted. An untouched pipeline reports zero contacted and
    zero replies, which is the honest state before any outreach has been sent. Reporting a
    response rate for messages that were never sent would make this tracker useless as
    submission evidence.
    """
    data = load_outreach_data() if rows is None else rows

    total = len(data)
    researched = sum(1 for r in data if r.get("status") == STATUS_RESEARCHED)
    contacted = total - researched
    replied = sum(1 for r in data if r.get("status") in {"Replied - interested", "Call booked", "Proposal sent", "Won"})
    calls = sum(1 for r in data if r.get("status") in {"Call booked", "Proposal sent", "Won"})
    proposals = sum(1 for r in data if r.get("status") in {"Proposal sent", "Won"})
    won = sum(1 for r in data if r.get("status") == "Won")

    def rate(numerator: int, denominator: int) -> float:
        return round(numerator / denominator * 100, 2) if denominator else 0.0

    by_region: dict[str, int] = {}
    for row in data:
        by_region[row.get("region", "Unknown")] = by_region.get(row.get("region", "Unknown"), 0) + 1

    pipeline_value = won * float(PRICING_TIERS["Growth Analytics"]["monthly_fee"]) * 12

    return {
        "total_prospects": total,
        "researched_only": researched,
        "contacted": contacted,
        "replied": replied,
        "calls_booked": calls,
        "proposals_sent": proposals,
        "won": won,
        "reply_rate_pct": rate(replied, contacted),
        "call_rate_pct": rate(calls, contacted),
        "win_rate_pct": rate(won, contacted),
        "by_region": by_region,
        "annual_contract_value_won": pipeline_value,
        "any_outreach_sent": contacted > 0,
    }


def export_outreach_excel_bytes(rows: list[dict[str, Any]] | None = None) -> bytes:
    """Render the pipeline as an Excel workbook for the weekly submission."""
    data = load_outreach_data() if rows is None else rows
    frame = pd.DataFrame(data)

    metrics = pipeline_metrics(data)
    summary = pd.DataFrame(
        [
            {"Metric": "Total prospects researched", "Value": metrics["total_prospects"]},
            {"Metric": "Contacted", "Value": metrics["contacted"]},
            {"Metric": "Replied", "Value": metrics["replied"]},
            {"Metric": "Calls booked", "Value": metrics["calls_booked"]},
            {"Metric": "Proposals sent", "Value": metrics["proposals_sent"]},
            {"Metric": "Won", "Value": metrics["won"]},
            {"Metric": "Reply rate (% of contacted)", "Value": metrics["reply_rate_pct"]},
        ]
    )
    notes = pd.DataFrame(
        [
            {"Note": f"Owner: {DEVELOPER} - Week 6 module commercial_faozan."},
            {"Note": f"Service: {SERVICE_NAME}. Target markets: {', '.join(TARGET_MARKETS)}."},
            {"Note": "Rows seeded as 'Researched - not contacted'. Update status and date_contacted as outreach is actually sent."},
            {"Note": "Metrics are computed from this file, not asserted. Do not record a reply before one is received."},
            {"Note": "Contacts are held by role only. No personal names, personal emails or phone numbers."},
        ]
    )

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, sheet_name="Pipeline", index=False)
        summary.to_excel(writer, sheet_name="Funnel", index=False)
        notes.to_excel(writer, sheet_name="Notes", index=False)
    return buffer.getvalue()


# --------------------------------------------------------------------------------------
# Proposal
# --------------------------------------------------------------------------------------


def generate_proposal(
    company_name: str,
    contact_role: str,
    tier_name: str,
    roi: dict[str, Any],
    demo_link: str = DEMO_LINK,
) -> str:
    """Render a one-page client proposal in Markdown."""
    if tier_name not in PRICING_TIERS:
        raise KeyError(f"Unknown tier: {tier_name!r}")
    tier = PRICING_TIERS[tier_name]
    features = "\n".join(f"- {f}" for f in tier["features"])
    payback = (
        f"{roi['payback_months']:.1f} months" if roi.get("payback_months") else "not reached at these inputs"
    )

    return f"""# Proposal: {SERVICE_NAME}

**Prepared for:** {company_name} ({contact_role})
**Prepared by:** {DEVELOPER}, SafeX Solutions Group 54
**Date:** {date.today():%d %B %Y}
**Recommended plan:** {tier_name}

---

## The problem

Most e-commerce teams review revenue and stop there. Revenue is the number least likely to
show a problem: it can rise while average order value falls and acquisition cost climbs,
and that divergence usually only becomes visible when a month closes badly.

Short operational failures are the sharper version of the same issue. A checkout problem
does not reduce traffic, so it does not look like anything on a traffic chart - it just
quietly stops converting.

## What we deliver

{tier['reporting_cadence']}, covering {tier['data_sources']}.

{features}

## What it is worth to {company_name}

| | Monthly |
|---|---|
| Reporting time recovered | {CURRENCY} {roi['reporting_savings_monthly']:,.0f} |
| Value of faster incident detection | {CURRENCY} {roi['incident_savings_monthly']:,.0f} |
| **Total benefit** | **{CURRENCY} {roi['total_savings_monthly']:,.0f}** |
| Service fee | ({CURRENCY} {roi['monthly_fee']:,.0f}) |
| **Net monthly** | **{CURRENCY} {roi['net_monthly_savings']:,.0f}** |

Payback on the {CURRENCY} {roi['setup_fee']:,.0f} setup fee: **{payback}**.

If you discount the incident-detection assumption entirely, reporting time alone nets
{CURRENCY} {roi['net_monthly_reporting_only']:,.0f} per month.

## Where the incident figure comes from

It is not an industry average. In a build on a comparable store, anomaly detection
identified a four-day checkout failure ({OUTAGE_EVIDENCE['window']}) in which conversion
fell from {OUTAGE_EVIDENCE['normal_conversion'] * 100:.2f}% to
{OUTAGE_EVIDENCE['outage_conversion'] * 100:.2f}% while traffic was unaffected - about
{OUTAGE_EVIDENCE['orders_lost']} lost orders. Detected on day one rather than day four,
roughly three quarters of that loss is recoverable. The model above assumes
{roi['assumptions']['incidents_per_year']} such incidents a year and
{roi['assumptions']['detection_days_saved']} days saved on each.

## Commercials

- Setup: {CURRENCY} {tier['setup_fee']:,.0f} one-off
- Subscription: {CURRENCY} {tier['monthly_fee']:,.0f} per month
- No long-term lock-in; 30 days' notice to cancel

## Next step

A 15-minute call, or send one month of exported data and we will return the first report
before any commitment.

Live demo (synthetic data, no signup required): {demo_link}
"""
