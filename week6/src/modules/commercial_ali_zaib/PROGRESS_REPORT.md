# SafeX Solutions AI/ML Internship · Week 6 Progress Report

**Project Title:** Insurance Lead Scoring — Commercialization Hub
**Developer:** Ali Zaib
**Cohort & Group:** SafeX Solutions Remote Summer Internship 2026 · Group 54
**Submission Status:** Completed & Submitted

---

## 1. Executive Summary

Week 6 turned the Week 5 Insurance & Finance Lead Qualifier from a working
prototype into a sellable service offering. I built a three-tier pricing
structure for insurance agencies and brokers, an interactive ROI
calculator sales reps can use live on discovery calls, a personalized
cold outreach sequence generator, and an outreach pipeline tracker —
mirroring the structure the Group Leader built for his own module, scoped
to the insurance domain.

---

## 2. Commercial Positioning

- **Value Proposition:** A transparent, five-factor AI lead qualification
  service for insurance agencies and brokers that scores and prioritizes
  policy applicants instantly — cutting manual review time while keeping
  every decision explainable for underwriting.
- **Target Markets:** USA, UK, Canada.
- **Pricing:** Broker Starter ($350/mo), Agency Pro ($800/mo),
  Underwriting Enterprise ($1,600/mo) — see `README.md` for full tier
  breakdowns.

---

## 3. Technical Approach

### ROI Calculator
Models automated qualification as eliminating 80% of manual first-pass
review time. Net monthly savings = (hours saved × reviewer hourly rate)
minus the subscription fee; annual savings also nets out the one-time
setup fee. Verified against hand-calculated values in testing (200
leads/mo, $35/hr, 12 min/lead, Agency Pro tier → 32 hours saved, $320 net
monthly savings, 40% ROI — confirmed exact match in unit tests).

### Data Isolation Decision
Before writing any persistence code, I inspected the Group Leader's own
`commercial_arsalan/engine.py` and found it **overwrites the entire
shared outreach tracker file** on every save (not an append). To avoid
clobbering his tracked outreach data, I scoped this module's own outreach
pipeline persistence to its own data folder only. This was a deliberate
design decision made after reading the existing code, not an oversight.

---

## 4. Verification & Testing

- **8 new unit tests**, all passing: pricing tier configuration, ROI math
  correctness (including scaling behavior and unknown-tier fallback),
  outreach sequence generation (including empty-input handling), and a
  full outreach-data save/load/export roundtrip using `tmp_path` and
  `monkeypatch` so tests never touch real tracker files.
- **Full Week 6 suite:** 14/14 tests pass (my 8 + Arsalan's existing 6) —
  confirmed nothing else broke.
- **End-to-end UI testing** via Streamlit's `AppTest`: loaded the module,
  ran the ROI calculator, generated an outreach sequence, and submitted
  the pipeline form — zero runtime exceptions. Verified the pipeline save
  actually wrote to disk correctly (in the module's own scoped folder).
- **Standalone deployment package** verified independently — identical
  ROI output to the in-suite version.

---

## 5. Challenges & Resolutions

- **Challenge:** the original module stub only had a static pricing-tier
  dictionary with no ROI logic, outreach tooling, or persistence — a
  "commercial hub" needs to actually help make and track sales, not just
  list prices.
  **Resolution:** built out the full stack (ROI calculator, personalized
  outreach generator, pipeline tracker) matching the depth of the Group
  Leader's own reference implementation.
- **Challenge:** avoiding a silent data-corruption bug where two team
  members' modules could overwrite each other's shared outreach data.
  **Resolution:** read the existing code first, identified the
  overwrite-not-append behavior, and scoped my own persistence to avoid
  the conflict entirely — documented clearly in `engine.py` and `README.md`
  so future contributors understand why.
