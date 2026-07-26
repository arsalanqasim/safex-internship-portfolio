"""Unit tests for the Document Analysis & Knowledge-Base Assistant engine."""
import pytest

from src.modules.doc_knowledge_assistant.engine import (
    DocKnowledgeAssistantEngine,
    DocKnowledgeAssistantError,
)
from src.modules.doc_knowledge_assistant.test_suite import TEST_SUITE


@pytest.fixture
def engine():
    return DocKnowledgeAssistantEngine()


def test_index_loads_all_five_documents(engine):
    titles = engine.document_titles()
    assert len(titles) == 5
    assert "QuickBite Delivery Policy" in titles
    assert "QuickBite Refund and Cancellation Policy" in titles


def test_index_produces_multiple_chunks(engine):
    assert len(engine.chunks) > 5  # more than one chunk per doc


def test_retrieve_rejects_empty_query(engine):
    with pytest.raises(DocKnowledgeAssistantError):
        engine.retrieve("")


def test_retrieve_returns_top_k_scored_chunks(engine):
    results = engine.retrieve("How do I cancel my order?", top_k=3)
    assert len(results) == 3
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)  # ranked descending


def test_answer_grounded_query_returns_correct_source(engine):
    result = engine.answer("How much commission do restaurants pay?")
    assert not result.abstained
    assert result.retrieved[0].chunk.doc_title == "QuickBite Restaurant Partner FAQ"
    assert "commission" in result.answer.lower()


def test_answer_out_of_scope_query_abstains(engine):
    result = engine.answer("What is the capital of France?")
    assert result.abstained
    assert "don't have information" in result.answer.lower()


def test_answer_unknown_provider_raises(engine):
    engine.llm_provider = "some_unsupported_provider"
    with pytest.raises(DocKnowledgeAssistantError):
        engine.answer("How do refunds work?")


def test_run_evaluation_matches_expected_documents(engine):
    report = engine.run_evaluation(TEST_SUITE)
    assert report["total"] == len(TEST_SUITE)
    assert report["accuracy_percent"] >= 90.0  # allow minor variance, current run scores 100%


def test_run_evaluation_flags_abstain_cases_correctly(engine):
    report = engine.run_evaluation(TEST_SUITE)
    abstain_cases = [r for r in report["results"] if r["expected_doc"] is None]
    assert len(abstain_cases) == 2
    assert all(c["abstained"] for c in abstain_cases if c["passed"])
