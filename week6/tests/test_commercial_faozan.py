"""Tests for the BI Reporting Service commercialization module (Week 6).

Owner: Muhammad Faozan Mujtaba.

Run from the week6 folder:

    pytest tests/test_commercial_faozan.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

WEEK6_DIR = Path(__file__).resolve().parents[1]
if str(WEEK6_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK6_DIR))

from src.modules.commercial_faozan.engine import (  # noqa: E402
    DEMO_LINK,
    OUTAGE_EVIDENCE,
    PRICING_TIERS,
    SEED_PIPELINE,
    STATUS_RESEARCHED,
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


# -- pricing ---------------------------------------------------------------------------


def test_three_tiers_are_fully_configured() -> None:
    assert len(PRICING_TIERS) == 3
    for name, tier in PRICING_TIERS.items():
        assert tier["monthly_fee"] > 0
        assert tier["setup_fee"] > 0
        assert tier["delivery_hours_monthly"] > 0
        assert len(tier["features"]) >= 5
        assert tier["reporting_cadence"]


def test_tiers_increase_in_price_and_delivery() -> None:
    fees = [t["monthly_fee"] for t in PRICING_TIERS.values()]
    hours = [t["delivery_hours_monthly"] for t in PRICING_TIERS.values()]
    assert fees == sorted(fees)
    assert hours == sorted(hours)


def test_every_tier_is_profitable_at_planned_delivery_hours() -> None:
    for name in PRICING_TIERS:
        economics = compute_tier_economics(name)
        assert economics.gross_profit > 0
        assert economics.gross_margin_pct > 50


def test_margin_falls_as_delivery_overruns() -> None:
    """The commercial risk the calculator exists to expose."""
    planned = compute_tier_economics("Starter Reporting")
    overrun = compute_tier_economics("Starter Reporting", hours_override=planned.delivery_hours * 3)
    assert overrun.gross_margin_pct < planned.gross_margin_pct
    assert overrun.effective_hourly_rate < planned.effective_hourly_rate


def test_a_tier_becomes_unprofitable_past_its_break_even_hours() -> None:
    economics = compute_tier_economics("Starter Reporting")
    beyond = compute_tier_economics("Starter Reporting", hours_override=economics.break_even_hours + 2)
    assert beyond.gross_profit < 0


def test_unknown_tier_raises() -> None:
    with pytest.raises(KeyError):
        compute_tier_economics("Platinum Unlimited")


def test_pricing_table_covers_every_tier() -> None:
    table = pricing_table()
    assert len(table) == len(PRICING_TIERS)
    assert set(table["tier"]) == set(PRICING_TIERS)


# -- client ROI ------------------------------------------------------------------------


def test_roi_separates_the_safe_benefit_from_the_assumed_one() -> None:
    """Reporting savings and incident savings must stay separable, never blended."""
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics")
    assert roi["reporting_savings_monthly"] == pytest.approx(12 * 45)
    assert roi["incident_savings_monthly"] > 0
    assert roi["total_savings_monthly"] == pytest.approx(
        roi["reporting_savings_monthly"] + roi["incident_savings_monthly"]
    )
    assert roi["net_monthly_reporting_only"] == pytest.approx(
        roi["reporting_savings_monthly"] - roi["monthly_fee"]
    )


def test_roi_scales_with_client_revenue() -> None:
    small = calculate_client_roi(100_000, 10, 40, "Starter Reporting")
    large = calculate_client_roi(1_000_000, 10, 40, "Starter Reporting")
    assert large["incident_savings_monthly"] > small["incident_savings_monthly"]
    # Reporting savings depend on staff time, not revenue, so they must not move.
    assert large["reporting_savings_monthly"] == small["reporting_savings_monthly"]


def test_zero_assumed_incidents_removes_the_assumed_benefit() -> None:
    """A client who rejects the incident assumption must still get an honest number."""
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics", incidents_per_year=0)
    assert roi["incident_savings_monthly"] == 0
    assert roi["total_savings_monthly"] == pytest.approx(roi["reporting_savings_monthly"])


def test_roi_reports_assumptions_alongside_the_number() -> None:
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics")
    assumptions = roi["assumptions"]
    assert assumptions["incidents_per_year"] == 2.0
    assert assumptions["detection_days_saved"] == 3.0
    assert "Week 5" in assumptions["evidence"]


def test_roi_rejects_invalid_revenue() -> None:
    with pytest.raises(ValueError):
        calculate_client_roi(0, 12, 45, "Growth Analytics")


def test_payback_is_none_when_the_client_does_not_profit() -> None:
    roi = calculate_client_roi(
        20_000, 0, 10, "Enterprise BI", incidents_per_year=0, detection_days_saved=0
    )
    assert roi["net_monthly_savings"] < 0
    assert roi["payback_months"] is None


def test_outage_evidence_is_internally_consistent() -> None:
    """The ROI model rests on this evidence, so its arithmetic is asserted."""
    assert (
        OUTAGE_EVIDENCE["orders_expected"] - OUTAGE_EVIDENCE["orders_actual"]
        == OUTAGE_EVIDENCE["orders_lost"]
    )
    assert OUTAGE_EVIDENCE["outage_conversion"] < OUTAGE_EVIDENCE["normal_conversion"]
    per_day = OUTAGE_EVIDENCE["revenue_lost_pkr"] / OUTAGE_EVIDENCE["days"]
    assert per_day == pytest.approx(OUTAGE_EVIDENCE["revenue_lost_per_day_pkr"], rel=0.01)


# -- outreach sequences ----------------------------------------------------------------


def test_sequence_has_three_personalised_steps() -> None:
    sequence = generate_cold_outreach_sequence(
        prospect_name="Alex",
        company_name="Allbirds",
        industry="Footwear DTC",
        observation="revenue grew while gross margin fell in your last two updates",
    )
    assert "Allbirds" in sequence["step_1_subject"]
    assert "Alex" in sequence["step_1_body"]
    assert DEMO_LINK in sequence["step_1_body"]
    assert sequence["step_2_subject"].startswith("Re:")
    assert "close your file" in sequence["step_3_subject"].lower()


def test_sequence_states_the_demo_is_synthetic() -> None:
    """A prospect must never be left thinking the demo runs on their own data."""
    sequence = generate_cold_outreach_sequence(
        "Alex", "Allbirds", "Footwear DTC", "margin fell last quarter"
    )
    assert "synthetic" in sequence["step_1_body"].lower()


def test_sequence_requires_a_specific_observation() -> None:
    """Without an observation it is a template, and templates are worthless."""
    with pytest.raises(ValueError):
        generate_cold_outreach_sequence("Alex", "Allbirds", "Footwear DTC", "   ")


# -- pipeline --------------------------------------------------------------------------


def test_seed_pipeline_covers_the_target_markets() -> None:
    assert len(SEED_PIPELINE) >= 15
    regions = {row["region"] for row in SEED_PIPELINE}
    assert regions == {"USA", "Canada", "Europe"}


def test_seed_rows_are_recorded_as_researched_not_contacted() -> None:
    """Seeded prospects must never claim outreach that has not happened."""
    for row in SEED_PIPELINE:
        assert row["status"] == STATUS_RESEARCHED
        assert row["date_contacted"] == ""


def test_seed_stores_no_personal_contact_details() -> None:
    """AGENTS.md forbids personal names, emails and phone numbers in the repo."""
    for row in SEED_PIPELINE:
        assert "@" not in row["contact_role"]
        assert "contact_email" not in row
        assert "phone" not in row


def test_pipeline_round_trips_through_disk(tmp_path: Path) -> None:
    target = tmp_path / "pipeline.json"
    rows = load_outreach_data(target)
    assert len(rows) == len(SEED_PIPELINE)
    assert target.exists()

    rows[0]["status"] = "Contacted - awaiting reply"
    assert save_outreach_data(rows, target) is True
    assert json.loads(target.read_text())[0]["status"] == "Contacted - awaiting reply"


def test_untouched_pipeline_reports_zero_rather_than_estimated_rates() -> None:
    metrics = pipeline_metrics(list(SEED_PIPELINE))
    assert metrics["total_prospects"] == len(SEED_PIPELINE)
    assert metrics["contacted"] == 0
    assert metrics["replied"] == 0
    assert metrics["reply_rate_pct"] == 0.0
    assert metrics["any_outreach_sent"] is False


def test_metrics_follow_the_funnel_as_statuses_advance() -> None:
    rows = [dict(r) for r in SEED_PIPELINE]
    rows[0]["status"] = "Contacted - awaiting reply"
    rows[1]["status"] = "Replied - interested"
    rows[2]["status"] = "Call booked"
    rows[3]["status"] = "Won"

    metrics = pipeline_metrics(rows)
    assert metrics["contacted"] == 4
    assert metrics["replied"] == 3      # replied, call booked and won all imply a reply
    assert metrics["calls_booked"] == 2  # call booked and won
    assert metrics["won"] == 1
    assert metrics["reply_rate_pct"] == pytest.approx(75.0)
    assert metrics["any_outreach_sent"] is True


def test_excel_export_produces_a_valid_workbook() -> None:
    payload = export_outreach_excel_bytes(list(SEED_PIPELINE))
    assert isinstance(payload, bytes)
    assert len(payload) > 1000
    assert payload[:2] == b"PK"  # xlsx is a zip container


# -- proposal --------------------------------------------------------------------------


def test_proposal_contains_the_commercials_and_the_evidence() -> None:
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics")
    proposal = generate_proposal("Allbirds", "Director of Retail Analytics", "Growth Analytics", roi)
    assert "Allbirds" in proposal
    assert "Growth Analytics" in proposal
    assert f"{PRICING_TIERS['Growth Analytics']['monthly_fee']:,}" in proposal
    assert OUTAGE_EVIDENCE["window"] in proposal
    assert DEMO_LINK in proposal


def test_proposal_states_the_reporting_only_figure() -> None:
    """The client must be able to see the case without the incident assumption."""
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics")
    proposal = generate_proposal("Allbirds", "Head of Data", "Growth Analytics", roi)
    assert "reporting time alone" in proposal.lower()


def test_proposal_rejects_an_unknown_tier() -> None:
    roi = calculate_client_roi(250_000, 12, 45, "Growth Analytics")
    with pytest.raises(KeyError):
        generate_proposal("Allbirds", "Head of Data", "Platinum Unlimited", roi)
