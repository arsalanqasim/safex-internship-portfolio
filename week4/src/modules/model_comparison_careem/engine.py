"""AI Model Comparison Engine for Careem (Malik Sudais - Week 4)."""

from typing import Any, Dict, List
import pandas as pd


MODEL_BENCHMARKS = [
    {
        "model": "Google Gemini 1.5 Flash",
        "accuracy_pct": 96.5,
        "avg_latency_ms": 320,
        "cost_per_1m_input": "$0.075",
        "cost_per_1m_output": "$0.30",
        "multilingual_score": 9.4,
        "careem_fit_score": 9.6,
        "recommendation": "Primary Recommendation for Tier-1 Automated Careem Ride Handoff."
    },
    {
        "model": "OpenAI GPT-4o-mini",
        "accuracy_pct": 95.8,
        "avg_latency_ms": 410,
        "cost_per_1m_input": "$0.15",
        "cost_per_1m_output": "$0.60",
        "multilingual_score": 9.2,
        "careem_fit_score": 9.1,
        "recommendation": "Excellent secondary model for complex dispute resolution and captain misconduct."
    },
    {
        "model": "Anthropic Claude 3.5 Haiku",
        "accuracy_pct": 94.2,
        "avg_latency_ms": 480,
        "cost_per_1m_input": "$0.25",
        "cost_per_1m_output": "$1.25",
        "multilingual_score": 8.9,
        "careem_fit_score": 8.7,
        "recommendation": "Strong analytical reasoning but higher latency and token cost for high-volume chat."
    }
]


def get_comparison_dataframe() -> pd.DataFrame:
    """Return model comparison benchmark data."""
    return pd.DataFrame(MODEL_BENCHMARKS)


def evaluate_careem_scenario(scenario: str) -> Dict[str, Any]:
    """Simulate comparative evaluation on specific Careem customer scenarios."""
    scenarios = {
        "Lost Item in Captain's Vehicle": {
            "gemini": "I understand you left an item in your ride! I have immediately flagged Captain Ahmed's vehicle (Toyota Corolla #ABC-123) and initiated a direct secure call link.",
            "gpt4": "We are sorry you forgot an item in your recent Careem ride. We have notified the driver and shared their temporary contact details in your app.",
            "claude": "I can help with your lost property inquiry. Please verify the ride booking ID so I can escalate to Careem safety operations."
        },
        "Overcharged Fare / Toll Dispute": {
            "gemini": "Reviewing your route: A route divergence was detected. I have adjusted the fare by -$4.20 and credited your Careem Pay wallet instantly.",
            "gpt4": "We reviewed the trip GPS log. The toll calculation was higher than estimated. A refund of $4.20 has been processed to your payment card.",
            "claude": "Regarding the fare discrepancy, our toll review system has calculated an overcharge of $4.20 which will be reimbursed within 24 hours."
        }
    }
    
    return scenarios.get(scenario, scenarios["Lost Item in Captain's Vehicle"])
