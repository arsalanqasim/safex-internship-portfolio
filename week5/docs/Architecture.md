# SafeX Week 5 · Chatbot System Architecture & Design Specification

## System Overview

The **Client-Ready AI Customer Support Chatbot** is designed to provide 24/7 conversational support for e-commerce platforms. Built using a layered hybrid approach, it guarantees sub-second response times, zero hallucination on official store policies, and graceful fallback when external LLM APIs are unreachable.

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
                                     [Score >= 0.28 (Match)]                 [Score < 0.28 (Low Conf)]
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

1. **Presentation Layer (`ui.py`)**: Modern Streamlit interface with 4 dedicated tabs (Live Chat, Admin CRUD Panel, Real-Time Audit Logs, and Benchmark Suite).
2. **Controller & Business Logic (`engine.py`)**: Sentiment analysis, TF-IDF cosine matching, dynamic prompt generation, error handling, and KPI aggregation.
3. **Data & Persistence Layer (`data/`)**:
   - `faq_knowledge_base.json`: Dynamic store for FAQ entries, editable via Admin Panel.
   - `chat_logs.json`: Real-time audit log recording every inquiry, matched intent, sentiment, confidence, and timestamp.
4. **Packaging & Standalone Tooling (`deploy_prep.py`)**: Automated script to bundle the module into `chatbot_deploy_package/` with isolated dependencies.
