# ShopEase AI Customer Support Chatbot

**Developer:** Ali Ammar Haider
**Institution:** COMSATS University Islamabad
**Role:** Team Member — SafeX Group 54
**Domain:** E-Commerce & Retail Customer Support Automation
**Task Track:** AI Customer Support Chatbot (Client-Ready) — Week 5

---

## Executive Overview

The **ShopEase AI Customer Support Chatbot** is a production-grade, client-ready conversational agent designed to automate repetitive customer service inquiries for modern e-commerce stores, retail brands, and service businesses.

By pairing a hybrid **TF-IDF Vectorizer (scikit-learn)** with N-gram keyword matching, dynamic confidence scoring, explicit human escalation rules, real-time audit logging, and a persistent no-code Admin Panel, ShopEase reduces customer support resolution times from hours to milliseconds while eliminating AI hallucinations.

---

## Key Features

1. **Local & Off-line Capable NLP Engine**:
   - Natural language question variation matching ("Where is my order?" = "Can I track my parcel?").
   - TF-IDF matrix cosine similarity blended with keyword weighting.
   - 0.0 to 1.0 dynamic confidence scoring.
   - Zero hallucination policy — falls back to polite support contact message for out-of-scope inquiries.

2. **Intelligent Human Escalation**:
   - Triggers automatic human handoff when match confidence drops below 0.42.
   - Immediately detects explicit human requests ("talk to agent", "speak to real person", "manager").

3. **No-Code Admin Panel (CRUD)**:
   - Live management of active FAQs (Add, Edit, Delete, Factory Reset).
   - Real-time JSON persistence (`faq_knowledge_base.json`).

4. **Analytics & Audit Logs**:
   - Real-time KPI dashboard: Total Conversations, Average Confidence %, Resolution Rate %, Human Handoff Rate %, and Average Latency.
   - Comprehensive chat interaction logging (`chat_logs.json`) with timestamps, confidence scores, and latency metrics.

5. **Automated Accuracy Benchmark Suite**:
   - 17-question test suite measuring intent detection accuracy and latency.
   - 100% test pass rate on core customer service scenarios.

---

## System Architecture

```text
                               +----------------------------+
                               |     Streamlit UI (ui.py)    |
                               +--------------+-------------+
                                              |
                                              v
                              +-------------------------------+
                              | CustomerSupportEngine (engine) |
                              +---------------+---------------+
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
                     v                        v                        v
        +-------------------------+  +-----------------+  +-------------------------+
        | TF-IDF & NLP Matcher    |  | Human Escalation|  | Admin CRUD Manager      |
        | (scikit-learn/cosine)   |  | & Fallback Logic|  | (JSON Persistence)      |
        +------------+------------+  +--------+--------+  +------------+------------+
                     |                        |                        |
                     +------------------------+------------------------+
                                              |
                                              v
                                +---------------------------+
                                | JSON Data Store           |
                                | - faq_knowledge_base.json |
                                | - chat_logs.json          |
                                +---------------------------+
```

---

## Folder Structure

```text
week5/src/modules/chatbot_ali_ammar/
├── __init__.py
├── engine.py                  # Core NLP engine, TF-IDF matching, CRUD & benchmarking
├── ui.py                      # Streamlit UI with 5 interactive tabs
├── README.md                  # Detailed module documentation
└── data/
    ├── faq_knowledge_base.json # Persistent 15+ FAQ database
    └── chat_logs.json         # Interaction audit logs
```

---

## How to Run

### Option 1: Via Main Week 5 Suite Application
From repository root:
```bash
streamlit run week5/src/app.py
```
Select **ShopEase AI Customer Support Chatbot (Ali Ammar Haider)** in the sidebar module selector.

### Option 2: Via Standalone Deployment Package
From `week5/chatbot_deploy_package_ali_ammar/`:
```bash
cd week5/chatbot_deploy_package_ali_ammar
pip install -r requirements.txt
streamlit run app.py
```

---

## Testing & Verification

Run the full pytest suite:
```bash
python -m pytest week5/tests/test_chatbot_ali_ammar.py -v
```

All 12 unit tests pass, verifying:
- Known FAQ questions
- Question variations
- Out-of-scope fallback
- Explicit human escalation
- Confidence score ranges
- Conversation logging
- Admin CRUD operations
- Benchmark runner & KPI calculations
