# Weekly Task Log

This file documents what Group 54 was asked to build each week, how the work is organized, and how member contributions should be tracked.

## Week 1 - SafeX AI/ML Prototype

### Original Task

Build a small AI/ML prototype for SafeX, for example:

- FAQ chatbot for safexsolutions.com or SafeX-related information.
- Social-media engagement forecast model.
- Data dashboard using real or sample data.

Also document the approach and results as a portfolio case study.

Group leader responsibility:

- consolidate the group's weekly submissions
- send a short summary to the Team Lead by Friday
- submit anonymous feedback on the Team Lead / overall program through the feedback form

### Group Direction

Group 54 selected the FAQ chatbot prototype.

### What Was Built

The Week 1 workspace contains a local SafeX FAQ chatbot with:

- FAQ data in JSON format
- text similarity matching
- chatbot response logic
- Streamlit interface
- evaluation scripts and tests
- portfolio case-study documentation

### How It Was Built

Primary approach:

- Store FAQ content in `week1/data/faq.json`.
- Load and normalize FAQ entries through the knowledge base layer.
- Use vector similarity to match user questions with the closest FAQ answer.
- Render the chatbot through Streamlit.
- Validate expected responses through tests and evaluation questions.

Important files:

- `week1/src/app.py`
- `week1/src/chatbot.py`
- `week1/src/knowledge_base.py`
- `week1/src/similarity.py`
- `week1/data/faq.json`
- `week1/docs/Case_Study.md`
- `week1/docs/Evaluation.md`
- `week1/evaluation/benchmark.py`
- `week1/tests/test_chatbot.py`

### Week 1 Member Tracking

| Member | Contribution Area | Evidence | Status | Notes |
|---|---|---|---|---|
| Arsalan Qasim | Group consolidation and FAQ chatbot contribution | `week1/` project files and docs | Submitted | Consolidated group summary. |
| MUHAMMAD WASIM | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Muhammad Faozan Mujtaba | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Shahidullah | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Ali Ammar Haider | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Abdul Haseeb | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Hammad Abbas | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Ali Zaib | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Malik Sudais | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |

## Week 2 - Business Automation Research

### Original Task

Each member designs, builds, and documents one component of the Business Automation Research project. Each module should continue the group's Week 1 work and integrate cleanly with the other modules.

Common deliverables:

- Jupyter notebook or script with sample input/output.
- Source code or working files for the assigned module.
- Short written documentation explaining what was built, how it works, and how to run or view it.
- Screenshots or a short recording of the module working.
- GitHub repository updates.
- Final working demo.
- Progress report.
- Mandatory explanation video, 5-15 minutes, HD, face visible, covering architecture, challenges, tools used, and working demo.

Common technologies:

- Python
- Pandas / NumPy
- NLP libraries such as spaCy or NLTK, or an LLM API
- Flask or FastAPI where applicable
- Streamlit for local module demos
- WhatsApp Business API or Twilio where applicable

### Group Direction

Group 54 organized Week 2 as a modular business automation suite under `week2/`.

The shared Streamlit app routes to member-owned modules. Each module should stay isolated so members can work without duplicating or overwriting each other's work.

### Module Assignments

| Member | Module | Objective | Difficulty |
|---|---|---|---|
| Arsalan Qasim | Invoice Automation Prototype | Research and prototype a workflow that auto-generates and sends invoices for a sample small business. | Advanced |
| MUHAMMAD WASIM | Attendance Automation Prototype | Design an automated attendance-tracking workflow, such as QR or geofence check-in, for a sample organization. | Advanced |
| Muhammad Faozan Mujtaba | HR Automation Proposal | Propose and partially prototype an automated onboarding or leave-request workflow for a sample business. | Intermediate |
| Shahidullah | AI Email Assistant Prototype | Build a small prototype that drafts reply suggestions for common customer emails. | Advanced |
| Ali Ammar Haider | AI Report Generator Prototype | Build a script that turns raw sample data into a formatted weekly report. | Intermediate |
| Abdul Haseeb | Resume Screening Prototype | Build a small tool that scores sample resumes against a job description using keyword or embedding matching. | Advanced |
| Hammad Abbas | OCR / Document Processing Prototype | Build a prototype that extracts structured fields from a scanned sample document using OCR. | Intermediate |
| Ali Zaib | Predictive Analytics Mini-Study | Use a small sample or public dataset to build a simple predictive model and report findings. | Advanced |
| Malik Sudais | Invoice Automation Prototype | Standalone Invoice Automation Prototype (GitHub repo & Google Drive submission). | Submitted |


