"""Standalone Chatbot App Entrypoint for Production Hosting."""
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
