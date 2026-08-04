# Week 3 Progress Report — AI Meeting Summarizer & Action-Item Extractor

**Member:** Muhammad Faozan Mujtaba
**Group:** Group 54 · SafeX Solutions Summer Internship
**Module:** `week3/src/modules/meeting_summarizer/`
**Target company:** Meridian Softworks — fictional software house, Islamabad
**Report date:** 2026-08-03
**Status:** Submission Ready (explanation video not produced)

---

## 1. Objective

Build an AI agent that converts a raw meeting transcript into a structured record: an
executive summary, the decisions the group settled on, and action items each carrying an
**owner** and an **absolute calendar deadline**.

## 2. Business case

Meridian Softworks runs sprint reviews, client calls and hiring syncs every week. Notes are
taken in roughly half of them, and commitments made out loud are not captured anywhere. The
consequences are concrete: a blocker rediscovered a week later, a client told about a slip
after it has already happened, an action nobody remembers owning.

The gap is not note-taking — it is the structure of the notes. Who owns what, and by when.

## 3. What was built

| Component | Description |
|---|---|
| Transcript parser | Speaker turns, `[timestamp]` prefixes, `(Role)` annotations, wrapped lines, header metadata |
| Decision extractor | Settled-choice cues with negation guards, so "has not signed off" is not read as a decision |
| Action extractor | Requires a commitment marker **and** a work verb |
| Owner resolver | Named person → first-person speaker → `Unassigned`. Never guesses |
| Deadline resolver | 14 phrase families → absolute ISO dates, anchored to the meeting date |
| Risk extractor | Blockers, and questions the meeting genuinely left deferred |
| Summary ranker | TF-IDF sentence scoring with a word floor, so short reactions do not surface |
| Exports | Markdown minutes, structured JSON, print-ready HTML → PDF |
| Streamlit UI | Four tabs: Summarize, Accuracy Benchmark, Architecture, Prompt Templates |

The pipeline runs **fully offline**. `LLM_PROVIDER=mock` is the default, matching
`week3/.env.example`, so the prototype demos with no API key and no network. A hosted-LLM
seam exists and sends the same versioned prompt templates from `prompts.py`, with the
deterministic pipeline as the fallback whenever that call fails.

## 4. Results

Three transcripts were annotated by hand — 16 action items with expected owners and
deadlines — **before** the extraction rules were tuned.

| Metric | Result |
|---|---|
| Transcripts evaluated | 3 |
| Action items in gold set | 16 |
| Action items extracted | 17 |
| **Recall** | **100.00%** |
| **Precision** | **94.12%** |
| **F1** | **96.97%** |
| **Owner accuracy** (matched pairs) | **100.00%** |
| **Deadline accuracy** (matched pairs) | **93.75%** |
| Decisions found / expected | 6 / 6 |

Per transcript:

| Transcript | Gold | Extracted | Matched | Owner ✓ | Deadline ✓ |
|---|---|---|---|---|---|
| Sprint 14 Review | 6 | 6 | 6 | 6 | 6 |
| Orchard Phase 2 Kickoff | 5 | 5 | 5 | 5 | 4 |
| Engineering Hiring Sync | 5 | 6 | 5 | 5 | 5 |

**Test suite:** 38 tests for this module; 54/54 pass across the whole Week 3 workspace.

## 5. Before and after

**Input** (excerpt, sprint review):

```
[01:03] Ayesha: That is a genuine blocker. Bilal will chase Orchard for fresh sandbox
        credentials by tomorrow so that QA is not sitting idle.
[02:47] Danish: I'll set up an automated artefact cleanup job on the staging cluster by Friday.
[03:25] Ayesha: We decided to standardise on pnpm across all three repositories.
```

**Output** (excerpt, generated minutes):

| # | Action | Owner | Deadline | Priority |
|---|---|---|---|---|
| 1 | Chase Orchard for fresh sandbox credentials by tomorrow | Bilal Ahmed | 2026-07-29 (tomorrow) | High |
| 4 | Set up an automated artefact cleanup job on the staging cluster by Friday | Danish Iqbal | 2026-07-31 (by friday) | Medium |

> **Decisions Made**
> 2. We decided to standardise on pnpm across all three repositories, so the yarn lockfiles
>    are removed this sprint. — *Ayesha Rauf*

Full before/after evidence for all three meetings is in [`../sample_outputs/`](../sample_outputs/).

## 6. Known limitations

Both are reported in the metrics above rather than tuned away. Detail in
[`problems_encountered.md`](problems_encountered.md).

1. **Cross-turn deadlines are not attached** — a deadline stated several turns after its task
   requires coreference resolution across turns. Costs 1 of 16 deadlines.
2. **A restated task can be double-counted** — deduplicating differently-worded sentences that
   mean one task risks merging genuinely distinct tasks, a worse failure. Costs the single
   precision miss.

## 7. Repository compliance

- Changes are confined to `week3/src/modules/meeting_summarizer/` plus one new test file at
  `week3/tests/test_meeting_summarizer.py`.
- No shared file was edited — `app.py`, `registry.py`, `requirements.txt` and `.gitignore` are
  untouched, per the group workflow.
- No secrets, API keys or private contact details were added.
- Public functions and classes carry type hints, per `AGENTS.md` code standards.

**One item for the group leader:** the registry entry for `meeting_summarizer` still reads
`"status": "Placeholder (Scaffolding Ready)"`. Since `registry.py` is a shared file, it was
left untouched — it needs updating to `"Submission Ready"` on merge.

## 8. Next steps

1. Record the explanation video if it is reinstated as a requirement.
2. Cross-turn deadline attachment, the highest-value remaining accuracy gain.
3. Expand the gold set beyond three transcripts to make the metrics more robust.
4. Calendar export (`.ics`) so action items land directly in owners' calendars.
