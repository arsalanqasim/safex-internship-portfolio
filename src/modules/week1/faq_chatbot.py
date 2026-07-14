# Week 1 FAQ Chatbot UI Module
import streamlit as st
import time
import uuid
from datetime import datetime
from src.core.chatbot import FAQChatbot
from src.config import FAQ_PATH

@st.cache_resource
def get_chatbot_instance() -> FAQChatbot:
    """Load and train the chatbot orchestrator exactly once using Streamlit caching."""
    return FAQChatbot(FAQ_PATH)

def get_chatbot_response(query: str, threshold: float) -> str:
    """Queries the actual backend similarity-based FAQ chatbot orchestrator."""
    bot = get_chatbot_instance()
    response = bot.query(query, threshold)
    return response["answer"]

def init_session_state() -> None:
    """Initialize chatbot-specific session state variables."""
    if "chats" not in st.session_state:
        first_id = str(uuid.uuid4())
        st.session_state.chats = {
            first_id: {
                "title": "New Conversation",
                "messages": [],
                "created_at": datetime.now(),
            }
        }
        st.session_state.current_chat_id = first_id

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = next(iter(st.session_state.chats))

    if "threshold" not in st.session_state:
        st.session_state.threshold = 0.35

    if "search_term" not in st.session_state:
        st.session_state.search_term = ""

    if "renaming_chat_id" not in st.session_state:
        st.session_state.renaming_chat_id = None

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None

def get_current_chat() -> dict:
    """Return the dict for the currently active chat."""
    return st.session_state.chats[st.session_state.current_chat_id]

def create_new_chat() -> None:
    """Create a fresh, empty chat and make it the active one."""
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Conversation",
        "messages": [],
        "created_at": datetime.now(),
    }
    st.session_state.current_chat_id = new_id
    st.session_state.renaming_chat_id = None

def switch_chat(chat_id: str) -> None:
    """Switch the active chat pointer."""
    st.session_state.current_chat_id = chat_id
    st.session_state.renaming_chat_id = None

def delete_chat(chat_id: str) -> None:
    """Delete a chat. Ensures at least one chat always exists."""
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

    if not st.session_state.chats:
        create_new_chat()
        return

    if st.session_state.current_chat_id == chat_id:
        st.session_state.current_chat_id = next(iter(st.session_state.chats))

def start_rename(chat_id: str) -> None:
    """Put a given chat into rename mode."""
    st.session_state.renaming_chat_id = chat_id

def confirm_rename(chat_id: str, new_title: str) -> None:
    """Persist a new title for a chat and exit rename mode."""
    clean_title = new_title.strip()
    if clean_title:
        st.session_state.chats[chat_id]["title"] = clean_title[:40]
    st.session_state.renaming_chat_id = None

def auto_title_from_first_message(chat_id: str, text: str) -> None:
    """Auto-generate a chat title from the first user message."""
    chat = st.session_state.chats[chat_id]
    if chat["title"] == "New Conversation":
        title = text.strip()
        chat["title"] = (title[:32] + "…") if len(title) > 32 else title

def filter_chats(search_term: str) -> list:
    """Return chat ids sorted by most-recent first, filtered by search term."""
    items = list(st.session_state.chats.items())
    items.sort(key=lambda kv: kv[1]["created_at"], reverse=True)

    if search_term.strip():
        term = search_term.strip().lower()
        items = [(cid, c) for cid, c in items if term in c["title"].lower()]

    return items

SUGGESTED_PROMPTS = [
    ("🏢", "What is SafeX?", "Learn about the company"),
    ("🕐", "Office timings", "Check working hours"),
    ("📝", "Leave policy", "How to apply for leave"),
    ("🔑", "Reset password", "IT support steps"),
    ("👥", "Contact HR", "Get in touch with HR"),
    ("🎓", "Internship rules", "Guidelines & expectations"),
]

