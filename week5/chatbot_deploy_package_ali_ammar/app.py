"""Standalone Streamlit Deployment App for ShopEase AI Customer Support Chatbot (Ali Ammar Haider)."""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="ShopEase · AI Customer Support Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Insert local directory into sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
