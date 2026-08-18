"""Insurance Lead Qualifier Commercial Engine (Ali Zaib - Week 6)."""
from typing import Dict, Any


def get_insurance_scoring_tiers() -> Dict[str, Any]:
    """Get insurance lead scoring commercial packages."""
    return {
        "Broker Starter ($350/mo)": "Up to 200 applicants scored/mo with automated underwriting rubric.",
        "Agency Pro ($800/mo)": "Up to 1,000 policy leads scored + CRM webhook sync and instant risk tiering.",
        "Underwriting Enterprise ($1,600/mo)": "Custom multi-line risk models + regulatory audit compliance export."
    }
