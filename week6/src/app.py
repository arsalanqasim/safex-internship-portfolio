"""Shared Streamlit shell for Week 6 Sell Your Skills Commercialization Suite."""

from __future__ import annotations

import importlib
import os
import sys

import streamlit as st

# Clean up sys.modules and sys.path to prevent cross-talk/collisions between weeks
if not os.environ.get("SAFEX_ROOT_DASHBOARD"):
    for key in list(sys.modules.keys()):
        if (key == "src" or key.startswith("src.")) and key != __name__ and not key.startswith(__name__ + "."):
            sys.modules.pop(key, None)
    importlib.invalidate_caches()

current_week_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path = [p for p in sys.path if not any(w in p for w in ["week1", "week2", "week3", "week4", "week5", "week6"]) or p == current_week_dir]

if current_week_dir not in sys.path:
    sys.path.insert(0, current_week_dir)

from src.modules.registry import MODULE_REGISTRY

st.set_page_config(page_title="SafeX Sell Your Skills · Week 6", page_icon="💰", layout="wide", initial_sidebar_state="expanded")


def inject_css() -> None:
    """Style the shared shell matching design aesthetics."""
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
        section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--line); }
        section[data-testid="stSidebar"] > div { padding-top: 1.25rem; }
        .block-container { max-width: 1180px; padding-top: 3.5rem; padding-bottom: 4rem; }
        html, body, #root, .stApp, [class*="css"] { font-family: Inter, "Segoe UI", ui-sans-serif, system-ui, sans-serif !important; }
        h1, h2, h3, p { color: var(--ink); }
        .app-mark { display: flex; gap: 10px; align-items: center; margin-bottom: 1.6rem; }
        .app-mark__square { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 8px; background: var(--accent); color: white; font-weight: 700; font-size: 1.1rem; }
        .app-mark__name { font-size: 0.95rem; font-weight: 700; color: var(--ink); }
        .app-mark__caption { font-size: 0.75rem; color: var(--muted); }
        .side-heading { color: var(--muted); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin: 1.35rem 0 0.4rem; }
        .sidebar-note { color: var(--muted); font-size: 0.8rem; line-height: 1.45; margin-top: 1rem; }
        .dashboard-link { display: block; padding: 0.7rem 0.85rem; margin-bottom: 1.25rem; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); color: var(--ink) !important; font-weight: 650; text-align: center; text-decoration: none !important; }
        .dashboard-link:hover { border-color: var(--accent); background: var(--accent-soft); color: var(--accent-dark) !important; }
        [data-testid="stPageLink"] a { display: flex; justify-content: center; width: 100%; box-sizing: border-box; padding: 0.7rem 0.85rem; margin-bottom: 1.25rem; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); color: var(--ink) !important; font-weight: 650; text-decoration: none !important; }
        [data-testid="stPageLink"] a:hover { border-color: var(--accent); background: var(--accent-soft); color: var(--accent-dark) !important; }
        [data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: var(--ink) !important; }
        [data-testid="stRadio"] input { accent-color: var(--accent); }
        .stButton > button { border-radius: 8px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); font-weight: 650; min-height: 2.6rem; box-shadow: none; }
        .stButton > button p { color: inherit !important; }
        .stButton > button:hover { border-color: var(--accent); color: var(--accent-dark); background: var(--accent-soft); }
        .stButton > button[kind="primary"] { background: var(--accent); color: #ffffff; border-color: var(--accent); }
        .stButton > button[kind="primary"]:hover { background: var(--accent-dark); color: #ffffff; }
        [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 0.85rem; }
        div[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] { border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-baseweb="select"] > div { border-radius: 8px; border-color: var(--line); background: var(--surface); color: var(--ink); }
        [data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color: var(--muted); }
        [data-testid="stTextInput"]:focus-within, [data-testid="stTextArea"]:focus-within { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
        .hero-wrap { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }
        .hero-badge { display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-dark); background: var(--accent-soft); padding: 0.25rem 0.6rem; border-radius: 999px; margin-bottom: 0.5rem; }
        .hero-title { font-size: 1.6rem; font-weight: 800; color: var(--ink); margin-bottom: 0.25rem; }
        .hero-subtitle { font-size: 0.95rem; color: var(--muted); line-height: 1.5; }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
        hr { border-color: var(--line) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    theme = st.session_state.get("ui_theme_choice", "Light")
    if theme == "Dark":
        tokens = "--ink:#f8fafc;--muted:#a8b3c2;--line:#334155;--soft:#0e1117;--surface:#151b24;--accent:#2dd4bf;--accent-dark:#5eead4;--accent-soft:#123c3a;"
    else:
        tokens = "--ink:#172033;--muted:#64748b;--line:#dce3ec;--soft:#f6f8fb;--surface:#ffffff;--accent:#0f766e;--accent-dark:#0b5e58;--accent-soft:#e6f5f2;"
    st.markdown(f"<style>:root {{{tokens}}}</style>", unsafe_allow_html=True)


def render_sidebar() -> str:
    """Render shared module navigation and return the selected module key."""
    with st.sidebar:
        dashboard_page = st.session_state.get("_safex_home_page")
        if dashboard_page is not None:
            st.page_link(dashboard_page, label="← Back to Dashboard", icon=":material/home:", width="stretch")
        else:
            st.markdown('<a class="dashboard-link" href="/">← Back to Dashboard</a>', unsafe_allow_html=True)
    
    modules = MODULE_REGISTRY["week6"]
    active_key = st.session_state.get("week6_active_module_key", "commercial_arsalan")
    if active_key not in modules:
        active_key = "commercial_arsalan"
    
    module_keys = list(modules.keys())
    default_index = module_keys.index(active_key)

    with st.sidebar:
        st.markdown(
            """
            <div class="app-mark">
                <div class="app-mark__square">6</div>
                <div>
                    <div class="app-mark__name">SafeX Week 6</div>
                    <div class="app-mark__caption">Sell Your Skills</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-heading">Select Commercial Deck</div>', unsafe_allow_html=True)
        selected_key = st.radio(
            "Module Selector",
            options=module_keys,
            format_func=lambda k: f"{modules[k]['developer']} ({modules[k]['name'][:22]}...)",
            index=default_index,
            label_visibility="collapsed",
        )
        st.session_state["week6_active_module_key"] = selected_key
        st.session_state["active_module_key"] = selected_key

        mod = modules[selected_key]
        st.markdown('<div class="side-heading">Deck Meta</div>', unsafe_allow_html=True)
        st.markdown(f"**Developer:** {mod['developer']}")
        st.markdown(f"**Role:** {mod['role']}")
        st.markdown(f"**Service:** {mod['service_offering']}")
        st.markdown(f"**Markets:** {mod['target_markets']}")
        st.markdown(f"**Status:** `{mod['status']}`")

        if mod.get("deployed_url"):
            st.markdown(f"🌐 [**Live Portfolio Link**]({mod['deployed_url']})")

    return selected_key


def main() -> None:
    inject_css()
    selected_module = render_sidebar()

    try:
        module = importlib.import_module(f"src.modules.{selected_module}")
        if hasattr(module, "render_ui"):
            module.render_ui()
        else:
            st.error(f"Module `src.modules.{selected_module}` does not implement `render_ui()`.")
    except Exception as e:
        st.error(f"Failed to load module `{selected_module}`: {e}")
        st.exception(e)


if __name__ == "__main__":
    main()