### Week 2 Workspace

Important files:

- `week2/src/app.py`
- `week2/src/config.py`
- `week2/src/modules/registry.py`
- `week2/src/modules/attendance/`
- `week2/src/modules/email_assistant/`
- `week2/src/modules/hr_proposal/`
- `week2/src/modules/invoice_automation/`
- `week2/src/modules/ocr_document/`
- `week2/src/modules/predictive_analytics/`
- `week2/src/modules/report_generator/`
- `week2/src/modules/resume_screening/`
- `week2/docs/Weekly/Week2_Status_Report.md`

### How Week 2 Is Built

Each module should provide:

- an `engine.py` for core workflow logic
- a `ui.py` with a `render_ui()` Streamlit entrypoint
- module-level documentation where needed
- sample inputs and outputs
- screenshots or recordings for evidence
- tests for core logic where practical

### Week 2 Progress Tracking

Use `docs/team-roster.md` as the source for member-level progress. Use `week2/docs/Weekly/Week2_Status_Report.md` for the weekly consolidated summary.

When a member is not responding:

1. Mark the status as `No response` only after a follow-up date is known.
2. Add the first and second follow-up dates.
3. Record the exact deliverables missing.
4. Keep notes factual and professional.

## Week 3 - AI Agent Automation Proposal Suite

### Original Task

Each member designs, builds, and documents an AI agent prototype for a specific business automation domain and target company.

Common deliverables:

- Working prototype (script or hosted demo).
- Prompt template / architecture documentation & diagrams.
- Sample dataset / inputs and before-after outputs.
- Weekly Progress Report (PDF) & Daily Work Log.
- Demo Video (5-10 min, HD, face visible).
- Presentation Slides & Problems Encountered writeup.

### Group Direction

Group 54 organized Week 3 as an AI Agent Automation Proposal Suite under `week3/`.
The shared Streamlit app routes to member-owned modules, providing clean isolation and consistent UI styling.

### Module Assignments

| Member | Module Key | Assigned Project | Scope Summary |
|---|---|---|---|
| Arsalan Qasim | `customer_support_chatbot` | AI Customer Support Chatbot | Map 12+ queries, build intent classifier + escalation rules, 10+ query test benchmark with accuracy score. |
| MUHAMMAD WASIM | `email_auto_reply` | AI Email Automation & Auto-Reply | Collect 15-20 queries, prompt templates, draft reply generation, human-review step. |
| Muhammad Faozan Mujtaba | `meeting_summarizer` | AI Meeting Summarizer & Action-Item Extractor | Process meeting transcripts, extract summary, decisions, action items with owners & deadlines. |
| Shahidullah | `report_generation_agent` | Automatic Report Generation Agent | Read operational CSVs, generate narrative written report using LLM + embedded charts. |
| Ali Ammar Haider | `social_media_scheduler` | AI Social Media Scheduler & Caption Generator | 7-day content calendar, LLM caption generator, Buffer/Meta API integration proposal. |
| Abdul Haseeb | `lead_qualification` | AI Lead Qualification & Sales Assistant | 5-8 scoring criteria, LLM rubric engine, qualification score + next action for 10+ leads. |
| Hammad Abbas | `resume_interview_assistant` | Resume Screening & Interview Assistant | Screen 5-8 resumes against job description, fit explanation, 5 tailored interview questions. |
| Ali Zaib | `doc_knowledge_assistant` | Document Knowledge Assistant (RAG) | RAG pipeline over policy docs, vector similarity, log accuracy across 10+ questions. |
| Malik Sudais | `proposal_invoice_generator` | Invoice / Proposal Generator Agent | Structured input template, LLM cover paragraph, formatted proposal & invoice packages. |

### Week 3 Workspace

Important files:

