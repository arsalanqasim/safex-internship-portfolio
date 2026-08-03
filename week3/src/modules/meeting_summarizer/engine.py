"""AI Meeting Summarizer & Action-Item Extractor engine.

Week 3 AI Agent Automation Proposal module owned by Muhammad Faozan Mujtaba.
Target company: Meridian Softworks, a fictional software house in Islamabad that runs
sprint reviews, client calls and hiring syncs every week and loses follow-ups between
them.

The engine turns a raw meeting transcript into a structured report containing an
executive summary, the decisions the group settled on, action items carrying an owner
and an absolute calendar deadline, plus blockers and open questions.

It runs fully offline by default (``LLM_PROVIDER=mock``), so the prototype demos with
no API key and no network. When a hosted provider is configured the same prompt
templates in ``prompts.py`` are sent to it, and the deterministic extraction below is
used as the fallback whenever that call is unavailable or fails.
"""

from __future__ import annotations

import calendar
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

from src.modules.meeting_summarizer import prompts

MODULE_DIR = Path(__file__).resolve().parent
TRANSCRIPT_DIR = MODULE_DIR / "data" / "transcripts"
EVALUATION_SET_PATH = MODULE_DIR / "data" / "evaluation_set.json"

TARGET_COMPANY = "Meridian Softworks"

# --------------------------------------------------------------------------------------
# Linguistic cues
# --------------------------------------------------------------------------------------

DECISION_CUES = [
    "decided to", "decided that", "we decided", "we've decided", "we have decided",
    "decision is", "the decision", "we agreed", "we've agreed", "agreed that",
    "agreed to", "we all agree", "let's go with",
    "we'll go with", "we will go with", "we're going with", "going with option",
    "final call", "that's the call", "settled on", "locking in", "lock it in",
    "we approved", "we're approving", "consensus is", "so that's confirmed",
    "confirmed then", "we're standardising on", "we are standardising on",
    "we're standardizing on", "ruled out", "we're dropping",
]

# A sentence only counts as an action item when it pairs a commitment marker with a
# verb that describes real work. "Legal will have a view" carries a marker but no work,
# and would otherwise flood the task list with conversational filler.
COMMITMENT_MARKERS = [
    "will ", "i'll ", "we'll ", "you'll ", "going to ", "action item",
    "take ownership", "takes ownership", "owns ", "assigned to", "responsible for",
    "please ", "can you ", "could you ", "needs to ", "need to ", "has to ",
    "let's have ", "i can ",
]

ACTION_VERBS = [
    "chase", "mirror", "set up", "prepare", "send", "circulate", "draft", "write",
    "review", "schedule", "book", "raise", "open a", "update", "fix", "ship",
    "deploy", "migrate", "document", "audit", "check", "confirm", "share",
    "pick up", "follow up", "circle back", "create", "build", "add", "remove",
    "post", "publish", "sign", "test", "investigate", "clean", "rotate",
    "onboard", "take", "ready", "set-up", "arrange", "collect", "compile",
]

FIRST_PERSON_CUES = ["i'll ", "i will ", "i can ", "i'm going to ", "i am going to ", "let me "]

BLOCKER_CUES = [
    "blocked", "blocker", "at risk", "risk of", "we're stuck", "stuck on",
    "waiting on", "waiting for", "dependency on", "depends on", "bottleneck",
    "can't proceed", "cannot proceed", "slipping", "behind schedule", "delayed",
    "short on", "over budget", "concern is", "worried about", "problem is",
]

# Deferral cues only. Anything actionable ("we need to confirm X") belongs in the
# action-item list instead, so those phrases are deliberately absent here.
OPEN_QUESTION_CUES = [
    "still unclear", "not clear yet", "open question", "tbd", "to be decided",
    "not know yet", "don't know yet", "undecided", "no view on that yet",
]

URGENCY_CUES = ["urgent", "asap", "as soon as possible", "critical", "immediately", "blocker", "escalate"]

# Sentences that are pure meeting noise and never belong in a summary.
NOISE_PATTERNS = [
    r"^(ok|okay|right|cool|great|thanks|thank you|sure|yeah|yep|no worries|sounds good|perfect|agreed)[\.\!]?$",
    r"^(hi|hello|hey|morning|good morning|good afternoon)\b.{0,40}$",
    r"^(can everyone hear me|you're on mute|sorry i'm late|let's get started|let me share my screen).{0,20}$",
]

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fourteen": 14,
    "fifteen": 15, "twenty": 20, "thirty": 30, "a": 1, "a couple of": 2, "a few": 3,
}

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


# --------------------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------------------


@dataclass
class Utterance:
    """A single speaker turn inside a transcript."""

    speaker: str
    text: str
    line_no: int
    timestamp: str | None = None


@dataclass
class ActionItem:
    """A commitment made during the meeting, with an owner and a resolved deadline."""

    task: str
    owner: str
    deadline_phrase: str | None
    deadline_date: str | None
    priority: str
    raised_by: str
    line_no: int


@dataclass
class Decision:
    """A choice the group settled on during the meeting."""

    decision: str
    decided_by: str
    line_no: int


