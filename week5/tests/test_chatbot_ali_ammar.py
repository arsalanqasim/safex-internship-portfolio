"""
Unit test suite for Ali Ammar Haider's ShopEase AI Customer Support Chatbot Engine.
"""

import os
import sys
import pytest

# Ensure week5 directory is in sys.path
week5_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if week5_dir not in sys.path:
    sys.path.insert(0, week5_dir)

from src.modules.chatbot_ali_ammar.engine import CustomerSupportEngine


@pytest.fixture
def engine():
    """Create fresh instance of CustomerSupportEngine for testing."""
    eng = CustomerSupportEngine(confidence_threshold=0.42)
    eng.reset_factory_faqs()
    return eng


def test_1_known_faq_question(engine):
    """Verify known exact question returns correct answer and high confidence."""
    res = engine.get_response("How can I track my order or package?")
    assert res["confidence"] >= 0.8
    assert res["matched_faq"] == "FAQ001"
    assert res["human_handoff"] is False
    assert "tracking link" in res["response"].lower() or "track" in res["response"].lower()


def test_2_faq_variation(engine):
    """Verify semantic variation maps to correct FAQ."""
    res = engine.get_response("Can I track my package location?")
    assert res["confidence"] >= 0.42
    assert res["matched_faq"] == "FAQ001"
    assert res["human_handoff"] is False


def test_3_unknown_question(engine):
    """Verify completely out-of-scope question triggers fallback and human handoff."""
    res = engine.get_response("Do you sell commercial diesel aircraft engines?")
    assert res["confidence"] < 0.42
    assert res["human_handoff"] is True
    assert "don't have enough information" in res["response"].lower()


def test_4_human_handoff_request(engine):
    """Verify explicit human request triggers escalation immediately."""
    res = engine.get_response("I want to speak to a real human agent right now")
    assert res["confidence"] == 1.0
    assert res["human_handoff"] is True
    assert res["matched_faq"] == "HUMAN_HANDOFF"
    assert "connecting" in res["response"].lower() or "support" in res["response"].lower()


def test_5_low_confidence_question(engine):
    """Verify question with confidence below threshold triggers fallback handoff."""
    res = engine.get_response("quantum string theory astrophysics")
    assert res["confidence"] < 0.42
    assert res["human_handoff"] is True


def test_6_confidence_range(engine):
    """Verify confidence scores are strictly between 0.0 and 1.0."""
    queries = [
        "How long does delivery take?",
        "What is return policy?",
        "gibberish 12345 xyz",
        "human representative",
        "shipping fee"
    ]
    for q in queries:
        res = engine.get_response(q)
        assert 0.0 <= res["confidence"] <= 1.0


def test_7_conversation_logging(engine):
    """Verify conversation interactions are recorded in chat_logs.json."""
    logs_before = len(engine.get_chat_logs())
    engine.get_response("How much is shipping?")
    logs_after = len(engine.get_chat_logs())
    assert logs_after == logs_before + 1

    last_log = engine.get_chat_logs()[-1]
    assert "user_query" in last_log
    assert "bot_response" in last_log
    assert "confidence" in last_log
    assert "response_time_ms" in last_log
    assert last_log["response_time_ms"] >= 0.0


def test_8_faq_add(engine):
    """Verify adding a new FAQ entry."""
    success, msg = engine.add_faq(
        category="Testing",
        question="Is this a test question for unit testing?",
        answer="Yes this is a verified test answer.",
        keywords=["test", "unit testing"]
    )
    assert success is True
    assert any(f["question"] == "Is this a test question for unit testing?" for f in engine.faqs)


def test_9_faq_update(engine):
    """Verify updating an existing FAQ entry."""
    # Add a temporary FAQ first
    engine.add_faq("Temp", "Temporary question?", "Temp answer", ["temp"])
    added_faq = [f for f in engine.faqs if f["question"] == "Temporary question?"][0]
    faq_id = added_faq["id"]

    success, msg = engine.update_faq(
        faq_id=faq_id,
        category="Updated Temp",
        question="Temporary question?",
        answer="Updated answer text.",
        keywords=["updated"]
    )
    assert success is True
    updated_faq = [f for f in engine.faqs if f["id"] == faq_id][0]
    assert updated_faq["answer"] == "Updated answer text."


def test_10_faq_delete(engine):
    """Verify deleting an FAQ entry."""
    engine.add_faq("DeleteMe", "Delete this item?", "Answer", ["delete"])
    added_faq = [f for f in engine.faqs if f["question"] == "Delete this item?"][0]
    faq_id = added_faq["id"]

    success, msg = engine.delete_faq(faq_id)
    assert success is True
    assert not any(f["id"] == faq_id for f in engine.faqs)


def test_11_reset_factory_faqs(engine):
    """Verify resetting factory default FAQs."""
    engine.add_faq("Extra", "Extra question?", "Answer", ["extra"])
    success, msg = engine.reset_factory_faqs()
    assert success is True
    assert len(engine.faqs) == 15


def test_12_benchmark_functionality(engine):
    """Verify execution of automated benchmark suite."""
    results = engine.run_benchmark_suite()
    assert results["total_tests"] >= 15
    assert results["passed_tests"] >= 12
    assert results["accuracy_pct"] >= 80.0
    assert results["avg_latency_ms"] >= 0.0
