import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="Predictive Dashboard Tutor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.modules.predictive_dashboard_tutor.ui import render_ui

if __name__ == "__main__":
    render_ui()
