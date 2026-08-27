from __future__ import annotations

import pandas as pd
import streamlit as st

from src.registry import MODULE_REGISTRY
from src.engine import (
    DocKnowledgeAssistantEngine,
    DocKnowledgeAssistantError,
)
from src.test_suite import TEST_SUITE

_CSS = """
<style>
.st-key-kaf-root [data-testid="stMetric"]{background:var(--surface);border:1px solid var(--line);
  border-radius:10px;padding:0.85rem;}
.kaf-source{font-size:12.5px;color:var(--muted);}
.kaf-pitch{font-size:15px;line-height:1.55;}
</style>
"""


@st.cache_resource
def _get_engine() -> DocKnowledgeAssistantEngine:
    return DocKnowledgeAssistantEngine()


def render_ui() -> None:
    """Renders the Streamlit frontend for the client-facing RAG Knowledge Assistant demo."""
    metadata = MODULE_REGISTRY["week4"]["knowledge_assistant_foodpanda"]

    with st.container(key="kaf-root"):
        st.markdown(_CSS, unsafe_allow_html=True)

        st.markdown(f'''
        <div class="hero-wrap">
            <div class="hero-badge">📚 Client-Ready AI Demo</div>
            <div class="hero-title">Instant Answers From Your Own Policy Documents</div>
            <div class="hero-subtitle">
                Built by <strong>{metadata["developer"]}</strong> — SafeX Solutions AI & Automation Suite
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(
            '<p class="kaf-pitch">Every food-delivery business fields the same questions over and over — '
            '"how long is delivery," "how do refunds work," "how do I become a rider." This assistant '
            'answers all of them instantly from your own policy documents, 24/7, with no call center '
            'needed — and it never makes up an answer it doesn\'t actually have.</p>',
            unsafe_allow_html=True,
        )

        try:
            engine = _get_engine()
        except DocKnowledgeAssistantError as exc:
            st.error(str(exc))
            return

        st.markdown("---")
        tab_ask, tab_docs, tab_how, tab_tech = st.tabs(
            ["💬 Try It Live", "📄 Knowledge Base", "✨ Why It Works", "🔧 Technical Details"]
        )

        with tab_ask:
            _render_ask_tab(engine)
        with tab_docs:
            _render_docs_tab(engine)
        with tab_how:
            _render_pitch_tab()
        with tab_tech:
            _render_technical_tab(engine)


def _render_ask_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write(
        "This demo is loaded with sample policy documents for **QuickBite**, a fictional "
        "food-delivery business standing in for a real client like Foodpanda. Ask it anything "
        "a real customer might ask."
    )

    example_cols = st.columns(3)
    examples = [
        "How long does delivery usually take?",
        "How do I cancel my order?",
        "How much commission do restaurants pay?",
    ]
    for col, ex in zip(example_cols, examples):
        if col.button(ex, use_container_width=True):
            st.session_state["kaf_query"] = ex

    query = st.text_input(
        "Ask a question",
        value=st.session_state.get("kaf_query", ""),
        placeholder="e.g. What happens if my order arrives late?",
        key="kaf_query_input",
    )
    ask_clicked = st.button("Ask", type="primary")

    if ask_clicked and query.strip():
        try:
            result = engine.answer(query)
        except DocKnowledgeAssistantError as exc:
            st.error(str(exc))
            return

        if result.abstained:
            st.warning(result.answer)
        else:
            st.success(result.answer)

        with st.expander("How did it find this answer?"):
            for r in result.retrieved:
                st.markdown(
                    f"<span class='kaf-source'>confidence={r.score:.3f} · "
                    f"{r.chunk.doc_title} — \"{r.chunk.section}\"</span>",
                    unsafe_allow_html=True,
                )
                st.write(r.chunk.text)
                st.markdown("---")
    elif ask_clicked:
        st.info("Type a question first.")


def _render_docs_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write(
        f"This demo's knowledge base has **{len(engine.document_titles())} documents** — in a real "
        "deployment, this would be replaced with the client's actual policies, FAQs, and SOPs. "
        "No retraining or coding needed to update it, just replace the documents."
    )
    doc_choice = st.selectbox("View a document", engine.document_titles())
    for chunk in engine.chunks:
        if chunk.doc_title == doc_choice:
            with st.expander(chunk.section):
                st.write(chunk.text)


def _render_pitch_tab() -> None:
    st.markdown("#### Why this matters for your business")
    st.markdown(
        "- **Cuts support load.** Repetitive policy questions (delivery times, refunds, "
        "payment methods) get answered instantly, freeing your support team for issues that "
        "actually need a human.\n"
        "- **Always accurate, never invented.** The assistant only answers from your real "
        "documents. If something isn't covered, it says so honestly instead of guessing — "
        "so it can't give a customer wrong information about your policies.\n"
        "- **Easy to keep current.** Update a policy document and the assistant's answers "
        "update with it — no retraining, no engineering time.\n"
        "- **Deploys anywhere.** Runs as a standalone web app (as shown in this demo) or can "
        "be embedded into an existing website or WhatsApp/Messenger support flow."
    )
    st.markdown("#### How it works, in plain terms")
    st.markdown(
        "1. Your policy documents are broken into topic-sized sections.\n"
        "2. Each section is indexed so the assistant can find the most relevant one for any question.\n"
        "3. When a customer asks something, the assistant finds the best-matching section(s) and "
        "answers directly from that text — with the source shown, so answers are always traceable.\n"
        "4. If nothing in your documents is relevant, it tells the customer honestly instead of "
        "guessing."
    )
    st.caption("See the **Technical Details** tab for the full architecture and evaluation results.")


def _render_technical_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write("For technical reviewers: architecture, evaluation results, and known limitations.")

    st.code(
        "5 Markdown documents\n"
        "      |\n"
        "      v\n"
        "Chunking (by '## ' section heading)\n"
        "      |\n"
        "      v\n"
        "TF-IDF Embedding  (heading text boosted into each chunk's embedding)\n"
        "      |\n"
        "      v\n"
        "In-memory Vector Store  (TF-IDF matrix + chunk metadata)\n"
        "      |\n"
        "      v\n"
        "User Query --> Top-K Retrieval (cosine similarity)\n"
        "      |\n"
        "      +---> best score < threshold (0.12)? --> Abstain: \"I don't know\"\n"
        "      |\n"
        "      v\n"
        "Answer Synthesis (extractive by default, or an optional LLM call)\n"
        "      |\n"
        "      v\n"
        "Response + cited source",
        language=None,
    )

    if st.button("Run Evaluation (14-question test log)", type="primary"):
        st.session_state["kaf_report"] = engine.run_evaluation(TEST_SUITE)

    report = st.session_state.get("kaf_report")
    if report:
        m1, m2, m3 = st.columns(3)
        m1.metric("Accuracy", f"{report['accuracy_percent']}%")
        m2.metric("Passed", f"{report['correct']}/{report['total']}")
        m3.metric("Questions", report["total"])

        df = pd.DataFrame(report["results"])
        df["expected_doc"] = df["expected_doc"].fillna("— (out of scope) —")
        df["top_doc"] = df["top_doc"].fillna("—")
        st.dataframe(
            df[["query", "expected_doc", "top_doc", "top_score", "abstained", "passed"]],
            use_container_width=True, hide_index=True,
        )

    st.markdown("#### Known limitations")
    st.markdown(
        "- **Lexical, not semantic, matching:** TF-IDF only recognizes shared words/phrases; "
        "a true embedding model would generalize across paraphrases better.\n"
        "- **Abstention is a similarity-score heuristic**, not true uncertainty estimation.\n"
        "- **Extractive answers only** by default — no generative LLM in this demo build, "
        "which limits hallucination risk but also limits how naturally answers combine "
        "information across documents.\n"
        "- **Small knowledge base** in this demo (5 documents) — a production deployment "
        "would use the client's full document set."
    )
    st.caption(
        "Full development writeup, including a documented accuracy improvement from 71.4% to "
        "100% via heading-boosted embeddings, is in "
        "`week3/src/modules/doc_knowledge_assistant/README.md`."
    )
