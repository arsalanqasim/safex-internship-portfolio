# Daily Work Log - Week 4

Member: Muhammad Faozan Mujtaba
Module: `week4/src/modules/knowledge_assistant_airline/`
Week 4 window: Monday 2026-08-24 to Friday 2026-08-28

---

## Monday 2026-08-24 - Build day

| Time block | Activity | Outcome |
|---|---|---|
| Morning | Read `AGENTS.md`, the five `docs/` harness files and the Week 4 brief. Synced local repo with `origin/main`, which had gained `week4/`, and branched `feature/fozanmujtaba-knowledge_assistant_airline`. | Confirmed assignment: `knowledge_assistant_airline`, RAG-based Knowledge Assistant. |
| Morning | Studied the Week 4 shell (`src/app.py`), the registry contract, and the two modules already marked Submission Ready to match house patterns. | Established module shape and the `tutor_deploy_package/` precedent for per-member deployment. |
| Midday | Chose the client - Indus Air, a fictional Pakistani carrier - and wrote 7 synthetic policy documents (519 lines) covering baggage, changes and refunds, check-in and boarding, disruption, loyalty, assistance and minors, pets and restricted items. | Knowledge base: 48 chunks, ~3,960 words. |
| Midday | Wrote `prompts.py` (grounding rules, refusal wording) and `engine.py` (chunking, `VectorIndex` interface, TF-IDF backend, query expansion, similarity floor, extractive composer, evaluation harness). | Pipeline running end to end offline. |
| Afternoon | Wrote the 38-question gold set in passenger phrasing **before** tuning the retriever, including 5 out-of-scope questions. First benchmark: recall@k 100%, answer accuracy 93.94%, refusal accuracy 80%. | Three failures identified for investigation. |
| Afternoon | Diagnosed the refusal failure to scikit-learn's smoothed IDF flooring universal terms at 1.0 - the carrier name appears in all 48 chunks and carried real weight. Fixed with `max_df=0.9`; added the two missing synonym bridges. | Answer accuracy 100%, refusal accuracy 100%, precision@1 93.94%. |
| Afternoon | Spot-checked answer text and found fragment quotes caused by splitting hard-wrapped markdown on physical newlines. Rewrote `_split_units` to rejoin paragraphs and bullets while keeping table rows whole. | Answers now read as complete statements. |
| Late | Built `ui.py` with four tabs (Ask, Knowledge base, Benchmark, How it works) and verified it through the shared shell with `AppTest` - ask flow, refusal path and benchmark button all driven programmatically, zero exceptions. | UI verified without manual clicking. |
| Late | Wrote 31 tests; wrote `deploy_prep.py` and generated `knowledge_assistant_deploy_package/`, then verified the standalone app runs on its own. Updated the registry entry. Prepared the outreach tracker with 3 targets and drafted messages. | All tests passing; package verified; documentation written. |

**End-of-day status**: module complete and verified locally. Deployment, video recording
and outreach sending remain - all three need interactive accounts or a camera.

---

## Planned - Tuesday 2026-08-25

- Push `knowledge_assistant_deploy_package/` to a personal GitHub repo and deploy on
  Streamlit Community Cloud.
- Test the live link: ask flow, refusal path, benchmark tab, cold start.
- Set `deployed_url` in `week4/src/modules/registry.py` to the live link and confirm the
  green "Live" badge appears on the master dashboard.

## Planned - Wednesday 2026-08-26

- Capture screenshots from the running app for the presentation.
- Record the 3-5 minute client demo (`demo_video_script.md`).
- Record the 5-10 minute HD explanation video (`explanation_video_script.md`).

## Planned - Thursday 2026-08-27

- Send the 3 outreach messages with the live demo URL substituted in; update
  `week4/data/outreach_tracker.xlsx` with real send dates and responses.
- Build the slide deck from `presentation_outline.md`.

## Planned - Friday 2026-08-28

- Open the pull request to `origin/main` and notify the group leader.
- Submit weekly logs and slides.
- Follow up on any outreach replies.
