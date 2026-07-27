from __future__ import annotations

import pandas as pd
import streamlit as st

from src.modules.registry import MODULE_REGISTRY
from src.modules.doc_knowledge_assistant.engine import (
    DocKnowledgeAssistantEngine,
    DocKnowledgeAssistantError,
)
from src.modules.doc_knowledge_assistant.test_suite import TEST_SUITE

_CSS = """
<style>
.st-key-dka-root [data-testid="stMetric"]{background:var(--card-bg);border:1px solid var(--card-border);
  border-radius:10px;padding:0.85rem;}
.dka-source{font-size:12.5px;color:var(--text-muted);}
</style>
"""


@st.cache_resource
def _get_engine() -> DocKnowledgeAssistantEngine:
    return DocKnowledgeAssistantEngine()


def render_ui() -> None:
    """Renders the Streamlit frontend tab for the Document Analysis & Knowledge-Base Assistant."""
    metadata = MODULE_REGISTRY["week3"]["doc_knowledge_assistant"]

    with st.container(key="dka-root"):
        st.markdown(_CSS, unsafe_allow_html=True)

        st.markdown(f'''
        <div class="hero-wrap">
            <div class="hero-badge">📚 AI Agent Automation Suite</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Assigned to: <strong>{metadata["developer"]}</strong> ({metadata["role"]})
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.info(
            f"**Developer E-mail:** {metadata['email']}  \n"
            f"**Tech:** {', '.join(metadata['tech'])}"
        )

        st.subheader("Objective & Scope")
        st.write(metadata["description"])
        st.caption(
            "Target company: **QuickBite** — an original, fictional food-delivery company standing in "
            "for Foodpanda (per the assignment's substitution note). All 5 knowledge-base documents "
            "below are original content written for this exercise, not sourced from any real company."
        )

        try:
            engine = _get_engine()
        except DocKnowledgeAssistantError as exc:
            st.error(str(exc))
            return

        st.markdown("---")
        tab_ask, tab_docs, tab_eval, tab_arch = st.tabs(
            ["💬 Ask a Question", "📄 Knowledge Base", "✅ Evaluation Log", "🧭 Architecture"]
        )

        with tab_ask:
            _render_ask_tab(engine)
        with tab_docs:
            _render_docs_tab(engine)
        with tab_eval:
            _render_eval_tab(engine)
        with tab_arch:
            _render_architecture_tab()


def _render_ask_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write(
        "Ask a question about QuickBite's delivery, refunds, payments, rider, or restaurant-partner "
        "policies. The assistant retrieves the most relevant document section(s) and answers from "
        "them — or tells you it doesn't know, rather than guessing."
    )

    example_cols = st.columns(3)
    examples = [
        "How long does delivery usually take?",
        "How do I cancel my order?",
        "How much commission do restaurants pay?",
    ]
    for col, ex in zip(example_cols, examples):
        if col.button(ex, use_container_width=True):
            st.session_state["dka_query"] = ex

    query = st.text_input(
        "Your question",
        value=st.session_state.get("dka_query", ""),
        placeholder="e.g. What happens if my order arrives late?",
        key="dka_query_input",
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

        with st.expander("Show retrieved chunks (what the model saw)"):
            for r in result.retrieved:
                st.markdown(
                    f"<span class='dka-source'>score={r.score:.3f} · "
                    f"{r.chunk.doc_title} — \"{r.chunk.section}\"</span>",
                    unsafe_allow_html=True,
                )
                st.write(r.chunk.text)
                st.markdown("---")
    elif ask_clicked:
        st.info("Type a question first.")


def _render_docs_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write(
        f"**{len(engine.document_titles())} documents**, chunked into "
        f"**{len(engine.chunks)} sections** and embedded with TF-IDF."
    )
    doc_choice = st.selectbox("View a document", engine.document_titles())
    for chunk in engine.chunks:
        if chunk.doc_title == doc_choice:
            with st.expander(chunk.section):
                st.write(chunk.text)


def _render_eval_tab(engine: DocKnowledgeAssistantEngine) -> None:
    st.write(
        f"A labeled test suite of **{len(TEST_SUITE)} questions** (12 answerable + 2 deliberately "
        "out-of-scope) checks whether the assistant retrieves the correct source document, and "
        "whether it correctly abstains on questions the knowledge base can't answer."
    )

    if st.button("Run Evaluation", type="primary"):
        report = engine.run_evaluation(TEST_SUITE)
        st.session_state["dka_report"] = report

    report = st.session_state.get("dka_report")
    if report is None:
        st.info("Click **Run Evaluation** to score the assistant against the test suite.")
        return

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
        "- **Lexical, not semantic, matching:** TF-IDF only recognizes shared words/phrases. "
        "Early testing (before boosting section headings into the embedding step) missed several "
        "correctly-answerable questions purely because the question paraphrased the source text "
        "with different words (e.g. *\"how long does delivery **usually take**\"* vs. the document's "
        "*\"delivered **within 30-45 minutes**\"*). A true embedding model (e.g. sentence-transformers) "
        "would handle this better.\n"
        "- **Abstention is a similarity-score heuristic**, not true uncertainty estimation — a "
        "borderline question could still get a confident-looking but wrong answer if it happens to "
        "share vocabulary with the wrong document.\n"
        "- **Extractive answers only** by default (no generative LLM) — answers are always grounded "
        "in the retrieved text, which limits hallucination risk, but also means answers can't "
        "combine or rephrase information the way a generative model could.\n"
        "- **Small knowledge base** (5 documents) — accuracy at this scale doesn't guarantee the same "
        "performance on a much larger, more overlapping document set."
    )


def _render_architecture_tab() -> None:
    st.write("The RAG pipeline used by this module:")
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
        "Answer Synthesis\n"
        "      +-- mock (default): extractive answer directly from top chunk(s)\n"
        "      +-- openai / gemini (optional): LLM call grounded in retrieved context\n"
        "      |\n"
        "      v\n"
        "Response + cited source shown to user",
        language=None,
    )
    st.caption(
        "See `src/modules/doc_knowledge_assistant/README.md` for the full write-up and a "
        "rendered diagram image."
    )
