"""Unit test suite for Week 6 Insurance Lead Qualifier Commercialization Engine (Ali Zaib)."""
import os
import sys
import pytest

week6_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if week6_dir not in sys.path:
    sys.path.insert(0, week6_dir)

from src.modules.commercial_ali_zaib.engine import (
    PRICING_TIERS,
    calculate_client_roi,
    generate_cold_outreach_sequence,
    load_outreach_data,
    save_outreach_data,
    export_outreach_excel_bytes,
    get_outreach_dataframe,
)


def test_pricing_tiers_configuration():
    assert len(PRICING_TIERS) == 3
    for name, tier in PRICING_TIERS.items():
        assert tier["monthly_fee"] > 0
        assert tier["setup_fee"] > 0
        assert len(tier["features"]) >= 3


def test_pricing_tiers_ascending_cost():
    fees = [tier["monthly_fee"] for tier in PRICING_TIERS.values()]
    assert fees == sorted(fees)


def test_calculate_roi_returns_expected_keys():
    roi = calculate_client_roi(200, 35.0, 12.0, "Agency Pro")
    for key in ["hours_saved_monthly", "manual_cost_monthly", "net_monthly_savings",
                "annual_net_savings", "roi_percentage"]:
        assert key in roi


def test_calculate_roi_scales_with_lead_volume():
    small = calculate_client_roi(50, 35.0, 12.0, "Agency Pro")
    large = calculate_client_roi(500, 35.0, 12.0, "Agency Pro")
    assert large["hours_saved_monthly"] > small["hours_saved_monthly"]
    assert large["manual_cost_monthly"] > small["manual_cost_monthly"]


def test_calculate_roi_unknown_tier_falls_back():
    roi = calculate_client_roi(200, 35.0, 12.0, "Nonexistent Tier")
    assert roi["tier_monthly_fee"] == PRICING_TIERS["Agency Pro"]["monthly_fee"]


def test_generate_outreach_sequence_has_three_steps():
    seq = generate_cold_outreach_sequence("Sarah", "Meridian Insurance", "USA", "", "https://demo.link")
    for step in [1, 2, 3]:
        assert f"step_{step}_subject" in seq
        assert f"step_{step}_body" in seq
        assert "Meridian Insurance" in seq[f"step_{step}_body"]


def test_generate_outreach_sequence_handles_empty_inputs():
    seq = generate_cold_outreach_sequence("", "", "UK", "", "")
    assert "there" in seq["step_1_body"]
    assert "your agency" in seq["step_1_body"]


def test_outreach_data_roundtrip(tmp_path, monkeypatch):
    import src.modules.commercial_ali_zaib.engine as engine_module
    monkeypatch.setattr(engine_module, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(engine_module, "JSON_TRACKER", str(tmp_path / "outreach_tracker.json"))
    monkeypatch.setattr(engine_module, "EXCEL_TRACKER", str(tmp_path / "outreach_tracker.xlsx"))

    assert engine_module.load_outreach_data() == []

    entry = {"agency_name": "Test Agency", "region": "USA", "website": "https://test.com",
              "contact_person": "Jane Doe", "contact_method": "Cold Email",
              "date_contacted": "2026-08-01", "service_offered": "Insurance Lead Qualifier",
              "response": "Awaiting Reply", "followup_date": "2026-08-06",
              "result_status": "Initial Outreach"}
    assert engine_module.save_outreach_data([entry]) is True

    loaded = engine_module.load_outreach_data()
    assert len(loaded) == 1
    assert loaded[0]["agency_name"] == "Test Agency"

    df = engine_module.get_outreach_dataframe()
    assert len(df) == 1

    excel_bytes = engine_module.export_outreach_excel_bytes()
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0
