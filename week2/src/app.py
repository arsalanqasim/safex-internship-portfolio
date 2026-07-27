"""Shared Streamlit shell for the Week 2 automation modules."""

from __future__ import annotations

import importlib
import os
import sys

import streamlit as st

# Clean up sys.modules and sys.path to prevent cross-talk/collisions between weeks
for key in list(sys.modules.keys()):
    if (key == "src" or key.startswith("src.")) and key != __name__:
        del sys.modules[key]

current_week_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path = [p for p in sys.path if not any(w in p for w in ["week1", "week2", "week3"]) or p == current_week_dir]

if current_week_dir not in sys.path:
    sys.path.insert(0, current_week_dir)

from src.modules.registry import MODULE_REGISTRY


st.set_page_config(page_title="SafeX Automation Suite", page_icon="S", layout="wide", initial_sidebar_state="expanded")


def inject_css() -> None:
    """Style the shared shell without requiring changes to member modules."""
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
        .block-container { max-width: 1180px; padding-top: 4.5rem; padding-bottom: 4rem; }
        html, body, #root, .stApp, [class*="css"] { font-family: Inter, "Segoe UI", ui-sans-serif, system-ui, sans-serif !important; }
        h1, h2, h3, p { color: var(--ink); }
        .app-mark { display: flex; gap: 10px; align-items: center; margin-bottom: 1.6rem; }
        .app-mark__square { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 7px; background: var(--accent); color: white; font-weight: 700; }
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
    """Render the sidebar and return the selected module key."""
    with st.sidebar:
        dashboard_page = st.session_state.get("_safex_home_page")
        if dashboard_page is not None:
            st.page_link(dashboard_page, label="← Back to Dashboard", icon=":material/home:", width="stretch")
        else:
            st.markdown('<a class="dashboard-link" href="/">← Back to Dashboard</a>', unsafe_allow_html=True)
    modules = MODULE_REGISTRY["week2"]
    active_key = st.session_state.get("active_module_key", "invoice_automation")
    if active_key not in modules:
        active_key = "invoice_automation"
    with st.sidebar:
        st.markdown(
            """
            <div class="app-mark">
                <div class="app-mark__square">S</div>
                <div><div class="app-mark__name">SafeX</div><div class="app-mark__caption">Automation Suite · Week 2</div></div>
            </div>
            <div class="side-heading">Modules</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="side-heading">Appearance</div>', unsafe_allow_html=True)
        st.radio(
            "Color mode",
            ["Light", "Dark"],
            key="ui_theme_choice",
            horizontal=True,
            label_visibility="collapsed",
        )
        for key, module in modules.items():
            label = module["title"]
            if st.button(label, key=f"module_{key}", use_container_width=True):
                active_key = key
                st.session_state.active_module_key = key
                st.rerun()
        st.divider()
        st.markdown('<div class="side-heading">Workspace</div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-note">Each automation module is independently owned. This workspace provides one consistent place to review their work.</p>', unsafe_allow_html=True)
    return active_key


def apply_active_module_style(active_key: str) -> None:
    """Highlight the module currently displayed in the workspace."""
    st.markdown(
        f"""
        <style>
        div.st-key-module_{active_key} button {{
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent-dark);
            box-shadow: inset 3px 0 0 var(--accent);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_module(active_key: str) -> None:
    metadata = MODULE_REGISTRY["week2"][active_key]
    if metadata["status"] not in {"Completed", "Submission Ready"}:
        render_pending_module(metadata)
        return
    try:
        importlib.import_module(metadata["import_path"]).render_ui()
    except Exception as exc:
        st.error(f"The {metadata['title']} module could not be loaded.")
        st.exception(exc)


def render_pending_module(metadata: dict[str, object]) -> None:
    """Show a clear review screen for a member assignment that is not yet complete."""
    st.markdown('<div class="eyebrow">Week 2 · Assigned module</div>', unsafe_allow_html=True)
    st.title(str(metadata["title"]))
    st.caption("This assignment is awaiting a completed module submission.")

    member, status = st.columns(2)
    with member:
        st.markdown("**Assigned member**")
        st.write(str(metadata["developer"]))
    with status:
        st.markdown("**Current status**")
        st.write("Not submitted")

    st.subheader("Assignment details")
    st.write(str(metadata["description"]))

    detail_left, detail_right = st.columns(2)
    with detail_left:
        st.markdown("**Member contact**")
        st.write(str(metadata["email"]))
    with detail_right:
        st.markdown("**Expected stack**")
        st.write(" · ".join(str(item) for item in metadata["tech"]))

    st.info("The shared application shell is ready. This screen will be replaced automatically when the member module is marked complete and integrated.")


def main() -> None:
    inject_css()
    active_key = render_sidebar()
    apply_active_module_style(active_key)
    render_module(active_key)


if __name__ == "__main__":
    main()
