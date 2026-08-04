"""Standalone Deployment Preparation Script for Chatbot Deployment Module.

Extracts chatbot engine and UI files into a self-contained folder ('deploy_package/')
with a custom main entrypoint app.py and requirements.txt, ready for independent deployment.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

WEEK4_DIR = Path(__file__).resolve().parent
DEPLOY_DIR = WEEK4_DIR / "deploy_package"


def prepare_standalone_package() -> None:
    print("=" * 70)
    print("  SafeX Solutions Group 54 - Chatbot Deployment Packager")
    print("=" * 70)
    
    # 1. Recreate clean deploy directory
    if DEPLOY_DIR.exists():
        shutil.rmtree(DEPLOY_DIR)
    DEPLOY_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[+] Created package directory: {DEPLOY_DIR}")

    # 2. Define source paths
    module_src = WEEK4_DIR / "src" / "modules" / "chatbot_deployment"
    engine_src = module_src / "engine.py"
    ui_src = module_src / "ui.py"

    if not engine_src.exists() or not ui_src.exists():
        print("[-] Error: Chatbot source files not found. Build them first!")
        return

    # 3. Create structure inside deploy_package
    (DEPLOY_DIR / "src").mkdir(parents=True, exist_ok=True)
    # Write a dummy config.py inside src/ to prevent import crashes
    with open(DEPLOY_DIR / "src" / "config.py", "w") as f:
        f.write('from pathlib import Path\nDATA_DIR = Path(__file__).resolve().parent.parent / "data"\n')

    # Create dummy registry.py inside src/
    registry_content = """
MODULE_REGISTRY = {
    "week4": {
        "chatbot_deployment": {
            "title": "Client-Ready AI Chatbot Deployment Package",
            "developer": "Arsalan Qasim",
            "role": "Group Leader",
            "email": "arsalanqasim400@gmail.com",
            "description": "Production chatbot module",
            "tech": ["Python", "scikit-learn", "Streamlit"]
        }
    }
}
"""
    with open(DEPLOY_DIR / "src" / "registry.py", "w", encoding="utf-8") as f:
        f.write(registry_content)

    # 4. Copy chatbot source files
    shutil.copy2(engine_src, DEPLOY_DIR / "src" / "engine.py")
    shutil.copy2(ui_src, DEPLOY_DIR / "src" / "ui.py")

    # Fix relative imports in copied files (change src.modules.chatbot_deployment.engine to src.engine)
    for filepath in [DEPLOY_DIR / "src" / "ui.py", DEPLOY_DIR / "src" / "engine.py"]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # replace import path
        content = content.replace("src.modules.chatbot_deployment.engine", "src.engine")
        content = content.replace("src.modules.registry", "src.registry")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("[+] Copied engine and UI source files and adjusted namespaces.")

    # 5. Create standalone entrypoint app.py at deploy root
    app_entrypoint = """\"\"\"Standalone Chatbot App Entrypoint for Production Hosting.\"\"\"
import os
import streamlit as st

# Setup sys.path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import and execute UI
from src.ui import render_ui

# Set page config as absolute first action
st.set_page_config(page_title="AI Chatbot Deployment", page_icon="💬", layout="wide")

# Hide standard sidebar and navigation if running standalone
st.markdown("<style>[data-testid='stSidebarNav'] {display: none !important;}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_ui()
"""
    with open(DEPLOY_DIR / "app.py", "w", encoding="utf-8") as f:
        f.write(app_entrypoint)
    print("[+] Created standalone app.py entrypoint.")

    # 6. Copy requirements.txt
    requirements_content = """streamlit>=1.25.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.2.0
openpyxl>=3.1.0
"""
    with open(DEPLOY_DIR / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("[+] Created standalone requirements.txt.")

    print("\n" + "=" * 70)
    print("  STANDALONE PACKAGE PREPARED SUCCESSFULLY!")
    print("=" * 70)
    print(f"Your deployment-ready package is inside: {DEPLOY_DIR}\n")
    print("HOW TO DEPLOY:")
    print("1. Open your terminal and change directory to the deploy folder:")
    print(f"   cd {DEPLOY_DIR}")
    print("2. Initialize a new Git repository, commit, and push it to your OWN GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial chatbot release'")
    print("   git remote add origin <your-personal-github-repo-url>")
    print("   git push -u origin main")
    print("3. Deploy to a hosting service:")
    print("   - Hugging Face Spaces: Choose Streamlit SDK, upload or push files directly.")
    print("   - Render: Create a new 'Web Service', link your GitHub repo, set build command to 'pip install -r requirements.txt', and start command to 'streamlit run app.py'.")
    print("4. Update the 'deployed_url' inside week4/src/modules/registry.py with your live link!")
    print("=" * 70)


if __name__ == "__main__":
    prepare_standalone_package()
