"""Prompt templates for the AI Meeting Summarizer & Action-Item Extractor.

These templates are the contract between the transcript and whichever LLM backend is
configured. They are kept in their own module so they can be reviewed, versioned and
documented independently of the extraction code, and so the Week 3 prompt-template
deliverable points at real executable source rather than a copy in a markdown file.

Every template is a ``str.format`` style template. Placeholders are documented in the
``PROMPT_VARIABLES`` mapping below.
"""

from __future__ import annotations

PROMPT_VERSION = "1.0.0"

SYSTEM_PROMPT = """You are a precise meeting-notes analyst for Meridian Softworks, a \
software house in Islamabad. You convert raw meeting transcripts into structured, \
factual records.

Hard rules:
1. Never invent information. If a detail is not in the transcript, omit it.
2. An action item must have a real owner named in the transcript. If nobody was \
named, mark the owner as "Unassigned" rather than guessing.
3. Resolve relative deadlines ("by Friday", "end of the month") into absolute \
calendar dates using the supplied meeting date. If no deadline was stated, return null.
4. Preserve the speaker's intent. Do not soften commitments or escalate suggestions \
into decisions.
5. A decision is something the group settled. A suggestion that was not agreed to is \
not a decision.
6. Return valid JSON only. No prose outside the JSON object."""

SUMMARY_PROMPT = """Summarise the following meeting transcript.

Meeting title: {title}
Meeting date: {meeting_date}
Participants: {participants}

Produce a factual executive summary of at most {max_sentences} sentences. Cover what \
was discussed and where the meeting landed. Do not list action items here.

TRANSCRIPT:
{transcript}

Return JSON: {{"summary": "<text>", "key_points": ["<point>", ...]}}"""

DECISION_PROMPT = """Extract the decisions made in the following meeting transcript.

A decision is a choice the group settled on. Ignore options that were raised but not \
agreed to, and ignore action items (those are extracted separately).

Meeting date: {meeting_date}

TRANSCRIPT:
{transcript}

Return JSON: {{"decisions": [{{"decision": "<text>", "decided_by": "<speaker>"}}]}}"""

ACTION_ITEM_PROMPT = """Extract every action item from the following meeting transcript.

For each action item identify:
- task: what must be done, phrased as an imperative
- owner: the person responsible, exactly as named in the transcript, or "Unassigned"
- deadline_phrase: the deadline exactly as spoken, or null
- deadline_date: that deadline resolved to an absolute YYYY-MM-DD date relative to the \
meeting date of {meeting_date}, or null
- priority: High, Medium or Low, inferred from urgency language and deadline proximity

Known participants: {participants}

TRANSCRIPT:
{transcript}

Return JSON: {{"action_items": [{{"task": "...", "owner": "...", \
"deadline_phrase": "...", "deadline_date": "YYYY-MM-DD", "priority": "..."}}]}}"""

RISK_PROMPT = """Identify blockers, risks and unresolved questions in this transcript.

A blocker stops work from progressing. An open question is something the group \
explicitly left undecided or needs to confirm later.

TRANSCRIPT:
{transcript}

Return JSON: {{"blockers": ["<text>", ...], "open_questions": ["<text>", ...]}}"""

PROMPT_VARIABLES = {
    "SYSTEM_PROMPT": [],
    "SUMMARY_PROMPT": ["title", "meeting_date", "participants", "max_sentences", "transcript"],
    "DECISION_PROMPT": ["meeting_date", "transcript"],
    "ACTION_ITEM_PROMPT": ["meeting_date", "participants", "transcript"],
    "RISK_PROMPT": ["transcript"],
}

ALL_PROMPTS = {
    "SYSTEM_PROMPT": SYSTEM_PROMPT,
    "SUMMARY_PROMPT": SUMMARY_PROMPT,
    "DECISION_PROMPT": DECISION_PROMPT,
    "ACTION_ITEM_PROMPT": ACTION_ITEM_PROMPT,
    "RISK_PROMPT": RISK_PROMPT,
}