def render_suggested_prompts() -> None:
    """Render a responsive 3-column grid of clickable suggested-question cards."""
    st.markdown('<div class="suggested-label">Try asking one of these</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (icon, title, subtitle) in enumerate(SUGGESTED_PROMPTS):
        with cols[i % 3]:
            if st.button(
                f"{icon}  **{title}**\n\n{subtitle}",
                key=f"suggested_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_prompt = title
                st.rerun()

def render_empty_state() -> None:
    """Render the empty-state placeholder shown before any messages."""
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon-circle">💬</div>
            <p>Ask a question about SafeX Solutions policies, timings, or procedures below.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_chat_messages(messages: list) -> None:
    """Render the full conversation using native st.chat_message bubbles."""
    for message in messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🛡️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

def render_typing_animation(placeholder, final_text: str) -> None:
    """Show a typing indicator, then progressively reveal the final answer."""
    with placeholder.container():
        with st.chat_message("assistant", avatar="🛡️"):
            dots_area = st.empty()
            for _ in range(2):
                dots_area.markdown(
                    '<div class="typing-dots"><span></span><span></span><span></span></div>',
                    unsafe_allow_html=True,
                )
                time.sleep(0.35)

            words = final_text.split(" ")
            revealed = ""
            text_area = dots_area
            for word in words:
                revealed += word + " "
                text_area.markdown(revealed + "▌")
                time.sleep(0.03)
            text_area.markdown(revealed.strip())

def scroll_to_bottom() -> None:
    """Inject a tiny invisible HTML component that auto-scrolls the page."""
    st.components.v1.html(
        """
        <script>
            var mainEl = window.parent.document.querySelector('section.main');
            if (mainEl) { mainEl.scrollTo({top: mainEl.scrollHeight, behavior: 'smooth'}); }
        </script>
        """,
        height=0,
    )

def render_sidebar_controls() -> None:
    """Renders the chat list and settings controls in the sidebar when Week 1 is active."""
    init_session_state()

    # ---- New Chat Button ----
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕  New Chat", use_container_width=True, key="btn_new_chat"):
        create_new_chat()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Search Input ----
    st.markdown('<div class="sidebar-section-label">Search</div>', unsafe_allow_html=True)
    st.session_state.search_term = st.text_input(
        "Search chats",
        value=st.session_state.search_term,
        placeholder="🔍  Search conversations...",
        label_visibility="collapsed",
        key="search_input",
    )

    # ---- Conversation History ----
    st.markdown('<div class="sidebar-section-label">Conversations</div>', unsafe_allow_html=True)
    visible_chats = filter_chats(st.session_state.search_term)

    if not visible_chats:
        st.caption("No conversations found.")

    for chat_id, chat in visible_chats:
        is_active = chat_id == st.session_state.current_chat_id
        row_class = "chat-row active" if is_active else "chat-row"

        if st.session_state.renaming_chat_id == chat_id:
            st.markdown(f'<div class="{row_class} rename-mode">', unsafe_allow_html=True)
            new_title = st.text_input(
                "Rename",
                value=chat["title"],
                key=f"rename_input_{chat_id}",
                label_visibility="collapsed",
            )
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown('<div class="rename-action save">', unsafe_allow_html=True)
                if st.button("✓ Save", key=f"save_{chat_id}", use_container_width=True):
                    confirm_rename(chat_id, new_title)
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="rename-action cancel">', unsafe_allow_html=True)
                if st.button("✕ Cancel", key=f"cancel_{chat_id}", use_container_width=True):
                    st.session_state.renaming_chat_id = None
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
            col_title, col_menu = st.columns([7, 1])

            with col_title:
                icon = "💬" if not is_active else "🟢"
                if st.button(
                    f"{icon}  {chat['title']}",
                    key=f"select_{chat_id}",
                    use_container_width=True,
                ):
                    switch_chat(chat_id)
                    st.rerun()

            with col_menu:
                st.markdown('<div class="menu-trigger">', unsafe_allow_html=True)
                with st.popover("⋮", use_container_width=False):
                    if st.button(
                        "✏️  Rename",
                        key=f"rename_{chat_id}",
                        use_container_width=True,
                    ):
                        start_rename(chat_id)
                        st.rerun()

                    st.markdown('<div class="popover-danger">', unsafe_allow_html=True)
                    if st.button(
                        "🗑️  Delete",
                        key=f"delete_{chat_id}",
                        use_container_width=True,
                    ):
                        delete_chat(chat_id)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # ---- Chatbot Settings ----
    st.markdown('<div class="sidebar-section-label">Settings</div>', unsafe_allow_html=True)
    with st.expander("⚙️  Preferences", expanded=False):
        st.markdown("**Similarity Threshold**")
        st.session_state.threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.threshold,
            step=0.05,
            label_visibility="collapsed",
            key="threshold_slider",
        )
        st.caption("Controls how closely a question must match the FAQ base.")

    with st.expander("ℹ️  About Chatbot", expanded=False):
        st.markdown(
            """
            **SafeX AI FAQ Assistant**
            
            Processes queries locally on-device using a TF-IDF vectorizer + Cosine Similarity engine to find the closest match.
            """
        )

def render_ui() -> None:
    """Renders the main FAQ chatbot panel."""
    init_session_state()
    current_chat = get_current_chat()
    messages = current_chat["messages"]

    # ---- Hero Title ----
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge">🛡️ SafeX Solutions · Internal AI</div>
            <div class="hero-title">SafeX AI Knowledge Assistant</div>
            <div class="hero-subtitle">
                Ask questions about internships, company guidelines, leave policies, or IT support.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(messages) == 0:
        render_suggested_prompts()
        st.markdown("<br>", unsafe_allow_html=True)
        render_empty_state()
    else:
        render_chat_messages(messages)

    response_placeholder = st.empty()

    # ---- Chat Input ----
    prompt = st.chat_input("Message SafeX AI...")

    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt:
        messages.append({"role": "user", "content": prompt})
        auto_title_from_first_message(st.session_state.current_chat_id, prompt)

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        answer = get_chatbot_response(prompt, st.session_state.threshold)
        render_typing_animation(response_placeholder, answer)

        messages.append({"role": "assistant", "content": answer})
        scroll_to_bottom()
        st.rerun()
