# SafeX Solutions AI/ML Internship · Week 5 Progress Report

**Project Title:** Insurance & Finance Lead Qualifier
**Developer:** Ali Zaib
**Cohort & Group:** SafeX Solutions Remote Summer Internship 2026 · Group 54
**Submission Status:** Completed & Submitted

---

## 1. Executive Summary

Insurance and wealth-management sales teams receive a high volume of leads
of wildly varying quality — some ready to buy immediately, others years
away from a decision, and many with budget or risk profiles that make them
a poor fit for the requested coverage. During Week 5, I built an **Insurance
& Finance Lead Qualifier** that scores incoming leads on five weighted,
explainable factors and sorts them into clear sales/underwriting priority
tiers, so a sales rep or underwriter can immediately see which leads to
act on first — and why.

---

## 2. Problem Statement & Business Opportunity

- **The Problem:** Sales reps and underwriters manually review every
  incoming lead with no consistent prioritization, wasting time on
  low-quality or poor-fit leads while hot leads sit in the same queue.
- **Target Audience:** Insurance agencies and wealth-management firms
  processing policy applications across corporate, fleet, and individual
  product lines.
- **Value Proposition:** Instantly ranks a batch of leads by qualification
  score, flags specific risk/budget issues for manual review, and gives a
  transparent breakdown a sales rep can act on without needing to
  re-derive the reasoning themselves.

---

## 3. Technical Approach & Engineering

### Why a rubric, not a black-box ML model?
For an underwriting-adjacent use case, transparency matters more than
squeezing out marginal accuracy — a sales rep or underwriter needs to see
*why* a lead scored the way it did. A weighted, explainable rubric can show
its work; a black-box classifier can't. I deliberately chose this over
training a classifier on the sample data.

### Scoring architecture
```
Lead Input (policy type, coverage, timeline, claims history,
            age, occupation risk, budget, contact channel)
       |
       v
Five independent factor scorers:
  - Policy Value Fit        (0-25)
  - Coverage/Budget Fit     (0-20)  <- checked against an industry
                                        rule-of-thumb premium rate
  - Urgency/Timeline        (0-20)
  - Risk Profile            (0-20)  <- claims count, age band, occupation
  - Engagement/Channel      (0-15)
       |
       v
Total score (0-100) + Tier (Hot/Qualified/Nurture/Low Priority)
       |
       v
Qualitative flags (e.g. "budget below estimated premium",
                    "prior claims — flag for manual review")
```

### Key engineering decisions
1. **Coverage/budget sanity check:** rather than just scoring coverage
   amount in isolation, the engine checks whether the applicant's stated
   monthly budget could plausibly support their requested coverage, using
   an industry rule-of-thumb premium rate (~1.5%/year of coverage). A
   mismatch generates a specific, actionable flag instead of silently
   scoring the lead low.
2. **Batch scoring:** built alongside the single-lead form, since real
   sales workflows process lists of leads, not one at a time — a rep can
   upload a CSV and get a ranked, downloadable output immediately.
3. **Validation over silent failure:** every input is validated (known
   categories, positive coverage/budget, realistic age range) and raises a
   clear error rather than producing a nonsensical score.

---

## 4. Verification & Testing Results

- **Unit tests:** 11 pytest functions covering scoring correctness (hot vs.
  low-quality leads), tier boundaries, all five validation error paths, and
  batch-scoring behavior (sort order, missing-column handling). All 11 pass.
- **Sample dataset validation:** ran the full 40-lead synthetic sample
  batch through the scorer — produced a realistic tier distribution (16
  Hot, remainder split across Qualified/Nurture/Low Priority in one
  representative run) with no crashes
  or nonsensical scores.
- **End-to-end UI testing:** verified via Streamlit's `AppTest` — submitted
  the single-lead form and ran batch scoring against the live rendered UI,
  confirming no runtime exceptions and correct metric/score display.
- **Standalone deployment package:** verified independently via the same
  `AppTest` harness after packaging, confirming the standalone app produces
  identical results to the in-suite version.

---

## 5. Challenges & Resolutions

- **Challenge:** the original module stub scored leads with only two
  branches (policy type OR coverage amount), which couldn't meaningfully
  differentiate leads or explain its reasoning.
  **Resolution:** redesigned as a five-factor weighted rubric with
  per-factor point breakdowns, so every score is explainable and every
  contributing factor is visible in the UI.
- **Challenge:** a coverage amount alone doesn't indicate lead quality — a
  lead requesting high coverage with an unrealistically low budget isn't
  actually a good lead.
  **Resolution:** added the coverage/budget-fit check against an industry
  rule-of-thumb premium rate, which surfaces this mismatch as a specific,
  actionable flag rather than an opaque low score.
