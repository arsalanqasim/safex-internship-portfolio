"""Unit tests for the Week 4 RAG-based Knowledge Assistant (client-ready build)."""
from __future__ import annotations

import sys
from pathlib import Path

WEEK4_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WEEK4_DIR))

import pytest

from src.modules.knowledge_assistant_foodpanda.engine import (
    DocKnowledgeAssistantEngine,
    DocKnowledgeAssistantError,
)
from src.modules.knowledge_assistant_foodpanda.test_suite import TEST_SUITE


@pytest.fixture
def engine():
    return DocKnowledgeAssistantEngine()


def test_index_loads_all_five_documents(engine):
    titles = engine.document_titles()
    assert len(titles) == 5


def test_answer_grounded_query_returns_correct_source(engine):
    result = engine.answer("How much commission do restaurants pay?")
    assert not result.abstained
    assert result.retrieved[0].chunk.doc_title == "QuickBite Restaurant Partner FAQ"


def test_answer_out_of_scope_query_abstains(engine):
    result = engine.answer("What is the capital of France?")
    assert result.abstained


def test_run_evaluation_matches_expected_documents(engine):
    report = engine.run_evaluation(TEST_SUITE)
    assert report["total"] == len(TEST_SUITE)
    assert report["accuracy_percent"] >= 90.0
