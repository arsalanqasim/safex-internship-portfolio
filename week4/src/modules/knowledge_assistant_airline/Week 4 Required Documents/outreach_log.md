# Week 4 Outreach Log - RAG Knowledge Assistant

Owner: Muhammad Faozan Mujtaba
Module: `week4/src/modules/knowledge_assistant_airline/`
Logged: 2026-08-24

This file is the committed mirror of `week4/data/outreach_tracker.xlsx`. The workbook
itself is listed in `week4/.gitignore`, so it stays local and this Markdown copy is what
survives in the pull request as review evidence.

Contacts are recorded **by role only**, routed through each company's **published corporate**
contact channel. No personal names, personal email addresses or phone numbers are stored,
per `AGENTS.md`.

## Target Outreach Records

| # | Company | Country | Website | Contact (role) | Channel | Date | Status |
|---|---|---|---|---|---|---|---|
| 1 | Airblue | Pakistan | airblue.com | Head of Customer Experience | Corporate contact form + LinkedIn | 2026-08-24 | Ready to send |
| 2 | Fly Jinnah | Pakistan | flyjinnah.com | Customer Experience / Contact Centre Manager | Corporate contact page + published support address | 2026-08-25 | Ready to send |
| 3 | Bookme.pk | Pakistan | bookme.pk | Customer Support Operations Lead | LinkedIn + support enquiry form | 2026-08-24 | Ready to send |

**Service offered:** RAG Knowledge Assistant (client-ready) - cited answers over a
company's own policy documents, with an explicit refusal path for out-of-scope questions.

### Why these three

All three run a customer contact operation where the same policy questions repeat daily
and a wrong answer has a direct financial cost - refunds, baggage claims, rescheduling
fees. That is the exact problem this module addresses, and each publishes the policy
documents that would form the knowledge base, so a demo can be built against their real
content without any data access.

### Target changed 2026-08-26: Serene Air replaced with Fly Jinnah

Serene Air was the original second target. Checking its current status before sending showed
its **flight operations have been suspended since 2025-10-02**, pending compliance with safety
and regulatory conditions. An airline that is not flying is not buying a contact-centre tool,
so the slot was reassigned to **Fly Jinnah**, an operating carrier on an expanding domestic
network - the case where contact-centre query volume grows faster than headcount, which is
exactly the pressure this module relieves.

## Status Note

Updated **2026-08-25**: all three messages are now **finalised and ready to send**. The live
demo link is embedded in each one:

https://indus-air-knowledge-assistant-msjvdeswzeu3drqeasmytn.streamlit.app

They are **not yet sent**. The full text of each message is in `outreach_messages.md` in this
folder, and in the *Outreach Messages* sheet of the workbook.

After sending each message, record what actually happened - set `Date Sent` in the
*Outreach Messages* sheet, and update `Response`, `Follow-up Date` and `Result/Status` in
the *Outreach Log* sheet. Do not record a response before one is received; this tracker is
submission evidence. Follow-up date set for all three: **2026-08-28**.
