# Week 4 Outreach Log - RAG Knowledge Assistant

Owner: Muhammad Faozan Mujtaba
Module: `week4/src/modules/knowledge_assistant_airline/`
Logged: 2026-08-24

This file is the committed mirror of `week4/data/outreach_tracker.xlsx`. The workbook
itself is listed in `week4/.gitignore`, so it stays local and this Markdown copy is what
survives in the pull request as review evidence.

Contacts are recorded **by role only**. No personal names, personal email addresses or
phone numbers are stored, per `AGENTS.md`.

## Target Outreach Records

| # | Company | Country | Website | Contact (role) | Channel | Date | Status |
|---|---|---|---|---|---|---|---|
| 1 | Airblue | Pakistan | airblue.com | Head of Customer Experience | Corporate contact form + LinkedIn | 2026-08-24 | Prepared, not yet sent |
| 2 | Serene Air | Pakistan | sereneair.com | Contact Centre / Ground Ops Manager | Corporate enquiry form | 2026-08-24 | Prepared, not yet sent |
| 3 | Bookme.pk | Pakistan | bookme.pk | Customer Support Operations Lead | LinkedIn + support enquiry form | 2026-08-24 | Prepared, not yet sent |

**Service offered:** RAG Knowledge Assistant (client-ready) - cited answers over a
company's own policy documents, with an explicit refusal path for out-of-scope questions.

### Why these three

All three run a customer contact operation where the same policy questions repeat daily
and a wrong answer has a direct financial cost - refunds, baggage claims, rescheduling
fees. That is the exact problem this module addresses, and each publishes the policy
documents that would form the knowledge base, so a demo can be built against their real
content without any data access.

## Status Note

These rows are logged as **prepared and awaiting send**, not as completed outreach. The
drafted messages are in the *Outreach Messages* sheet of the workbook. Before sending,
replace the `<deployed URL>` placeholder with the live Streamlit link, then update
`Response`, `Follow-up Date` and `Result/Status` in the workbook with what actually
happens. Follow-up date set for all three: **2026-08-28**.
