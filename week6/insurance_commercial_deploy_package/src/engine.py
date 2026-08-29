"""Insurance Lead Qualifier Commercialization Engine (Ali Zaib - Week 6).

Turns the Week 5 Insurance & Finance Lead Qualifier into a sellable
service offering: tiered agency pricing, an ROI calculator quantifying
manual-review time saved, a personalized cold outreach sequence
generator for insurance brokers/agencies, and a local outreach pipeline
tracker.

Note on data isolation: this module writes its outreach pipeline to its
OWN data folder only (`commercial_ali_zaib/data/`), not to the shared
`week6/src/data/outreach_tracker.xlsx` used by the Group Leader's own
module — that shared file is fully overwritten (not appended to) on every
save in the leader's engine, so writing to it here would risk clobbering
his tracked outreach data. Keeping this module's persistence scoped to
its own folder avoids that conflict entirely.
"""
from __future__ import annotations

import io
import json
import os
from typing import Any, Dict, List

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
JSON_TRACKER = os.path.join(DATA_DIR, "outreach_tracker.json")
EXCEL_TRACKER = os.path.join(DATA_DIR, "outreach_tracker.xlsx")

# 3-Tier Commercial Pricing Packages for insurance agencies/brokers
PRICING_TIERS: Dict[str, Dict[str, Any]] = {
    "Broker Starter": {
        "monthly_fee": 350,
        "setup_fee": 199,
        "lead_limit": "Up to 200 applicants scored/mo",
        "channels": "Manual CSV Upload",
        "features": [
            "Automated 5-Factor Underwriting Rubric",
            "Single-Lead & Batch CSV Scoring",
            "Tier-Based Lead Prioritization (Hot/Qualified/Nurture/Low)",
            "Standard Business Hours Support",
        ],
    },
    "Agency Pro": {
        "monthly_fee": 800,
        "setup_fee": 399,
        "lead_limit": "Up to 1,000 policy leads scored/mo",
        "channels": "CSV Upload + CRM Webhook Sync",
        "features": [
            "Everything in Broker Starter",
            "CRM Webhook Sync (Salesforce/HubSpot)",
            "Instant Risk Tiering & Flag Alerts",
            "Custom Scoring Weight Calibration",
            "Weekly Lead Quality Health Reports",
        ],
    },
    "Underwriting Enterprise": {
        "monthly_fee": 1600,
        "setup_fee": 799,
        "lead_limit": "Unlimited policy leads scored",
        "channels": "Omnichannel (CRM, API, Broker Portal)",
        "features": [
            "Everything in Agency Pro",
            "Custom Multi-Line Risk Models",
            "Regulatory Audit Compliance Export",
            "Dedicated Underwriting Account Manager",
            "Custom SLA & Priority Support",
        ],
    },
}


