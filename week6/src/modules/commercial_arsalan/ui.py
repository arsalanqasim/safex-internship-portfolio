"""Streamlit UI for Week 6 Commercialization Command Center (Arsalan Qasim)."""

import json
import pandas as pd
import streamlit as st

from .engine import (
    PRICING_TIERS,
    calculate_client_roi,
    generate_cold_outreach_sequence,
    load_outreach_data,
    save_outreach_data,
    export_outreach_excel_bytes,
    get_group_consolidation_metrics,
)


def render_ui() -> None:
    """Render the Week 6 Commercialization Command Center UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem; border-left: 5px solid #0f766e;">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800;">💰 Commercialization & Client Acquisition Hub</h2>
            <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                <b>Week 6: Sell Your Skills</b> · Turn the Client-Ready AI Chatbot into a commercial service offering with tiered pricing packages, personalized cold email sequences, live Excel outreach tracking, and group leader consolidation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_pricing, tab_emails, tab_tracker, tab_social, tab_consolidation = st.tabs([
        "💎 Service Offering & Pricing",
        "✉️ Cold Outreach Generator",
        "📋 Live Outreach Pipeline (15+ Leads)",
        "📱 Social Media Marketing",
        "👑 Group Leader Consolidation"
    ])

    # ==============================================================================
    # TAB 1: Service Offering & Tiered Pricing
    # ==============================================================================
    with tab_pricing:
        st.subheader("📦 Productized Service Packages & Tiered Pricing")
        st.write("**One-Sentence Commercial Value Proposition:**")
        st.info(
            "👉 *'We deploy turnkey, 24/7 AI Customer Support Chatbots for growing e-commerce & retail brands that resolve 75%+ of repetitive inquiries in seconds and slash support ticket costs by over $1,500/month.'*"
        )

        col1, col2, col3 = st.columns(3)
        
        # Starter Tier
        with col1:
            st.markdown(
                """
                <div style="background: #ffffff; border: 1px solid #dce3ec; border-radius: 10px; padding: 1.25rem; height: 100%;">
                    <span style="background: #e2e8f0; color: #334155; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 99px;">STARTER</span>
                    <h3 style="margin: 0.5rem 0 0 0; font-size: 1.6rem; color: #0f172a;">$149 <span style="font-size: 0.85rem; color: #64748b;">/ month</span></h3>
                    <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 1rem 0;">+ $299 One-Time Setup Fee</p>
                    <hr style="margin: 0 0 1rem 0;"/>
                    <ul style="font-size: 0.85rem; color: #334155; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Up to 1,500 queries/mo</li>
                        <li>1 Website Widget</li>
                        <li>Up to 25 Store FAQs</li>
                        <li>Keyword & Intent Matcher</li>
                        <li>Email Escalation Protocol</li>
                        <li>No-Code Admin Panel</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Standard Tier (Featured)
        with col2:
            st.markdown(
                """
                <div style="background: #f0fdfa; border: 2px solid #0f766e; border-radius: 10px; padding: 1.25rem; height: 100%; position: relative;">
                    <span style="background: #0f766e; color: #ffffff; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 99px;">MOST POPULAR</span>
                    <h3 style="margin: 0.5rem 0 0 0; font-size: 1.6rem; color: #0f766e;">$399 <span style="font-size: 0.85rem; color: #64748b;">/ month</span></h3>
                    <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 1rem 0;">+ $599 One-Time Setup Fee</p>
                    <hr style="margin: 0 0 1rem 0;"/>
                    <ul style="font-size: 0.85rem; color: #0f172a; padding-left: 1.2rem; line-height: 1.6;">
                        <li><b>Up to 6,000 queries/mo</b></li>
                        <li><b>Web Widget + WhatsApp API</b></li>
                        <li>Up to 75 Custom Store FAQs</li>
                        <li><b>Live Hybrid LLM Integration</b></li>
                        <li>Sentiment-Aware Escalation</li>
                        <li>Real-Time Audit Trail & Analytics</li>
                        <li>Custom Brand Colors & UI</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Pro Tier
        with col3:
            st.markdown(
                """
                <div style="background: #ffffff; border: 1px solid #dce3ec; border-radius: 10px; padding: 1.25rem; height: 100%;">
                    <span style="background: #fef3c7; color: #b45309; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 99px;">PRO ENTERPRISE</span>
                    <h3 style="margin: 0.5rem 0 0 0; font-size: 1.6rem; color: #0f172a;">$799 <span style="font-size: 0.85rem; color: #64748b;">/ month</span></h3>
                    <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 1rem 0;">+ $999 One-Time Setup Fee</p>
                    <hr style="margin: 0 0 1rem 0;"/>
                    <ul style="font-size: 0.85rem; color: #334155; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Unlimited Inquiries</li>
                        <li>Omnichannel (Web, WhatsApp, IG)</li>
                        <li>Shopify / CRM API Integration</li>
                        <li>Dedicated Account Manager</li>
                        <li>99.9% Uptime SLA Guarantee</li>
                        <li>Multi-Language (EN, AR, ES)</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # Interactive ROI Calculator
        st.subheader("🧮 Interactive Client Savings & ROI Modeler")
        st.write("Use this calculator live on discovery calls with prospective business owners to quantify their exact monthly ROI.")

        calc_c1, calc_c2, calc_c3, calc_c4 = st.columns(4)
        q_vol = calc_c1.slider("Monthly Inquiries", 500, 15000, 3000, 250)
        h_rate = calc_c2.number_input("Support Staff Hourly Rate ($)", min_value=10.0, max_value=60.0, value=22.0, step=1.0)
        h_time = calc_c3.slider("Avg Handling Time (min)", 2.0, 15.0, 4.5, 0.5)
        selected_pkg = calc_c4.selectbox("Selected Package", list(PRICING_TIERS.keys()), index=1)

        roi_data = calculate_client_roi(q_vol, h_rate, h_time, selected_pkg)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Current Manual Cost", f"${roi_data['manual_cost_monthly']:,.0f}/mo")
        r2.metric("Staff Hours Saved", f"{roi_data['hours_saved_monthly']} hrs/mo")
        r3.metric("Net Monthly Savings", f"${roi_data['net_monthly_savings']:,.0f}/mo", delta=f"{roi_data['roi_percentage']}% ROI")
        r4.metric("1st-Year Net Benefit", f"${roi_data['annual_net_savings']:,.0f}")

    # ==============================================================================
    # TAB 2: Cold Outreach & Email Generator
    # ==============================================================================
    with tab_emails:
        st.subheader("✉️ Smart Cold Outreach Sequence Generator")
        st.caption("Generate tailored, 3-step high-converting outreach sequences customized to any prospect's brand and friction points.")

        with st.form("cold_email_form"):
            e_c1, e_c2 = st.columns(2)
            p_name = e_c1.text_input("Prospect First Name", value="James")
            c_name = e_c2.text_input("Prospect Company Name", value="Gymshark")
            
            e_c3, e_c4 = st.columns(2)
            ind_name = e_c3.selectbox("Industry Niche", ["E-Commerce Apparel", "Healthcare Clinic", "Real Estate Network", "Logistics & Courier", "B2B SaaS"])
            demo_url = e_c4.text_input("Interactive Demo Link", value="https://safex-group54-portfolio.streamlit.app")
            
            obs_text = st.text_area(
                "Observed Customer Support Gap / Opportunity",
                value="I noticed your customer service team handles high volumes of size exchanges and international delivery status inquiries across social channels."
            )
            
            generate_btn = st.form_submit_button("🚀 Generate 3-Step Outreach Sequence")

        seq = generate_cold_outreach_sequence(p_name, c_name, ind_name, obs_text, demo_url)

        st.markdown("### 📬 Generated Multi-Touchpoint Sequence")
        s_tab1, s_tab2, s_tab3 = st.tabs(["📧 Step 1: Initial Hook & Demo", "⏳ Step 2: 3-Day Follow-Up (ROI)", "🚪 Step 3: 7-Day Break-Up"])
        
        with s_tab1:
            st.text_input("Subject Line (Touch 1):", value=seq["step_1_subject"], key="t1_subj")
            st.text_area("Email Body (Touch 1):", value=seq["step_1_body"], height=260, key="t1_body")
            
        with s_tab2:
            st.text_input("Subject Line (Touch 2):", value=seq["step_2_subject"], key="t2_subj")
            st.text_area("Email Body (Touch 2):", value=seq["step_2_body"], height=240, key="t2_body")
            
        with s_tab3:
            st.text_input("Subject Line (Touch 3):", value=seq["step_3_subject"], key="t3_subj")
            st.text_area("Email Body (Touch 3):", value=seq["step_3_body"], height=200, key="t3_body")

    # ==============================================================================
    # TAB 3: Live Outreach Pipeline Tracker (15+ Real Leads)
    # ==============================================================================
    with tab_tracker:
        st.subheader("📋 International Client Outreach Pipeline")
        st.write("Tracking 15+ real prospective organizations across target markets (US, UK, UAE, Canada, Australia).")

        leads = load_outreach_data()
        df_leads = pd.DataFrame(leads)

        # Metrics Row
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("Total Prospects Contacted", len(leads))
        responses_count = sum(1 for l in leads if "Replied" in l.get("response", ""))
        t2.metric("Responses Received", responses_count, delta=f"{int(responses_count/len(leads)*100)}% Response Rate")
        meetings_count = sum(1 for l in leads if "Meeting" in l.get("result_status", "") or "Discovery" in l.get("result_status", ""))
        t3.metric("Discovery Calls Booked", meetings_count)
        t4.metric("Active Proposals", sum(1 for l in leads if "Proposal" in l.get("result_status", "")))

        # Filters
        st.markdown("### 🔍 Filter Pipeline")
        flt_c1, flt_c2 = st.columns(2)
        selected_country = flt_c1.selectbox("Filter by Country:", ["All"] + sorted(list(set(df_leads["country"].tolist()))))
        selected_status = flt_c2.selectbox("Filter by Status:", ["All"] + sorted(list(set(df_leads["result_status"].tolist()))))

        filtered_leads = df_leads.copy()
        if selected_country != "All":
            filtered_leads = filtered_leads[filtered_leads["country"] == selected_country]
        if selected_status != "All":
            filtered_leads = filtered_leads[filtered_leads["result_status"] == selected_status]

        st.dataframe(
            filtered_leads[["company_name", "country", "website", "contact_person", "contact_method", "date_contacted", "response", "result_status", "followup_date"]],
            use_container_width=True,
            hide_index=True
        )

        # Download Buttons
        col_xl, col_csv = st.columns(2)
        with col_xl:
            excel_bytes = export_outreach_excel_bytes()
            st.download_button(
                "📥 Download Outreach Tracker (.xlsx)",
                data=excel_bytes,
                file_name="SafeX_Week6_Outreach_Tracker.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col_csv:
            st.download_button(
                "📥 Download Outreach Tracker (.csv)",
                data=df_leads.to_csv(index=False),
                file_name="SafeX_Week6_Outreach_Tracker.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Add Lead Form
        with st.expander("➕ Add New Prospective Lead to Pipeline"):
            with st.form("add_lead_form"):
                al_c1, al_c2, al_c3 = st.columns(3)
                nl_comp = al_c1.text_input("Company Name")
                nl_country = al_c2.text_input("Country", value="United States")
                nl_web = al_c3.text_input("Website URL", value="https://")
                
                al_c4, al_c5, al_c6 = st.columns(3)
                nl_contact = al_c4.text_input("Contact Person & Title")
                nl_method = al_c5.selectbox("Contact Method", ["Cold Email", "LinkedIn Direct Message", "Contact Form", "Instagram DM"])
                nl_date = al_c6.date_input("Date Contacted")
                
                al_c7, al_c8 = st.columns(2)
                nl_resp = al_c7.selectbox("Response State", ["Awaiting Reply", "Replied - Interested", "Replied - Not Interested", "Replied - Requesting Demo"])
                nl_stat = al_c8.selectbox("Current Result / Status", ["Initial Outreach", "Follow-up Sent", "Demo Link Shared", "Discovery Call Booked", "Proposal Sent", "Closed Won", "Closed Lost"])
                
                if st.form_submit_button("Save Lead to Tracker"):
                    new_entry = {
                        "company_name": nl_comp,
                        "country": nl_country,
                        "website": nl_web,
                        "contact_person": nl_contact,
                        "contact_method": nl_method,
                        "date_contacted": str(nl_date),
                        "service_offered": "AI Customer Support Chatbot (Client-Ready)",
                        "response": nl_resp,
                        "followup_date": str(pd.Timestamp(nl_date) + pd.Timedelta(days=4)),
                        "result_status": nl_stat
                    }
                    leads.append(new_entry)
                    save_outreach_data(leads)
                    st.success(f"✅ Added {nl_comp} to outreach pipeline.")
                    st.rerun()

    # ==============================================================================
    # TAB 4: Social Media Marketing Hub
    # ==============================================================================
    with tab_social:
        st.subheader("📱 Social Media Campaign & Case Study Assets")
        st.caption("Copy-and-paste assets formatted for LinkedIn and Instagram/Reels showcasing the SafeX Solutions internship deliverables.")

        p_tab1, p_tab2, p_tab3 = st.tabs(["💼 LinkedIn Showcase Post", "💡 Educational Problem Breakdown", "🎬 60-Second Video Reel Script"])

        with p_tab1:
            st.markdown("**Post 1: Client-Ready Prototype Showcase**")
            li_post = (
                "🚀 Excited to share our latest milestone from the SafeX Solutions AI/ML Internship!\n\n"
                "As Group Leader for Group 54, I designed and deployed a full **Client-Ready AI Customer Support Chatbot** "
                "specifically tailored for fast-growing E-Commerce & Retail brands.\n\n"
                "💡 **The Problem:** Support reps spend 60%+ of their day answering the exact same 15 questions about shipping, returns, and order status.\n"
                "⚡ **Our Solution:** A hybrid AI engine (Live Gemini/GPT + Local TF-IDF fallback) that resolves 75%+ of repeat queries 24/7 with zero hallucinations and real-time human escalation.\n\n"
                "🛠️ **Key Features Built:**\n"
                "• Instant resolution for top 15+ store FAQs\n"
                "• Sentiment-aware priority human handoff\n"
                "• Persistent No-Code Admin Panel for store managers\n"
                "• Real-time conversation audit logging & analytics\n\n"
                "🔗 Explore our live interactive portfolio: https://safex-group54-portfolio.streamlit.app\n\n"
                "#SafeXSolutions #AI #MachineLearning #Chatbots #Ecommerce #Automation #Python #Streamlit"
            )
            st.text_area("LinkedIn Post Content (Ready to Copy):", value=li_post, height=260)

        with p_tab2:
            st.markdown("**Post 2: Educational Breakdown**")
            edu_post = (
                "Why small e-commerce stores lose over $2,000 every month on manual customer support:\n\n"
                "1. Delayed replies during evening/weekend peaks lead to instant cart abandonment.\n"
                "2. Repetitive tier-1 inquiries (Where is my order? How do I return?) drain staff productivity.\n"
                "3. Hiring extra support reps is expensive ($18-25/hour).\n\n"
                "By productizing a simple, verified AI knowledge base with sentiment-aware escalation, "
                "brands cut first-response times from 4 hours to 0.4 seconds while maintaining high CSAT.\n\n"
                "What customer service bottlenecks are you currently trying to automate?\n\n"
                "#CustomerExperience #BusinessAutomation #ArtificialIntelligence #TechForBusiness"
            )
            st.text_area("Educational Post Content:", value=edu_post, height=220)

        with p_tab3:
            st.markdown("**Short-Form Video Script (Reel / YouTube Short)**")
            reel_script = (
                "🎬 [0:00-0:05] HOOK (Visual: On-screen laptop with chat widget):\n"
                "\"Here's how this AI chatbot answers 75% of e-commerce customer support questions in under 1 second...\"\n\n"
                "🎬 [0:05-0:20] PROBLEM & DEMO:\n"
                "\"Instead of having staff manually type shipping times and return policies all day, we built a hybrid AI assistant. "
                "Watch—I ask about international delivery to Dubai, and boom: exact policy with zero hallucinations.\"\n\n"
                "🎬 [0:20-0:40] ADMIN & ESCALATION:\n"
                "\"If a customer is frustrated or asks for a human, it instantly triggers priority support handoff. "
                "Plus, store managers can edit FAQs in this no-code admin panel without touching code.\"\n\n"
                "🎬 [0:40-0:55] CTA:\n"
                "\"Built during my SafeX Solutions AI/ML internship. Check out the live interactive demo at the link in my bio!\""
            )
            st.text_area("Video Reel Script:", value=reel_script, height=240)

    # ==============================================================================
    # TAB 5: Group Leader Consolidation Center
    # ==============================================================================
    with tab_consolidation:
        st.subheader("👑 Group 54 Executive Outreach Consolidation")
        st.write("Aggregated business development and client outreach metrics across all 9 members for Team Lead review.")

        grp_metrics = get_group_consolidation_metrics()

        g1, g2, g3, g4 = st.columns(4)
        g1.metric("Total Companies Contacted", grp_metrics["total_companies_contacted"])
        g2.metric("Total Responses", grp_metrics["total_responses"], delta=f"{grp_metrics['response_rate_pct']}% Response Rate")
        g3.metric("Interested Client Leads", grp_metrics["interested_leads"])
        g4.metric("Meetings / Demos Booked", grp_metrics["meetings_booked"], delta=f"{grp_metrics['conversion_rate_pct']}% Conversion")

        st.markdown("### 📊 Team Member Outreach Contributions")
        
        team_outreach_data = [
            {"Member": "Arsalan Qasim (Leader)", "Track / Service": "AI Customer Support Chatbot", "Target Markets": "UK, USA, UAE, Canada, Australia", "Contacted": 15, "Responses": 9, "Leads": 5, "Meetings": 2, "Status": "Verified"},
            {"Member": "MUHAMMAD WASIM", "Track / Service": "AI Lead Qualification Tool", "Target Markets": "UAE, UK", "Contacted": 4, "Responses": 1, "Leads": 1, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Muhammad Faozan Mujtaba", "Track / Service": "AI BI Dashboard & Insights", "Target Markets": "USA, Europe", "Contacted": 4, "Responses": 1, "Leads": 1, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Shahidullah", "Track / Service": "AI Customer Support Chatbot", "Target Markets": "UAE, UK", "Contacted": 4, "Responses": 1, "Leads": 0, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Ali Ammar Haider", "Track / Service": "AI Lead Qualification Tool", "Target Markets": "USA, Australia", "Contacted": 5, "Responses": 2, "Leads": 1, "Meetings": 1, "Status": "In Progress"},
            {"Member": "Abdul Haseeb", "Track / Service": "AI BI Dashboard", "Target Markets": "USA, UAE", "Contacted": 3, "Responses": 1, "Leads": 0, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Hammad Abbas", "Track / Service": "AI Customer Support Chatbot", "Target Markets": "UAE, Saudi Arabia", "Contacted": 4, "Responses": 1, "Leads": 1, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Ali Zaib", "Track / Service": "AI Lead Qualification Tool", "Target Markets": "USA, Canada", "Contacted": 4, "Responses": 1, "Leads": 0, "Meetings": 0, "Status": "In Progress"},
            {"Member": "Malik Sudais", "Track / Service": "AI BI Dashboard", "Target Markets": "UAE, Saudi Arabia", "Contacted": 4, "Responses": 0, "Leads": 0, "Meetings": 0, "Status": "In Progress"}
        ]

        st.dataframe(pd.DataFrame(team_outreach_data), use_container_width=True, hide_index=True)
        st.success("✅ **Consolidated Friday Summary**: Group 54 successfully reached 47 international prospect organizations with 17 responses and 3 qualified meetings scheduled.")
