"""Central dashboard entrypoint for SafeX Internship Portfolio - Group 54."""

import importlib.util
import os
import sys
import streamlit as st

# ==============================================================================
# 1. Global Page Configuration
# ==============================================================================
# set_page_config must be called as the absolute first Streamlit command.
st.set_page_config(
    page_title="SafeX Group 54 · Portfolio Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Save the original set_page_config so it doesn't get completely lost, 
# then patch it to be a no-op for subpages.
_original_set_page_config = st.set_page_config
st.set_page_config = lambda *args, **kwargs: None


# ==============================================================================
# 2. Dynamic Registry Loader Helper
# ==============================================================================
def load_weekly_registry(week_dir: str, week_key: str) -> dict | None:
    """Dynamically load MODULE_REGISTRY from a specific week directory without polluting sys.path."""
    registry_path = os.path.join(os.path.abspath(week_dir), "src", "modules", "registry.py")
    if not os.path.exists(registry_path):
        return None
    try:
        spec = importlib.util.spec_from_file_location(f"{week_key}_registry_temp", registry_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.MODULE_REGISTRY.get(week_key, {})
    except Exception:
        return None


# ==============================================================================
# 3. Custom CSS Styles Injection (SafeX Aesthetics)
# ==============================================================================
def inject_global_styles() -> None:
    """Inject premium CSS styling matching SafeX branding guidelines."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #172033;
            --muted: #64748b;
            --line: #dce3ec;
            --soft: #f6f8fb;
            --surface: #ffffff;
            --surface-raised: #ffffff;
            --accent: #0f766e;
            --accent-dark: #0b5e58;
            --accent-soft: #e6f5f2;
            --hero-badge-text: #d1fae5;
            --success-bg: #ecfdf5;
            --success-text: #065f46;
            --warning-bg: #fffbeb;
            --warning-text: #b45309;
        }

        /* Global typography & layout */
        html, body, #root, .stApp, [class*="css"] {
            font-family: Inter, "Segoe UI", ui-sans-serif, system-ui, sans-serif !important;
        }
        
        header[data-testid="stHeader"] {
            background: transparent;
        }
        
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: var(--soft) !important;
            color: var(--ink);
        }
        
        section[data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--line);
        }
        
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }
        
        .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }
        
        /* Sidebar Logo */
        .app-mark {
            display: flex;
            gap: 12px;
            align-items: center;
            margin-bottom: 1.8rem;
            padding: 0 0.5rem;
        }
        .app-mark__square {
            display: grid;
            place-items: center;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            font-weight: 800;
            font-size: 1.25rem;
        }
        .app-mark__name {
            font-size: 1rem;
            font-weight: 700;
            color: var(--ink);
        }
        .app-mark__caption {
            font-size: 0.75rem;
            color: var(--muted);
        }
        .side-heading {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 1.35rem 0.5rem 0.4rem;
        }
        .sidebar-note {
            color: var(--muted);
            font-size: 0.8rem;
            line-height: 1.5;
            margin: 1rem 0.5rem 0;
        }
        .stButton > button {
            min-height: 2.6rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--surface);
            color: var(--ink);
            font-weight: 650;
            box-shadow: none;
            transition: border-color .15s ease, background .15s ease, color .15s ease;
        }
        .stButton > button p { color: inherit !important; }
        .stButton > button:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
            color: var(--accent-dark);
        }
        .stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
            color: #062e2b;
        }
        .stButton > button[kind="primary"] p { color: inherit !important; }
        .stButton > button[kind="primary"]:hover {
            background: var(--accent-dark);
            border-color: var(--accent-dark);
            color: #062e2b;
        }
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] label p,
        [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
            color: var(--ink) !important;
        }
        [data-testid="stRadio"] input { accent-color: var(--accent); }
        
        /* Hero Section */
        .hero-banner {
            background: linear-gradient(135deg, #0f766e 0%, #115e59 50%, #134e4a 100%);
            border-radius: 16px;
            padding: 2.5rem 3rem;
            color: #ffffff;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.15);
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.03);
            pointer-events: none;
        }
        .hero-badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--hero-badge-text);
            border: 1px solid rgba(230, 245, 242, 0.3);
            background: rgba(230, 245, 242, 0.1);
            padding: 0.3rem 0.75rem;
            border-radius: 9999px;
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.25rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            line-height: 1.2;
            color: #ffffff;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #ccfbf1;
            margin: 0;
            max-width: 800px;
            font-weight: 400;
            line-height: 1.6;
        }
        
        /* Portfolio Cards Grid */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }
        .portfolio-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1.75rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        .portfolio-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent);
            box-shadow: 0 12px 20px -8px rgba(15, 118, 110, 0.15), 0 4px 6px -2px rgba(15, 118, 110, 0.05);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        .card-icon {
            font-size: 2rem;
            margin: 0;
        }
        .status-badge {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
        }
        .status-badge--ready {
            background-color: var(--success-bg);
            color: var(--success-text);
        }
        .status-badge--progress {
            background-color: var(--warning-bg);
            color: var(--warning-text);
        }
        .card-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--ink);
            margin: 0 0 0.5rem 0;
        }
        .card-desc {
            font-size: 0.875rem;
            color: var(--muted);
            line-height: 1.5;
            margin-bottom: 1.5rem;
        }
        
        /* Interactive Metrics */
        .metric-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: center;
        }
        .metric-card__val {
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--accent);
            margin-bottom: 0.25rem;
        }
        .metric-card__lbl {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Timeline styling */
        .timeline-container {
            position: relative;
            padding: 1rem 0;
        }
        .timeline-item {
            position: relative;
            padding-left: 2rem;
            padding-bottom: 1.5rem;
            border-left: 2px solid var(--line);
        }
        .timeline-item:last-child {
            border-left: 2px solid transparent;
            padding-bottom: 0;
        }
        .timeline-dot {
            position: absolute;
            left: -6px;
            top: 4px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent);
            border: 2px solid var(--surface);
        }
        .timeline-date {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }
        .timeline-title {
            font-size: 1rem;
            font-weight: 700;
            color: var(--ink);
            margin-bottom: 0.25rem;
        }
        .timeline-desc {
            font-size: 0.85rem;
            color: var(--muted);
            line-height: 1.45;
        }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
            border: 1px solid var(--line);
            border-radius: 10px;
            overflow: hidden;
        }
        [data-testid="stDataFrame"] *, [data-testid="stDataEditor"] * {
            border-color: var(--line) !important;
        }
        hr { border-color: var(--line) !important; }
        @media (max-width: 900px) {
            .hero-banner { padding: 2rem 1.5rem; }
            .hero-title { font-size: 1.8rem; }
            .card-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    theme = st.session_state.get("ui_theme_choice", "Light")
    if theme == "Dark":
        tokens = """
            --ink: #f8fafc; --muted: #a8b3c2; --line: #334155; --soft: #0e1117;
            --surface: #151b24; --surface-raised: #1e293b; --accent: #2dd4bf;
            --accent-dark: #5eead4; --accent-soft: #123c3a; --hero-badge-text: #ccfbf1;
            --success-bg: #123c32; --success-text: #86efac;
            --warning-bg: #4a3512; --warning-text: #fde68a;
        """
    else:
        tokens = """
            --ink: #172033; --muted: #64748b; --line: #dce3ec; --soft: #f6f8fb;
            --surface: #ffffff; --surface-raised: #ffffff; --accent: #0f766e;
            --accent-dark: #0b5e58; --accent-soft: #e6f5f2; --hero-badge-text: #d1fae5;
            --success-bg: #ecfdf5; --success-text: #065f46;
            --warning-bg: #fffbeb; --warning-text: #b45309;
        """
    st.markdown(f"<style>:root {{ {tokens} }}</style>", unsafe_allow_html=True)


# ==============================================================================
# 4. Home Dashboard Screen
# ==============================================================================
def show_dashboard() -> None:
    """Render the central Home Dashboard."""
    inject_global_styles()
    render_sidebar_branding()

    # Hero Banner Section
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-badge">SafeX Solutions · Summer Internship 2026</div>
            <h1 class="hero-title">Group 54 Internship Portfolio</h1>
            <p class="hero-subtitle">
                A unified corporate research and prototype workspace. Explore our weekly milestones, 
                AI solutions, and modular automated systems built to deliver commercial value.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Key Statistics
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.markdown('<div class="metric-card"><div class="metric-card__val">3</div><div class="metric-card__lbl">Milestone Weeks</div></div>', unsafe_allow_html=True)
    with col_stat2:
        st.markdown('<div class="metric-card"><div class="metric-card__val">19</div><div class="metric-card__lbl">Total Modules</div></div>', unsafe_allow_html=True)
    with col_stat3:
        st.markdown('<div class="metric-card"><div class="metric-card__val">9</div><div class="metric-card__lbl">Team Members</div></div>', unsafe_allow_html=True)
    with col_stat4:
        st.markdown('<div class="metric-card"><div class="metric-card__val">100%</div><div class="metric-card__lbl">Local Isolation</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Main Grid (Workspace milestones)
    st.subheader("🏁 Internship Milestones")
    
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown(
            """
            <div class="portfolio-card">
                <div class="card-header">
                    <span class="card-icon">💬</span>
                    <span class="status-badge status-badge--ready">Completed</span>
                </div>
                <div>
                    <h3 class="card-title">Week 1: AI FAQ Chatbot</h3>
                    <p class="card-desc">
                        A local SafeX FAQ chatbot leveraging advanced text similarity algorithms. Runs fully offline on standard CPU environments with zero external API costs.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 0.75rem;">
                    <strong>Core Stack:</strong> scikit-learn · NumPy · Pandas · pytest
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Launch Week 1", key="btn_w1", use_container_width=True):
            st.switch_page(week1_page)

    with col_w2:
        st.markdown(
            """
            <div class="portfolio-card">
                <div class="card-header">
                    <span class="card-icon">⚙️</span>
                    <span class="status-badge status-badge--ready">9 Modules</span>
                </div>
                <div>
                    <h3 class="card-title">Week 2: Business Automation</h3>
                    <p class="card-desc">
                        A suite of custom automation prototypes for internal workflows: automated invoicing, geofenced attendance logs, resume parsers, and PDF report engines.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 0.75rem;">
                    <strong>Core Stack:</strong> Streamlit Roster · Pandas · Matplotlib · OCR
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Launch Week 2", key="btn_w2", use_container_width=True):
            st.switch_page(week2_page)

    with col_w3:
        st.markdown(
            """
            <div class="portfolio-card">
                <div class="card-header">
                    <span class="card-icon">🤖</span>
                    <span class="status-badge status-badge--ready">9 Modules</span>
                </div>
                <div>
                    <h3 class="card-title">Week 3: AI Agent Proposals</h3>
                    <p class="card-desc">
                        Functional AI Agent designs tailored for corporate settings. Features intent classification, meeting summarization, content schedulers, and RAG pipelines.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 0.75rem;">
                    <strong>Core Stack:</strong> LLM Prompting · RAG · Similarity Engines
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Launch Week 3", key="btn_w3", use_container_width=True):
            st.switch_page(week3_page)

    st.markdown("---")

    # Double Column Layout for Timeline & Roster
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("📅 Workspace Timeline")
        st.markdown(
            """
            <div class="timeline-container">
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">Week 1 Milestone</div>
                    <div class="timeline-title">SafeX Knowledge Base Chatbot</div>
                    <div class="timeline-desc">Established underlying structure, TF-IDF cosine similarity model, and initial streamlit interface.</div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">Week 2 Milestone</div>
                    <div class="timeline-title">Business Automation Suite</div>
                    <div class="timeline-desc">Collaboratively integrated 9 business automation prototypes into a single workspace shell.</div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">Week 3 Milestone</div>
                    <div class="timeline-title">AI Agent Proposals</div>
                    <div class="timeline-desc">Deployed advanced agent systems including automated classifiers, schedulers, and document RAG.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.subheader("👥 Group Roster & Status Tracker")
        
        # Load registry data dynamically to show actual status
        w2_reg = load_weekly_registry("week2", "week2") or {}
        w3_reg = load_weekly_registry("week3", "week3") or {}
        
        team_members = [
            ("Arsalan Qasim", "Group Leader"),
            ("MUHAMMAD WASIM", "Member"),
            ("Muhammad Faozan Mujtaba", "Member"),
            ("Shahidullah", "Member"),
            ("Ali Ammar Haider", "Member"),
            ("Abdul Haseeb", "Member"),
            ("Hammad Abbas", "Member"),
            ("Ali Zaib", "Member"),
            ("Malik Sudais", "Member"),
        ]

        def get_status(registry, member_name):
            if not registry:
                return "⏳ Pending"
            for mod in registry.values():
                if mod.get("developer", "").strip() == member_name:
                    status = mod.get("status", "").lower()
                    if status in ["submitted", "submission ready", "completed"]:
                        return "✅ Completed"
                    elif status in ["in progress", "draft", "active"]:
                        return "🔄 In Progress"
            return "⏳ Pending"

        table_data = []
        for name, role in team_members:
            table_data.append({
                "Member": name,
                "Role": role,
                "Week 1": "✅ Completed",
                "Week 2": get_status(w2_reg, name),
                "Week 3": get_status(w3_reg, name)
            })
            
        st.dataframe(table_data, use_container_width=True, hide_index=True)


# ==============================================================================
# 5. Main App Setup & Execution
# ==============================================================================
def render_sidebar_branding() -> None:
    """Display consistent sidebar header elements."""
    st.sidebar.markdown(
        """
        <div class="app-mark">
            <div class="app-mark__square">S</div>
            <div>
                <div class="app-mark__name">SafeX Portfolio</div>
                <div class="app-mark__caption">Group 54 Suite</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown('<div class="side-heading">Appearance</div>', unsafe_allow_html=True)
    st.sidebar.radio(
        "Color mode",
        ["Light", "Dark"],
        key="ui_theme_choice",
        horizontal=True,
        label_visibility="collapsed",
    )


def render_dashboard_link() -> None:
    """Render an in-app link back to the registered dashboard page."""
    dashboard_page = st.session_state.get("_safex_home_page")
    if dashboard_page is not None:
        st.page_link(
            dashboard_page,
            label="← Back to Dashboard",
            icon=":material/home:",
            width="stretch",
        )


# Define global pages so they can be referenced inside show_dashboard
home_page = st.Page(show_dashboard, title="Home Dashboard", icon="🏠", default=True, url_path="home")
week1_page = st.Page("week1/src/app.py", title="Week 1: FAQ Chatbot", icon="💬", url_path="week1")
week2_page = st.Page("week2/src/app.py", title="Week 2: Automation Suite", icon="⚙️", url_path="week2")
week3_page = st.Page("week3/src/app.py", title="Week 3: AI Agent Proposals", icon="🤖", url_path="week3")

def main() -> None:
    # Set an environment variable so the child apps know they are running under the root dashboard
    os.environ["SAFEX_ROOT_DASHBOARD"] = "1"
    st.session_state["_safex_home_page"] = home_page

    # Group pages logically and hide the default navigation menu
    pg = st.navigation(
        {
            "Workspace": [home_page],
            "Submissions": [week1_page, week2_page, week3_page]
        }
    )
    
    # Run the navigation routing loop
    pg.run()

if __name__ == "__main__":
    main()