- `week3/src/app.py`
- `week3/src/config.py`
- `week3/src/modules/registry.py`
- `week3/src/modules/customer_support_chatbot/`
- `week3/src/modules/email_auto_reply/`
- `week3/src/modules/meeting_summarizer/`
- `week3/src/modules/report_generation_agent/`
- `week3/src/modules/social_media_scheduler/`
- `week3/src/modules/lead_qualification/`
- `week3/src/modules/resume_interview_assistant/`
- `week3/src/modules/doc_knowledge_assistant/`
- `week3/src/modules/proposal_invoice_generator/`
- `week3/docs/Self_Initiative.md`
- `week3/docs/Weekly/Week3_Status_Report.md`
- `week3/tests/`

---

## Week 4 - Client-Ready Sprint

### Original Task

Turn a Week 2/3 chatbot prototype into a client-presentable package: hosted demo, pricing options, and a one-page proposal. Also identify up to 3 organizations or professionals for client outreach, log outreach platforms and response dates in the outreach tracker log, and record a 3-5 min screen walkthrough demo video.

Group leader responsibility:
- consolidate the group's weekly submissions
- send a short status summary update to the Team Lead by Friday
- submit anonymous feedback on the Team Lead via the feedback form

### Group Direction

Group 54 organized Week 4 as a Client-Ready Sprint Suite under `week4/` with dynamic branding configurations, basic validation guards, warm human-handoff triggers, and direct deployment URLs integration inside the registry.

### Module Assignments

| Member | Module Key | Assigned Project | Scope Summary | Status |
|---|---|---|---|---|
| Arsalan Qasim | `chatbot_deployment` | Client-Ready AI Chatbot Deployment Package | Configurable client context, input validation, warm human handoff escalation, interactive ROI calculator, outreach Excel logger. | **Submitted** |
| MUHAMMAD WASIM | `roi_calculator_real_estate` | AI Automation ROI Calculator | Standard time/cost savings projection calculator. | In progress |
| Muhammad Faozan Mujtaba | `knowledge_assistant_airline` | RAG-based Knowledge Assistant | Chunk/embed Q&A assistant for company policies. | In progress |
| Shahidullah | `model_comparison_bank` | AI Model Comparison & Recommendation Report | Multi-vendor evaluation memo and recommendation scoring matrix. | In progress |
| Ali Ammar Haider | `predictive_dashboard_tutor` | Predictive Dashboard for a Small Business | Moving average/regression projection actual vs predicted dashboard. | **Submitted** |
| Abdul Haseeb | `chatbot_deployment_courier` | Client-Ready AI Chatbot Deployment Package | Courier chatbot client-ready deployment. | In progress |
| Hammad Abbas | `roi_calculator_daraz` | AI Automation ROI Calculator | Daraz business-case automation savings dashboard. | In progress |
| Ali Zaib | `knowledge_assistant_foodpanda` | RAG-based Knowledge Assistant | RAG Q&A retrieval engine with hallucination checks. | In progress |
| Malik Sudais | `model_comparison_careem` | AI Model Comparison & Recommendation Report | Careem model comparison audit and live hosted Streamlit deployment. | **Submitted** |

### Week 4 Workspace

Important files:

- `week4/src/app.py`
- `week4/src/config.py`
- `week4/src/modules/registry.py`
- `week4/src/modules/chatbot_deployment/`
- `week4/src/modules/predictive_dashboard_tutor/`
- `week4/src/modules/model_comparison_careem/`
- `week4/tutor_deploy_package/`
- `week4/data/outreach_tracker.xlsx`
- `week4/deploy_prep.py`
- `week4/docs/Weekly/Week4_Status_Report.md`

### What Was Built

1. **Client-Ready AI Chatbot Deployment Package (`chatbot_deployment`)**:
   - Dynamic rebranding panel in Streamlit UI adapting corporate name and terminology across chatbot simulator, 1-page proposal generator, and ROI calculator.
   - Input validation guards (regex gibberish checks and maximum length bounds).
   - Warm human support escalation system generating ticket tokens (`TK-XXXXX`) upon keyword triggers or low-confidence matches.
   - Excel outreach logger (`openpyxl`) storing client contact logs in `week4/data/outreach_tracker.xlsx`.
   - Standalone extraction script (`deploy_prep.py`) generating production-ready deployment packages.

