"""Standalone Streamlit App for SafeX Client-Ready Customer Support Chatbot."""

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