def ensure_data_dir() -> None:
    """Ensure this module's own data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


# ==============================================================================
# ROI & Time Savings Calculation Model
# ==============================================================================
def calculate_client_roi(
    monthly_leads: int,
    reviewer_hourly_rate: float,
    manual_review_min: float,
    tier_name: str,
) -> Dict[str, Any]:
    """Calculate financial ROI and reviewer time saved for a prospective
    insurance agency, comparing manual lead review against automated
    qualification at the given pricing tier."""
    tier_info = PRICING_TIERS.get(tier_name, PRICING_TIERS["Agency Pro"])
    monthly_fee = tier_info["monthly_fee"]
    setup_fee = tier_info["setup_fee"]

    # Automated qualification reduces manual review time by an assumed 80%
    # (reviewers still spot-check flagged/hot leads, but no longer manually
    # triage every incoming lead from scratch).
    automation_deflection_rate = 0.80
    hours_saved_monthly = (monthly_leads * manual_review_min * automation_deflection_rate) / 60.0
    manual_cost_monthly = (monthly_leads * manual_review_min / 60.0) * reviewer_hourly_rate
    automated_labor_savings = hours_saved_monthly * reviewer_hourly_rate

    net_monthly_savings = automated_labor_savings - monthly_fee
    annual_net_savings = (net_monthly_savings * 12) - setup_fee
    roi_percentage = (net_monthly_savings / max(1, monthly_fee)) * 100.0

    return {
        "monthly_leads": monthly_leads,
        "manual_review_min": manual_review_min,
        "reviewer_hourly_rate": reviewer_hourly_rate,
        "tier_name": tier_name,
        "tier_monthly_fee": monthly_fee,
        "tier_setup_fee": setup_fee,
        "hours_saved_monthly": round(hours_saved_monthly, 1),
        "manual_cost_monthly": round(manual_cost_monthly, 2),
        "net_monthly_savings": round(net_monthly_savings, 2),
        "annual_net_savings": round(annual_net_savings, 2),
        "roi_percentage": round(roi_percentage, 1),
    }


# ==============================================================================
# Cold Outreach Sequence Generator
# ==============================================================================
def generate_cold_outreach_sequence(
    prospect_name: str, agency_name: str, region: str, observation: str, demo_link: str
) -> Dict[str, str]:
    """Generate a personalized 3-step cold outreach email sequence for an
    insurance agency or brokerage prospect."""
    p_name = prospect_name.strip() or "there"
    a_name = agency_name.strip() or "your agency"
    obs = observation.strip() or (
        "I noticed your team handles a high volume of policy applications "
        "and likely spends significant time manually triaging lead quality."
    )
    link = demo_link.strip() or "https://insurance-lead-qualifier.streamlit.app"

    subject_1 = f"Cutting manual lead review time at {a_name}"
    body_1 = (
        f"Hi {p_name},\n\n"
        f"I came across {a_name} while researching {region} insurance agencies and {obs}\n\n"
        f"I built a transparent, five-factor lead qualification tool that scores incoming "
        f"policy applicants on value, budget fit, urgency, risk profile, and engagement quality "
        f"— sorting them into Hot/Qualified/Nurture/Low Priority tiers instantly, with every "
        f"score fully explainable for your underwriting team.\n\n"
        f"Here's a live interactive demo: {link}\n\n"
        f"Would you be open to a quick 15-minute call to see if this could save your team "
        f"real review time each week?\n\n"
        f"Best regards,\nAli Zaib\nAI/ML Automation Specialist | SafeX Solutions Cohort 2026\n"
        f"Demo: {link}"
    )

    subject_2 = f"Re: Cutting manual lead review time at {a_name}"
    body_2 = (
        f"Hi {p_name},\n\n"
        f"Following up briefly — I know lead triage is a constant background task for a busy "
        f"agency like {a_name}.\n\n"
        f"For an agency processing ~200 leads/month, automating first-pass qualification can "
        f"save dozens of reviewer hours monthly, at a fraction of the cost of that time.\n\n"
        f"You can test the live scoring tool yourself here: {link}\n\n"
        f"Do you have 10 minutes this week for a quick walkthrough?\n\nBest,\nAli"
    )

    subject_3 = f"Permission to close your file for {a_name}?"
    body_3 = (
        f"Hi {p_name},\n\n"
        f"I haven't heard back, so I'll assume automated lead qualification isn't a priority "
        f"for {a_name} right now.\n\n"
        f"I'll close your file for now — if you ever want to cut manual review time, feel free "
        f"to try the live demo anytime at {link}.\n\n"
        f"Wishing {a_name} continued growth!\n\nBest regards,\nAli Zaib"
    )

    return {
        "step_1_subject": subject_1,
        "step_1_body": body_1,
        "step_2_subject": subject_2,
        "step_2_body": body_2,
        "step_3_subject": subject_3,
        "step_3_body": body_3,
    }


# ==============================================================================
# Outreach Pipeline Tracker (scoped to this module's own data folder)
# ==============================================================================
_COLUMN_DISPLAY_NAMES = {
    "agency_name": "Agency Name",
    "region": "Region",
    "website": "Website",
    "contact_person": "Contact Person",
    "contact_method": "Contact Method",
    "date_contacted": "Date Contacted",
    "service_offered": "Service Offered",
    "response": "Response",
    "followup_date": "Follow-up Date",
    "result_status": "Result/Status",
}


def load_outreach_data() -> List[Dict[str, Any]]:
    """Load this module's outreach pipeline data from its own JSON file."""
    ensure_data_dir()
    if os.path.exists(JSON_TRACKER):
        try:
            with open(JSON_TRACKER, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_outreach_data(data: List[Dict[str, Any]]) -> bool:
    """Save this module's outreach pipeline to its own JSON and Excel
    files only — never touches the shared root outreach tracker."""
    ensure_data_dir()
    try:
        with open(JSON_TRACKER, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        df = pd.DataFrame(data)
        if not df.empty:
            df = df.rename(columns=_COLUMN_DISPLAY_NAMES)
        df.to_excel(EXCEL_TRACKER, index=False)
        return True
    except (OSError, ValueError):
        return False


def get_outreach_dataframe() -> pd.DataFrame:
    """Return this module's outreach pipeline as a DataFrame."""
    data = load_outreach_data()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


def export_outreach_excel_bytes() -> bytes:
    """Generate an Excel bytes buffer of this module's outreach pipeline
    for a Streamlit download button."""
    data = load_outreach_data()
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.rename(columns=_COLUMN_DISPLAY_NAMES)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Week6_Insurance_Outreach")
    return output.getvalue()
