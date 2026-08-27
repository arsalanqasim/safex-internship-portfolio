"""Standalone entrypoint for hosting the RAG Knowledge Assistant on
Streamlit Community Cloud, Render, or Hugging Face Spaces."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from src.ui import render_ui

st.set_page_config(
    page_title="QuickBite Knowledge Assistant — SafeX AI Demo",
    page_icon="📚",
    layout="wide",
)

# Shared theme (copied from the full suite's app.py inject_css(), so this
# standalone deployment looks identical to the module inside the full portfolio app).
st.markdown(
    """
    <style>
    :root {
        --ink: #172033; --muted: #64748b; --line: #dce3ec; --soft: #f6f8fb;
        --surface: #ffffff; --accent: #0f766e; --accent-dark: #0b5e58; --accent-soft: #e6f5f2;
    }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent; }
    html, body, .stApp, [data-testid="stAppViewContainer"] { background: var(--soft) !important; color: var(--ink); }
    .block-container { max-width: 1180px; padding-top: 3.5rem; padding-bottom: 4rem; }
    html, body, #root, .stApp, [class*="css"] { font-family: Inter, "Segoe UI", ui-sans-serif, system-ui, sans-serif !important; }
    h1, h2, h3, p { color: var(--ink); }
    .stButton > button { border-radius: 8px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); font-weight: 650; min-height: 2.6rem; box-shadow: none; }
    .stButton > button p { color: inherit !important; }
    .stButton > button:hover { border-color: var(--accent); color: var(--accent-dark); background: var(--accent-soft); }
    .stButton > button[kind="primary"] { background: var(--accent); color: #ffffff; border-color: var(--accent); }
    .stButton > button[kind="primary"]:hover { background: var(--accent-dark); color: #ffffff; }
    [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 0.85rem; }
    div[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }
    [data-testid="stDataFrame"], [data-testid="stDataEditor"] { border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }
    [data-testid="stTextInput"] input { border-radius: 8px; border-color: var(--line); background: var(--surface); color: var(--ink); }
    [data-testid="stTextInput"]:focus-within { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
    .hero-wrap { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }
    .hero-badge { display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-dark); background: var(--accent-soft); padding: 0.25rem 0.6rem; border-radius: 999px; margin-bottom: 0.5rem; }
    .hero-title { font-size: 1.6rem; font-weight: 800; color: var(--ink); margin-bottom: 0.25rem; }
    .hero-subtitle { font-size: 0.95rem; color: var(--muted); line-height: 1.5; }
    hr { border-color: var(--line) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

if __name__ == "__main__":
    render_ui()
