"""Unit test suite for Week 5 AI Customer Support Chatbot Engine."""

import os
import sys
import pytest

# Ensure week5 directory is in sys.path
week5_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if week5_dir not in sys.path:
    sys.path.insert(0, week5_dir)

from src.modules.chatbot_arsalan.engine import (
    load_faq_knowledge_base,
    match_faq_tfidf,
    generate_chat_response,
    detect_escalation_intent,
    add_faq_entry,
    update_faq_entry,
    delete_faq_entry,
    reset_factory_faqs,
    run_benchmark_tests,
    calculate_kpis,
    BENCHMARK_TEST_SET
)


def test_knowledge_base_initialization():
    """Verify default FAQ knowledge base loads 15+ verified entries."""
    faqs = load_faq_knowledge_base()
    assert isinstance(faqs, list)
    assert len(faqs) >= 15
    for item in faqs:
        assert "id" in item
        assert "question" in item
        assert "answer" in item
        assert "keywords" in item
        assert len(item["question"]) > 5
        assert len(item["answer"]) > 10


def test_tfidf_matching_accuracy():
    """Verify semantic matching for core customer inquiries."""
    faqs = load_faq_knowledge_base()
    
    # Shipping inquiry
    res1 = match_faq_tfidf("How long does shipping take to my address?", faqs)
    assert res1["matched"] is True
    assert res1["faq"]["id"] == "faq_01"
    assert res1["confidence"] > 0.3
    
    # Return policy inquiry
    res2 = match_faq_tfidf("What is your 30 day return policy?", faqs)
    assert res2["matched"] is True
    assert res2["faq"]["id"] == "faq_06"
    assert res2["confidence"] > 0.4


def test_human_escalation_detection():
    """Verify human handoff triggers on explicit requests and customer frustration."""
    # Explicit keyword
    is_esc1, reason1, sent1 = detect_escalation_intent("I want to speak with a human support agent")
    assert is_esc1 is True
    assert "human" in reason1 or "agent" in reason1
    
    # Severe negative frustration
    is_esc2, reason2, sent2 = detect_escalation_intent("This is a terrible awful service I am furious")
    assert is_esc2 is True
    assert sent2 == "negative"
    
    # Standard inquiry (no escalation)
    is_esc3, _, _ = detect_escalation_intent("Can you tell me about shirt sizing?")
    assert is_esc3 is False


def test_generate_chat_response_escalation():
    """Verify chat generator handles escalation priority."""
    res = generate_chat_response("Connect me to a manager right now")
    assert res["escalated"] is True
    assert res["source"] == "Human Escalation Fallback"
    assert "Priority Human Support" in res["answer"]


def test_generate_chat_response_fallback():
    """Verify low-confidence random queries trigger polite fallback."""
    res = generate_chat_response("xyz quantum astrophysics banana teleportation")
    assert res["escalated"] is False
    assert res["source"] == "Fallback Low Confidence"
    assert "not completely confident" in res["answer"]


def test_admin_crud_and_factory_reset():
    """Verify adding, updating, deleting FAQs, and factory reset."""
    # 1. Add
    success_add, _ = add_faq_entry("Test Category", "Is this a test question?", "Yes this is test answer.", ["test", "sample"])
    assert success_add is True
    faqs = load_faq_knowledge_base()
    test_faq = [f for f in faqs if f.get("question") == "Is this a test question?"]
    assert len(test_faq) == 1
    test_id = test_faq[0]["id"]
    
    # 2. Update
    success_up, _ = update_faq_entry(test_id, "Test Category", "Is this a test question?", "Updated test answer.", ["test"])
    assert success_up is True
    
    # 3. Delete
    success_del, _ = delete_faq_entry(test_id)
    assert success_del is True
    
    # 4. Reset
    reset_faqs = reset_factory_faqs()
    assert len(reset_faqs) == 15


def test_benchmark_suite_execution():
    """Verify benchmark tests execute and achieve high accuracy."""
    bench = run_benchmark_tests()
    assert bench["total_tests"] == len(BENCHMARK_TEST_SET)
    assert bench["passed_tests"] >= 12  # At least 80% accuracy threshold
    assert bench["accuracy_pct"] >= 80.0
    assert bench["avg_latency_ms"] >= 0


def test_kpi_calculation():
    """Verify KPI computation function."""
    kpis = calculate_kpis()
    assert "total_queries" in kpis
    assert "resolution_rate" in kpis
    assert "escalation_rate" in kpis
    assert "avg_confidence" in kpis
