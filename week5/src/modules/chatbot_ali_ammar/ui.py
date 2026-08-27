"""
ShopEase AI Customer Support Chatbot — Streamlit Interface
Developer: Ali Ammar Haider
Institution: COMSATS University Islamabad

Professional client-ready user interface featuring:
- ShopEase brand aesthetic
- 5 Interactive Tabs (Chat, Knowledge Base, Admin Panel, Analytics, Benchmark)
- Real-time confidence scores & human handoff indicators
- No-code Admin FAQ CRUD interface
- Live KPI Metrics & Chat Log inspector
- One-click Accuracy Benchmark Suite runner
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Handle both relative package import and standalone execution safely
try:
    from .engine import CustomerSupportEngine
except (ImportError, ValueError):
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    from engine import CustomerSupportEngine  # type: ignore


def render_ui() -> None:
    """Render the ShopEase AI Customer Support Chatbot UI."""

    # ------------------------------------------------------------------
    # Custom CSS & Branding
    # ------------------------------------------------------------------
    st.markdown(
        """
        <style>
        .shopease-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            color: #ffffff;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.2);
        }
        .shopease-header h1 {
            color: #ffffff !important;
            margin: 0;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }
        .shopease-header p {
            color: #dbeafe !important;
            margin: 0.4rem 0 0 0;
            font-size: 0.95rem;
        }
        .badge-confidence {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.78rem;
            margin-top: 0.3rem;
        }
        .badge-escalation {
            display: inline-block;
            background: #fef2f2;
            color: #991b1b;
            padding: 0.25rem 0.75rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.82rem;
            margin-top: 0.3rem;
            border: 1px solid #fecaca;
        }
        .metric-card-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Header Banner
    # ------------------------------------------------------------------
    st.markdown(
        """
        <div class="shopease-header">
            <h1>🛍️ ShopEase AI Customer Support Assistant</h1>
            <p>Production-grade AI chatbot automating e-commerce customer support FAQs, TF-IDF semantic matching, confidence-based human handoff, real-time logging, and no-code knowledge base management.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Initialize Engine & Session State
    # ------------------------------------------------------------------
    if "ali_chatbot_engine" not in st.session_state:
        st.session_state["ali_chatbot_engine"] = CustomerSupportEngine()

    engine: CustomerSupportEngine = st.session_state["ali_chatbot_engine"]

    if "ali_chat_history" not in st.session_state:
        st.session_state["ali_chat_history"] = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! Welcome to ShopEase Customer Support.\n\n"
                    "I can instantly help you with order tracking, shipping costs, return policies, "
                    "refunds, payment methods, exchanges, and product details. How can I assist you today?"
                ),
                "confidence": 1.0,
                "human_handoff": False,
            }
        ]

    # ------------------------------------------------------------------
    # Navigation Tabs
    # ------------------------------------------------------------------
    tab_chat, tab_kb, tab_admin, tab_analytics, tab_benchmark = st.tabs(
        [
            "💬 Customer Chat",
            "📚 Knowledge Base",
            "⚙️ Admin Panel",
            "📊 Analytics & Logs",
            "🎯 Accuracy Benchmark",
        ]
    )

    # ==================================================================
    # TAB 1: CUSTOMER CHAT
    # ==================================================================
    with tab_chat:
        st.markdown("### Customer Interaction Portal")

        # Quick FAQs Buttons
        st.markdown("**Popular Questions:**")
        quick_cols = st.columns(4)
        quick_questions = [
            "Where is my order?",
            "How much is shipping?",
            "What is your return policy?",
            "Talk to a human agent",
        ]

        selected_quick_q = None
        for i, q in enumerate(quick_questions):
            if quick_cols[i].button(q, key=f"btn_quick_{i}", use_container_width=True):
                selected_quick_q = q

        st.divider()

        # Chat History Container
        chat_box = st.container()
        with chat_box:
            for msg in st.session_state["ali_chat_history"]:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🛍️"):
                        st.markdown(msg["content"])
                        if "confidence" in msg:
                            conf = msg["confidence"]
                            if msg.get("human_handoff"):
                                st.markdown(
                                    f'<div class="badge-escalation">⚠️ Human Handoff Triggered | Confidence: {conf:.0%}</div>',
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    f'<div class="badge-confidence">✓ Match Confidence: {conf:.0%}</div>',
                                    unsafe_allow_html=True,
                                )

        # User Input
        user_input = st.chat_input("Type your question about ShopEase orders, shipping, or returns...")
        active_query = selected_quick_q or user_input

        if active_query:
            # Append User Question
            st.session_state["ali_chat_history"].append({"role": "user", "content": active_query})

            # Get Bot Response with typing indicator
            with st.spinner("ShopEase AI is typing..."):
                result = engine.get_response(active_query)

            # Append Assistant Answer
            st.session_state["ali_chat_history"].append(
                {
                    "role": "assistant",
                    "content": result["response"],
                    "confidence": result["confidence"],
                    "human_handoff": result["human_handoff"],
                }
            )
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        col_clear, col_space = st.columns([1, 4])
        with col_clear:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state["ali_chat_history"] = [
                    {
                        "role": "assistant",
                        "content": "👋 Hello! Welcome to ShopEase Support. How can I help you today?",
                        "confidence": 1.0,
                        "human_handoff": False,
                    }
                ]
                st.rerun()

    # ==================================================================
    # TAB 2: KNOWLEDGE BASE
    # ==================================================================
    with tab_kb:
        st.markdown("### Active FAQ Knowledge Base")
        st.info(f"The chatbot currently has **{len(engine.faqs)}** active FAQ entries in its local JSON knowledge base.")

        search_query = st.text_input("🔍 Search Knowledge Base by keyword or category...", "")

        filtered_faqs = engine.faqs
        if search_query.strip():
            sq = search_query.lower()
            filtered_faqs = [
                f for f in engine.faqs
                if sq in f["question"].lower() or sq in f["answer"].lower() or sq in f["category"].lower() or any(sq in k.lower() for k in f.get("keywords", []))
            ]

        for faq in filtered_faqs:
            with st.expander(f"📌 [{faq['id']}] {faq['question']} ({faq['category']})"):
                st.markdown(f"**Answer:** {faq['answer']}")
                st.markdown(f"**Category:** `{faq['category']}`")
                st.markdown(f"**Keywords:** {', '.join([f'`{k}`' for k in faq.get('keywords', [])])}")

    # ==================================================================
    # TAB 3: ADMIN PANEL (NO-CODE FAQ MANAGER)
    # ==================================================================
    with tab_admin:
        st.markdown("### ⚙️ Business Owner Admin Panel")
        st.caption("Manage customer support FAQs with real-time JSON persistence.")

        admin_action = st.radio("Select Action:", ["➕ Add New FAQ", "✏️ Edit FAQ", "❌ Delete FAQ", "🔄 Reset Factory Defaults"], horizontal=True)

        if admin_action == "➕ Add New FAQ":
            st.markdown("#### Add a New FAQ Entry")
            with st.form("form_add_faq"):
                new_cat = st.text_input("Category", "General")
                new_q = st.text_input("Question")
                new_a = st.text_area("Answer")
                new_kw = st.text_input("Keywords (comma separated)", "support, help, query")
                btn_add = st.form_submit_button("Save FAQ")

                if btn_add:
                    kws = [k.strip() for k in new_kw.split(",") if k.strip()]
                    success, msg = engine.add_faq(new_cat, new_q, new_a, kws)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        elif admin_action == "✏️ Edit FAQ":
            st.markdown("#### Edit an Existing FAQ Entry")
            if not engine.faqs:
                st.warning("No FAQs available to edit.")
            else:
                faq_options = {f"{f['id']} - {f['question']}": f for f in engine.faqs}
                selected_label = st.selectbox("Select FAQ to edit:", list(faq_options.keys()))
                faq_to_edit = faq_options[selected_label]

                with st.form("form_edit_faq"):
                    edit_cat = st.text_input("Category", faq_to_edit["category"])
                    edit_q = st.text_input("Question", faq_to_edit["question"])
                    edit_a = st.text_area("Answer", faq_to_edit["answer"])
                    edit_kw = st.text_input("Keywords (comma separated)", ", ".join(faq_to_edit.get("keywords", [])))
                    btn_update = st.form_submit_button("Update FAQ")

                    if btn_update:
                        kws = [k.strip() for k in edit_kw.split(",") if k.strip()]
                        success, msg = engine.update_faq(faq_to_edit["id"], edit_cat, edit_q, edit_a, kws)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

        elif admin_action == "❌ Delete FAQ":
            st.markdown("#### Delete an FAQ Entry")
            if not engine.faqs:
                st.warning("No FAQs available to delete.")
            else:
                faq_options_del = {f"{f['id']} - {f['question']}": f["id"] for f in engine.faqs}
                selected_del_label = st.selectbox("Select FAQ to delete:", list(faq_options_del.keys()))
                del_id = faq_options_del[selected_del_label]

                if st.button(f"Confirm Delete {del_id}", type="primary"):
                    success, msg = engine.delete_faq(del_id)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        elif admin_action == "🔄 Reset Factory Defaults":
            st.markdown("#### Reset Knowledge Base to Factory Defaults")
            st.warning("This action will restore the original 15 standard ShopEase FAQs.")
            if st.button("Reset to Default FAQs"):
                success, msg = engine.reset_factory_faqs()
                if success:
                    st.success(msg)
                    st.rerun()

    # ==================================================================
    # TAB 4: ANALYTICS & AUDIT LOGS
    # ==================================================================
    with tab_analytics:
        st.markdown("### 📊 Analytics & Interaction Audit Logs")
        kpis = engine.calculate_kpis()

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Inquiries", kpis["total_conversations"])
        m2.metric("Avg Confidence", f"{kpis['avg_confidence_pct']}%")
        m3.metric("Resolution Rate", f"{kpis['resolution_rate_pct']}%")
        m4.metric("Handoff Rate", f"{kpis['handoff_rate_pct']}%")
        m5.metric("Avg Latency", f"{kpis['avg_latency_ms']} ms")

        st.divider()
        st.markdown("#### Real-Time Chat Log History")
        logs = engine.get_chat_logs()

        if not logs:
            st.info("No customer chat logs recorded yet. Start a conversation in the 'Customer Chat' tab!")
        else:
            df_logs = pd.DataFrame(logs)
            st.dataframe(
                df_logs[["timestamp", "user_query", "bot_response", "confidence", "human_handoff", "response_time_ms"]],
                column_config={
                    "timestamp": "Timestamp",
                    "user_query": "Customer Query",
                    "bot_response": "Bot Response",
                    "confidence": st.column_config.NumberColumn("Confidence", format="%.2f"),
                    "human_handoff": "Handoff?",
                    "response_time_ms": st.column_config.NumberColumn("Latency (ms)", format="%.2f ms"),
                },
                use_container_width=True,
                hide_index=True,
            )

    # ==================================================================
    # TAB 5: ACCURACY BENCHMARK
    # ==================================================================
    with tab_benchmark:
        st.markdown("### 🎯 Accuracy Benchmark Suite")
        st.write("Run automated test inquiries against the ShopEase AI Customer Support Engine to measure accuracy and response latency.")

        if st.button("🚀 Run 17-Question Benchmark Suite", type="primary"):
            bench_results = engine.run_benchmark_suite()

            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Total Benchmark Cases", bench_results["total_tests"])
            b2.metric("Passed Tests", bench_results["passed_tests"])
            b3.metric("Overall Accuracy", f"{bench_results['accuracy_pct']}%")
            b4.metric("Avg Response Time", f"{bench_results['avg_latency_ms']} ms")

            st.divider()
            df_bench = pd.DataFrame(bench_results["results"])
            st.dataframe(
                df_bench[["query", "intent", "expected", "actual", "confidence", "latency_ms", "status"]],
                column_config={
                    "query": "Test Query",
                    "intent": "Target Intent",
                    "expected": "Expected FAQ ID",
                    "actual": "Matched FAQ ID",
                    "confidence": st.column_config.NumberColumn("Confidence", format="%.2f"),
                    "latency_ms": st.column_config.NumberColumn("Latency (ms)", format="%.2f ms"),
                    "status": "Result",
                },
                use_container_width=True,
                hide_index=True,
            )


if __name__ == "__main__":
    render_ui()