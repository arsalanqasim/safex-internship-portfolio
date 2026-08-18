"""Proposal & Invoice Generator Engine (Malik Sudais - Week 3)."""

from typing import Any, Dict, List
from datetime import datetime


def calculate_invoice_totals(line_items: List[Dict[str, Any]], discount_pct: float = 0.0, tax_pct: float = 5.0) -> Dict[str, Any]:
    """Calculate subtotal, discount, tax, and final invoice grand total."""
    subtotal = sum(item.get("qty", 1) * item.get("rate", 0.0) for item in line_items)
    discount_amount = (subtotal * discount_pct) / 100.0
    taxable = max(0.0, subtotal - discount_amount)
    tax_amount = (taxable * tax_pct) / 100.0
    grand_total = taxable + tax_amount
    
    return {
        "subtotal": round(subtotal, 2),
        "discount_pct": discount_pct,
        "discount_amount": round(discount_amount, 2),
        "tax_pct": tax_pct,
        "tax_amount": round(tax_amount, 2),
        "grand_total": round(grand_total, 2)
    }


def generate_commercial_proposal(
    client_name: str,
    client_company: str,
    project_title: str,
    timeline_weeks: int,
    line_items: List[Dict[str, Any]],
    discount_pct: float = 0.0,
    tax_pct: float = 5.0
) -> Dict[str, Any]:
    """Generate structured commercial proposal and invoice document package."""
    totals = calculate_invoice_totals(line_items, discount_pct, tax_pct)
    inv_number = f"INV-2026-{datetime.now().strftime('%m%d%H%M')}"
    date_str = datetime.now().strftime("%B %d, %Y")
    
    items_table = "| Description | Qty | Unit Rate ($) | Amount ($) |\n| :--- | :--- | :--- | :--- |\n"
    for it in line_items:
        amt = it.get("qty", 1) * it.get("rate", 0.0)
        items_table += f"| {it.get('desc', 'Item')} | {it.get('qty', 1)} | ${it.get('rate', 0.0):,.2f} | ${amt:,.2f} |\n"
        
    doc_markdown = f"""# Commercial Proposal & Project Invoice

**Invoice Number:** `{inv_number}`  
**Issue Date:** {date_str}  
**Prepared For:** {client_name} ({client_company})  
**Project Title:** {project_title}  
**Estimated Timeline:** {timeline_weeks} Weeks  

---

## 1. Executive Summary & Scope of Work
SafeX Solutions is pleased to submit this commercial proposal for **{project_title}** tailored for **{client_company}**. 
Our engineering team will design, deploy, and calibrate a high-reliability automated workflow addressing your operational requirements.

## 2. Itemized Deliverables & Commercial Investment

{items_table}

| Summary Metric | Value |
| :--- | :--- |
| **Subtotal** | **${totals['subtotal']:,.2f}** |
| **Discount ({discount_pct}%)** | -${totals['discount_amount']:,.2f} |
| **Sales Tax ({tax_pct}%)** | +${totals['tax_amount']:,.2f} |
| **Grand Total** | **${totals['grand_total']:,.2f}** |

---

## 3. Commercial Terms & Payment Milestones
1. **50% Advance Deposit** upon contract signing to initiate technical onboarding.
2. **50% Final Settlement** upon user acceptance testing (UAT) and production deployment.
3. Payment methods: Direct Wire Transfer, ACH, or Corporate Credit Card.

---
*Authorized by SafeX Solutions Cohort 2026 · Group 54*
"""

    return {
        "invoice_number": inv_number,
        "date": date_str,
        "client_name": client_name,
        "client_company": client_company,
        "project_title": project_title,
        "totals": totals,
        "document_markdown": doc_markdown
    }