@dataclass
class MeetingReport:
    """The full structured output produced for one transcript."""

    title: str
    meeting_date: str
    participants: list[str]
    summary: str
    key_points: list[str]
    decisions: list[Decision]
    action_items: list[ActionItem]
    blockers: list[str]
    open_questions: list[str]
    topics: list[str]
    provider: str
    stats: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Return the report as plain JSON-serialisable data."""
        return {
            "title": self.title,
            "meeting_date": self.meeting_date,
            "participants": self.participants,
            "summary": self.summary,
            "key_points": self.key_points,
            "decisions": [asdict(d) for d in self.decisions],
            "action_items": [asdict(a) for a in self.action_items],
            "blockers": self.blockers,
            "open_questions": self.open_questions,
            "topics": self.topics,
            "provider": self.provider,
            "stats": self.stats,
        }

    def to_json(self) -> str:
        """Serialise the report to indented JSON."""
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        """Render the report as a clean Markdown minutes document."""
        participant_line = ", ".join(self.participants) if self.participants else "Not identified"
        lines: list[str] = [
            f"# {self.title}",
            "",
            f"**Company:** {TARGET_COMPANY}  ",
            f"**Date:** {self.meeting_date}  ",
            f"**Participants:** {participant_line}  ",
            f"**Generated by:** AI Meeting Summarizer (provider: `{self.provider}`)",
            "",
            "---",
            "",
            "## Summary",
            "",
            self.summary or "_No summary could be produced from this transcript._",
            "",
        ]

        if self.key_points:
            lines += ["### Key Points", ""]
            lines += [f"- {point}" for point in self.key_points]
            lines.append("")

        lines += ["## Decisions Made", ""]
        if self.decisions:
            for idx, decision in enumerate(self.decisions, start=1):
                lines.append(f"{idx}. {decision.decision} — _{decision.decided_by}_")
        else:
            lines.append("_No explicit decisions were recorded._")
        lines.append("")

        lines += ["## Action Items", ""]
        if self.action_items:
            lines += [
                "| # | Action | Owner | Deadline | Priority |",
                "|---|---|---|---|---|",
            ]
            for idx, item in enumerate(self.action_items, start=1):
                if item.deadline_date and item.deadline_phrase:
                    deadline = f"{item.deadline_date} ({item.deadline_phrase})"
                else:
                    deadline = item.deadline_date or item.deadline_phrase or "—"
                lines.append(f"| {idx} | {item.task} | {item.owner} | {deadline} | {item.priority} |")
        else:
            lines.append("_No action items were assigned._")
        lines.append("")

        if self.blockers:
            lines += ["## Blockers & Risks", ""]
            lines += [f"- {b}" for b in self.blockers]
            lines.append("")

        if self.open_questions:
            lines += ["## Open Questions", ""]
            lines += [f"- {q}" for q in self.open_questions]
            lines.append("")

        return "\n".join(lines)

    def to_html(self) -> str:
        """Render a print-ready HTML document (browser 'Save as PDF' produces the PDF)."""
        def rows() -> str:
            if not self.action_items:
                return '<tr><td colspan="5" class="empty">No action items were assigned.</td></tr>'
            out = []
            for idx, item in enumerate(self.action_items, start=1):
                deadline = item.deadline_date or item.deadline_phrase or "—"
                out.append(
                    f"<tr><td>{idx}</td><td>{escape(item.task)}</td><td>{escape(item.owner)}</td>"
                    f"<td>{escape(str(deadline))}</td>"
                    f'<td><span class="pill pill--{item.priority.lower()}">{escape(item.priority)}</span></td></tr>'
                )
            return "".join(out)

        def bullets(items: list[str], empty: str) -> str:
            if not items:
                return f'<p class="empty">{empty}</p>'
            return "<ul>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"

        if self.decisions:
            decisions_html = "<ol>" + "".join(
                f"<li>{escape(d.decision)} <em>&mdash; {escape(d.decided_by)}</em></li>"
                for d in self.decisions
            ) + "</ol>"
        else:
            decisions_html = '<p class="empty">No explicit decisions were recorded.</p>'

        participant_line = ", ".join(self.participants) if self.participants else "Not identified"

        return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<title>{escape(self.title)} — Meeting Minutes</title>
<style>
  @page {{ margin: 18mm; }}
  body {{ font-family: Inter, "Segoe UI", system-ui, sans-serif; color: #172033; max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.55; }}
  h1 {{ font-size: 1.6rem; margin-bottom: .25rem; }}
  h2 {{ font-size: 1.1rem; margin-top: 2rem; border-bottom: 1px solid #dce3ec; padding-bottom: .35rem; }}
  .meta {{ color: #64748b; font-size: .9rem; margin-bottom: 1.5rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
  th, td {{ border: 1px solid #dce3ec; padding: .5rem .6rem; text-align: left; vertical-align: top; }}
  th {{ background: #f6f8fb; font-weight: 650; }}
  .pill {{ display: inline-block; padding: .1rem .5rem; border-radius: 999px; font-size: .75rem; font-weight: 650; }}
  .pill--high {{ background: #fee2e2; color: #991b1b; }}
  .pill--medium {{ background: #fef3c7; color: #92400e; }}
  .pill--low {{ background: #e6f5f2; color: #0b5e58; }}
  .empty {{ color: #94a3b8; font-style: italic; }}
</style></head>
<body>
  <h1>{escape(self.title)}</h1>
  <div class="meta">
    {escape(TARGET_COMPANY)} &middot; {escape(self.meeting_date)}<br/>
    Participants: {escape(participant_line)}<br/>
    Generated by AI Meeting Summarizer (provider: {escape(self.provider)})
  </div>
  <h2>Summary</h2>
  <p>{escape(self.summary)}</p>
  {bullets(self.key_points, "No key points extracted.")}
  <h2>Decisions Made</h2>
  {decisions_html}
  <h2>Action Items</h2>
  <table>
    <thead><tr><th>#</th><th>Action</th><th>Owner</th><th>Deadline</th><th>Priority</th></tr></thead>
    <tbody>{rows()}</tbody>
  </table>
  <h2>Blockers &amp; Risks</h2>
  {bullets(self.blockers, "None raised.")}
  <h2>Open Questions</h2>
  {bullets(self.open_questions, "None recorded.")}
</body></html>"""


