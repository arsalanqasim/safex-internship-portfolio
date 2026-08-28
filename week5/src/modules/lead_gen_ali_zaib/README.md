# Insurance & Finance Lead Qualifier

**Module:** `week5/src/modules/lead_gen_ali_zaib/`
**Developer:** Ali Zaib (AI/ML Intern)
**Part of:** SafeX Solutions — AI Products & Prototypes Suite, Week 5
**Domain:** Insurance & Wealth Management

## What this is

A transparent, rubric-based lead qualification tool for insurance/wealth-
management sales teams. Replaces a simple two-branch scoring rule with five
weighted, explainable factors that combine into a 0-100 score, a
sales/underwriting priority tier, and qualitative flags a human reviewer can
act on immediately.

## Why a rubric instead of a black-box ML model?

For an underwriting-adjacent use case, a sales rep or underwriter needs to
see *why* a lead scored the way it did — not just a number. A transparent,
weighted rubric can explain itself; a black-box classifier can't. Every
score breaks down into its five contributing factors in the UI.

## Scoring rubric (0-100)

| Factor | Points | What it measures |
|---|---|---|
| Policy Value Fit | 0-25 | Value/complexity of the requested product (Comprehensive Corporate > Fleet Commercial > Individual Basic) |
| Coverage/Budget Fit | 0-20 | Does the stated monthly budget realistically support the requested coverage, using a rough industry premium-rate assumption (~1.5%/year of coverage)? |
| Urgency/Timeline | 0-20 | How soon the applicant wants to decide |
| Risk Profile | 0-20 | Prior claims count, applicant age band, occupation risk — fewer/lower risk factors score higher |
| Engagement/Channel | 0-15 | Referrals and broker partners convert better than cold outreach |

**Tiers:** 80-100 Hot Lead · 60-79 Qualified · 40-59 Nurture · <40 Low Priority

## Files

| File | Purpose |
|---|---|
| `engine.py` | Scoring logic: single-lead scoring, batch scoring, validation, tier mapping. No Streamlit code. |
| `ui.py` | Three tabs: single-lead form, batch CSV scoring (with the sample dataset or an upload), and a "How Scoring Works" explainer. |
| `data/sample_leads.csv` | 28 synthetic sample leads with varied policy types, coverage, timelines, risk profiles, and channels. |
| `../../../tests/test_lead_gen_ali_zaib.py` | 11 unit tests covering scoring correctness, tier boundaries, validation errors, and batch scoring. |
| `../../deploy_prep_ali_zaib.py` | Packaging script that exports this module into a standalone, deployable app (mirrors Arsalan's `deploy_prep.py` pattern for his own module). |
| `../../lead_qualifier_deploy_package/` | Output of the above script — a self-contained Streamlit app ready to push to its own repo and deploy. |

## How to run

**Unit tests:**
```bash
cd week5
python -m pytest tests/test_lead_gen_ali_zaib.py -v
```

**Inside the full suite:**
```bash
cd week5
pip install -r requirements.txt
streamlit run src/app.py
```
Select **"Insurance & Finance Lead Qualifier"** from the sidebar.

**Standalone deployment package:**
```bash
cd week5
python deploy_prep_ali_zaib.py
cd lead_qualifier_deploy_package
pip install -r requirements.txt
streamlit run app.py
```
Then push `lead_qualifier_deploy_package/` to its own GitHub repo and deploy
on Streamlit Community Cloud (see that folder's own README.md for exact
steps) or Render.

## Known limitations

- The budget-fit check uses a **rough industry rule-of-thumb premium rate**
  (~1.5% of coverage annually), not a real underwriting quote — actual
  premiums vary by insurer, region, and applicant specifics.
- This is a **lead prioritization tool**, not a final underwriting decision
  — every lead should still go through proper underwriting review
  regardless of score.
- The rubric weights reflect reasonable sales/underwriting judgment for this
  exercise, not weights fitted to real historical conversion data — a
  production version would validate/tune these against actual close rates.
- The sample dataset (28 leads) is synthetic, generated to have realistic
  variation across policy types, coverage amounts, and risk factors — not
  real applicant data.
