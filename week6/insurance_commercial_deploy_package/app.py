"""Standalone Streamlit App for SafeX Insurance Lead Scoring Commercial Hub."""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SafeX Insurance Lead Qualifier - Commercial Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
