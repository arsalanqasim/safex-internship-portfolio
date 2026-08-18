"""B2B Lead Qualification Agent Engine (Ali Ammar Haider - Week 5)."""

from typing import Dict, Any


def score_b2b_lead(company_size: str, budget: float, decision_maker: bool) -> Dict[str, Any]:
    """Score inbound B2B sales prospect."""
    size_weights = {"Enterprise (500+ employees)": 90, "Mid-Market (50-500 employees)": 70, "Small Business (< 50 employees)": 40}
    s_score = size_weights.get(company_size, 50)
    b_score = min(100, int((budget / 10000.0) * 100))
    dm_bonus = 20 if decision_maker else 0
    
    total = min(100, int((s_score * 0.4) + (b_score * 0.4) + dm_bonus))
    
    tier = "Tier 1 (High Priority)" if total >= 70 else ("Tier 2 (Medium Priority)" if total >= 45 else "Tier 3 (Self-Serve)")
    return {
        "score": total,
        "priority_tier": tier,
        "summary": f"B2B Account in {company_size} with ${budget:,.0f} budget evaluated as {tier}."
    }
