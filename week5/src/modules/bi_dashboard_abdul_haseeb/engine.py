"""Marketing Agency BI Engine (Abdul Haseeb - Week 5)."""
import pandas as pd
import numpy as np
from typing import Dict, Any


def get_agency_metrics() -> Dict[str, Any]:
    """Calculate campaign KPIs for marketing agencies."""
    return {
        "ad_spend": 24500.0,
        "conversions": 1280,
        "cpa": 19.14,
        "roas": 3.85,
        "recommendation": "Scale ad spend on high-ROAS lookalike campaigns while pruning bottom 15% underperforming creatives."
    }
