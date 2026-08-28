"""Standalone deployment packaging script for SafeX Week 6 Insurance Lead
Scoring Commercial Service (Ali Zaib).

Exports `commercial_ali_zaib` into an isolated, standalone deployment
directory ready for 1-click publishing to Streamlit Community Cloud,
Render, or HuggingFace Spaces.
"""

import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SOURCE_MODULE = os.path.join(BASE_DIR, "src", "modules", "commercial_ali_zaib")
TARGET_DIR = os.path.join(BASE_DIR, "insurance_commercial_deploy_package")


def prepare_deployment_package() -> None:
    """Bundle the standalone commercial hub deployment package."""
    print(f"[PACKAGING] Standalone Commercial Hub to: {TARGET_DIR}")

    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "src", "data"), exist_ok=True)

    # 1. Copy engine and UI to src/
    shutil.copy2(os.path.join(SOURCE_MODULE, "engine.py"), os.path.join(TARGET_DIR, "src", "engine.py"))
    shutil.copy2(os.path.join(SOURCE_MODULE, "ui.py"), os.path.join(TARGET_DIR, "src", "ui.py"))

    # ui.py and engine.py use relative imports ("from .engine import ...")
    # since they're package submodules in the monorepo. Rewrite to a flat
    # "from src.engine import ..." style for the standalone package.
    ui_path = os.path.join(TARGET_DIR, "src", "ui.py")
    with open(ui_path, "r", encoding="utf-8") as f:
        ui_code = f.read()
    ui_code = ui_code.replace("from .engine import", "from src.engine import")
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(ui_code)

    # engine.py's DATA_DIR is relative to __file__, which still resolves
    # correctly once copied (it points to a "data" folder next to itself),
    # so no path rewriting is needed there.

    # 2. Create standalone entrypoint app.py
    standalone_app = """\"\"\"Standalone Streamlit App for SafeX Insurance Lead Scoring Commercial Hub.\"\"\"

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SafeX Insurance Lead Qualifier - Commercial Hub",
    page_icon="\U0001F6E1\ufe0f",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
"""
    with open(os.path.join(TARGET_DIR, "app.py"), "w", encoding="utf-8") as f:
        f.write(standalone_app)

    # 3. Create standalone requirements.txt
    standalone_reqs = """streamlit>=1.35.0
pandas>=2.0.0
openpyxl>=3.1.0
"""
    with open(os.path.join(TARGET_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(standalone_reqs)

    # 4. Create standalone README.md
    readme_content = """# \U0001F6E1\ufe0f SafeX Insurance Lead Qualifier — Commercial Hub

A sellable commercialization package for the Insurance & Finance Lead
Qualifier, built by **Ali Zaib** (SafeX Solutions AI/ML Internship, Group 54).

## Features
- **Tiered pricing** (Broker Starter / Agency Pro / Underwriting Enterprise)
  for insurance agencies and brokers.
- **Interactive ROI calculator** quantifying manual review time and cost
  savings from automated lead qualification.
- **Personalized cold outreach generator** — a 3-step email sequence for a
  named agency/broker prospect.
- **Outreach pipeline tracker** with Excel export.

## Local Setup & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Community Cloud
1. Push this folder to its own GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Create a new app, pick the repo/branch, set main file path to `app.py`.
4. Deploy.
"""
    with open(os.path.join(TARGET_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("[SUCCESS] Standalone deployment package created at `week6/insurance_commercial_deploy_package/`.")


if __name__ == "__main__":
    prepare_deployment_package()
