"""Tests for the Indus Air RAG Knowledge Assistant.

Run from the week4 folder:

    pytest src/modules/knowledge_assistant_airline/
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

WEEK4_DIR = Path(__file__).resolve().parents[4]
if str(WEEK4_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK4_DIR))

from src.modules.knowledge_assistant_airline.engine import (  # noqa: E402
    DEFAULT_SIMILARITY_FLOOR,
    AirlineKnowledgeAssistant,
    Chunk,
    TfidfVectorIndex,
    _split_units,
    compose_extractive_answer,
    expand_query,
    export_answer_json,
    load_evaluation_set,
    load_knowledge_base,
    resolve_follow_up,
)


@pytest.fixture(scope="module")
def assistant() -> AirlineKnowledgeAssistant:
    return AirlineKnowledgeAssistant()


# -- knowledge base loading ------------------------------------------------------------


def test_knowledge_base_loads_all_seven_documents() -> None:
    chunks = load_knowledge_base()
    documents = {chunk.document for chunk in chunks}
    assert len(documents) == 7
    assert "baggage_policy.md" in documents
    assert all(chunk.text.strip() for chunk in chunks)


def test_chunks_carry_document_title_and_section() -> None:
    chunks = load_knowledge_base()
    baggage = [c for c in chunks if c.document == "baggage_policy.md"]
    assert any(c.section == "Cabin Baggage Allowance" for c in baggage)
    assert all(c.document_title.startswith("Indus Air") for c in baggage)
    assert all(">" in c.citation for c in baggage)


def test_long_sections_are_split_into_parts_with_unique_ids() -> None:
    chunks = load_knowledge_base()
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    for chunk in chunks:
        assert 1 <= chunk.part <= chunk.total_parts


def test_missing_knowledge_base_directory_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_knowledge_base(tmp_path / "does_not_exist")


# -- query handling --------------------------------------------------------------------


def test_expand_query_bridges_passenger_wording_to_policy_wording() -> None:
    expanded = expand_query("How much hand luggage can I take?").lower()
    assert "cabin baggage" in expanded
    # The original wording must survive so an exact-match question is not diluted.
    assert "hand luggage" in expanded


def test_expand_query_leaves_unknown_wording_untouched() -> None:
    question = "What is the runway length at Skardu?"
    assert expand_query(question) == question


def test_resolve_follow_up_carries_the_previous_subject_forward() -> None:
    history = [("How much does it cost to change a Saver ticket?", "…")]
    resolved = resolve_follow_up("What about international?", history)
    assert "Saver" in resolved
    assert "international" in resolved.lower()


def test_resolve_follow_up_leaves_standalone_questions_alone() -> None:
    history = [("How much is excess baggage?", "…")]
    question = "What documents does my cat need to fly on an international sector?"
    assert resolve_follow_up(question, history) == question


def test_resolve_follow_up_with_no_history_is_a_no_op() -> None:
    assert resolve_follow_up("What about international?", []) == "What about international?"


# -- unit splitting --------------------------------------------------------------------


def test_split_units_rejoins_hard_wrapped_lines() -> None:
    text = "Snub nosed breeds are refused in the hold.\nThese breeds are at elevated risk\nof respiratory distress."
    units = _split_units(text)
    assert any(unit.endswith("respiratory distress.") and "elevated risk of" in unit for unit in units)


def test_split_units_keeps_table_rows_whole_and_drops_separators() -> None:
    text = "| Fare | Domestic |\n|---|---|\n| Indus Flex | 25 kg |"
    units = _split_units(text)
    assert "| Indus Flex | 25 kg |" in units
    assert not any(set(u) <= set("|-: ") for u in units)


def test_split_units_strips_bullet_markers() -> None:
    units = _split_units("- Cabin bag limit: 7 kg.\n- Personal item allowed.")
    assert units[0].startswith("Cabin bag limit")


# -- retrieval -------------------------------------------------------------------------


def test_retrieval_returns_ranked_passages(assistant: AirlineKnowledgeAssistant) -> None:
    passages = assistant.retrieve("What is the excess baggage rate?", top_k=3)
    assert len(passages) == 3
    assert [p.rank for p in passages] == [1, 2, 3]
    scores = [p.score for p in passages]
    assert scores == sorted(scores, reverse=True)


def test_retrieval_finds_the_right_policy_document(assistant: AirlineKnowledgeAssistant) -> None:
    passages = assistant.retrieve("Can I bring my dog in the cabin?")
    assert passages[0].chunk.document == "pets_and_restricted_items.md"


def test_carrier_name_alone_does_not_produce_a_confident_match(
    assistant: AirlineKnowledgeAssistant,
) -> None:
    """The carrier name appears in all 48 chunks, so it must carry no retrieval signal.

    Without the ``max_df`` cap on the vectoriser, scikit-learn floors the IDF of a term
    present in every document at 1.0 rather than 0, and any question merely naming the
    airline scored above the similarity floor.
    """
    result = assistant.answer("What is the share price of Indus Air today?")
    assert not result.grounded
    assert result.confidence < DEFAULT_SIMILARITY_FLOOR


# -- answering and grounding -----------------------------------------------------------


def test_answer_is_grounded_and_cited(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("How much hand luggage can I take on board?")
    assert result.grounded
    assert result.citations
    assert "[1]" in result.answer
    assert "7 kg" in result.answer


def test_extractive_answer_quotes_only_retrieved_text(assistant: AirlineKnowledgeAssistant) -> None:
    """Offline mode must not invent wording: every quoted line comes from a passage."""
    result = assistant.answer("What is the excess baggage rate on a domestic flight?")
    assert result.generator == "extractive"
    corpus = " ".join(p.chunk.text for p in result.passages)
    normalised_corpus = " ".join(corpus.split())
    for line in result.answer.splitlines():
        quoted = line.lstrip("- ").rsplit("[", 1)[0].strip()
        assert quoted in normalised_corpus


def test_out_of_scope_question_is_refused(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("Who won the cricket match last night?")
    assert not result.grounded
    assert "could not find this" in result.answer
    assert result.generator == "refusal"


def test_refusal_names_a_covered_topic(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("Which meals are served on the Jeddah route?")
    assert not result.grounded
    assert "Indus Air" in result.answer


def test_empty_question_is_handled(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("   ")
    assert not result.grounded
    assert result.confidence == 0.0


def test_lowering_the_floor_disables_the_refusal(assistant: AirlineKnowledgeAssistant) -> None:
    """The floor is the control, so removing it must change the behaviour it governs."""
    question = "Who won the cricket match last night?"
    assert not assistant.answer(question).grounded
    assert assistant.answer(question, similarity_floor=0.0).grounded


def test_table_row_is_quoted_for_a_fare_family_question(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("What is the checked baggage allowance on an Indus Flex ticket to Dubai?")
    assert "| Indus Flex |" in result.answer


def test_answer_serialises_to_json(assistant: AirlineKnowledgeAssistant) -> None:
    result = assistant.answer("When does online check-in open?")
    payload = json.loads(export_answer_json(result))
    assert payload["grounded"] is True
    assert payload["passages"]
    assert payload["passages"][0]["rank"] == 1


def test_compose_extractive_answer_falls_back_when_no_line_matches(
    assistant: AirlineKnowledgeAssistant,
) -> None:
    passages = assistant.retrieve("baggage", top_k=1)
    answer, citations = compose_extractive_answer("zzzz qqqq", passages)
    assert answer.strip()
    assert citations


# -- provider behaviour ----------------------------------------------------------------


def test_default_provider_is_offline_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    assert AirlineKnowledgeAssistant.provider() == "mock"


def test_provider_call_is_skipped_without_a_key(
    assistant: AirlineKnowledgeAssistant, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = assistant.answer("When does online check-in open?")
    assert result.generator == "extractive"


# -- custom index ----------------------------------------------------------------------


def test_custom_index_can_be_injected() -> None:
    """The VectorIndex seam is what makes the FAISS/Chroma swap a drop-in change."""
    index = TfidfVectorIndex()
    custom = AirlineKnowledgeAssistant(index=index, top_k=2)
    assert custom.index is index
    assert len(custom.retrieve("excess baggage")) == 2


# -- evaluation ------------------------------------------------------------------------


def test_evaluation_set_is_well_formed() -> None:
    cases = load_evaluation_set()
    assert len(cases) >= 30
    for case in cases:
        assert case["question"].strip()
        if not case.get("out_of_scope"):
            assert case["expected_document"].endswith(".md")


def test_benchmark_meets_the_reported_thresholds(assistant: AirlineKnowledgeAssistant) -> None:
    """Guards the numbers published in README.md against silent regression."""
    report = assistant.evaluate()
    assert report["retrieval_recall_at_k"] == 100.0
    assert report["answer_accuracy"] == 100.0
    assert report["refusal_accuracy"] == 100.0
    assert report["retrieval_precision_at_1"] >= 90.0
    assert len(report["rows"]) == report["total_cases"]


def test_knowledge_base_summary_covers_every_document(assistant: AirlineKnowledgeAssistant) -> None:
    summary = assistant.knowledge_base_summary()
    assert len(summary) == 7
    assert all(row["chunks"] > 0 and row["words"] > 0 for row in summary)


def test_stats_report_the_active_backend(assistant: AirlineKnowledgeAssistant) -> None:
    stats = assistant.stats
    assert stats["backend"] == "tfidf"
    assert stats["documents"] == 7
    assert stats["chunks"] > 0