2. **Predictive Dashboard for a Small Business (`predictive_dashboard_tutor`)**:
   - `scikit-learn` OLS Linear Regression forecasting engine predicting Month 25 student enrollments based on 24 months of historical operations for LearnHub Academy.
   - Model accuracy metrics ($R^2$ fit coefficient and Mean Absolute Error).
   - Matplotlib trendline chart dynamically matching Light/Dark theme selections.
   - Dynamically evaluated business recommendations (Tutor Recruiting, Funnel UX, Administrative Capacity).
   - Standalone production package (`week4/tutor_deploy_package/`) deployed live on Streamlit Cloud (`https://safex-week4-predictive-dashboard-tutor.streamlit.app`).

3. **AI Model Comparison & Recommendation Report (`model_comparison_careem`)**:
   - Multi-model evaluation comparing Gemini 1.5 Flash, GPT-4o-mini, and Claude 3.5 Haiku on Careem ride-hailing support prompts.
   - Live standalone Streamlit deployment hosted at `https://cxyaqlr4q4jdwtm7dadw8v.streamlit.app/`.

### How It Was Built

- Established a configurable brand input inside the UI so that chatbot, proposal documents, and ROI equations adapt dynamically.
- Implemented robust regex vowel-checks and length-validators inside the chatbot engine to ensure input quality.
- Added Excel logging capability (`openpyxl`) to track outreach actions.
- Created `deploy_prep.py` to allow teammates to extract and deploy standalone widgets, linking them back via the registry.
- Built comprehensive unit tests (`pytest`) covering dataset loading, model predictions, recommendations count, and dynamic scenario evaluation.

### Week 4 Member Tracking