# --------------------------------------------------------------------------------------
# Transcript parsing
# --------------------------------------------------------------------------------------

_HEADER_RE = re.compile(r"^(meeting|title|date|attendees|participants)\s*:\s*(.+)$", re.IGNORECASE)
_SPEAKER_RE = re.compile(
    r"^\s*(?:\[(?P<ts>[0-9:]{4,8})\]\s*)?(?P<speaker>[A-Z][\w'.-]*(?:\s+[A-Z][\w'.-]*){0,2})"
    r"(?:\s*\([^)]{0,40}\))?\s*:\s*(?P<text>.+)$"
)


def parse_transcript(raw_text: str) -> tuple[dict[str, str], list[Utterance]]:
    """Split a raw transcript into its header metadata and an ordered list of turns.

    Supports ``Speaker: text``, ``[00:12] Speaker: text`` and ``Speaker (Role): text``.
    Lines that do not start a new turn are appended to the previous speaker's text.
    """
    header: dict[str, str] = {}
    utterances: list[Utterance] = []

    for line_no, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or set(line) <= {"-", "=", "_"}:
            continue

        if not utterances:
            header_match = _HEADER_RE.match(line)
            if header_match:
                header[header_match.group(1).lower()] = header_match.group(2).strip()
                continue

        speaker_match = _SPEAKER_RE.match(line)
        if speaker_match:
            utterances.append(
                Utterance(
                    speaker=speaker_match.group("speaker").strip(),
                    text=speaker_match.group("text").strip(),
                    line_no=line_no,
                    timestamp=speaker_match.group("ts"),
                )
            )
        elif utterances:
            utterances[-1].text = f"{utterances[-1].text} {line}"
        else:
            utterances.append(Utterance(speaker="Unknown", text=line, line_no=line_no))

    return header, utterances


def split_sentences(text: str) -> list[str]:
    """Split a block of speech into sentences, keeping common abbreviations intact."""
    protected = re.sub(r"\b(e\.g|i\.e|etc|vs|Mr|Ms|Dr|approx)\.", r"\1<DOT>", text, flags=re.IGNORECASE)
    parts = re.split(r"(?<=[.!?])\s+", protected)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def _is_noise(sentence: str) -> bool:
    """Return True for filler sentences that carry no meeting content."""
    lowered = sentence.strip().lower()
    if len(lowered.split()) < 4:
        return True
    return any(re.match(pattern, lowered) for pattern in NOISE_PATTERNS)


# --------------------------------------------------------------------------------------
# Deadline resolution
# --------------------------------------------------------------------------------------


def _add_business_days(start: date, count: int) -> date:
    """Advance a date by whole business days, skipping Saturdays and Sundays."""
    current = start
    remaining = count
    while remaining > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            remaining -= 1
    return current


def _end_of_month(anchor: date, months_ahead: int = 0) -> date:
    """Return the last calendar day of the month ``months_ahead`` from the anchor."""
    month = anchor.month + months_ahead
    year = anchor.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return date(year, month, calendar.monthrange(year, month)[1])


def _as_count(token: str) -> int:
    """Read a duration written either as digits or as an English number word."""
    return int(token) if token.isdigit() else NUMBER_WORDS.get(token, 1)


def _next_weekday(anchor: date, weekday: int, force_future: bool = False) -> date:
    """Return the next occurrence of ``weekday`` on or after the anchor date."""
    delta = (weekday - anchor.weekday()) % 7
    if delta == 0 and force_future:
        delta = 7
    return anchor + timedelta(days=delta)


def _weekday_in_next_week(anchor: date, weekday: int) -> date:
    """Return ``weekday`` as it falls in the calendar week after the anchor.

    "Next Wednesday" said on a Tuesday means the Wednesday of the following week, not
    tomorrow, so relative weekday phrases prefixed with "next" resolve against the
    start of the next Monday-to-Sunday week rather than against the anchor day.
    """
    start_of_next_week = anchor + timedelta(days=7 - anchor.weekday())
    return start_of_next_week + timedelta(days=weekday)


