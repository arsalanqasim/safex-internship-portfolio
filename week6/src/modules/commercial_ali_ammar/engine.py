"""B2B Lead Qualification Commercial Engine (Ali Ammar Haider - Week 6)."""
from typing import Dict, Any


def get_b2b_agency_tiers() -> Dict[str, Any]:
    """Get B2B lead generation agency packages."""
    return {
        "Outbound Starter ($400/mo)": "List enrichment + automated intent qualification for 300 accounts.",
        "Growth Agency ($950/mo)": "Multi-channel lead scoring, CRM integration, and Slack hot-lead alerts.",
        "Scale Enterprise ($1,800/mo)": "Dedicated custom scoring pipeline + weekly pipeline optimization."
    }
