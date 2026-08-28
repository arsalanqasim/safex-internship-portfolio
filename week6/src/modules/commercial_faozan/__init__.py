"""BI Dashboard Monthly Reporting Service (Muhammad Faozan Mujtaba - Week 6)."""

from .engine import (
    PRICING_TIERS,
    calculate_client_roi,
    compute_tier_economics,
    export_outreach_excel_bytes,
    generate_cold_outreach_sequence,
    generate_proposal,
    load_outreach_data,
    pipeline_metrics,
    pricing_table,
    save_outreach_data,
)
from .ui import render_ui

__all__ = [
    "PRICING_TIERS",
    "calculate_client_roi",
    "compute_tier_economics",
    "export_outreach_excel_bytes",
    "generate_cold_outreach_sequence",
    "generate_proposal",
    "load_outreach_data",
    "pipeline_metrics",
    "pricing_table",
    "save_outreach_data",
    "render_ui",
]