def resolve_deadline(text: str, meeting_date: date) -> tuple[str | None, str | None]:
    """Find a deadline in ``text`` and resolve it to an absolute calendar date.

    Returns ``(phrase_as_spoken, iso_date)``. Both elements are ``None`` when the
    sentence states no deadline. Relative phrases resolve against the meeting date and
    never against "today", so re-running the engine on an old transcript reproduces the
    same output. "Next <weekday>" is read as the next strictly-future occurrence.
    """
    lowered = text.lower()

    iso_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", lowered)
    if iso_match:
        try:
            found = date(int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3)))
            return iso_match.group(0), found.isoformat()
        except ValueError:
            pass

    dmy_match = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", lowered)
    if dmy_match:
        try:
            found = date(int(dmy_match.group(3)), int(dmy_match.group(2)), int(dmy_match.group(1)))
            return dmy_match.group(0), found.isoformat()
        except ValueError:
            pass

    month_names = "|".join(MONTHS.keys())
    month_first = re.search(rf"\b({month_names})\s+(\d{{1,2}})(?:st|nd|rd|th)?\b", lowered)
    day_first = re.search(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+(?:of\s+)?({month_names})\b", lowered)
    if month_first or day_first:
        if month_first:
            month, day, phrase = MONTHS[month_first.group(1)], int(month_first.group(2)), month_first.group(0)
        else:
            month, day, phrase = MONTHS[day_first.group(2)], int(day_first.group(1)), day_first.group(0)
        for year in (meeting_date.year, meeting_date.year + 1):
            try:
                found = date(year, month, day)
            except ValueError:
                break
            if found >= meeting_date:
                return phrase, found.isoformat()

    # An explicit "by/next/this <weekday>" is a stronger deadline signal than a vague
    # "this week", and can co-occur with one ("if the icons land this week I can ship
    # it by next Wednesday"), so it is resolved first.
    weekday_match = re.search(rf"\b(next|this|by|before|on)\s+({'|'.join(WEEKDAYS)})\b", lowered)
    if weekday_match:
        target = WEEKDAYS[weekday_match.group(2)]
        if weekday_match.group(1) == "next":
            return weekday_match.group(0), _weekday_in_next_week(meeting_date, target).isoformat()
        return weekday_match.group(0), _next_weekday(meeting_date, target).isoformat()

    relative_checks: list[tuple[str, date]] = [
        ("day after tomorrow", meeting_date + timedelta(days=2)),
        ("end of next month", _end_of_month(meeting_date, 1)),
        ("end of the month", _end_of_month(meeting_date)),
        ("end of month", _end_of_month(meeting_date)),
        ("eom", _end_of_month(meeting_date)),
        ("end of the week", _next_weekday(meeting_date, 4)),
        ("end of week", _next_weekday(meeting_date, 4)),
        ("eow", _next_weekday(meeting_date, 4)),
        ("by the weekend", _next_weekday(meeting_date, 4)),
        ("end of the sprint", _next_weekday(meeting_date, 4, force_future=True)),
        ("end of day", meeting_date),
        ("eod", meeting_date),
        ("tomorrow", meeting_date + timedelta(days=1)),
        ("tonight", meeting_date),
        ("today", meeting_date),
        ("next week", meeting_date + timedelta(days=7)),
        ("this week", _next_weekday(meeting_date, 4)),
    ]
    for phrase, resolved in relative_checks:
        if re.search(rf"\b{re.escape(phrase)}\b", lowered):
            return phrase, resolved.isoformat()

    # Durations are spoken as often as they are written ("in five business days").
    count = rf"(\d{{1,2}}|{'|'.join(NUMBER_WORDS)})"

    business_match = re.search(rf"\b(?:in|within)\s+{count}\s+(?:business|working)\s+days?\b", lowered)
    if business_match:
        amount = _as_count(business_match.group(1))
        return business_match.group(0), _add_business_days(meeting_date, amount).isoformat()

    days_match = re.search(rf"\b(?:in|within)\s+{count}\s+days?\b", lowered)
    if days_match:
        amount = _as_count(days_match.group(1))
        return days_match.group(0), (meeting_date + timedelta(days=amount)).isoformat()

    weeks_match = re.search(rf"\b(?:in|within)\s+{count}\s+weeks?\b", lowered)
    if weeks_match:
        amount = _as_count(weeks_match.group(1))
        return weeks_match.group(0), (meeting_date + timedelta(weeks=amount)).isoformat()

    ordinal_match = re.search(r"\bby the (\d{1,2})(?:st|nd|rd|th)\b", lowered)
    if ordinal_match:
        day = int(ordinal_match.group(1))
        for months_ahead in (0, 1):
            month = meeting_date.month + months_ahead
            year = meeting_date.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            if day <= calendar.monthrange(year, month)[1]:
                found = date(year, month, day)
                if found >= meeting_date:
                    return ordinal_match.group(0), found.isoformat()

    bare_weekday = re.search(rf"\b({'|'.join(WEEKDAYS)})\b", lowered)
    if bare_weekday:
        return bare_weekday.group(0), _next_weekday(meeting_date, WEEKDAYS[bare_weekday.group(1)]).isoformat()

    return None, None


# --------------------------------------------------------------------------------------
# LLM providers
# --------------------------------------------------------------------------------------


class MockLLMProvider:
    """Default offline provider.

    The prototype must demo without an API key, so the "model" here is the
    deterministic extraction pipeline in :class:`MeetingSummarizerEngine`. This class
    exists to keep the provider seam honest: swapping in a hosted model changes only
    which provider is constructed, not the report contract.
    """

    name = "mock"
    available = True

    def complete(self, prompt: str, system: str = "") -> str | None:
        """Return ``None`` so the engine falls through to rule-based extraction."""
        return None


class GeminiProvider:
    """Google Gemini backend, used only when a key is present in the environment."""

    name = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash") -> None:
        self.api_key = api_key
        self.model = model

    @property
    def available(self) -> bool:
        """Report whether the SDK is importable and a key was supplied."""
        try:
            import google.generativeai  # noqa: F401
        except ImportError:
            return False
        return bool(self.api_key)

    def complete(self, prompt: str, system: str = "") -> str | None:
        """Send one prompt to Gemini, returning ``None`` on any failure."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model, system_instruction=system or None)
            return model.generate_content(prompt).text
        except Exception:
            return None


def build_provider(provider_name: str | None = None) -> MockLLMProvider | GeminiProvider:
    """Select a provider from the environment, always falling back to the mock one."""
    choice = (provider_name or os.getenv("LLM_PROVIDER", "mock")).strip().lower()
    if choice == "gemini":
        candidate = GeminiProvider(os.getenv("GEMINI_API_KEY", ""))
        if candidate.available:
            return candidate
    return MockLLMProvider()


# --------------------------------------------------------------------------------------
# Engine
# --------------------------------------------------------------------------------------


class MeetingSummarizerEngine:
    """Extract a structured meeting report from a raw transcript."""

    def __init__(
        self,
        provider: MockLLMProvider | GeminiProvider | None = None,
        summary_sentences: int = 4,
    ) -> None:
        self.provider = provider or build_provider()
        self.summary_sentences = summary_sentences

    # -- public API ---------------------------------------------------------------

    def summarize(
        self,
        raw_transcript: str,
        meeting_date: date | None = None,
        title: str | None = None,
    ) -> MeetingReport:
        """Produce the full structured report for one transcript."""
        header, utterances = parse_transcript(raw_transcript)

        resolved_date = meeting_date or self._header_date(header) or date.today()
        resolved_title = title or header.get("meeting") or header.get("title") or "Untitled Meeting"
        participants = self._participants(header, utterances)

        decisions = self._extract_decisions(utterances, participants)
        action_items = self._extract_action_items(utterances, participants, resolved_date)
        blockers = self._extract_by_cue(utterances, BLOCKER_CUES, participants)
        open_questions = self._extract_open_questions(utterances, participants)
        key_points = self._rank_sentences(utterances, limit=self.summary_sentences)
        topics = self._extract_topics(utterances)
        summary = self._compose_summary(
            resolved_title, resolved_date, participants, key_points, decisions, action_items
        )

        return MeetingReport(
            title=resolved_title,
            meeting_date=resolved_date.isoformat(),
            participants=participants,
            summary=summary,
            key_points=key_points,
            decisions=decisions,
            action_items=action_items,
            blockers=blockers,
            open_questions=open_questions,
            topics=topics,
            provider=self.provider.name,
            stats={
                "turns": len(utterances),
                "participants": len(participants),
                "decisions": len(decisions),
                "action_items": len(action_items),
                "action_items_with_owner": sum(1 for a in action_items if a.owner != "Unassigned"),
                "action_items_with_deadline": sum(1 for a in action_items if a.deadline_date),
                "blockers": len(blockers),
                "open_questions": len(open_questions),
            },
        )

    def run_benchmark(self) -> dict:
        """Score extraction against the hand-annotated evaluation set.

        A gold action item counts as recalled when a produced item covers at least half
        of its keywords; owner and deadline accuracy are then measured over those
        matched pairs only.
        """
        gold_cases = load_evaluation_set()
        results: list[dict] = []
        total_gold = total_predicted = total_matched = 0
        owner_correct = deadline_correct = 0

        for case in gold_cases:
            transcript = read_transcript(case["transcript"])
            report = self.summarize(transcript, meeting_date=date.fromisoformat(case["meeting_date"]))

            gold_items = case["expected_action_items"]
            unclaimed = list(report.action_items)
            matched_pairs: list[tuple[dict, ActionItem]] = []

            for gold in gold_items:
                best = self._best_match(gold["task_keywords"], unclaimed)
                if best is not None:
                    matched_pairs.append((gold, best))
                    unclaimed.remove(best)

            case_owner_ok = sum(1 for g, p in matched_pairs if p.owner == g["owner"])
            case_deadline_ok = sum(1 for g, p in matched_pairs if p.deadline_date == g["deadline_date"])

            total_gold += len(gold_items)
            total_predicted += len(report.action_items)
            total_matched += len(matched_pairs)
            owner_correct += case_owner_ok
            deadline_correct += case_deadline_ok

            results.append({
                "transcript": case["transcript"],
                "meeting": report.title,
                "gold_action_items": len(gold_items),
                "extracted_action_items": len(report.action_items),
                "matched": len(matched_pairs),
                "owner_correct": case_owner_ok,
                "deadline_correct": case_deadline_ok,
                "decisions_found": len(report.decisions),
                "gold_decisions": case["expected_decision_count"],
            })

        recall = (total_matched / total_gold * 100) if total_gold else 0.0
        precision = (total_matched / total_predicted * 100) if total_predicted else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        return {
            "transcripts_evaluated": len(gold_cases),
            "gold_action_items": total_gold,
            "extracted_action_items": total_predicted,
            "matched_action_items": total_matched,
            "recall_percent": round(recall, 2),
            "precision_percent": round(precision, 2),
            "f1_percent": round(f1, 2),
            "owner_accuracy_percent": round(owner_correct / total_matched * 100, 2) if total_matched else 0.0,
            "deadline_accuracy_percent": round(deadline_correct / total_matched * 100, 2) if total_matched else 0.0,
            "per_transcript": results,
        }

    # -- extraction internals -----------------------------------------------------

    @staticmethod
    def _header_date(header: dict[str, str]) -> date | None:
        """Read the meeting date out of the transcript header, if it carries one."""
        raw = header.get("date")
        if not raw:
            return None
        for fmt in ("%Y-%m-%d", "%d %B %Y", "%B %d, %Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(raw.strip(), fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _participants(header: dict[str, str], utterances: list[Utterance]) -> list[str]:
        """Collect participants from the header and from every speaker label seen.

        Header attendees are full names while speaker labels are usually first names
        only, so entries sharing a first name are merged and the fuller form kept.
        """
        names: list[str] = []

        def remember(candidate: str) -> None:
            cleaned = re.sub(r"\([^)]*\)", "", candidate).strip(" .,-")
            if not cleaned:
                return
            key = cleaned.split()[0].lower()
            for idx, existing in enumerate(names):
                if existing.split()[0].lower() == key:
                    if len(cleaned.split()) > len(existing.split()):
                        names[idx] = cleaned
                    return
            names.append(cleaned)

        # Strip role parentheticals before splitting, so "Nadia Sheikh (Orchard Foods,
        # Head of Digital)" does not break into two people on the inner comma.
        declared = re.sub(r"\([^)]*\)", "", header.get("attendees") or header.get("participants") or "")
        for chunk in re.split(r"[,;]", declared):
            remember(chunk)
        for utterance in utterances:
            if utterance.speaker != "Unknown":
                remember(utterance.speaker)
        return names

    @staticmethod
    def _canonical(name: str, participants: list[str]) -> str:
        """Expand a bare speaker label to the fullest known form of that person's name."""
        key = name.split()[0].lower() if name.split() else ""
        for participant in participants:
            if participant.split()[0].lower() == key:
                return participant
        return name

    def _extract_decisions(self, utterances: list[Utterance], participants: list[str]) -> list[Decision]:
        """Pull sentences that record a settled decision."""
        found: list[Decision] = []
        seen: set[str] = set()
        for utterance in utterances:
            for sentence in split_sentences(utterance.text):
                lowered = sentence.lower()
                if not any(cue in lowered for cue in DECISION_CUES):
                    continue
                if sentence.endswith("?") or _is_noise(sentence):
                    continue
                # "To be decided, finance has not signed off" reads as a decision cue
                # but records the absence of one.
                if any(cue in lowered for cue in OPEN_QUESTION_CUES):
                    continue
                if re.search(
                    r"\b(?:not|never|hasn't|haven't|hasnt|havent)\s+(?:yet\s+)?(?:been\s+)?"
                    r"(?:signed|approved|agreed|decided|confirmed)\b",
                    lowered,
                ):
                    continue
                cleaned = self._clean(sentence)
                fingerprint = cleaned.lower()
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                found.append(
                    Decision(
                        decision=cleaned,
                        decided_by=self._canonical(utterance.speaker, participants),
                        line_no=utterance.line_no,
                    )
                )
        return found

    def _extract_action_items(
        self,
        utterances: list[Utterance],
        participants: list[str],
        meeting_date: date,
    ) -> list[ActionItem]:
        """Pull commitments, resolving an owner and an absolute deadline for each."""
        found: list[ActionItem] = []
        seen: set[str] = set()

        for utterance in utterances:
            for sentence in split_sentences(utterance.text):
                lowered = sentence.lower()
                if sentence.endswith("?") or _is_noise(sentence):
                    continue
                if not any(marker in lowered for marker in COMMITMENT_MARKERS):
                    continue
                if not any(verb in lowered for verb in ACTION_VERBS):
                    continue
                # A settled decision belongs in its own section, not in the task list,
                # unless it also carries an explicit commitment.
                if any(cue in lowered for cue in DECISION_CUES) and not any(
                    marker in lowered for marker in ("will ", "i'll ", "action item")
                ):
                    continue

                phrase, deadline = resolve_deadline(sentence, meeting_date)
                task = self._to_task_phrase(self._clean(sentence), participants)
                fingerprint = task.lower()
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)

                found.append(
                    ActionItem(
                        task=task,
                        owner=self._resolve_owner(sentence, utterance.speaker, participants),
                        deadline_phrase=phrase,
                        deadline_date=deadline,
                        priority=self._priority(lowered, deadline, meeting_date),
                        raised_by=self._canonical(utterance.speaker, participants),
                        line_no=utterance.line_no,
                    )
                )
        return found

    @classmethod
    def _resolve_owner(cls, sentence: str, speaker: str, participants: list[str]) -> str:
        """Decide who owns a commitment, preferring an explicitly named person."""
        lowered = sentence.lower()
        first_names = {p.split()[0].lower(): p for p in participants if p}
        speaker_name = cls._canonical(speaker, participants)

        explicit = re.search(
            r"\b(?:assigned to|over to|hand(?:ed)? to|owner is)\s+([A-Za-z][\w'-]*)", lowered
        )
        if explicit and explicit.group(1) in first_names:
            return first_names[explicit.group(1)]

        # "<Name> will ...", "<Name> to ...", "<Name>, please ..."
        for name_key, full_name in first_names.items():
            pattern = (
                rf"\b{re.escape(name_key)}\b\s*,?\s*"
                r"(?:will|to|can|should|is going to|needs to|please|owns|takes)\b"
            )
            if re.search(pattern, lowered):
                return full_name

        if any(cue in lowered for cue in FIRST_PERSON_CUES):
            return speaker_name

        others = [
            full for key, full in first_names.items()
            if re.search(rf"\b{re.escape(key)}\b", lowered) and full != speaker_name
        ]

        if re.search(r"\b(?:can|could|would)\s+you\b|^please\b|\bplease\s+(?:can\s+)?you\b", lowered):
            return others[0] if len(others) == 1 else "Unassigned"

        if len(others) == 1:
            return others[0]

        if re.search(r"\bwe(?:'ll| will)\b", lowered):
            return "Unassigned"

        return speaker_name

    @staticmethod
    def _to_task_phrase(sentence: str, participants: list[str]) -> str:
        """Rewrite a spoken commitment as an imperative task.

        "I'll chase Orchard for credentials so QA is not idle" becomes "Chase Orchard
        for credentials". The owner is already captured in its own field, and the
        trailing justification is not part of the work.
        """
        first_names = "|".join(re.escape(p.split()[0]) for p in participants if p) or r"\bnope\b"
        preambles = [
            r"^(?:i'll|i will|i can|i'm going to|i am going to|let me)\s+",
            r"^(?:we'll|we will|we need to|we have to)\s+",
            rf"^(?:{first_names})\s*,?\s*(?:will|to|can|should|is going to|needs to|please)\s+",
            r"^(?:please|can you|could you|would you)\s+",
            r"^(?:let's have|action item:?)\s+",
        ]
        task = sentence
        for pattern in preambles:
            task = re.sub(pattern, "", task, flags=re.IGNORECASE)

        # Drop trailing justification, which explains the task rather than defining it.
        task = re.split(r",?\s+(?:so that|so this|so we are|so we're|because)\s+", task, maxsplit=1)[0]
        task = task.strip().rstrip(".,;") or sentence
        return task[0].upper() + task[1:]

    @staticmethod
    def _priority(lowered: str, deadline: str | None, meeting_date: date) -> str:
        """Grade urgency from explicit language first, then deadline proximity."""
        if any(cue in lowered for cue in URGENCY_CUES):
            return "High"
        if deadline:
            days_out = (date.fromisoformat(deadline) - meeting_date).days
            if days_out <= 2:
                return "High"
            if days_out <= 7:
                return "Medium"
            return "Low"
        return "Medium"

    def _extract_by_cue(
        self, utterances: list[Utterance], cues: list[str], participants: list[str]
    ) -> list[str]:
        """Collect distinct sentences matching any of the supplied cue phrases."""
        found: list[str] = []
        seen: set[str] = set()
        for utterance in utterances:
            for sentence in split_sentences(utterance.text):
                lowered = sentence.lower()
                if not any(cue in lowered for cue in cues) or _is_noise(sentence):
                    continue
                # "That is a genuine blocker" restates the previous speaker rather than
                # describing one, so cue sentences need enough substance to stand alone.
                if len(sentence.split()) < 6:
                    continue
                cleaned = f"{self._clean(sentence)} ({self._canonical(utterance.speaker, participants)})"
                if cleaned.lower() in seen:
                    continue
                seen.add(cleaned.lower())
                found.append(cleaned)
        return found

    def _extract_open_questions(self, utterances: list[Utterance], participants: list[str]) -> list[str]:
        """Collect questions the meeting left unresolved, plus explicit deferrals.

        A question mark alone is not enough: most questions in a meeting get answered
        in the very next breath. A question is only "open" when the reply that follows
        defers it, so the next turn is inspected before the question is kept.
        """
        found: list[str] = []
        seen: set[str] = set()

        def remember(sentence: str, speaker: str) -> None:
            cleaned = f"{self._clean(sentence)} ({self._canonical(speaker, participants)})"
            if cleaned.lower() in seen:
                return
            seen.add(cleaned.lower())
            found.append(cleaned)

        for index, utterance in enumerate(utterances):
            following = " ".join(u.text.lower() for u in utterances[index + 1: index + 3])
            for sentence in split_sentences(utterance.text):
                lowered = sentence.lower()

                if any(cue in lowered for cue in OPEN_QUESTION_CUES) and len(sentence.split()) >= 5:
                    remember(sentence, utterance.speaker)
                    continue

                if not sentence.endswith("?") or len(sentence.split()) < 6:
                    continue
                # A directed request ("can you send it?") is a task, not an open question.
                if re.search(r"\b(?:can|could|would|will)\s+you\b|\bplease\b", lowered):
                    continue
                if any(cue in following for cue in OPEN_QUESTION_CUES):
                    remember(sentence, utterance.speaker)

        return found

    def _rank_sentences(self, utterances: list[Utterance], limit: int) -> list[str]:
        """Score content sentences with TF-IDF and return the strongest, in order.

        Short reactions ("I want to flag a problem") score well on a length-normalised
        TF-IDF but say nothing, so candidates must clear a word floor and the length
        penalty is deliberately mild.
        """
        candidates: list[str] = []
        for utterance in utterances:
            for sentence in split_sentences(utterance.text):
                if _is_noise(sentence) or sentence.endswith("?"):
                    continue
                if len(sentence.split()) < 8:
                    continue
                candidates.append(self._clean(sentence))

        if len(candidates) <= limit:
            return candidates

        try:
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            matrix = vectorizer.fit_transform(candidates)
        except ValueError:
            return candidates[:limit]

        scores = matrix.sum(axis=1).A1 / (matrix.getnnz(axis=1) ** 0.35 + 1e-9)
        strongest = sorted(range(len(candidates)), key=lambda i: scores[i], reverse=True)[:limit]
        return [candidates[i] for i in sorted(strongest)]

    @staticmethod
    def _extract_topics(utterances: list[Utterance], limit: int = 8) -> list[str]:
        """Surface the dominant terms of the meeting as a topic list."""
        corpus = [u.text for u in utterances if u.text.strip()]
        if not corpus:
            return []
        try:
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=400)
            matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            return []
        weights = matrix.sum(axis=0).A1
        names = vectorizer.get_feature_names_out()
        ranked = sorted(zip(names, weights), key=lambda pair: pair[1], reverse=True)
        return [name for name, _ in ranked[:limit]]

    def _compose_summary(
        self,
        title: str,
        meeting_date: date,
        participants: list[str],
        key_points: list[str],
        decisions: list[Decision],
        action_items: list[ActionItem],
    ) -> str:
        """Build the narrative summary, delegating to the LLM when one is configured."""
        llm_text = self.provider.complete(
            prompts.SUMMARY_PROMPT.format(
                title=title,
                meeting_date=meeting_date.isoformat(),
                participants=", ".join(participants),
                max_sentences=self.summary_sentences,
                transcript=" ".join(key_points),
            ),
            system=prompts.SYSTEM_PROMPT,
        )
        if llm_text:
            return llm_text.strip()

        if len(participants) > 1:
            attendee_text = f"{', '.join(participants[:-1])} and {participants[-1]}"
        elif participants:
            attendee_text = participants[0]
        else:
            attendee_text = "the team"

        opening = f"{title} was held on {meeting_date.strftime('%d %B %Y')} with {attendee_text}. "
        closing = (
            f" The meeting produced {len(decisions)} recorded "
            f"{'decision' if len(decisions) == 1 else 'decisions'} and "
            f"{len(action_items)} action {'item' if len(action_items) == 1 else 'items'}."
        )
        return (opening + " ".join(key_points) + closing).strip()

    @staticmethod
    def _clean(sentence: str) -> str:
        """Tidy a raw spoken sentence into something readable in a report."""
        cleaned = re.sub(r"\s+", " ", sentence).strip()
        cleaned = re.sub(
            r"^(so|ok|okay|right|well|and|but|um|uh|yeah|alright)[,\s]+", "", cleaned, flags=re.IGNORECASE
        )
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
        return cleaned

    @staticmethod
    def _best_match(keywords: list[str], candidates: list[ActionItem]) -> ActionItem | None:
        """Find the produced action item that best covers a gold item's keywords."""
        needed = max(1, (len(keywords) + 1) // 2)
        best: ActionItem | None = None
        best_hits = 0
        for candidate in candidates:
            lowered = candidate.task.lower()
            hits = sum(1 for keyword in keywords if keyword.lower() in lowered)
            if hits >= needed and hits > best_hits:
                best, best_hits = candidate, hits
        return best


# --------------------------------------------------------------------------------------
# Sample data helpers
# --------------------------------------------------------------------------------------


def list_transcripts() -> list[str]:
    """Return the filenames of the bundled sample transcripts."""
    if not TRANSCRIPT_DIR.exists():
        return []
    return sorted(path.name for path in TRANSCRIPT_DIR.glob("*.txt"))


def read_transcript(filename: str) -> str:
    """Read one bundled sample transcript by filename."""
    return (TRANSCRIPT_DIR / filename).read_text(encoding="utf-8")


def load_evaluation_set() -> list[dict]:
    """Load the hand-annotated gold standard used by :meth:`run_benchmark`."""
    if not EVALUATION_SET_PATH.exists():
        return []
    return json.loads(EVALUATION_SET_PATH.read_text(encoding="utf-8"))["cases"]
