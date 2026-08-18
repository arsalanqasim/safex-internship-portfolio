"""Healthcare & Clinic AI Chatbot Engine (Shahidullah - Week 5)."""
from typing import Dict, Any


def get_clinic_faqs() -> Dict[str, str]:
    """Sample FAQ knowledge base for healthcare clinic."""
    return {
        "hours": "Our clinic is open Monday to Saturday from 8:00 AM to 8:00 PM.",
        "appointment": "You can schedule appointments online or by calling our desk at +92-51-1234567.",
        "insurance": "We accept major insurance providers including State Life, Jubilee, and EFU.",
        "emergency": "For severe emergencies, please proceed immediately to the nearest hospital ER."
    }


def match_clinic_query(query: str) -> Dict[str, Any]:
    """Simple keyword matcher for clinic queries."""
    q = query.lower()
    faqs = get_clinic_faqs()
    for k, ans in faqs.items():
        if k in q:
            return {"answer": ans, "confidence": 0.85, "escalated": False}
    if "doctor" in q or "specialist" in q:
        return {"answer": "We have general physicians, cardiologists, and pediatricians available.", "confidence": 0.80, "escalated": False}
    return {
        "answer": "Thank you for contacting the clinic. Please specify if your query relates to clinic hours, appointment booking, or doctor consultations.",
        "confidence": 0.40,
        "escalated": False
    }
