"""Standalone deployment packaging script for SafeX Week 5 Insurance & Finance
Lead Qualifier (Ali Zaib).

Exports `lead_gen_ali_zaib` into an isolated, standalone deployment directory
ready for 1-click publishing to Streamlit Community Cloud, Render, or HuggingFace Spaces.
"""

import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SOURCE_MODULE = os.path.join(BASE_DIR, "src", "modules", "lead_gen_ali_zaib")
TARGET_DIR = os.path.join(BASE_DIR, "lead_qualifier_deploy_package")


def prepare_deployment_package() -> None:
    """Bundle the standalone lead qualifier deployment package."""
    print(f"[PACKAGING] Standalone Lead Qualifier to: {TARGET_DIR}")

    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "src", "data"), exist_ok=True)

    # 1. Copy data files
    data_src = os.path.join(SOURCE_MODULE, "data")
    if os.path.exists(data_src):
        for fname in os.listdir(data_src):
            src_f = os.path.join(data_src, fname)
            if os.path.isfile(src_f):
                shutil.copy2(src_f, os.path.join(TARGET_DIR, "src", "data", fname))

    # 2. Copy engine and UI to src/
    shutil.copy2(os.path.join(SOURCE_MODULE, "engine.py"), os.path.join(TARGET_DIR, "src", "engine.py"))
    shutil.copy2(os.path.join(SOURCE_MODULE, "ui.py"), os.path.join(TARGET_DIR, "src", "ui.py"))

    # ui.py uses a relative import ("from .engine import ...") since it's a
    # package submodule in the monorepo. Rewrite it to a flat "from src.engine
    # import ..." style so the standalone package (no package __init__ needed)
    # imports correctly.
    ui_path = os.path.join(TARGET_DIR, "src", "ui.py")
    with open(ui_path, "r", encoding="utf-8") as f:
        ui_code = f.read()
    ui_code = ui_code.replace("from .engine import", "from src.engine import")
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(ui_code)

    # 3. Create standalone entrypoint app.py
    standalone_app = """\"\"\"Standalone Streamlit App for SafeX Insurance & Finance Lead Qualifier.\"\"\"

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SafeX Insurance & Finance Lead Qualifier",
    page_icon="\U0001F6E1\ufe0f",
    layout="wide",
    initial_sidebar_state="collapsed",
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
pandas>=2.0.0
numpy>=1.24.0
"""
    with open(os.path.join(TARGET_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(standalone_reqs)

    # 5. Create standalone README.md
    readme_content = """# \U0001F6E1\ufe0f SafeX Insurance & Finance Lead Qualifier

A transparent, rubric-based lead scoring tool for insurance/wealth-management
sales teams, built by **Ali Zaib** (SafeX Solutions AI/ML Internship, Group 54).

## Features
- **Five-factor weighted scoring** (0-100): policy value fit, coverage/budget
  fit, urgency/timeline, risk profile, and engagement channel quality.
- **Explainable, not a black box**: every score breaks down into its five
  contributing factors, plus qualitative flags a human reviewer can act on.
- **Single-lead qualification form** and **batch CSV scoring** (28-lead sample
  dataset included, or upload your own).
- **Tier-based prioritization**: Hot Lead, Qualified, Nurture, or Low Priority.

## Local Setup & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Community Cloud
1. Push this folder to its own GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Create a new app, pick the repo/branch, set main file path to `app.py`.
4. Deploy — Streamlit Cloud installs `requirements.txt` automatically.
"""
    with open(os.path.join(TARGET_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("[SUCCESS] Standalone deployment package created successfully at `week5/lead_qualifier_deploy_package/`.")


if __name__ == "__main__":
    prepare_deployment_package()
