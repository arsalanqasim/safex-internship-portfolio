"""Unit test suite for Week 5 Insurance & Finance Lead Qualifier Engine."""
import os
import sys
import pytest

week5_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if week5_dir not in sys.path:
    sys.path.insert(0, week5_dir)

from src.modules.lead_gen_ali_zaib.engine import (
    LeadQualifierError,
    load_sample_leads,
    score_insurance_lead,
    score_leads_batch,
)


def test_hot_lead_scores_high():
    result = score_insurance_lead(
        "Comprehensive Corporate", 250000, "Immediate (< 14 days)",
        prior_claims_count=0, applicant_age=42, occupation_risk="Low Risk (Office/Admin)",
        stated_monthly_budget=400, contact_channel="Referral",
    )
    assert result.total_score >= 80
    assert result.tier == "Hot Lead — Fast-Track Underwriting"
    assert result.flags == []


def test_low_quality_lead_scores_low_and_flags_issues():
    result = score_insurance_lead(
        "Individual Basic", 400000, "Exploratory",
        prior_claims_count=3, applicant_age=22, occupation_risk="High Risk (Hazardous/Manual)",
        stated_monthly_budget=60, contact_channel="Cold Outreach",
    )
    assert result.total_score < 40
    assert result.tier == "Low Priority — Manual Review Likely"
    assert len(result.flags) >= 3


def test_sub_scores_sum_to_total():
    result = score_insurance_lead(
        "Fleet Commercial", 100000, "Within 1 Month",
        prior_claims_count=1, applicant_age=30, occupation_risk="Medium Risk (Field/Trade)",
        stated_monthly_budget=150, contact_channel="Website Form",
    )
    assert sum(result.sub_scores.values()) == result.total_score


def test_invalid_policy_type_raises():
    with pytest.raises(LeadQualifierError):
        score_insurance_lead("Nonexistent Policy", 50000, "Immediate (< 14 days)")


def test_invalid_timeline_raises():
    with pytest.raises(LeadQualifierError):
        score_insurance_lead("Individual Basic", 50000, "Sometime Eventually")


def test_negative_claims_raises():
    with pytest.raises(LeadQualifierError):
        score_insurance_lead("Individual Basic", 50000, "Within 1 Month", prior_claims_count=-1)


def test_out_of_range_age_raises():
    with pytest.raises(LeadQualifierError):
        score_insurance_lead("Individual Basic", 50000, "Within 1 Month", applicant_age=10)


def test_zero_budget_raises():
    with pytest.raises(LeadQualifierError):
        score_insurance_lead("Individual Basic", 50000, "Within 1 Month", stated_monthly_budget=0)


def test_load_sample_leads_has_expected_columns():
    df = load_sample_leads()
    assert len(df) == 40
    for col in ["policy_type", "coverage_amount", "decision_timeline", "prior_claims_count"]:
        assert col in df.columns


def test_score_leads_batch_sorted_descending():
    df = load_sample_leads()
    scored = score_leads_batch(df)
    scores = scored["total_score"].tolist()
    assert scores == sorted(scores, reverse=True)
    assert len(scored) == len(df)
    assert "tier" in scored.columns


def test_score_leads_batch_missing_column_raises():
    import pandas as pd
    bad_df = pd.DataFrame([{"policy_type": "Individual Basic"}])
    with pytest.raises(LeadQualifierError):
        score_leads_batch(bad_df)
