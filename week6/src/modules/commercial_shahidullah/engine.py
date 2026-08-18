"""Clinic Chatbot Monetization Engine (Shahidullah - Week 6)."""
from typing import Dict, Any


def get_clinic_bot_pricing() -> Dict[str, Any]:
    """Get clinic bot service packages."""
    return {
        "Clinic Starter ($199/mo)": "Patient FAQs, clinic hours, and email triage.",
        "Medical Pro ($499/mo)": "Automated appointment scheduling + WhatsApp integration.",
        "Multi-Clinic Network ($899/mo)": "Centralized patient routing across multiple branch locations."
    }
