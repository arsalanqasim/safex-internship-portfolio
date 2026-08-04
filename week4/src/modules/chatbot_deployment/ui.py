"""Streamlit UI for AI Customer Support Chatbot Deployment Package.

Features dynamic client rebranding, floating widget simulator, custom proposal viewer,
interactive ROI calculator, Excel outreach logging form, and video walkthrough guidelines.
"""

from __future__ import annotations

import os
from pathlib import Path
import pandas as pd
import streamlit as st

from src.config import DATA_DIR
from src.modules.chatbot_deployment.engine import BENCHMARK_TEST_SUITE, CustomerSupportEngine
from src.modules.registry import MODULE_REGISTRY


def get_outreach_tracker_path() -> Path:
    """Resolve absolute path to outreach tracker Excel sheet."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / "outreach_tracker.xlsx"


def load_outreach_logs() -> pd.DataFrame:
    """Load outreach logs from the Excel sheet."""
    tracker_path = get_outreach_tracker_path()
    if tracker_path.exists():
        try:
            return pd.read_excel(tracker_path)
        except Exception:
            pass
    return pd.DataFrame(columns=["Organization Name", "Platform Used", "Contact Date", "Response Status", "Outreach Details"])


def save_outreach_log(org_name: str, platform: str, date_str: str, status: str, details: str) -> None:
    """Save a new outreach record to the Excel sheet."""
    df = load_outreach_logs()
    new_record = pd.DataFrame([{
        "Organization Name": org_name,
        "Platform Used": platform,
        "Contact Date": date_str,
        "Response Status": status,
        "Outreach Details": details
    }])
    df = pd.concat([df, new_record], ignore_index=True)
    tracker_path = get_outreach_tracker_path()
    df.to_excel(tracker_path, index=False, engine="openpyxl")


def get_secret(key_name: str) -> str | None:
    """Safely fetch a secret from Streamlit secrets or OS environment."""
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name)


def render_ui() -> None:
    """Render Arsalan Qasim's submission-ready chatbot deployment package."""
    metadata = MODULE_REGISTRY["week4"]["chatbot_deployment"]

    # 1. Page Header
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">💼 Client Ready Sprint · Group Leader Module</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Developer: <strong>{metadata["developer"]}</strong> ({metadata["role"]}) · <code>{metadata["email"]}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Dynamic Branding Config & API Config Panel
    with st.sidebar:
        st.markdown("### Client Branding Settings")
        st.caption("Change the client organization details below. The entire dashboard and chatbot will adapt dynamically!")
        brand_name = st.text_input("Configured Client Brand Name", value="ThreadStyle Co.")
        st.divider()

        st.markdown("### 🔌 Live LLM API Configuration")
        st.caption("Select your AI model provider and input an API key to enable advanced conversational intelligence with live fallback support.")

        env_gemini_key = get_secret("GEMINI_API_KEY") or get_secret("GOOGLE_API_KEY")
        env_openai_key = get_secret("OPENAI_API_KEY")

        default_provider = "None (Local TF-IDF)"
        if env_gemini_key:
            default_provider = "Gemini"
        elif env_openai_key:
            default_provider = "OpenAI"

        provider_options = ["None (Local TF-IDF)", "Gemini", "OpenAI"]
        default_index = provider_options.index(default_provider)

        api_provider = st.selectbox("AI Model Provider", options=provider_options, index=default_index)

        api_key = ""
        api_model_name = "gemini-1.5-flash"  # Default
        if api_provider == "Gemini":
            # Model selection
            st.markdown("#### Gemini Model Selection")
            st.caption("Both of these models are available on the free tier. Flash is faster and has higher limits; Pro is more capable.")
            api_model_name = st.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
            
            default_key = env_gemini_key or ""
            if default_key:
                st.success("🔒 API Key loaded from server secrets.")
                override = st.checkbox("Override server API Key")
                if override:
                    api_key = st.text_input("Enter Custom Gemini API Key", type="password", help="Obtain a free key from Google AI Studio")
                else:
                    api_key = default_key
            else:
                api_key = st.text_input("Gemini API Key", type="password", help="Obtain a free key from Google AI Studio")
        elif api_provider == "OpenAI":
            default_key = env_openai_key or ""
            if default_key:
                st.success("🔒 API Key loaded from server secrets.")
                override = st.checkbox("Override server API Key")
                if override:
                    api_key = st.text_input("Enter Custom OpenAI API Key", type="password", help="Obtain an API key from OpenAI Platform")
                else:
                    api_key = default_key
            else:
                api_key = st.text_input("OpenAI API Key", type="password", help="Obtain an API key from OpenAI Platform")

        engine_provider = None if api_provider == "None (Local TF-IDF)" else api_provider
        engine_key = api_key if engine_provider else None
        st.divider()

    # Instantiate engine with the chosen brand name and API credentials
    engine = CustomerSupportEngine(
        brand_name=brand_name,
        confidence_threshold=0.20,
        api_provider=engine_provider,
        api_key=engine_key,
        api_model=api_model_name
    )

    # Expanded details
    with st.expander("📌 Module Specifications", expanded=False):
        st.write(f"**Objective:** {metadata['description']}")
        st.write(f"**Tech Stack:** {' · '.join(metadata['tech'])}")
        st.write(f"**Configured Client:** {brand_name}")
        st.write(f"**Engine Active:** {api_provider}")

    # UI Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Live Shop Chatbot", 
        "📄 1-Page Proposal", 
        "🧮 Interactive ROI Calculator", 
        "📊 Outreach Tracker", 
        "📝 Walkthrough Video Script"
    ])

    # Tab 1: Live Chatbot Simulator
    with tab1:
        st.subheader(f"Interactive Webpage Integration & Chatbot Simulator")
        st.caption("Test the chatbot prototype inside a simulated storefront widget. Notice the error handling filters (gibberish/length) and the human escalation fallback triggers.")

        # Website mock card
        st.markdown(
            f"""
            <div style="background-color: var(--surface); padding: 1.5rem; border: 1px solid var(--line); border-radius: 12px; margin-bottom: 1.5rem; border-top: 4px solid var(--accent);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0; font-size: 1.2rem; color: var(--ink);">🛍️ {brand_name} Storefront Mockup</h4>
                    <span style="font-size: 0.75rem; background-color: #22c55e; color: white; padding: 2px 8px; border-radius: 999px; font-weight: 700;">🟢 Online</span>
                </div>
                <p style="font-size: 0.85rem; color: var(--muted); margin-bottom: 0;">
                    Welcome to the <strong>{brand_name}</strong> client e-commerce store. Browse products, add to cart, and chat with our AI agent to manage orders, check return policies, or ask about fits.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("**Sample Customer Queries:**")
        col_p1, col_p2, col_p3 = st.columns(3)
        if col_p1.button("📦 Track shipment"):
            st.session_state.chat_query_val = "How can I track my shipment?"
        if col_p2.button("👚 Sizing assistance"):
            st.session_state.chat_query_val = "What size should I order for a chest size of 40?"
        if col_p3.button("🚨 Dispute/Escalation query"):
            st.session_state.chat_query_val = "You stole my money, cancel this order and refund me!"

        query_input = st.text_input(
            "Enter customer query",
            value=st.session_state.get("chat_query_val", ""),
            placeholder=f"Ask {brand_name} assistant...",
            key="client_query_text_input",
        )

        if st.button("Send Message", type="primary", key="send_client_chat_query_btn"):
            if query_input:
                result = engine.classify_query(query_input)
                st.session_state.last_client_chat_result = result

        res = st.session_state.get("last_client_chat_result")
        if res:
            st.divider()
            res_col1, res_col2 = st.columns([2, 1])
            with res_col1:
                st.markdown("#### Chatbot Response")
                if "Error" in res["intent"]:
                    st.error(f"⚠️ **Validation Check Failed**\n\n{res['response']}")
                    st.caption(f"**Error Category:** {res['category']} | **Diagnostic Trigger:** {res['escalation_reason']}")
                elif res["escalated"]:
                    st.warning(f"🚨 **Handoff to Support Agent**\n\n{res['response']}")
                    st.caption(f"**Escalation Trigger:** {res['escalation_reason']}")
                else:
                    st.success(f"🤖 **AI Agent Response:**\n\n{res['response']}")

            with res_col2:
                st.markdown("#### Diagnostics")
                st.metric("Intent Detected", res["intent"])
                st.metric("Confidence Score", f"{res['confidence']:.2f}")
                st.write(f"**Engine Used:** `{res.get('engine_used', 'Local TF-IDF')}`")
                st.write(f"**Category:** {res['category']}")
                
                if res.get("api_error"):
                    st.error(f"🔌 **API Error Details:**\n\n{res['api_error']}")
                elif res.get("matched_pattern"):
                    st.caption(f"Matched training pattern: *\"{res['matched_pattern']}\"*")

    # Tab 2: 1-Page Client Proposal
    with tab2:
        st.subheader("1-Page Client Commercial Proposal")
        st.caption("A premium productized proposal suitable for pitching this automated chatbot system to clients.")

        # Construct markdown proposal
        proposal_md = f"""# CLIENT SERVICE PROPOSAL

**Prepared For:** {brand_name}
**Prepared By:** Arsalan Qasim, SafeX Solutions Engineering Team
**Date:** August 2026

---

### 1. Executive Summary
Currently, customer support teams spend roughly 60% of their operational hours answering highly repetitive inquiries (e.g. shipping updates, size questions, and return policy details). This proposal outlines an AI-powered conversational agent that integrates directly into the **{brand_name}** website to automate up to 75% of repetitive queries, freeing up human support personnel to tackle high-value checkout resolutions.

### 2. The Solution
*   **Intelligent Intent Classifier**: A TF-IDF similarity engine mapping standard inquiries to instant, accurate corporate policy resolutions.
*   **Input Quality Protection**: Custom validation filters blocking junk submissions, excessive inputs, or blank text queries.
*   **Intelligent Human Escalation**: Immediate detection of frustrated customer sentiment or complex disputes (e.g., refunds, damage claims), auto-creating support tickets and executing warm handoffs.

### 3. Implementation Plan & Timeline
*   **Week 1**: FAQ knowledge acquisition and similarity engine custom training.
*   **Week 2**: Front-end storefront integration and interface customization matching **{brand_name}** brand guidelines.
*   **Week 3**: User acceptance testing (UAT) with a 10+ query benchmark check.
*   **Week 4**: Production launch, system logging, and staff handoff training.

---

### 4. Commercial Pricing Options
We offer three scalable tiers to match **{brand_name}**'s query volumes:

| Plan | Monthly Cost | Volume Limit | Support Handoff | Integrations |
|---|---|---|---|---|
| **Starter Tier** | **$49 / month** | Up to 500 queries | Standard email ticket | Web Widget |
| **Pro Tier** | **$149 / month** | Up to 2,500 queries | Real-time chat transfer | Web + WhatsApp + CRM |
| **Enterprise Tier** | **$499 / month** | Unlimited queries | Dedicated human operator | Full omnichannel custom API |
"""
        st.markdown(proposal_md)

        st.download_button(
            "📥 Download Proposal (Markdown)",
            data=proposal_md,
            file_name=f"{brand_name.lower().replace(' ', '_')}_chatbot_proposal.md",
            mime="text/markdown"
        )

    # Tab 3: ROI Calculator
    with tab3:
        st.subheader("AI Automation ROI Estimator")
        st.caption("Quantify the exact financial savings this automation can provide based on the client's current operations.")

        calc_col1, calc_col2 = st.columns(2)

        with calc_col1:
            st.markdown("#### Input Variables")
            staff_hours = st.slider("Staff hours spent on routine queries (Monthly)", min_value=5, max_value=120, value=40, step=5)
            staff_cost = st.slider("Staff hourly cost ($)", min_value=10, max_value=100, value=25, step=5)
            monthly_queries = st.number_input("Average monthly support volume (queries)", min_value=50, max_value=10000, value=800, step=50)

        # Calculate costs
        manual_support_cost = staff_hours * staff_cost
        
        # Decide tier based on queries
        if monthly_queries < 500:
            recommended_tier = "Starter Plan"
            recommended_cost = 49
        elif monthly_queries <= 2500:
            recommended_tier = "Pro Plan"
            recommended_cost = 149
        else:
            recommended_tier = "Enterprise Plan"
            recommended_cost = 499

        monthly_savings = max(0, manual_support_cost - recommended_cost)
        annual_savings = monthly_savings * 12
        roi_pct = (monthly_savings / recommended_cost) * 100.0 if recommended_cost > 0 else 0

        with calc_col2:
            st.markdown("#### Cost & Savings Summary")
            st.metric("Current Manual Cost (Monthly)", f"${manual_support_cost:,.2f}")
            st.metric(f"Recommended System ({recommended_tier})", f"${recommended_cost:,.2f} / month")
            st.metric("Estimated Cost Savings (Monthly)", f"${monthly_savings:,.2f}")
            st.metric("Estimated Cost Savings (Annual)", f"${annual_savings:,.2f}")
            st.metric("Projected ROI", f"{roi_pct:,.1f}%")

            st.markdown(
                f"""
                > [!NOTE]
                > By deploying the **{recommended_tier}**, **{brand_name}** can save approximately **${monthly_savings:,.2f} per month** while increasing customer satisfaction via instant 24/7 response times.
                """
            )

    # Tab 4: Outreach Tracker
    with tab4:
        st.subheader("Client Outreach Tracker & Log")
        st.caption("Record and monitor client outreach attempts to professionals and organizations. Data is written to `week4/data/outreach_tracker.xlsx`.")

        outreach_form_col, outreach_history_col = st.columns([1, 1.5])

        with outreach_form_col:
            st.markdown("#### Log New Outreach")
            with st.form("outreach_tracker_form", clear_on_submit=True):
                target_org = st.text_input("Target Organization / Professional Name", placeholder="e.g. Acme Clothing Corp")
                platform_used = st.selectbox("Outreach Platform", ["Email", "LinkedIn DM", "WhatsApp", "Phone Call", "Other"])
                contact_date = st.date_input("Contact Date")
                response_status = st.selectbox("Response Status", [
                    "Sent (Awaiting Response)", 
                    "Replied (Interested)", 
                    "Replied (Not Interested)", 
                    "No Response", 
                    "Intro Call Scheduled", 
                    "Client Signed"
                ])
                outreach_details = st.text_area("Outreach Message / Summary Details")

                submit_outreach = st.form_submit_button("Save Log Entry", type="primary")

                if submit_outreach:
                    if target_org:
                        save_outreach_log(
                            org_name=target_org,
                            platform=platform_used,
                            date_str=str(contact_date),
                            status=response_status,
                            details=outreach_details
                        )
                        st.success(f"Success! Outreach log for '{target_org}' saved successfully.")
                    else:
                        st.error("Please enter a valid target organization name.")

        with outreach_history_col:
            st.markdown("#### Outreach Logs History")
            history_df = load_outreach_logs()
            if history_df.empty:
                st.info("No outreach logs found yet. Submit the form on the left to record your first outreach attempt!")
            else:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Download log option
                tracker_path = get_outreach_tracker_path()
                if tracker_path.exists():
                    with open(tracker_path, "rb") as f:
                        st.download_button(
                            "📥 Download Excel Logs Sheet",
                            data=f.read(),
                            file_name="outreach_tracker.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

    # Tab 5: Walkthrough Video Script Guidelines
    with tab5:
        st.subheader("Client-Presentation Video Script Guidelines")
        st.caption("Use this script layout to record your mandatory 3-5 minute client walkthrough video.")

        st.markdown(
            f"""
            ### Walkthrough Demo Video Script (Duration: 3 - 5 mins)
            
            **[0:00 - 0:45] Intro & Business Problem**
            *   *Visual*: Face visible on camera, main Streamlit app homepage in background.
            *   *What to say*: "Hello, my name is Arsalan Qasim, Group Leader of Group 54. Today, I am presenting our client-ready AI Customer Support Chatbot Deployment Package. E-commerce organizations like **{brand_name}** lose significant staff hours and customer engagement manually answering repetitive questions regarding shipping, sizing, and store hours. Our solution automates these workflows..."

            **[0:45 - 2:00] Live Chatbot Demonstration**
            *   *Visual*: Streamlit screen share of **Tab 1: Live Shop Chatbot**.
            *   *What to say*: "Let's test this in action. The chatbot engine uses TF-IDF vector similarity. If I ask 'where is my order?', it instantly triggers the order tracking intent. We've built robust input guards. For instance, if I enter gibberish like 'qqq' or submit empty text, the validation checks flag the error. Additionally, if the customer is frustrated and mentions keywords like 'refund' or 'scam', the engine automatically flags the conversation and executes a Support Agent Ticket escalation..."

            **[2:00 - 3:00] Business Proposal & Financial ROI**
            *   *Visual*: Screen share of **Tab 2 (Proposal)** and **Tab 3 (ROI Calculator)**.
            *   *What to say*: "To make this proposal product-ready, we've drafted a commercial proposal showing three pricing tiers: Starter at $49/mo, Pro at $149/mo, and Enterprise. Let's look at our ROI calculator. If a client currently spends 40 hours monthly answering routine emails at a support staff cost of $25/hour, that's $1,000 in support cost. With our automated Pro tier system at $149/mo, they achieve an instant **PKR/USD savings of $851 per month**, yielding over **570% ROI**."

            **[3:00 - 3:30] Outreach & Client Tracking**
            *   *Visual*: Screen share of **Tab 4 (Outreach Tracker)**.
            *   *What to say*: "Finally, to test the market, we've launched our outreach sprint, logging intro calls and prospective organizations directly in our tracker. This completes our Client-Ready Sprint Package. Thank you for your time!"
            """
        )
