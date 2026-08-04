"""Tests for Muhammad Faozan Mujtaba's AI Meeting Summarizer & Action-Item Extractor."""

from datetime import date

import pytest

from src.modules.meeting_summarizer.engine import (
    MeetingSummarizerEngine,
    list_transcripts,
    parse_transcript,
    read_transcript,
    resolve_deadline,
    split_sentences,
)

# 2026-07-28 is a Tuesday; every relative-date expectation below is anchored to it.
MEETING_DATE = date(2026, 7, 28)


@pytest.fixture(scope="module")
def engine() -> MeetingSummarizerEngine:
    """Provide a single offline engine for the whole module."""
    return MeetingSummarizerEngine()


@pytest.fixture(scope="module")
def sprint_report(engine: MeetingSummarizerEngine):
    """Summarise the bundled sprint review transcript once."""
    return engine.summarize(read_transcript("2026-07-28_sprint14_review.txt"))


# -- transcript parsing --------------------------------------------------------------


def test_parse_transcript_reads_header_and_turns():
    """Header metadata is separated from speaker turns."""
    header, utterances = parse_transcript(
        "Meeting: Weekly Sync\n"
        "Date: 2026-07-28\n"
        "Attendees: Ayesha Rauf (Lead), Bilal Ahmed\n"
        "---\n"
        "Ayesha: Let's begin.\n"
        "Bilal: The build is green.\n"
    )
    assert header["meeting"] == "Weekly Sync"
    assert header["date"] == "2026-07-28"
    assert [u.speaker for u in utterances] == ["Ayesha", "Bilal"]
    assert utterances[1].text == "The build is green."


def test_parse_transcript_handles_timestamps_and_roles():
    """Timestamp prefixes and inline role annotations are stripped from the speaker."""
    _, utterances = parse_transcript("[00:12] Hina Shah (QA Lead): Regression is done.")
    assert utterances[0].speaker == "Hina Shah"
    assert utterances[0].timestamp == "00:12"
    assert utterances[0].text == "Regression is done."


def test_parse_transcript_continues_wrapped_lines():
    """A line that does not open a new turn extends the previous speaker's text."""
    _, utterances = parse_transcript("Ayesha: We closed eleven stories\nand velocity is holding.")
    assert len(utterances) == 1
    assert utterances[0].text == "We closed eleven stories and velocity is holding."


def test_split_sentences_keeps_abbreviations_intact():
    """Common abbreviations do not create spurious sentence breaks."""
    assert split_sentences("Ship it, e.g. on Friday. Then review.") == [
        "Ship it, e.g. on Friday.",
        "Then review.",
    ]


# -- deadline resolution -------------------------------------------------------------


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("send it by tomorrow", "2026-07-29"),
        ("have it ready today", "2026-07-28"),
        ("ship it by Friday", "2026-07-31"),
        ("ship it by next Wednesday", "2026-08-05"),
        ("finish by the end of the week", "2026-07-31"),
        ("done by the end of the month", "2026-07-31"),
        ("deliver in five business days", "2026-08-04"),
        ("deliver within 3 days", "2026-07-31"),
        ("review it in 2 weeks", "2026-08-11"),
        ("submit by 5 August", "2026-08-05"),
        ("submit by August 12", "2026-08-12"),
        ("due 2026-09-01", "2026-09-01"),
        ("due 14/08/2026", "2026-08-14"),
        ("wrap up next week", "2026-08-04"),
    ],
)
def test_resolve_deadline_maps_phrases_to_absolute_dates(phrase: str, expected: str):
    """Relative and explicit deadline phrases resolve against the meeting date."""
    _, resolved = resolve_deadline(phrase, MEETING_DATE)
    assert resolved == expected


def test_resolve_deadline_returns_none_when_no_date_is_stated():
    """A sentence with no deadline yields no phrase and no date."""
    assert resolve_deadline("I'll mirror the config into the vault.", MEETING_DATE) == (None, None)


def test_resolve_deadline_prefers_explicit_weekday_over_vague_week():
    """'By next Wednesday' wins over a co-occurring 'this week' condition."""
    phrase, resolved = resolve_deadline(
        "If the icons land this week I can ship it by next Wednesday.", MEETING_DATE
    )
    assert phrase == "next wednesday"
    assert resolved == "2026-08-05"


def test_resolve_deadline_is_anchored_not_wall_clock():
    """The same sentence resolves differently for two different meeting dates."""
    _, first = resolve_deadline("due by Friday", date(2026, 7, 28))
    _, second = resolve_deadline("due by Friday", date(2026, 8, 4))
    assert (first, second) == ("2026-07-31", "2026-08-07")


# -- extraction ----------------------------------------------------------------------


def test_summarize_populates_every_report_section(sprint_report):
    """A realistic transcript produces a fully populated report."""
    assert sprint_report.title == "Sprint 14 Review - Orchard Foods Portal"
    assert sprint_report.meeting_date == "2026-07-28"
    assert sprint_report.summary
    assert sprint_report.decisions
    assert sprint_report.action_items
    assert sprint_report.blockers


def test_participants_merge_header_names_with_speaker_labels(sprint_report):
    """'Ayesha Rauf' from the header and 'Ayesha' from a turn are one person."""
    assert sprint_report.participants == [
        "Ayesha Rauf",
        "Bilal Ahmed",
        "Hina Shah",
        "Usman Tariq",
        "Danish Iqbal",
    ]


