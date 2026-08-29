# SafeX Week 5 · Presentation & Explanation Video Outline

**Presenter:** Ali Zaib (Group Member, Group 54)
**Target Duration:** 5–10 Minutes (HD Video, Face Visible)
**Evaluation Standard:** HEC / University Academic Evaluation & SafeX Portfolio

---

## Slide Structure & Script Outline

### Slide 1: Title & Introduction (0:00 - 0:45)
- **Title:** Insurance & Finance Lead Qualifier
- **Subtitle:** Transparent, Rubric-Based Lead Scoring for Insurance & Wealth Management
- **Presenter:** Ali Zaib · BS Artificial Intelligence, COMSATS University Islamabad
- **Context:** SafeX Solutions AI/ML Internship 2026 (Group 54)

### Slide 2: Business Problem & Opportunity (0:45 - 2:00)
- **Problem:** Sales teams and underwriters manually review every incoming
  lead with no consistent prioritization — hot leads and poor-fit leads sit
  in the same queue.
- **Pain Points:** Wasted rep time on low-quality leads, inconsistent
  qualification standards across reps, no visibility into *why* a lead was
  deprioritized.
- **Target Audience:** Insurance agencies and wealth-management firms
  processing corporate, fleet, and individual policy applications.

### Slide 3: Technical Approach & Design Decisions (2:00 - 4:00)
- **Why a rubric, not a black-box model?** Transparency matters for an
  underwriting-adjacent decision — a five-factor weighted score can explain
  itself; a black-box classifier can't.
- **Five scoring factors:** Policy Value Fit, Coverage/Budget Fit,
  Urgency/Timeline, Risk Profile, Engagement/Channel — each visible in the
  breakdown, not hidden inside a single number.
- **Budget sanity check:** compares stated budget against an
  industry rule-of-thumb premium rate, flagging mismatches instead of
  silently scoring low.
- **Batch scoring:** built for real sales workflows — score a whole CSV of
  leads at once, ranked and downloadable.

### Slide 4: Live Working Demo (4:00 - 7:00)
*Demo walkthrough:*
1. Submit a strong lead (Comprehensive Corporate, high coverage, immediate
   timeline, clean risk profile, referral channel) — show it scoring 90+ as
   a Hot Lead with a clean score breakdown.
2. Submit a poor-fit lead (low budget vs. high coverage, prior claims,
   exploratory timeline) — show the specific flags it raises (budget
   mismatch, prior claims for manual review).
3. Switch to the Batch Scoring tab, run the 40-lead sample dataset, show
   the tier distribution chart and ranked table.
4. Download the scored CSV.
5. Briefly show the "How Scoring Works" tab explaining the rubric to a
   non-technical viewer.

### Slide 5: Verification, Impact, and Next Steps (7:00 - 8:30)
- **Testing:** 11 unit tests (all passing) covering scoring correctness,
  tier boundaries, and validation; end-to-end UI testing with zero runtime
  errors.
- **Key design lesson:** coverage amount alone doesn't indicate lead
  quality — pairing it with a budget-fit check surfaced a whole class of
  leads (high coverage, unrealistic budget) that a simpler model would
  have scored incorrectly.
- **Next steps (Week 6):** package this as a sellable underwriting
  qualifier service — pricing tiers, broker pitch materials, and outreach
  to target agencies.
