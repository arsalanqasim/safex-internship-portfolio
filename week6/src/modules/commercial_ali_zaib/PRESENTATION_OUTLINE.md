# SafeX Week 6 · Presentation & Explanation Video Outline

**Presenter:** Ali Zaib (Group Member, Group 54)
**Target Duration:** 5–10 Minutes (HD Video, Face Visible)
**Evaluation Standard:** HEC / University Academic Evaluation & SafeX Portfolio

---

## Slide Structure & Script Outline

### Slide 1: Title & Introduction (0:00 - 0:45)
- **Title:** Insurance Lead Scoring — Commercialization Hub
- **Subtitle:** Turning a Working Prototype into a Sellable Service
- **Presenter:** Ali Zaib · BS Artificial Intelligence, COMSATS University Islamabad
- **Context:** SafeX Solutions AI/ML Internship 2026 (Group 54), Week 6

### Slide 2: From Prototype to Product (0:45 - 2:00)
- **Week 5 recap:** built a five-factor transparent lead scoring engine
  for insurance/wealth management.
- **Week 6 goal:** package it as an actual sellable service — pricing,
  ROI justification, outreach materials, and a sales pipeline.
- **Target Markets:** USA, UK, Canada insurance agencies and brokers.

### Slide 3: Commercial Package & Pricing (2:00 - 3:30)
- **Three tiers:** Broker Starter ($350/mo), Agency Pro ($800/mo),
  Underwriting Enterprise ($1,600/mo).
- **Live demo:** show the ROI calculator — plug in realistic numbers
  (200 leads/month, $35/hr reviewer rate, 12 min/lead) and show the
  $320/month net savings and 40% ROI it calculates live.

### Slide 4: Sales Tooling Demo (3:30 - 6:00)
*Demo walkthrough:*
1. Generate a personalized 3-step cold outreach sequence for a named
   prospect agency.
2. Add an entry to the outreach pipeline tracker, show the saved data.
3. Show the LinkedIn post and video reel script in the Social Media tab.

### Slide 5: An Engineering Decision Worth Highlighting (6:00 - 7:30)
- **The problem:** the Group Leader's own commercial module writes to a
  shared outreach tracker file — but overwrites it completely on every
  save, not appending.
- **The risk:** if my module wrote to the same shared file, it would
  silently destroy his tracked outreach data.
- **The fix:** I read his code first, identified this, and scoped my
  module's persistence to its own folder — a real example of checking
  existing code before adding new features in a shared codebase.

### Slide 6: Verification & Next Steps (7:30 - 8:30)
- **Testing:** 8 new unit tests, all passing; full Week 6 suite (14
  tests, mine + the leader's) confirmed nothing broke.
- **Deployed:** standalone version live on Streamlit Community Cloud.
- **Next steps:** real broker outreach using the generated sequences,
  and validating the 80% automation-deflection ROI assumption against
  actual agency review-time data.
