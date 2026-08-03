"""Streamlit UI for the AI Meeting Summarizer & Action-Item Extractor.

Week 3 module owned by Muhammad Faozan Mujtaba. Page-level configuration stays in
``week3/src/app.py``; everything here renders inside ``render_ui()``.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.modules.meeting_summarizer import prompts
from src.modules.meeting_summarizer.engine import (
    TARGET_COMPANY,
    MeetingReport,
    MeetingSummarizerEngine,
    list_transcripts,
    read_transcript,
)
from src.modules.registry import MODULE_REGISTRY

ARCHITECTURE_DIAGRAM = """```mermaid
graph TD
    A[Raw Transcript<br/>paste, upload or sample] --> B[Transcript Parser<br/>speaker turns + header metadata]
    B --> C[Sentence Segmentation<br/>+ filler removal]
    C --> D[Decision Extractor<br/>settled-choice cues]
    C --> E[Action Extractor<br/>commitment marker + work verb]
    C --> F[Risk Extractor<br/>blockers & deferred questions]
    C --> G[TF-IDF Sentence Ranker<br/>executive summary]
    E --> H[Owner Resolver<br/>named person > speaker > Unassigned]
    E --> I[Deadline Resolver<br/>relative phrase to ISO date]
    D --> J[Structured MeetingReport]
    F --> J
    G --> J
    H --> J
    I --> J
    J --> K[Markdown / JSON / print-ready HTML]
    G -.->|LLM_PROVIDER set| L[Hosted LLM<br/>same prompt templates]
    L -.->|on failure, falls back| G
```"""


def _summary_metrics(report: MeetingReport) -> None:
    """Render the headline counts for a produced report."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Decisions", report.stats.get("decisions", 0))
    col2.metric("Action Items", report.stats.get("action_items", 0))
    col3.metric(
        "With Owner",
        f"{report.stats.get('action_items_with_owner', 0)}/{report.stats.get('action_items', 0)}",
    )
    col4.metric(
        "With Deadline",
        f"{report.stats.get('action_items_with_deadline', 0)}/{report.stats.get('action_items', 0)}",
    )


def _render_report(report: MeetingReport) -> None:
    """Render one structured meeting report in the workspace."""
    _summary_metrics(report)
    st.divider()

    st.markdown("### Summary")
    st.write(report.summary)
    if report.participants:
        st.caption(f"**Participants:** {', '.join(report.participants)}")
    if report.topics:
        st.caption(f"**Topics:** {' · '.join(report.topics)}")

    st.markdown("### Decisions Made")
    if report.decisions:
        for idx, decision in enumerate(report.decisions, start=1):
            st.markdown(f"**{idx}.** {decision.decision}  \n<small>— {decision.decided_by}</small>", unsafe_allow_html=True)
    else:
        st.caption("No explicit decisions were recorded in this transcript.")

    st.markdown("### Action Items")
    if report.action_items:
        frame = pd.DataFrame([
            {
                "Action": item.task,
                "Owner": item.owner,
                "Deadline": item.deadline_date or "—",
                "As spoken": item.deadline_phrase or "—",
                "Priority": item.priority,
            }
            for item in report.action_items
        ])
        st.dataframe(
            frame,
            column_config={
                "Action": st.column_config.TextColumn("Action", width="large"),
                "Owner": st.column_config.TextColumn("Owner"),
                "Deadline": st.column_config.TextColumn("Deadline"),
                "As spoken": st.column_config.TextColumn("As spoken"),
                "Priority": st.column_config.TextColumn("Priority"),
            },
            use_container_width=True,
            hide_index=True,
        )
        unassigned = [item for item in report.action_items if item.owner == "Unassigned"]
        if unassigned:
            st.warning(
                f"⚠️ {len(unassigned)} action "
                f"{'item has' if len(unassigned) == 1 else 'items have'} no named owner. "
                "The agent never guesses an owner; assign these manually before circulating."
            )
    else:
        st.caption("No action items were assigned in this transcript.")

    if report.blockers:
        st.markdown("### Blockers & Risks")
        for blocker in report.blockers:
            st.markdown(f"- {blocker}")

    if report.open_questions:
        st.markdown("### Open Questions")
        for question in report.open_questions:
            st.markdown(f"- {question}")

    st.divider()
    st.markdown("### Export")
    col1, col2, col3 = st.columns(3)
    stem = report.title.lower().replace(" ", "_").replace("/", "-")[:60]
    col1.download_button(
        "⬇️ Markdown minutes",
        data=report.to_markdown(),
        file_name=f"{stem}_minutes.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col2.download_button(
        "⬇️ Structured JSON",
        data=report.to_json(),
        file_name=f"{stem}_minutes.json",
        mime="application/json",
        use_container_width=True,
    )
    col3.download_button(
        "⬇️ Print-ready HTML → PDF",
        data=report.to_html(),
        file_name=f"{stem}_minutes.html",
        mime="text/html",
        use_container_width=True,
        help="Open the downloaded file and use the browser's Print → Save as PDF.",
    )

    with st.expander("Preview the Markdown minutes"):
        st.code(report.to_markdown(), language="markdown")


