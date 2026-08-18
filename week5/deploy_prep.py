"""Standalone deployment packaging script for SafeX Week 5 Chatbot.

Exports `chatbot_arsalan` into an isolated, standalone deployment directory
ready for 1-click publishing to Streamlit Community Cloud, Render, or HuggingFace Spaces.
"""

import os
import shutil
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SOURCE_MODULE = os.path.join(BASE_DIR, "src", "modules", "chatbot_arsalan")
TARGET_DIR = os.path.join(BASE_DIR, "chatbot_deploy_package")


def prepare_deployment_package() -> None:
    """Bundle the standalone chatbot deployment package."""
    print(f"[PACKAGING] Standalone Chatbot to: {TARGET_DIR}")
    
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "data"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "src"), exist_ok=True)


    # 1. Copy Data files
    data_src = os.path.join(SOURCE_MODULE, "data")
    if os.path.exists(data_src):
        for fname in os.listdir(data_src):
            src_f = os.path.join(data_src, fname)
            if os.path.isfile(src_f):
                shutil.copy2(src_f, os.path.join(TARGET_DIR, "data", fname))

    # 2. Copy Engine and UI to src/
    shutil.copy2(os.path.join(SOURCE_MODULE, "engine.py"), os.path.join(TARGET_DIR, "src", "engine.py"))
    shutil.copy2(os.path.join(SOURCE_MODULE, "ui.py"), os.path.join(TARGET_DIR, "src", "ui.py"))
    shutil.copy2(os.path.join(SOURCE_MODULE, "__init__.py"), os.path.join(TARGET_DIR, "src", "__init__.py"))

    # 3. Create standalone entrypoint app.py
    standalone_app = """\"\"\"Standalone Streamlit App for SafeX Client-Ready Customer Support Chatbot.\"\"\"

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SafeX Apparel · Customer Support AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Insert local directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
"""
    with open(os.path.join(TARGET_DIR, "app.py"), "w", encoding="utf-8") as f:
        f.write(standalone_app)

    # 4. Create standalone requirements.txt
    standalone_reqs = """streamlit>=1.35.0
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.0.0
python-dotenv>=1.0.1
"""
    with open(os.path.join(TARGET_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(standalone_reqs)

    # 5. Create .env.example
    env_example = """# SafeX Chatbot Live API Keys (Optional - Local TF-IDF Fallback Active)
GEMINI_API_KEY=
OPENAI_API_KEY=
"""
    with open(os.path.join(TARGET_DIR, ".env.example"), "w", encoding="utf-8") as f:
        f.write(env_example)

    # 6. Create standalone README.md
    readme_content = """# 🛍️ SafeX Client-Ready AI Customer Support Chatbot

A production-ready AI Customer Support Chatbot built for **SafeX Apparel & Co.** by **Arsalan Qasim** (SafeX Solutions AI/ML Internship Group 54).

## 🚀 Features
- **15+ Verified FAQs**: Instant answers for shipping, returns, international delivery, sizing, and payment methods.
- **Sentiment & Escalation Layer**: Automated sentiment-aware human handoff for customer frustration or explicit live agent requests.
- **No-Code Admin Panel**: Manage, add, edit, or delete store FAQ policies without touching code.
- **Real-Time Audit Trail**: Complete conversation logging with CSV/JSON export.
- **Hybrid AI Engine**: Live Gemini / OpenAI synthesis with fail-safe local TF-IDF semantic vector fallback.

## 🛠️ Local Setup & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
"""
    with open(os.path.join(TARGET_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("[SUCCESS] Standalone deployment package created successfully at `week5/chatbot_deploy_package/`.")




if __name__ == "__main__":
    prepare_deployment_package()

