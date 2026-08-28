"""Insurance & Finance Lead Qualifier Engine (Ali Zaib - Week 5).

A weighted, multi-factor lead scoring model for insurance/wealth-management
sales teams. Replaces a simple two-branch rule with five explainable
sub-scores that sum to a 0-100 qualification score, mapped to an
underwriting/sales-priority tier, plus qualitative risk flags a human
underwriter or sales rep can act on immediately.

Scoring rubric (out of 100):
    - Policy value fit        (0-25): how valuable/complex the requested product is
    - Coverage/budget fit     (0-20): does the stated budget realistically support
                                       the requested coverage amount?
    - Urgency / timeline      (0-20): how soon the applicant wants to decide
    - Risk profile            (0-20): prior claims, age band, occupation risk
                                       (fewer/lower risk factors = more points)
    - Engagement / channel    (0-15): quality signal of the contact source

This is a transparent rubric-based model (not a black-box ML classifier),
which is a deliberate choice for an underwriting-adjacent use case: sales
and underwriting teams need to see *why* a lead scored the way it did, not
just a number — see README.md for the reasoning.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_DATA_DIR = Path(__file__).parent / "data"
SAMPLE_LEADS_FILE = "sample_leads.csv"

POLICY_TYPES = ["Comprehensive Corporate", "Fleet Commercial", "Individual Basic"]
TIMELINES = ["Immediate (< 14 days)", "Within 1 Month", "Exploratory"]
OCCUPATION_RISK_LEVELS = ["Low Risk (Office/Admin)", "Medium Risk (Field/Trade)", "High Risk (Hazardous/Manual)"]
CONTACT_CHANNELS = ["Referral", "Broker Partner", "Website Form", "Cold Outreach"]

_POLICY_VALUE_POINTS = {
    "Comprehensive Corporate": 25,
    "Fleet Commercial": 18,
    "Individual Basic": 12,
}
_TIMELINE_POINTS = {
    "Immediate (< 14 days)": 20,
    "Within 1 Month": 13,
    "Exploratory": 5,
}
_OCCUPATION_RISK_POINTS = {  # higher risk occupation -> fewer points (safer applicants score higher)
    "Low Risk (Office/Admin)": 10,
    "Medium Risk (Field/Trade)": 6,
    "High Risk (Hazardous/Manual)": 2,
}
_CHANNEL_POINTS = {
    "Referral": 15,
    "Broker Partner": 13,
    "Website Form": 9,
    "Cold Outreach": 4,
}

# Rough industry rule-of-thumb: annual premium ~ 0.8%-2.5% of coverage amount
# for the products this qualifier covers. Used only to sanity-check whether
# the applicant's stated budget could plausibly support their requested
# coverage -- not an actual underwriting quote.
_ASSUMED_ANNUAL_PREMIUM_RATE = 0.015


class LeadQualifierError(ValueError):
    """Raised for invalid lead inputs (unknown category, out-of-range values, etc.)."""


@dataclass
class LeadScoreResult:
    total_score: int
    tier: str
    sub_scores: dict[str, int]
    flags: list[str]
    summary: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "total_score": self.total_score,
            "tier": self.tier,
            "sub_scores": self.sub_scores,
            "flags": self.flags,
            "summary": self.summary,
        }


def _validate_choice(value: str, allowed: list[str], field_name: str) -> None:
    if value not in allowed:
        raise LeadQualifierError(f"Invalid {field_name} '{value}'. Must be one of {allowed}.")


def _score_policy_value(policy_type: str) -> int:
    return _POLICY_VALUE_POINTS[policy_type]


def _score_coverage_budget_fit(coverage_amount: float, stated_monthly_budget: float) -> tuple[int, list[str]]:
    """Checks whether the stated monthly budget plausibly supports the
    requested coverage, using a rough industry premium-rate assumption."""
    flags: list[str] = []
    estimated_annual_premium = coverage_amount * _ASSUMED_ANNUAL_PREMIUM_RATE
    estimated_monthly_premium = estimated_annual_premium / 12

    if stated_monthly_budget <= 0 or coverage_amount <= 0:
        raise LeadQualifierError("coverage_amount and stated_monthly_budget must be positive.")

    ratio = stated_monthly_budget / estimated_monthly_premium

    if ratio >= 1.3:
        points = 20
    elif ratio >= 0.9:
        points = 15
    elif ratio >= 0.6:
        points = 9
        flags.append(
            f"Stated budget (${stated_monthly_budget:,.0f}/mo) is below the estimated "
            f"premium (~${estimated_monthly_premium:,.0f}/mo) for the requested coverage — "
            "confirm budget expectations before quoting."
        )
    else:
        points = 3
        flags.append(
            f"Stated budget (${stated_monthly_budget:,.0f}/mo) is well below the estimated "
            f"premium (~${estimated_monthly_premium:,.0f}/mo) for ${coverage_amount:,.0f} coverage — "
            "likely needs a lower coverage tier or budget conversation."
        )
    return points, flags


def _score_timeline(timeline: str) -> int:
    return _TIMELINE_POINTS[timeline]


def _score_risk_profile(prior_claims_count: int, applicant_age: int, occupation_risk: str) -> tuple[int, list[str]]:
    flags: list[str] = []
    if prior_claims_count < 0:
        raise LeadQualifierError("prior_claims_count cannot be negative.")
    if not (16 <= applicant_age <= 100):
        raise LeadQualifierError("applicant_age must be between 16 and 100.")

    claims_points = max(0, 6 - 2 * prior_claims_count)  # 0 claims=6, 1=4, 2=2, 3+=0
    if prior_claims_count >= 2:
        flags.append(f"{prior_claims_count} prior claims on record — flag for manual underwriting review.")

    if 25 <= applicant_age <= 55:
        age_points = 4
    elif applicant_age < 25:
        age_points = 2
        flags.append("Applicant under 25 — may carry a higher risk premium adjustment.")
    else:
        age_points = 2
        flags.append("Applicant over 55 — may require additional health/risk disclosures.")

    occupation_points = _OCCUPATION_RISK_POINTS[occupation_risk]
    if occupation_risk == "High Risk (Hazardous/Manual)":
        flags.append("High-risk occupation — expect a higher premium loading at underwriting.")

    return claims_points + age_points + occupation_points, flags


def _score_channel(contact_channel: str) -> int:
    return _CHANNEL_POINTS[contact_channel]


def _tier_for_score(total_score: int) -> str:
    if total_score >= 80:
        return "Hot Lead — Fast-Track Underwriting"
    if total_score >= 60:
        return "Qualified — Standard Underwriting"
    if total_score >= 40:
        return "Nurture — Needs More Information"
    return "Low Priority — Manual Review Likely"


def score_insurance_lead(
    policy_type: str,
    coverage_amount: float,
    decision_timeline: str,
    prior_claims_count: int = 0,
    applicant_age: int = 35,
    occupation_risk: str = "Low Risk (Office/Admin)",
    stated_monthly_budget: float = 200.0,
    contact_channel: str = "Website Form",
) -> LeadScoreResult:
    """Score a single insurance lead across five weighted factors and
    return a total score (0-100), a sales/underwriting tier, per-factor
    sub-scores, and qualitative flags for a human reviewer."""
    _validate_choice(policy_type, POLICY_TYPES, "policy_type")
    _validate_choice(decision_timeline, TIMELINES, "decision_timeline")
    _validate_choice(occupation_risk, OCCUPATION_RISK_LEVELS, "occupation_risk")
    _validate_choice(contact_channel, CONTACT_CHANNELS, "contact_channel")

    flags: list[str] = []

    policy_points = _score_policy_value(policy_type)
    budget_points, budget_flags = _score_coverage_budget_fit(coverage_amount, stated_monthly_budget)
    timeline_points = _score_timeline(decision_timeline)
    risk_points, risk_flags = _score_risk_profile(prior_claims_count, applicant_age, occupation_risk)
    channel_points = _score_channel(contact_channel)

    flags.extend(budget_flags)
    flags.extend(risk_flags)

    total = policy_points + budget_points + timeline_points + risk_points + channel_points
    tier = _tier_for_score(total)

    sub_scores = {
        "Policy Value Fit": policy_points,
        "Coverage/Budget Fit": budget_points,
        "Urgency/Timeline": timeline_points,
        "Risk Profile": risk_points,
        "Engagement/Channel": channel_points,
    }

    summary = (
        f"{policy_type} applicant requesting ${coverage_amount:,.0f} coverage, "
        f"deciding {decision_timeline.lower()}, scored {total}/100 → {tier}."
    )

    return LeadScoreResult(total_score=total, tier=tier, sub_scores=sub_scores, flags=flags, summary=summary)


def load_sample_leads(data_dir: Path | str = DEFAULT_DATA_DIR) -> pd.DataFrame:
    path = Path(data_dir) / SAMPLE_LEADS_FILE
    if not path.exists():
        raise LeadQualifierError(f"Sample leads file not found at {path}")
    return pd.read_csv(path)


def score_leads_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Score every row in a leads DataFrame and return it with score
    columns appended, sorted by total_score descending (hottest leads first)."""
    required_cols = [
        "policy_type", "coverage_amount", "decision_timeline", "prior_claims_count",
        "applicant_age", "occupation_risk", "stated_monthly_budget", "contact_channel",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise LeadQualifierError(f"Missing required column(s) for batch scoring: {missing}")

    results = []
    for _, row in df.iterrows():
        result = score_insurance_lead(
            policy_type=row["policy_type"],
            coverage_amount=float(row["coverage_amount"]),
            decision_timeline=row["decision_timeline"],
            prior_claims_count=int(row["prior_claims_count"]),
            applicant_age=int(row["applicant_age"]),
            occupation_risk=row["occupation_risk"],
            stated_monthly_budget=float(row["stated_monthly_budget"]),
            contact_channel=row["contact_channel"],
        )
        results.append({
            "total_score": result.total_score,
            "tier": result.tier,
            "flag_count": len(result.flags),
        })

    scored = pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
    return scored.sort_values("total_score", ascending=False).reset_index(drop=True)
