# Week 5 · Daily Work Log

**Developer:** Ali Zaib
**Project:** Insurance & Finance Lead Qualifier

| Day | Work Completed |
|---|---|
| Day 1 | Reviewed the assigned module scaffold and registry entry; designed the five-factor scoring rubric (Policy Value Fit, Coverage/Budget Fit, Urgency/Timeline, Risk Profile, Engagement/Channel) as a replacement for the original two-branch stub. Generated the initial synthetic sample-leads dataset. |
| Day 2 | Implemented `engine.py`: single-lead scoring, the coverage/budget-fit sanity check against an industry rule-of-thumb premium rate, tier mapping, and batch scoring. Wrote and ran the initial unit test suite. |
| Day 3 | Built `ui.py`: single-lead qualification form, batch CSV scoring tab (upload or bundled sample), and a "How Scoring Works" explainer tab for non-technical reviewers. Verified end-to-end with Streamlit's `AppTest` harness. |
| Day 4 | Built the standalone deployment package (`deploy_prep_ali_zaib.py`, mirroring the Group Leader's own `deploy_prep.py` pattern); tested the standalone build independently; deployed live to Streamlit Community Cloud. |
| Day 5 | Wrote README, Progress Report, and Presentation Outline documentation. Opened the PR, registered the live deployment URL in `registry.py`. |
| Day 6 (revision pass) | Addressed a task-spec review: expanded the sample dataset from 28 to 40 rows (spec calls for 30-50), added explicit red/yellow/green color-coded row styling to the batch scoring dashboard, and converted the Progress Report to PDF as required by the submission checklist. |

## Problems Encountered & Solutions

- **Problem:** the original stub scored leads with only two branches, which couldn't meaningfully differentiate leads or explain its reasoning to an underwriter.
  **Solution:** redesigned as a five-factor weighted rubric with visible per-factor point breakdowns.
- **Problem:** a high coverage request alone doesn't indicate lead quality — a lead requesting high coverage with an unrealistically low stated budget isn't actually a good lead.
  **Solution:** added a coverage/budget-fit check against an industry rule-of-thumb premium rate, surfacing the mismatch as a specific, actionable flag.
- **Problem:** initial batch dashboard listed leads in a plain table with no at-a-glance visual prioritization.
  **Solution:** added explicit red/yellow/green row-level color coding matching each lead's tier, so a non-technical sales rep can scan the table in seconds.

## Next Week's Plan (Week 6)

- Package this tool as a sellable commercial service: tiered pricing for insurance agencies/brokers, an ROI calculator for discovery calls, and outreach materials.
- Conduct genuine outreach to real prospective agencies (not simulated), per the Week 6 task's real business-development requirement.
