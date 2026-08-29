"""Standalone Streamlit App for SafeX Insurance & Finance Lead Qualifier."""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SafeX Insurance & Finance Lead Qualifier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Insert local directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
