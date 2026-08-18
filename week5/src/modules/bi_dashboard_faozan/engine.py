"""BI Dashboard Engine (Muhammad Faozan Mujtaba - Week 5)."""

import pandas as pd
import numpy as np
from typing import Dict, Any


def generate_sample_sales_data(domain: str) -> pd.DataFrame:
    """Generate 60 days of historical sales and lead traffic data."""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq="D")
    base_rev = 1200 if "E-Commerce" in domain else 2500
    rev = base_rev + np.random.normal(loc=150, scale=80, size=len(dates)).cumsum()
    traffic = np.random.randint(300, 1500, size=len(dates))
    
    return pd.DataFrame({
        "Date": dates,
        "Revenue ($)": np.maximum(500, rev).round(2),
        "Visitors": traffic,
        "Conversions": (traffic * np.random.uniform(0.02, 0.06, size=len(dates))).astype(int)
    })


def generate_executive_insights(df: pd.DataFrame, domain: str) -> str:
    """Generate AI plain-English performance insight narrative."""
    total_rev = df["Revenue ($)"].sum()
    avg_conv = df["Conversions"].mean()
    growth_rate = ((df["Revenue ($)"].iloc[-1] - df["Revenue ($)"].iloc[0]) / df["Revenue ($)"].iloc[0]) * 100
    
    trend = "strong upward momentum" if growth_rate > 0 else "a slight consolidation phase"
    
    return (
        f"**Weekly Executive Summary ({domain}):**\n\n"
        f"Over the last 60-day operational period, total cumulative revenue reached **${total_rev:,.2f}** with "
        f"average daily conversions of **{avg_conv:.1f} orders/deals**. The business is experiencing {trend} "
        f"(**{growth_rate:+.1f}% net change**). Recommended priority: Optimize high-converting traffic channels "
        f"to scale 30-day forecast projections."
    )