| Member | Module Key | Contribution & Submission | Evidence | Status |
|---|---|---|---|---|
| Arsalan Qasim | `chatbot_deployment` | Client-Ready AI Chatbot Deployment Package with dynamic branding, input validation, human handoff, ROI calculator, and Excel logger. | `week4/src/modules/chatbot_deployment/`, `deploy_prep.py`, `outreach_tracker.xlsx` | **Submitted** |
| Ali Ammar Haider | `predictive_dashboard_tutor` | Predictive Dashboard for LearnHub Academy with OLS regression engine, dynamic recommendations, Matplotlib chart, tests, and live deployment package. | `week4/src/modules/predictive_dashboard_tutor/`, `week4/tutor_deploy_package/`, PR #15 | **Submitted** |
| MUHAMMAD WASIM | `roi_calculator_real_estate` | AI Automation ROI Calculator (Scaffolding ready). | `week4/src/modules/roi_calculator_real_estate/` | In progress |
| Muhammad Faozan Mujtaba | `knowledge_assistant_airline` | RAG-based Knowledge Assistant (Scaffolding ready). | `week4/src/modules/knowledge_assistant_airline/` | In progress |
| Shahidullah | `model_comparison_bank` | AI Model Comparison & Recommendation Report (Scaffolding ready). | `week4/src/modules/model_comparison_bank/` | In progress |
| Abdul Haseeb | `chatbot_deployment_courier` | Client-Ready AI Chatbot Deployment Package (Scaffolding ready). | `week4/src/modules/chatbot_deployment_courier/` | In progress |
| Hammad Abbas | `roi_calculator_daraz` | AI Automation ROI Calculator (Scaffolding ready). | `week4/src/modules/roi_calculator_daraz/` | In progress |
| Ali Zaib | `knowledge_assistant_foodpanda` | RAG-based Knowledge Assistant (Scaffolding ready). | `week4/src/modules/knowledge_assistant_foodpanda/` | In progress |
| Malik Sudais | `model_comparison_careem` | AI Model Comparison & Recommendation Report for Careem (Live App: https://cxyaqlr4q4jdwtm7dadw8v.streamlit.app/). | `week4/src/modules/model_comparison_careem/`, Live App | **Submitted** |


---

---

## Week 5 - AI Products & Prototypes Suite

### Original Task

Design, build, and document client-ready AI products addressing business pain points across 3 project tracks (or Option B: Propose Your Own Project):
1. **AI Customer Support Chatbot (Client-Ready)**: Automate top 10–15 repeat queries, escalate low-confidence queries to human support, log conversations for audit, and provide a no-code admin view to edit answers without coding.
2. **AI-Powered Lead Generation & Qualification Tool**: Ingest leads, score using a rubric (budget, urgency, fit), flag hot leads for immediate follow-up, and generate one-line AI summaries.
3. **AI Business Intelligence Dashboard**: Ingest sales/marketing data, build interactive charts, run moving average/regression forecasts for the next 30 days, and generate plain-English weekly written insights with exportable PDF/reports.

Testing requirements: 15+ realistic sample questions/leads, verified formulas, responsive UI/UX, and standalone deployment preparation.

### Group Direction & Assignments

Group 54 split across the 3 tracks with member-keyed sandboxes allowing each contributor to define their chosen business domain:
- **AI Customer Support Chatbot**: Arsalan Qasim (`chatbot_arsalan`), Shahidullah (`chatbot_shahidullah`), Hammad Abbas (`chatbot_hammad`).
- **AI Lead Generation & Qualification**: MUHAMMAD WASIM (`lead_gen_wasim`), Ali Ammar Haider (`lead_gen_ali_ammar`), Ali Zaib (`lead_gen_ali_zaib`).
- **AI Business Intelligence Dashboard**: Muhammad Faozan Mujtaba (`bi_dashboard_faozan`), Abdul Haseeb (`bi_dashboard_abdul_haseeb`), Malik Sudais (`bi_dashboard_malik_sudais`).

### What Was Built (Leader Module - Arsalan Qasim)

Group Leader Arsalan Qasim built a complete production-grade **AI Customer Support Chatbot (Client-Ready)** tailored for high-volume E-Commerce Retail:
- **Hybrid AI Engine**: Live Gemini / OpenAI REST integration with automatic local TF-IDF semantic vector fallback for 100% offline grading reliability.
- **Top 15+ FAQ Knowledge Base**: Covering international shipping, order tracking, returns, sizing, discounts, defective items, and payment methods.
- **Sentiment & Escalation Layer**: Automatic sentiment-aware human handoff trigger when confidence falls below threshold or when user explicitly requests a representative.
- **No-Code Admin Panel**: Interactive CRUD interface to add, edit, delete FAQs with persistent local JSON storage and factory reset.
- **Audit & Analytics Viewer**: Real-time log inspector with sentiment analytics, resolution rates, and CSV/JSON export.
- **Automated Benchmark Suite**: Runs 15+ realistic customer queries computing latency, accuracy, and hallucination metrics.
- **Standalone Deployment Bundler**: `deploy_prep.py` generates an isolated, zero-dependency `week5/chatbot_deploy_package/`.

### Week 5 Member Tracking

| Member | Module Key | Contribution & Submission | Evidence | Status |
|---|---|---|---|---|
| Arsalan Qasim | `chatbot_arsalan` | Production Client-Ready Chatbot with Admin Panel, Fallback Engine, Benchmark Suite, Tests, and Deploy Package. | `week5/src/modules/chatbot_arsalan/`, `deploy_prep.py`, `tests/test_chatbot.py` | **Submitted** |
| MUHAMMAD WASIM | `lead_gen_wasim` | AI Lead Qualification Tool (Scaffolding ready with domain selector). | `week5/src/modules/lead_gen_wasim/` | In progress |
| Muhammad Faozan Mujtaba | `bi_dashboard_faozan` | AI BI Dashboard & Forecasting (Scaffolding ready). | `week5/src/modules/bi_dashboard_faozan/` | In progress |
| Shahidullah | `chatbot_shahidullah` | AI Customer Support Chatbot (Scaffolding ready). | `week5/src/modules/chatbot_shahidullah/` | In progress |
| Ali Ammar Haider | `lead_gen_ali_ammar` | AI Lead Qualification Tool (Scaffolding ready). | `week5/src/modules/lead_gen_ali_ammar/` | In progress |
| Abdul Haseeb | `bi_dashboard_abdul_haseeb` | AI BI Dashboard (Scaffolding ready). | `week5/src/modules/bi_dashboard_abdul_haseeb/` | In progress |
| Hammad Abbas | `chatbot_hammad` | AI Customer Support Chatbot (Scaffolding ready). | `week5/src/modules/chatbot_hammad/` | In progress |
| Ali Zaib | `lead_gen_ali_zaib` | AI Lead Qualification Tool (Scaffolding ready). | `week5/src/modules/lead_gen_ali_zaib/` | In progress |
| Malik Sudais | `bi_dashboard_malik_sudais` | AI BI Dashboard (Scaffolding ready). | `week5/src/modules/bi_dashboard_malik_sudais/` | In progress |

---

## Week 6 - Sell Your Skills: Monetization & Client Acquisition

### Original Task

Turn the Week 5 project into a commercial service offering and execute real business development and client acquisition:
1. **Service Packaging**: Define high-value service offering, target customer profile, and 3-tier pricing structure (Starter / Standard / Pro).
2. **Prospect Research**: Identify 15–20 real prospective businesses across US, UK, UAE, Saudi Arabia, Qatar, Canada, Australia, and Europe.
3. **Outreach Execution**: Draft personalized cold emails with custom observations, value hooks, and portfolio links.
4. **Social Media Campaigns**: Create LinkedIn case studies, educational problem breakdowns, and short-form video demo scripts.
5. **Outreach Tracking**: Maintain structured outreach pipeline tracking company, country, contact, date, channel, status, and follow-ups.
6. **Group Consolidation**: As Group Leader, consolidate team outreach metrics (total contacted, response rate, leads, meetings booked) for Team Lead submission.

### What Was Built (Leader Module - Arsalan Qasim)

Group Leader Arsalan Qasim built an **Interactive Commercialization Command Center**:
- **Service Proposal & Interactive ROI / Pricing Calculator**: Dynamic 3-tier client packaging ($149 Starter / $399 Standard / $799 Pro) with customizable query volume, staff savings, and ROI projections.
- **Smart Cold Outreach Generator**: Generates customized 5-step cold outreach sequences (Initial Pitch, Case Study Follow-up, 15-min Call CTA) based on company name and observed customer service friction.
- **Interactive Live Outreach Tracker**: Full pipeline management board loaded from `week6/data/outreach_tracker.xlsx` pre-populated with 15+ real international prospect organizations across USA, UK, UAE, and Canada.
- **Social Media Marketing Hub**: Copyable, production-ready LinkedIn project launch post, industry carousel script, and short-form video script.
- **Group Leader Consolidation Center**: Dynamic analytics dashboard aggregating group outreach KPIs, conversion funnels, and submission summaries.

### Week 6 Member Tracking

| Member | Module Key | Contribution & Submission | Evidence | Status |
|---|---|---|---|---|
| Arsalan Qasim | `commercial_arsalan` | Full Commercial Command Center, Tiered Pricing, 15+ Real International Leads in Excel Tracker, Cold Email Sequences, Social Media Posts, and Group Consolidation. | `week6/src/modules/commercial_arsalan/`, `week6/data/outreach_tracker.xlsx`, `tests/test_commercial.py` | **Submitted** |
| MUHAMMAD WASIM | `commercial_wasim` | Lead Gen Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_wasim/` | In progress |
| Muhammad Faozan Mujtaba | `commercial_faozan` | BI Dashboard Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_faozan/` | In progress |
| Shahidullah | `commercial_shahidullah` | Chatbot Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_shahidullah/` | In progress |
| Ali Ammar Haider | `commercial_ali_ammar` | Lead Gen Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_ali_ammar/` | In progress |
| Abdul Haseeb | `commercial_abdul_haseeb` | BI Dashboard Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_abdul_haseeb/` | In progress |
| Hammad Abbas | `commercial_hammad` | Chatbot Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_hammad/` | In progress |
| Ali Zaib | `commercial_ali_zaib` | Lead Gen Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_ali_zaib/` | In progress |
| Malik Sudais | `commercial_malik_sudais` | BI Dashboard Commercial Deck & Outreach (Scaffolding ready). | `week6/src/modules/commercial_malik_sudais/` | In progress |