def render_ui() -> None:
    """Render Muhammad Faozan Mujtaba's AI Meeting Summarizer module."""
    metadata = MODULE_REGISTRY["week3"]["meeting_summarizer"]
    engine = MeetingSummarizerEngine()

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">📝 Submission Ready</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Developer: <strong>{metadata["developer"]}</strong> ({metadata["role"]}) · <code>{metadata["email"]}</code><br/>
                Target company: <strong>{TARGET_COMPANY}</strong> · Runs offline on provider <code>{engine.provider.name}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📌 Module Overview & Specifications", expanded=False):
        st.write(f"**Objective:** {metadata['description']}")
        st.write(f"**Tech Stack:** {' · '.join(metadata['tech'])}")
        st.write(
            f"**Target Company:** {TARGET_COMPANY} — a software house in Islamabad running "
            "sprint reviews, client calls and hiring syncs every week, where follow-ups are "
            "lost between meetings."
        )
        st.write(
            "**Scope Handled:** transcript parsing, executive summary, decisions, action items "
            "with owner and resolved calendar deadline, blockers, open questions, and "
            "Markdown / JSON / PDF-ready export."
        )

    tab_run, tab_bench, tab_arch, tab_prompts = st.tabs([
        "📝 Summarize a Meeting",
        "📊 Accuracy Benchmark",
        "🗺️ Architecture",
        "🧠 Prompt Templates",
    ])

    with tab_run:
        st.subheader("Transcript to Structured Minutes")
        st.caption(
            "Pick a bundled sample meeting, upload a transcript, or paste one in. "
            "Deadlines resolve against the meeting date, so results are reproducible."
        )

        source = st.radio(
            "Transcript source",
            ["Sample meeting", "Upload a file", "Paste text"],
            horizontal=True,
            key="ms_source",
        )

        transcript_text = ""
        override_date: date | None = None

        if source == "Sample meeting":
            samples = list_transcripts()
            if not samples:
                st.error("No sample transcripts are bundled with this module.")
            else:
                chosen = st.selectbox("Sample meeting", samples, key="ms_sample")
                transcript_text = read_transcript(chosen)
                with st.expander("View raw transcript"):
                    st.text(transcript_text)
        elif source == "Upload a file":
            uploaded = st.file_uploader("Transcript (.txt or .md)", type=["txt", "md"], key="ms_upload")
            if uploaded is not None:
                transcript_text = uploaded.getvalue().decode("utf-8", errors="replace")
            override_date = st.date_input("Meeting date", value=date.today(), key="ms_upload_date")
        else:
            transcript_text = st.text_area(
                "Paste the transcript",
                height=220,
                placeholder="Ayesha: We closed eleven of the fourteen stories this sprint.\nBilal: I'll chase the client for credentials by Friday.",
                key="ms_paste",
            )
            override_date = st.date_input("Meeting date", value=date.today(), key="ms_paste_date")

        if st.button("Generate Minutes", type="primary", key="ms_run"):
            if not transcript_text.strip():
                st.warning("Add a transcript first.")
            else:
                with st.spinner("Extracting decisions, owners and deadlines…"):
                    st.session_state.ms_report = engine.summarize(transcript_text, meeting_date=override_date)

        report = st.session_state.get("ms_report")
        if report is not None:
            st.divider()
            _render_report(report)

    with tab_bench:
        st.subheader("Extraction Accuracy Against a Hand-Annotated Gold Set")
        st.caption(
            "Three transcripts were annotated by hand before the engine was tuned. An action "
            "item counts as recalled when a produced item covers at least half of the gold "
            "item's keywords; owner and deadline accuracy are measured over matched pairs."
        )

        if st.button("Run Benchmark", type="primary", key="ms_bench"):
            st.session_state.ms_bench = engine.run_benchmark()

        bench = st.session_state.get("ms_bench") or engine.run_benchmark()

        col1, col2, col3 = st.columns(3)
        col1.metric("Recall", f"{bench['recall_percent']}%")
        col2.metric("Precision", f"{bench['precision_percent']}%")
        col3.metric("F1", f"{bench['f1_percent']}%")

        col4, col5, col6 = st.columns(3)
        col4.metric("Owner Accuracy", f"{bench['owner_accuracy_percent']}%")
        col5.metric("Deadline Accuracy", f"{bench['deadline_accuracy_percent']}%")
        col6.metric("Gold Action Items", bench["gold_action_items"])

        st.dataframe(
            pd.DataFrame(bench["per_transcript"]),
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "**Known failure modes.** A deadline stated in a later turn than its task "
            '("I\'ll draft it." … "In five business days.") is not attached, and a restated '
            "task can be counted twice. Both are visible in the numbers above rather than "
            "tuned away."
        )

    with tab_arch:
        st.subheader("Pipeline Architecture")
        st.markdown(ARCHITECTURE_DIAGRAM)
        st.markdown(
            """
            **Design rules the agent follows**

            1. **Never invent an owner.** If nobody was named, the item is `Unassigned` and
               the UI flags it for manual assignment.
            2. **Deadlines resolve against the meeting date**, never against today, so
               re-running an old transcript reproduces the same dates.
            3. **A decision is not a task.** Settled choices are recorded separately, so the
               action list stays executable.
            4. **A question is only open if the reply defers it** — most meeting questions
               are answered in the next breath and are noise in a minutes document.
            5. **The LLM is optional.** The provider seam takes the same prompt templates, and
               the deterministic pipeline is the fallback whenever a hosted call is
               unavailable or fails.
            """
        )

    with tab_prompts:
        st.subheader("Prompt Templates")
        st.caption(
            f"Version `{prompts.PROMPT_VERSION}` · these are the exact templates sent to a "
            "hosted model when `LLM_PROVIDER` is configured."
        )
        for name, template in prompts.ALL_PROMPTS.items():
            variables = prompts.PROMPT_VARIABLES.get(name, [])
            with st.expander(f"`{name}`" + (f" — variables: {', '.join(variables)}" if variables else "")):
                st.code(template, language="text")
