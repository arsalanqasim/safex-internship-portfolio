# Daily Work Log — AI Meeting Summarizer & Action-Item Extractor

**Member:** Muhammad Faozan Mujtaba
**Module:** `meeting_summarizer`
**Target company:** Meridian Softworks

> This log records the implementation session for the module. Add further dated rows below
> if work continues before submission.

---

## 2026-08-03 — Implementation session

| # | Activity | Output |
|---|---|---|
| 1 | Synced the fork with `origin/main` after the group leader published the Week 3 workspace | Local `main` fast-forwarded `ec2d4b9 → 48feef2`; branch `feature/fozanmujtaba-meeting_summarizer` cut |
| 2 | Read the Week 3 brief, `AGENTS.md` harness rules and the two already-submitted peer modules to match house conventions | Confirmed module shape (`__init__/engine/ui`), `render_ui()` contract, no page config in module files, no edits to shared files |
| 3 | Chose the target company and scoped the problem | Meridian Softworks — sprint reviews, client calls, hiring syncs; the gap is structured follow-ups, not note-taking |
| 4 | Wrote three sample transcripts in the company's voice | `data/transcripts/` — sprint review, client kickoff, hiring sync |
| 5 | Built the transcript parser | Speaker turns, `[timestamp]` prefixes, `(Role)` annotations, wrapped-line continuation, header metadata |
| 6 | Built the deadline resolver | 14 phrase families → absolute ISO dates, anchored to the meeting date rather than the wall clock |
| 7 | Built the decision / action / risk extractors and the TF-IDF summary ranker | `engine.py` extraction pipeline producing a `MeetingReport` dataclass |
| 8 | Hand-annotated the gold standard **before** tuning the rules | `data/evaluation_set.json` — 16 action items with expected owner and deadline |
| 9 | First benchmark run exposed over-extraction | Filler sentences were being reported as decisions and tasks; see `problems_encountered.md` §1 |
| 10 | Restructured action detection to require a commitment marker **and** a work verb | Precision recovered without losing recall |
| 11 | Fixed participant parsing, "next \<weekday\>" semantics, deadline precedence, spoken number words | Four defects found by the benchmark and the test suite |
| 12 | Wrote the Streamlit UI | Four tabs: Summarize, Accuracy Benchmark, Architecture, Prompt Templates |
| 13 | Wrote the test suite | 38 tests covering parsing, 14 deadline phrase families, extraction rules, exports, determinism, benchmark floor |
| 14 | Generated before/after evidence and wrote documentation | `sample_outputs/`, module `README.md`, architecture SVG, this deliverables set |

**Verification at end of session:** 54/54 Week 3 tests pass (38 new, 16 pre-existing).
Benchmark: recall 100.00%, precision 94.12%, F1 96.97%, owner accuracy 100.00%, deadline
accuracy 93.75%.

**Not done:** explanation video (deliberately skipped for this submission).

---

## Time allocation

| Area | Share |
|---|---|
| Extraction logic and rule tuning | ~40% |
| Sample data and hand annotation | ~20% |
| Tests and benchmark harness | ~20% |
| Streamlit UI | ~10% |
| Documentation | ~10% |
