"""Unit tests for Week 4 Customer Support Chatbot Deployment Engine."""

from __future__ import annotations

import sys
from pathlib import Path

# Setup paths to import the engine
WEEK4_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WEEK4_DIR))

from src.modules.chatbot_deployment.engine import CustomerSupportEngine


def test_empty_query() -> None:
    """Test empty string and whitespace input handling."""
    engine = CustomerSupportEngine()
    
    # Blank query
    res = engine.classify_query("")
    assert "Error" in res["intent"]
    assert res["category"] == "Error Handling"
    
    # Whitespace query
    res = engine.classify_query("   ")
    assert "Error" in res["intent"]
    assert "Empty" in res["intent"]


def test_long_query() -> None:
    """Test query length limits."""
    engine = CustomerSupportEngine()
    long_query = "a" * 305
    res = engine.classify_query(long_query)
    assert "Error" in res["intent"]
    assert "Too Long" in res["intent"]
    assert res["escalated"] is False


def test_gibberish_query() -> None:
    """Test short gibberish without vowels."""
    engine = CustomerSupportEngine()
    res = engine.classify_query("bcdfgh")
    assert "Error" in res["intent"]
    assert "Gibberish" in res["intent"]


def test_standard_matching() -> None:
    """Test accurate classification for valid patterns."""
    engine = CustomerSupportEngine(brand_name="TestShop")
    
    # Standard order tracking query
    res = engine.classify_query("How can I track my shipment?")
    assert res["intent"] == "Track Order Status"
    assert "TestShop" in res["response"]
    assert res["escalated"] is False

    # Standard returns query
    res = engine.classify_query("What is your return policy?")
    assert res["intent"] == "Return & Refund Policy"
    assert "TestShop" in res["response"]
    assert res["escalated"] is False


def test_human_escalation_triggers() -> None:
    """Test key word triggers and low confidence fallbacks."""
    engine = CustomerSupportEngine(brand_name="TestShop")
    
    # Low confidence query
    res = engine.classify_query("What is the capital of France?")
    assert res["intent"] == "Out of Scope / Unmapped"
    assert res["escalated"] is True
    assert "below threshold" in res["escalation_reason"]

    # Explicit escalation keyword (e.g. scam)
    res = engine.classify_query("This store is a fake and a scam, refund my money!")
    assert res["escalated"] is True
    assert "keyword" in res["escalation_reason"]
