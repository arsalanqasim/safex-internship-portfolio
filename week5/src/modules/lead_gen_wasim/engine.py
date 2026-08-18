"""Lead Generation & Qualification Engine (MUHAMMAD WASIM - Week 5)."""

from typing import Any, Dict, List
import pandas as pd


def get_default_rubric() -> Dict[str, int]:
    """Default scoring weights for lead qualification."""
    return {
        "budget_threshold_k": 10,
        "urgency_weight": 30,
        "budget_weight": 40,
        "fit_weight": 30
    }


def score_lead(name: str, company: str, budget_k: float, urgency: str, fit_score: int) -> Dict[str, Any]:
    """Score a lead based on qualification parameters."""
    urgency_scores = {"Immediate (< 1 month)": 100, "Moderate (1-3 months)": 60, "Low (> 3 months)": 20}
    u_score = urgency_scores.get(urgency, 50)
    
    b_score = min(100, int((budget_k / 20.0) * 100))
    f_score = min(100, max(0, fit_score * 10))
    
    total_score = int((b_score * 0.4) + (u_score * 0.3) + (f_score * 0.3))
    
    if total_score >= 75:
        category = "🔥 Hot Lead"
        action = "Schedule urgent discovery call within 24h"
    elif total_score >= 50:
        category = "⚡ Warm Lead"
        action = "Send case study and follow up in 3 days"
    else:
        category = "❄️ Cold Lead"
        action = "Nurture via email newsletter"
        
    return {
        "name": name,
        "company": company,
        "budget_k": budget_k,
        "urgency": urgency,
        "score": total_score,
        "category": category,
        "recommended_action": action,
        "summary": f"{name} from {company} has a ${budget_k}k budget with {urgency.lower()} timeline."
    }
