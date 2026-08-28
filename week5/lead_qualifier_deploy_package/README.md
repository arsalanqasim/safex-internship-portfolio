# 🛡️ SafeX Insurance & Finance Lead Qualifier

A transparent, rubric-based lead scoring tool for insurance/wealth-management
sales teams, built by **Ali Zaib** (SafeX Solutions AI/ML Internship, Group 54).

## Features
- **Five-factor weighted scoring** (0-100): policy value fit, coverage/budget
  fit, urgency/timeline, risk profile, and engagement channel quality.
- **Explainable, not a black box**: every score breaks down into its five
  contributing factors, plus qualitative flags a human reviewer can act on.
- **Single-lead qualification form** and **batch CSV scoring** (28-lead sample
  dataset included, or upload your own).
- **Tier-based prioritization**: Hot Lead, Qualified, Nurture, or Low Priority.

## Local Setup & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Community Cloud
1. Push this folder to its own GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Create a new app, pick the repo/branch, set main file path to `app.py`.
4. Deploy — Streamlit Cloud installs `requirements.txt` automatically.
