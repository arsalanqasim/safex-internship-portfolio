"""Insurance & Finance Lead Qualifier Engine (Ali Zaib - Week 5)."""
from typing import Dict, Any


def score_insurance_lead(policy_type: str, coverage_amt: float, timeline: str) -> Dict[str, Any]:
    """Score insurance policyholder applicant."""
    score = 80 if "Comprehensive" in policy_type or coverage_amt >= 50000 else 55
    return {
        "score": score,
        "underwriting_tier": "Standard Approved" if score >= 70 else "Manual Review Required",
        "summary": f"Applicant for {policy_type} (${coverage_amt:,.0f} coverage) processed with score {score}/100."
    }
