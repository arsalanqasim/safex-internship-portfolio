# Group 54 - Week 4 Sprint Consolidated Progress Report

**Date**: August 2026  
**Group Leader**: Arsalan Qasim  
**Project**: AI Department - Client-Ready Sprint  
**To**: SafeX Solutions Team Lead / Evaluators  

---

## Executive Summary
During Week 4, Group 54 transitioned their Week 3 AI agent prototypes into productized, client-ready packages. We have established a unified portfolio dashboard under `week4/` that isolates each member's module. To facilitate individual hosting setups on Render/Vercel/HF Spaces without repository conflict, we introduced a **decentralized deployment registry architecture** where members deploy from their forks and register their live URL links directly back to the central hub.

---

## Team Roster & Milestone Status

| Member Name | Assigned Module | Local Folder Path | Live Deployment URL | Current Status |
|---|---|---|---|---|
| **Arsalan Qasim** | Client-Ready AI Chatbot Deployment Package | `week4/src/modules/chatbot_deployment/` | *Simulated Store Mockup* | **Submission Ready** |
| **MUHAMMAD WASIM** | AI Automation ROI Calculator | `week4/src/modules/roi_calculator_real_estate/` | *Pending Member release* | In Progress |
| **Muhammad Faozan Mujtaba** | RAG-based Knowledge Assistant | `week4/src/modules/knowledge_assistant_airline/` | *Pending Member release* | In Progress |
| **Shahidullah** | AI Model Comparison & Recommendation Report | `week4/src/modules/model_comparison_bank/` | *Pending Member release* | In Progress |
| **Ali Ammar Haider** | Predictive Dashboard for a Small Business | `week4/src/modules/predictive_dashboard_tutor/` | [Live Streamlit App](https://safex-week4-predictive-dashboard-tutor.streamlit.app) | **Submission Ready** |
| **Abdul Haseeb** | Client-Ready AI Chatbot Deployment Package | `week4/src/modules/chatbot_deployment_courier/` | *Pending Member release* | In Progress |
| **Hammad Abbas** | AI Automation ROI Calculator | `week4/src/modules/roi_calculator_daraz/` | *Pending Member release* | In Progress |
| **Ali Zaib** | RAG-based Knowledge Assistant | `week4/src/modules/knowledge_assistant_foodpanda/` | *Pending Member release* | In Progress |
| **Malik Sudais** | AI Model Comparison & Recommendation Report | `week4/src/modules/model_comparison_careem/` | *Pending Member release* | In Progress |

---

## Completed Deliverables

### 1. Client-Ready AI Chatbot Deployment Package (Arsalan Qasim - Group Leader)
1. **Dynamic Rebranding**: A configuration panel in the Streamlit UI enabling dynamic adaptation of corporate branding (brand name and terminology) across the chatbot simulator, 1-page proposal, and ROI calculations.
2. **Error Guard Filters**: Regex gibberish input checks and maximum string length filters preventing empty text or junk submissions.
3. **Warm Human Support Handoff**: Keywords list and low-confidence matching trigger auto-generation of support tickets (`TK-XXXXX`) to simulate live agent transfer.
4. **Interactive ROI Cost Calculator**: Slider inputs mapping staff hours and hourly wages against AI pricing options to output real cost savings.
5. **Excel Outreach Tracker**: A logging interface writing target organization outreach platform, date, and status logs into `week4/data/outreach_tracker.xlsx`.
6. **Walkthrough Guidelines**: Visual presenter walkthrough template and a preparation script (`deploy_prep.py`) for standalone deployment.

### 2. Predictive Dashboard for a Small Business (Ali Ammar Haider)
1. **OLS Linear Regression Forecasting Engine**: Trained `scikit-learn` Linear Regression model on 24 months of enrollment data to project Month 25 student recruitment and evaluate fit accuracy ($R^2$, MAE).
2. **Historical vs. Predicted Visualizations**: Matplotlib trendline charts dynamically styled to match Light/Dark UI theme selections.
3. **Dynamic Business Recommendations**: Programmatically evaluates dataset metrics to generate 3 actionable operational insights (Tutor Recruiting, Funnel UX, Administrative Capacity).
4. **Standalone Deployment Package**: Extracted production package under `week4/tutor_deploy_package/` deployed live at [safex-week4-predictive-dashboard-tutor.streamlit.app](https://safex-week4-predictive-dashboard-tutor.streamlit.app).
5. **Automated Test Suite**: Full `pytest` coverage for dataset loading, regression predictions, recommendation counts, and dynamic scenario evaluation.

---

## Action Items & Next Steps
- Remaining team members will complete their specific business logic inside their assigned module folders and deploy them.
- Deployed URLs will be linked in `week4/src/modules/registry.py` to activate the "🟢 Live" badge on the Home dashboard.
- Consolidated status reports will be shared with the SafeX Solutions Team Lead.
