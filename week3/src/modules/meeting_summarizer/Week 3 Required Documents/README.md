# Week 3 Deliverables — AI Meeting Summarizer & Action-Item Extractor

**Member:** Muhammad Faozan Mujtaba
**Module:** `week3/src/modules/meeting_summarizer/`
**Target company:** Meridian Softworks (fictional software house, Islamabad)

## Deliverable checklist

| # | Required deliverable | Status | Where |
|---|---|---|---|
| 1 | Working prototype | ✅ Complete | `engine.py`, `ui.py` — runs in the Week 3 Streamlit app |
| 2 | Prompt template documentation | ✅ Complete | `prompts.py` (versioned source) + **Prompt Templates** tab |
| 3 | Architecture documentation & diagram | ✅ Complete | [`../README.md`](../README.md), [`../architecture_diagram.svg`](../architecture_diagram.svg), **Architecture** tab |
| 4 | Sample dataset / inputs | ✅ Complete | [`../data/transcripts/`](../data/transcripts/) — 3 annotated meetings |
| 5 | Before / after outputs | ✅ Complete | [`../sample_outputs/`](../sample_outputs/) — Markdown + JSON per transcript |
| 6 | Weekly progress report | ✅ Complete | [`progress_report.md`](progress_report.md) → export to PDF, see note below |
| 7 | Daily work log | ✅ Complete | [`daily_work_log.md`](daily_work_log.md) |
| 8 | Problems encountered writeup | ✅ Complete | [`problems_encountered.md`](problems_encountered.md) |
| 9 | Presentation slides | ✅ Outline ready | [`presentation_outline.md`](presentation_outline.md) — build deck from this |
| 10 | Screenshots | ✅ Complete | [`screenshots/`](screenshots/) — 5 captures of the running app |
| 11 | Demo video (5–10 min) | ⛔ **Not produced** | Deliberately skipped for this submission |

### Screenshots

| File | Shows |
|---|---|
| `01_summarize_input.png` | Transcript source selection and the generated summary |
| `02_summarize_results.png` | Decisions, the action-item table with owners and deadlines, blockers, open questions |
| `03_accuracy_benchmark.png` | Benchmark metrics and the per-transcript breakdown |
| `04_architecture.png` | Pipeline diagram and the five design rules |
| `05_prompt_templates.png` | Versioned prompt templates with their variables |

> **Note on item 11.** The explanation video was not recorded. Every other code and
> documentation deliverable is complete. The module demos live from the Week 3 app if a
> walkthrough is needed.

> **Note on the PDF.** The repository has no PDF library installed and
> `week3/requirements.txt` is a shared file that members should not edit, so the progress
> report is delivered as Markdown. Convert with any Markdown viewer's Print → Save as PDF.
> The generated *minutes* themselves do ship a print-ready HTML export built for this.

## Quick verification

From `week3/`:

```bash
pip install -r requirements.txt
python -m pytest tests/test_meeting_summarizer.py    # 38 tests
streamlit run src/app.py                             # sidebar → AI Meeting Summarizer
```

## Headline result

| Metric | Result |
|---|---|
| Recall (16 hand-annotated action items) | 100.00% |
| Precision | 94.12% |
| F1 | 96.97% |
| Owner accuracy | 100.00% |
| Deadline accuracy | 93.75% |

Two known failure modes are documented rather than tuned away — see
[`problems_encountered.md`](problems_encountered.md).
