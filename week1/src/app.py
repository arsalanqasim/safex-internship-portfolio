"""Streamlit interface for the SafeX FAQ knowledge assistant."""

from __future__ import annotations

import os
import sys
import uuid
from datetime import datetime

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chatbot import FAQChatbot
from src.config import FAQ_PATH


st.set_page_config(
    page_title="SafeX Knowledge Assistant",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)


SUGGESTED_QUESTIONS = [
    "What is SafeX?",
    "What are the office timings?",
    "What is the leave policy?",
    "How do I reset my password?",
]


def inject_css() -> None:
    """Apply the shared, minimal application style."""
    st.markdown(
        """
        <style>
        :root { --ink: #172033; --muted: #64748b; --line: #dce3ec; --soft: #f6f8fb; --accent: #0f766e; --accent-dark: #0b5e58; }
        #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
        header[data-testid="stHeader"] { background: var(--soft); }
        .stApp, [data-testid="stAppViewContainer"] { background: var(--soft); color: var(--ink); }
        section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }
        section[data-testid="stSidebar"] > div { padding-top: 1.25rem; }
        .block-container { max-width: 1020px; padding-top: 4.5rem; padding-bottom: 5.5rem; }
        html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
        h1, h2, h3, p { color: var(--ink); }
        .app-mark { display: flex; gap: 10px; align-items: center; margin-bottom: 1.75rem; }
        .app-mark__square { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 7px; background: var(--accent); color: white; font-weight: 700; }
        .app-mark__name { font-size: 0.95rem; font-weight: 700; color: var(--ink); }
        .app-mark__caption { font-size: 0.75rem; color: var(--muted); }
        .eyebrow { color: var(--accent); font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem; }
        .page-title { font-size: 2rem; font-weight: 700; line-height: 1.15; margin: 0; color: var(--ink); }
        .page-subtitle { color: var(--muted); font-size: 1rem; margin: 0.7rem 0 1.5rem; max-width: 650px; }
        .info-strip { display: flex; gap: 1.4rem; flex-wrap: wrap; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 0.75rem 0; color: var(--muted); font-size: 0.84rem; margin: 1.5rem 0; }
        .suggestion-title { color: var(--muted); font-size: 0.84rem; font-weight: 600; margin: 1rem 0 0.55rem; }
        .stButton > button { border-radius: 6px; border: 1px solid var(--line); background: #ffffff; color: var(--ink); font-weight: 600; min-height: 2.45rem; box-shadow: none; }
        .stButton > button:hover { border-color: var(--accent); color: var(--accent); background: #f0fdfa; }
        .stButton > button[kind="primary"] { background: var(--accent); color: #ffffff; border-color: var(--accent); }
        .stButton > button[kind="primary"]:hover { background: var(--accent-dark); color: #ffffff; }
        [data-testid="stChatMessage"] { background: #ffffff; border: 1px solid var(--line); border-radius: 8px; padding: 0.15rem 0.75rem; margin-bottom: 0.75rem; }
        [data-testid="stChatInput"] { border: 1px solid var(--line); border-radius: 8px; background: #ffffff; }
        [data-testid="stChatInput"] textarea { color: var(--ink); }
        .sidebar-note { color: var(--muted); font-size: 0.8rem; line-height: 1.5; margin-top: 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_chatbot() -> FAQChatbot:
    return FAQChatbot(FAQ_PATH)


def init_state() -> None:
    if "conversations" not in st.session_state:
        conversation_id = str(uuid.uuid4())
        st.session_state.conversations = {
            conversation_id: {"title": "New conversation", "messages": [], "created_at": datetime.now()}
        }
        st.session_state.active_conversation = conversation_id
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None


def new_conversation() -> None:
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = {
        "title": "New conversation", "messages": [], "created_at": datetime.now(),
    }
    st.session_state.active_conversation = conversation_id


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="app-mark">
                <div class="app-mark__square">S</div>
                <div><div class="app-mark__name">SafeX</div><div class="app-mark__caption">Knowledge Assistant</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("New conversation", type="primary", use_container_width=True):
            new_conversation()
            st.rerun()

        st.caption("Conversations")
        conversations = sorted(st.session_state.conversations.items(), key=lambda item: item[1]["created_at"], reverse=True)
        for conversation_id, conversation in conversations:
            is_active = conversation_id == st.session_state.active_conversation
            label = ("Current: " if is_active else "") + conversation["title"]
            if st.button(label, key=f"conversation_{conversation_id}", use_container_width=True):
                st.session_state.active_conversation = conversation_id
                st.rerun()

        st.divider()
        st.caption("Answer matching")
        st.session_state.similarity_threshold = st.slider("Similarity threshold", 0.0, 1.0, 0.35, 0.05)
        st.markdown('<p class="sidebar-note">Answers are retrieved from the local SafeX FAQ knowledge base using text similarity.</p>', unsafe_allow_html=True)


def render_intro() -> None:
    st.markdown('<div class="eyebrow">Week 1 · FAQ chatbot</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Ask SafeX, get a clear answer.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">A focused knowledge assistant for common questions about the internship, workplace policies, onboarding, and support.</p>', unsafe_allow_html=True)
    st.markdown('<div class="info-strip"><span>Local FAQ knowledge base</span><span>TF-IDF retrieval</span><span>No external API required</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-title">Start with a common question</div>', unsafe_allow_html=True)
    columns = st.columns(2)
    for index, question in enumerate(SUGGESTED_QUESTIONS):
        with columns[index % 2]:
            if st.button(question, key=f"suggestion_{index}", use_container_width=True):
                st.session_state.pending_question = question
                st.rerun()


def main() -> None:
    init_state()
    inject_css()
    render_sidebar()
    active = st.session_state.conversations[st.session_state.active_conversation]
    messages = active["messages"]
    if not messages:
        render_intro()
    else:
        st.markdown('<div class="eyebrow">SafeX knowledge assistant</div>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="page-title">{active["title"]}</h1>', unsafe_allow_html=True)
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about SafeX")
    if st.session_state.pending_question:
        prompt = st.session_state.pending_question
        st.session_state.pending_question = None
    if prompt:
        messages.append({"role": "user", "content": prompt})
        if active["title"] == "New conversation":
            active["title"] = prompt[:42] + ("..." if len(prompt) > 42 else "")
        response = get_chatbot().query(prompt, st.session_state.get("similarity_threshold", 0.35))
        messages.append({"role": "assistant", "content": response["answer"]})
        st.rerun()


if __name__ == "__main__":
    main()
