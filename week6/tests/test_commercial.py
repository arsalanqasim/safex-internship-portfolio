"""Unit test suite for Week 6 Commercialization & Client Acquisition Engine."""

import os
import sys
import pytest
import pandas as pd

# Ensure week6 directory is in sys.path
week6_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if week6_dir not in sys.path:
    sys.path.insert(0, week6_dir)

from src.modules.commercial_arsalan.engine import (
    PRICING_TIERS,
    calculate_client_roi,
    generate_cold_outreach_sequence,
    load_outreach_data,
    save_outreach_data,
    export_outreach_excel_bytes,
    get_group_consolidation_metrics
)


def test_pricing_tiers_configuration():
    """Verify all 3 commercial pricing tiers are properly configured."""
    assert len(PRICING_TIERS) == 3
    for name, tier in PRICING_TIERS.items():
        assert tier["monthly_fee"] > 0
        assert tier["setup_fee"] > 0
        assert len(tier["features"]) >= 4
        assert "query_limit" in tier


def test_roi_calculator_logic():
    """Verify financial ROI model and time savings calculations."""
    res = calculate_client_roi(
        monthly_queries=3000,
        staff_hourly_rate=20.0,
        handling_time_min=4.0,
        tier_name="Standard Package"
    )
    # 3000 * 0.75 = 2250 automated queries.
    # 2250 * 4 / 60 = 150 hours saved.
    # 150 * $20 = $3000 gross savings.
    # Net monthly = $3000 - $399 = $2601.
    assert res["hours_saved_monthly"] == 150.0
    assert res["net_monthly_savings"] == 2601.0
    assert res["roi_percentage"] > 500.0


def test_cold_email_sequence_generation():
    """Verify 3-step personalized outreach sequences are generated."""
    seq = generate_cold_outreach_sequence(
        prospect_name="Elena",
        company_name="Alo Yoga",
        industry="E-Commerce Apparel",
        observation="your support response time is over 6 hours on weekends.",
        demo_link="https://safex-group54-portfolio.streamlit.app"
    )
    assert "Alo Yoga" in seq["step_1_subject"]
    assert "Elena" in seq["step_1_body"]
    assert "https://safex-group54-portfolio.streamlit.app" in seq["step_1_body"]
    assert "Re:" in seq["step_2_subject"]
    assert "close your file" in seq["step_3_subject"].lower()


def test_outreach_tracker_loading_and_saving():
    """Verify loading and updating the 15+ international leads pipeline."""
    leads = load_outreach_data()
    assert isinstance(leads, list)
    assert len(leads) >= 15
    
    first = leads[0]
    assert "company_name" in first
    assert "country" in first
    assert "result_status" in first
    
    # Test saving
    success = save_outreach_data(leads)
    assert success is True


def test_excel_export_bytes():
    """Verify Excel workbook generation buffer."""
    buf = export_outreach_excel_bytes()
    assert isinstance(buf, bytes)
    assert len(buf) > 1000  # Valid binary Excel file


def test_group_consolidation_metrics():
    """Verify Group 54 executive outreach consolidation metrics."""
    metrics = get_group_consolidation_metrics()
    assert metrics["total_companies_contacted"] >= 40
    assert metrics["total_responses"] >= 15
    assert metrics["meetings_booked"] >= 3
    assert metrics["response_rate_pct"] > 30.0