def test_action_items_carry_owner_and_resolved_deadline(sprint_report):
    """The sandbox-credentials commitment is attributed and dated."""
    item = next(a for a in sprint_report.action_items if "sandbox credentials" in a.task.lower())
    assert item.owner == "Bilal Ahmed"
    assert item.deadline_date == "2026-07-29"
    assert item.priority == "High"


def test_first_person_commitment_is_owned_by_its_speaker(sprint_report):
    """'I'll set up…' is owned by whoever said it, in canonical full-name form."""
    item = next(a for a in sprint_report.action_items if "cleanup job" in a.task.lower())
    assert item.owner == "Danish Iqbal"
    assert item.deadline_date == "2026-07-31"


def test_unowned_commitment_is_not_guessed(sprint_report):
    """A task nobody was named for stays Unassigned rather than being attributed."""
    item = next(a for a in sprint_report.action_items if "pnpm migration" in a.task.lower())
    assert item.owner == "Unassigned"


def test_decisions_are_recorded_separately_from_tasks(sprint_report):
    """Settled choices land in the decision list and not in the action list."""
    joined = " ".join(d.decision.lower() for d in sprint_report.decisions)
    assert "sprint 15" in joined
    assert "pnpm" in joined
    assert all("we agreed to move" not in a.task.lower() for a in sprint_report.action_items)


def test_decided_by_uses_canonical_participant_name(sprint_report):
    """Decision attribution matches the participant list, not the bare speaker label."""
    assert all(d.decided_by in sprint_report.participants for d in sprint_report.decisions)


def test_answered_questions_are_not_reported_as_open(engine):
    """A question answered in the next turn is not an open question."""
    report = engine.summarize(
        "Meeting: Quick Sync\nDate: 2026-07-28\n---\n"
        "Ayesha: When does the winter campaign start?\n"
        "Nadia: The eighteenth of November, confirmed.\n",
        meeting_date=MEETING_DATE,
    )
    assert report.open_questions == []


def test_deferred_question_is_reported_as_open(engine):
    """A question the next turn defers is kept as an open question."""
    report = engine.summarize(
        "Meeting: Quick Sync\nDate: 2026-07-28\n---\n"
        "Sana: Do we need a separate data processing agreement for the loyalty data?\n"
        "Nadia: To be decided, our legal team will have a view on that.\n",
        meeting_date=MEETING_DATE,
    )
    assert any("data processing agreement" in q.lower() for q in report.open_questions)


def test_conversational_filler_is_excluded(engine):
    """Greetings and acknowledgements never reach the report body."""
    report = engine.summarize(
        "Meeting: Quick Sync\nDate: 2026-07-28\n---\n"
        "Ayesha: Good morning everyone, let's get started.\n"
        "Bilal: Thanks.\n"
        "Ayesha: I'll send the deployment checklist by Friday.\n",
        meeting_date=MEETING_DATE,
    )
    assert len(report.action_items) == 1
    assert "deployment checklist" in report.action_items[0].task.lower()


def test_empty_transcript_produces_an_empty_report(engine):
    """An empty input degrades gracefully instead of raising."""
    report = engine.summarize("", meeting_date=MEETING_DATE)
    assert report.action_items == []
    assert report.decisions == []
    assert report.stats["turns"] == 0


# -- exports -------------------------------------------------------------------------


def test_markdown_export_contains_every_section(sprint_report):
    """The Markdown minutes carry all four required headings."""
    markdown = sprint_report.to_markdown()
    for heading in ("## Summary", "## Decisions Made", "## Action Items", "## Blockers & Risks"):
        assert heading in markdown
    assert "| # | Action | Owner | Deadline | Priority |" in markdown


def test_json_export_round_trips(sprint_report):
    """The JSON export is valid and preserves the action items."""
    import json

    payload = json.loads(sprint_report.to_json())
    assert payload["meeting_date"] == "2026-07-28"
    assert len(payload["action_items"]) == sprint_report.stats["action_items"]
    assert payload["action_items"][0]["owner"]


def test_html_export_escapes_user_content(engine):
    """Transcript text is escaped so the print-ready export cannot inject markup."""
    report = engine.summarize(
        "Meeting: Quick Sync\nDate: 2026-07-28\n---\n"
        "Ayesha: I'll review the <script>alert(1)</script> report by Friday.\n",
        meeting_date=MEETING_DATE,
    )
    html = report.to_html()
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


# -- benchmark ------------------------------------------------------------------------


def test_bundled_sample_transcripts_are_present():
    """The module ships the three annotated sample meetings."""
    assert len(list_transcripts()) == 3


def test_benchmark_meets_target_accuracy(engine):
    """Extraction holds its documented accuracy on the hand-annotated gold set."""
    result = engine.run_benchmark()
    assert result["transcripts_evaluated"] == 3
    assert result["gold_action_items"] == 16
    assert result["recall_percent"] >= 90.0
    assert result["precision_percent"] >= 85.0
    assert result["owner_accuracy_percent"] >= 90.0
    assert result["deadline_accuracy_percent"] >= 85.0


def test_summarize_is_deterministic(engine):
    """The offline pipeline returns identical output for identical input."""
    transcript = read_transcript("2026-07-30_hiring_sync.txt")
    assert engine.summarize(transcript).to_json() == engine.summarize(transcript).to_json()
