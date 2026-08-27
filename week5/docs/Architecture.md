# SafeX Week 5 · Chatbot System Architecture & Design Specification

## System Overview

The **Client-Ready AI Customer Support Chatbot** suite is designed to provide 24/7 conversational support for e-commerce platforms. Built using a layered hybrid approach, it guarantees sub-second response times, zero hallucination on official store policies, and graceful fallback when external LLM APIs are unreachable.

---

## Architecture Diagram

```text
                               ┌─────────────────────────┐
                               │   Customer Interaction   │
                               │ (Streamlit Chat Widget) │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │ Intent & Sentiment Gate │
                               └────────────┬────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         [Frustration / Human Request]                   [Standard FAQ Inquiry]
                    │                                               │
                    ▼                                               ▼
       ┌────────────────────────┐                      ┌────────────────────────┐
       │ Human Handoff Protocol │                      │   TF-IDF Semantic      │
       │ Priority Support Desk  │                      │   Vector Matcher       │
       └────────────────────────┘                      └────────────┬───────────┘
                                                                    │
                                                ┌───────────────────┴───────────────────┐
                                                ▼                                       ▼
                                     [Score >= Threshold (Match)]            [Score < Threshold (Low Conf)]
                                                │                                       │
                                                ▼                                       ▼
                                    ┌───────────────────────┐               ┌───────────────────────┐
                                    │ Live LLM API Synthesis│               │ Polite Topic Guidance │
                                    │ (Gemini / OpenAI)     │               │   & Escalation Prompt │
                                    └───────────┬───────────┘               └───────────────────────┘
                                                │ (Offline Fallback)
                                                ▼
                                    ┌───────────────────────┐
                                    │  Grounded FAQ Policy  │
                                    │      JSON Store       │
                                    └───────────────────────┘
```

---

## Layer Breakdown

1. **Presentation Layer (`ui.py`)**: Modern Streamlit interface with 5 dedicated tabs (Live Customer Chat, Knowledge Base, Admin CRUD Panel, Real-Time Audit Logs, and Benchmark Suite).
2. **Controller & Business Logic (`engine.py`)**: Sentiment analysis, TF-IDF cosine matching & token overlap calculation, dynamic confidence scoring, error handling, and KPI aggregation.
3. **Data & Persistence Layer (`data/`)**:
   - `faq_knowledge_base.json`: Dynamic store for FAQ entries, editable via Admin Panel.
   - `chat_logs.json`: Real-time audit log recording every inquiry, matched intent, confidence, handoff status, response time, and timestamp.
4. **Standalone Packaging**: Isolated deploy packages (e.g. `chatbot_deploy_package/` and `chatbot_deploy_package_ali_ammar/`) with independent dependencies and entrypoints.

---

## Module Implementations

### 1. `chatbot_arsalan` (SafeX Apparel & Co.)
* **Developer:** Arsalan Qasim
* **Path:** `week5/src/modules/chatbot_arsalan/`
* **Features:** TF-IDF semantic vector matcher, sentiment-aware escalation, real-time audit logging, persistent admin panel.

### 2. `chatbot_ali_ammar` (ShopEase E-Commerce)
* **Developer:** Ali Ammar Haider
* **Path:** `week5/src/modules/chatbot_ali_ammar/`
* **Deploy Package:** `week5/chatbot_deploy_package_ali_ammar/`
* **Features:** Hybrid TF-IDF + token overlap engine, dynamic confidence scoring (0.0 to 1.0), explicit human escalation, conversation logging, persistent admin CRUD, live analytics dashboard, 17-case benchmark suite.
