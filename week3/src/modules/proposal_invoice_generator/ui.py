"""Streamlit UI for Proposal & Invoice Generator Agent (Malik Sudais - Week 3)."""

import streamlit as st
import pandas as pd
from .engine import generate_commercial_proposal, calculate_invoice_totals


def render_ui() -> None:
    """Render the Proposal & Invoice Generator UI."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 1.5rem 2rem; border-radius: 12px; color: white; margin-bottom: 1.5rem; border-left: 5px solid #0284c7;">
            <h2 style="margin: 0; color: #ffffff;">📄 Proposal & Invoice Generator Agent</h2>
            <p style="margin: 0.5rem 0 0 0; color: #cbd5e1; font-size: 0.95rem;">
                Developer: <b>Malik Sudais</b> · Week 3 Submission & Project Deliverable
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Submission Evidence Card
    col_repo, col_drive = st.columns(2)
    with col_repo:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem; margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #0284c7;">GITHUB REPOSITORY</span><br/>
                <a href="https://github.com/maliksudais24/Proposal-invoice-automation-.git" target="_blank" style="text-decoration: none; font-weight: 600; color: #0f172a;">
                    🔗 maliksudais24/Proposal-invoice-automation-
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_drive:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem; margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #0284c7;">GOOGLE DRIVE SUBMISSION</span><br/>
                <a href="https://drive.google.com/drive/folders/1UWGCupMZC2UafccOs2fStmVO_WEQxPfJ?usp=sharing" target="_blank" style="text-decoration: none; font-weight: 600; color: #0f172a;">
                    📁 View Screen Recording & Video
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Interactive Generator
    st.subheader("📝 Proposal & Invoice Generator Tool")
    
    col_client, col_proj = st.columns(2)
    with col_client:
        client_name = st.text_input("Client Contact Name", value="Alex Morgan")
        client_comp = st.text_input("Client Organization", value="Vertex Logistics Co.")
    with col_proj:
        proj_title = st.text_input("Project / Service Name", value="AI Fleet Routing & Logistics Automation")
        timeline = st.slider("Delivery Timeline (Weeks)", 1, 12, 4)

    st.markdown("### 📋 Line Items & Rates")
    col_i1, col_i2, col_i3 = st.columns([3, 1, 1])
    item1_desc = col_i1.text_input("Item 1 Description", value="AI Route Optimization Algorithm Architecture")
    item1_qty = col_i2.number_input("Item 1 Qty", min_value=1, value=1)
    item1_rate = col_i3.number_input("Item 1 Rate ($)", min_value=0.0, value=1200.0, step=100.0)

    col_i4, col_i5, col_i6 = st.columns([3, 1, 1])
    item2_desc = col_i4.text_input("Item 2 Description", value="Fleet Telematics API Webhook Integration")
    item2_qty = col_i5.number_input("Item 2 Qty", min_value=1, value=1)
    item2_rate = col_i6.number_input("Item 2 Rate ($)", min_value=0.0, value=850.0, step=50.0)

    col_i7, col_i8, col_i9 = st.columns([3, 1, 1])
    item3_desc = col_i7.text_input("Item 3 Description", value="Executive Dispatch Dashboard & Testing")
    item3_qty = col_i8.number_input("Item 3 Qty", min_value=1, value=1)
    item3_rate = col_i9.number_input("Item 3 Rate ($)", min_value=0.0, value=650.0, step=50.0)

    col_d, col_t = st.columns(2)
    discount = col_d.slider("Discount (%)", 0.0, 30.0, 5.0, 1.0)
    tax = col_t.slider("Sales Tax (%)", 0.0, 15.0, 5.0, 0.5)

    line_items = [
        {"desc": item1_desc, "qty": item1_qty, "rate": item1_rate},
        {"desc": item2_desc, "qty": item2_qty, "rate": item2_rate},
        {"desc": item3_desc, "qty": item3_qty, "rate": item3_rate}
    ]

    totals = calculate_invoice_totals(line_items, discount, tax)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Subtotal", f"${totals['subtotal']:,.2f}")
    m2.metric(f"Discount ({discount}%)", f"-${totals['discount_amount']:,.2f}")
    m3.metric(f"Tax ({tax}%)", f"+${totals['tax_amount']:,.2f}")
    m4.metric("Grand Total", f"${totals['grand_total']:,.2f}")

    if st.button("🚀 Generate Commercial Proposal & Invoice Package", type="primary", use_container_width=True):
        doc = generate_commercial_proposal(client_name, client_comp, proj_title, timeline, line_items, discount, tax)
        
        st.markdown("### 📑 Formatted Document Package Preview")
        st.markdown(doc["document_markdown"])
        
        st.download_button(
            "📥 Download Proposal Package (.md)",
            data=doc["document_markdown"],
            file_name=f"Proposal_{client_comp.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
