# Insurance Lead Scoring — Commercialization Hub

**Module:** `week6/src/modules/commercial_ali_zaib/`
**Developer:** Ali Zaib (AI/ML Intern)
**Part of:** SafeX Solutions — Sell Your Skills Commercialization Suite, Week 6
**Target Markets:** USA, UK, Canada

## What this is

Turns the Week 5 Insurance & Finance Lead Qualifier into a sellable
service offering for insurance agencies and brokers: tiered pricing, an
interactive ROI calculator, a personalized cold outreach generator, and
an outreach pipeline tracker — mirroring the structure of the Group
Leader's own `commercial_arsalan` module, scoped to the insurance domain.

## Data isolation note (important)

This module writes its outreach pipeline to its **own** data folder
(`commercial_ali_zaib/data/`) only — never to the shared
`week6/src/data/outreach_tracker.xlsx`. The Group Leader's own engine
**overwrites the entire shared file** on every save (not append), so
writing to it here would risk clobbering his tracked outreach data. This
was a deliberate design choice after inspecting his `commercial_arsalan/engine.py`.

## Files

| File | Purpose |
|---|---|
| `engine.py` | Pricing tiers, ROI calculator, cold outreach sequence generator, outreach pipeline persistence (JSON + Excel). No Streamlit code. |
| `ui.py` | Four tabs: Service Offering & Pricing (with ROI calculator), Cold Outreach Generator, Outreach Pipeline, Social Media Marketing. |
| `../../../tests/test_commercial_ali_zaib.py` | 8 unit tests covering pricing config, ROI math, outreach generation, and data persistence (using `tmp_path`/`monkeypatch` so tests never touch real tracker files). |
| `../../deploy_prep_ali_zaib.py` | Packaging script exporting this module into a standalone deployable app, mirroring Arsalan's own `deploy_prep.py` pattern. |
| `../../insurance_commercial_deploy_package/` | Output of the above script — self-contained, tested, ready to deploy. |

## Pricing tiers

| Tier | Monthly | Setup | Limit |
|---|---|---|---|
| Broker Starter | $350 | $199 | Up to 200 leads/mo |
| Agency Pro | $800 | $399 | Up to 1,000 leads/mo |
| Underwriting Enterprise | $1,600 | $799 | Unlimited |

## ROI model

Assumes automated qualification eliminates **80%** of manual first-pass
review time (reviewers still spot-check flagged/hot leads). Net savings =
automated labor cost savings minus the subscription fee; annual savings
also subtracts the one-time setup fee.

## How to run

**Unit tests:**
```bash
cd week6
python -m pytest tests/test_commercial_ali_zaib.py -v
```

**Inside the full suite:**
```bash
cd week6
pip install -r requirements.txt
streamlit run src/app.py
```
Select **"Insurance Lead Scoring Commercial Service"** from the sidebar.

**Standalone deployment package:**
```bash
cd week6
python deploy_prep_ali_zaib.py
cd insurance_commercial_deploy_package
pip install -r requirements.txt
streamlit run app.py
```
Then push to its own GitHub repo and deploy on Streamlit Community Cloud
(see that folder's own README.md).

## Known limitations

- The ROI model's 80% automation-deflection assumption is a reasonable
  estimate for this exercise, not validated against real agency data.
- The outreach pipeline is a local demo tracker for this module only —
  real production outreach tracking would need a shared CRM, not a
  per-module local file.
- Pricing tiers reflect reasonable market judgment for this exercise, not
  a formal competitive pricing analysis.
