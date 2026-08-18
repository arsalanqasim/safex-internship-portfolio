# Agent Memory

This file stores durable project context for future coding agents. Keep entries short, dated, factual, and useful.

Do not store:

- phone numbers
- personal emails
- API keys or credentials
- private feedback form content
- sensitive personal comments
- unverified assumptions presented as facts

## Persistent Repo Facts

- 2026-07-17: Repository is the SafeX Solutions Summer Internship portfolio for Group 54.
- 2026-07-17: The repo is split into independent week folders: `week1/` and `week2/`.
- 2026-07-17: Week 1 is the SafeX FAQ chatbot prototype.
- 2026-07-17: Week 2 is the Business Automation Research prototype suite.
- 2026-07-17: Week 2 modules live under `week2/src/modules/`.
- 2026-07-17: Each Week 2 module is expected to have `__init__.py`, `engine.py`, and `ui.py`.
- 2026-07-19: Created Week 2 Self-Initiative report (`week2/docs/Self_Initiative.md`) documenting the modular Streamlit host, contribution registry, global CSS branding, and sandboxed scaffolding.
- 2026-07-23: Created Week 3 workspace (`week3/`) for AI Agent Automation Proposal suite.
- 2026-07-23: Week 3 modules live under `week3/src/modules/` with 9 assigned modules mapping all 9 group members.
- 2026-07-23: Group Leader Arsalan Qasim's module `customer_support_chatbot` is submission-ready with 100% intent classification accuracy across 12 test queries, escalation trigger rules, and Streamlit UI.
- 2026-07-23: 8 teammate modules (`email_auto_reply`, `meeting_summarizer`, `report_generation_agent`, `social_media_scheduler`, `lead_qualification`, `resume_interview_assistant`, `doc_knowledge_assistant`, `proposal_invoice_generator`) established with lightweight scaffolding (`engine.py`, `ui.py`, `__init__.py`) containing member name, target company, assigned task details, and status.
- 2026-07-27: Added root Streamlit app (`app.py`) as a unified portfolio router using `st.navigation` and `st.Page`.
- 2026-08-04: Created Week 4 workspace (`week4/`) for Client-Ready Sprint.
- 2026-08-04: Added `deployed_url` configuration parameters in `registry.py` to allow team members to deploy their modules independently and register their live links in the root portfolio application.
- 2026-08-04: Leader module `chatbot_deployment` implements dynamic client organization configuration, basic error validations, and sentiment-based human support handoffs, storing outreach tracker logs in `week4/data/outreach_tracker.xlsx`.
- 2026-08-04: Upgraded the `chatbot_deployment` engine to a hybrid model supporting live Gemini or OpenAI API requests via direct HTTP POST calls, using local TF-IDF as a fail-safe offline fallback. Implemented key fetching from `.env` and Streamlit Secrets.
- 2026-08-18: Created Week 5 workspace (`week5/`) for AI Products Suite. Member modules use member-keyed directories (`chatbot_arsalan`, `lead_gen_wasim`, etc.) with neutral domain selectors to allow teammates flexibility.
- 2026-08-18: Week 5 Arsalan module `chatbot_arsalan` features production-grade customer support chatbot with persistent JSON-based no-code Admin Panel, 15+ FAQ benchmark tester, audit logs, and standalone deploy package exporter.
- 2026-08-18: Created Week 6 workspace (`week6/`) for Sell Your Skills: Commercialization & Client Acquisition.
- 2026-08-18: Week 6 Arsalan module `commercial_arsalan` features an interactive Commercial Command Center with dynamic 3-tier pricing calculator, automated cold email generator, interactive outreach tracker with Excel export (`outreach_tracker.xlsx`), social media marketing assets, and group consolidation metrics.
- 2026-08-18: Registered `week5/src/app.py` and `week6/src/app.py` into the root multi-page navigation router in `app.py`.

## Decisions Made


- 2026-07-17: Harness files should target any coding agent, not only one tool.
- 2026-07-17: Harness files should avoid personal phone numbers and emails.
- 2026-07-17: Agent memory should live at `docs/agent-memory.md`.
- 2026-07-17: The harness file set is `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/project.mdc`, and docs under `docs/`.
- 2026-07-17: The roster fields `Internship Field (Original Response)` and `Field Category` are not task assignments and should not be inserted into harness docs as task data.
- 2026-07-19: Integrated the Group Leader Self-Initiative report under `week2/docs/Self_Initiative.md` and added summary sections to `Week2_Status_Report.md`.
- 2026-07-27: Placed module and path isolation blocks in `week1`, `week2`, and `week3` main apps to enable clean navigation switching without import collisions on the `src` namespace, keeping the workspace folders fully independent.
- 2026-07-27: Monkey-patched `st.set_page_config` to a no-op inside the root entrypoint to prevent Streamlit page configuration crashes when subpages load in the multi-page structure.

## Workflow Notes

- 2026-07-17: For Week 2 Streamlit modules, keep module rendering inside `render_ui()` in each module's `ui.py`.
- 2026-07-17: Keep app-level Streamlit setup in `week2/src/app.py`.
- 2026-07-17: Keep `week2/src/modules/registry.py` aligned with module folders and app routing.
- 2026-07-17: Track non-responsive members in `docs/team-roster.md` using factual status fields and follow-up dates.

## Member / Progress Observations

- 2026-07-17: Current confirmed Week 2 assignments are listed in `docs/team-roster.md`.
- 2026-07-17: Malik Sudais appears in the source roster with an Invoice Automation Prototype assignment, while `week2/src/modules/` currently has one `invoice_automation` module associated with Arsalan Qasim. Confirm ownership before changing module structure.
- 2026-07-19: Verified through Git PR history that 3 group members completed and integrated their Week 2 modules (Muhammad Faozan Mujtaba, Shahidullah, Ali Ammar Haider) in addition to Arsalan Qasim.
- 2026-07-19: Inactive members who have not submitted PRs or commits for Week 2 are MUHAMMAD WASIM, Abdul Haseeb, Hammad Abbas, and Ali Zaib. They are marked 'No response' with a follow-up date of 2026-07-19.
- 2026-07-19: Malik Sudais is confirmed to be not active as a team member for Week 2. Leadership will review his status in Week 3.
- 2026-07-19: Screenshot, recording, progress report, and video submissions are tracked dynamically in the shared Google Sheet: https://docs.google.com/spreadsheets/d/1KySlQDSuPAtdBWXqFlEKz8NFvk0yfzs6KrTVqTZ5AaQ/edit?gid=800509207#gid=800509207.
- 2026-08-09: Reviewed and merged PR #15 implementing the Week 4 Predictive Dashboard Tutor module for Ali Ammar Haider, updating the module registry status to "Submission Ready" and the team roster to "Submitted".

## Open Questions

- 2026-07-19: Are there any specific integration challenges faced by the 3 active members during team branch merges? (None reported so far.)

## Do-Not-Repeat Mistakes

- Do not copy private contact details from source rosters into public project harness docs.
- Do not treat internship preference fields as task assignments.
- Do not make broad cross-week refactors when a request targets only one week or module.
- Do not update member status without evidence.
