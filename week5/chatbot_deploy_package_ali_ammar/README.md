# ShopEase AI Customer Support Chatbot — Standalone Deployment Package

**Developer:** Ali Ammar Haider
**SafeX Solutions Internship — Week 5 Deliverable**

This is the standalone, production-ready deployment package for the **ShopEase AI Customer Support Chatbot**. It can be deployed directly to **Streamlit Community Cloud**, **Hugging Face Spaces**, **AWS**, or **Render**.

---

## Package Contents

```text
chatbot_deploy_package_ali_ammar/
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Independent Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Deployment instructions
├── src/
│   ├── __init__.py
│   ├── engine.py              # NLP Engine, TF-IDF, CRUD & Benchmarking
│   └── ui.py                  # Full 5-tab Streamlit user interface
└── data/
    ├── faq_knowledge_base.json # Persistent 15+ FAQ database
    └── chat_logs.json         # Conversation audit logs
```

---

## Quick Start (Local Run)

1. Navigate into this deployment directory:
   ```bash
   cd week5/chatbot_deploy_package_ali_ammar
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`.

---

## Features

- **Offline-Ready Hybrid NLP**: Powered by TF-IDF & Cosine Similarity with Token Overlap score.
- **Dynamic Confidence & Escalation**: Automatic fallback for queries < 0.42 confidence and explicit human requests.
- **No-Code Admin Panel**: Add, edit, delete, or reset FAQs with instant JSON storage persistence.
- **Interaction Analytics**: Live KPIs for total inquiries, resolution rates, confidence, and latency.
- **Automated Benchmark Suite**: Built-in 17-question test runner for instant validation.
