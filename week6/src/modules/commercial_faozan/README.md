# BI Dashboard Monthly Reporting Service

Week 6 Commercialization & Client Acquisition module for SafeX Solutions Group 54.

- **Developer**: Muhammad Faozan Mujtaba
- **Role**: Team Member (Group 54), NUST H-12
- **Module path**: `week6/src/modules/commercial_faozan/`
- **Monetizes**: `week5/src/modules/bi_dashboard_faozan/`
- **Target markets**: USA, Canada, Europe

## What Is Being Sold

Executive BI analytics and AI narrative reporting, delivered to e-commerce operators as a
monthly retainer. The client gets the Week 5 product as a service: a monthly or weekly KPI
pack against a like-for-like prior window, a backtested revenue forecast, anomaly alerting,
and a written summary grounded in their own figures.

## Two Things That Make This More Than a Pricing Deck

### 1. Prices carry a cost basis

Each tier declares the delivery hours it consumes, so gross margin, effective hourly rate
and break-even hours are **computed, not asserted**.

| Tier | Monthly | Setup | Hours/mo | Gross margin | Effective rate | Break-even |
|---|---|---|---|---|---|---|
| Starter Reporting | $249 | $399 | 3.0 | 73.5% | $83.00/hr | 13.2 hrs |
| Growth Analytics | $599 | $899 | 7.5 | 75.5% | $79.87/hr | 32.6 hrs |
| Enterprise BI | $1,199 | $1,899 | 16.0 | 75.0% | $74.94/hr | 65.9 hrs |

*At $18/hr internal delivery cost and $12/mo infrastructure per client.*

The number that actually decides profitability is not the planned delivery time but the
time spent once a client starts asking for extras. The app exposes an overrun slider, so
you can find where each tier stops being viable — Starter survives to about 13 hours a
month and loses money past it. That is a commercial risk worth seeing before signing, not
after.

### 2. The ROI claim is measured, not an industry average

Most pitch decks assert something like "increase revenue 40%". This one uses a number
produced by the Week 5 module's own anomaly detection on the Chinar Cart dataset:

| | |
|---|---|
| Incident | Checkout failure, 8–11 Jul 2026 |
| Conversion, normal → outage | 2.71% → 0.77% |
| Orders received vs expected | 131 vs 463 |
| **Orders lost** | **332** |
| **Revenue lost** | **PKR 1,811,177** over 4 days |
| Recoverable if caught on day 1 | PKR 1,358,383 |

Traffic was unaffected throughout — which is exactly why the incident is invisible on a
revenue chart and why it ran four days. That works out at **2.16% of monthly revenue per
undetected day**, and that is the figure scaled to each prospect.

**The two benefits are kept separate and never blended.** Reporting time saved is the safe
part of the claim (hours × rate). Faster incident detection is larger but rests on an
assumption, so the calculator always shows the reporting-only figure beside it. At the
default inputs the Growth tier is actually **$59/month short on reporting time alone** —
the app says so plainly rather than hiding it inside a total, because a client who
discovers that themselves stops trusting the rest of the numbers.

## Outreach Pipeline

16 researched prospects across the three target markets (Europe 8, USA 4, Canada 4), all
DTC e-commerce or marketplace operators selected because the product's core pitch — revenue
rising while basket size falls, or a silent conversion failure — is specifically relevant
to them. Each row carries the reason it was chosen.

**Every row is logged as `Researched - not contacted`, and funnel metrics are computed from
the file rather than asserted.** An untouched pipeline honestly reports zero contacted and
a zero reply rate. Recording a reply before one arrives would make the tracker worthless as
submission evidence, which is the whole point of keeping it.

Contacts are held **by role only** — no personal names, personal emails or phone numbers,
per `AGENTS.md`. A test enforces this.

The pipeline is editable in the app and exports to Excel for the weekly submission.

## Also Included

- **Three-step cold outreach sequence generator.** A specific observation about the
  prospect is a *required* argument, not optional: a sequence that cannot name something
  particular about the company is a template, and templates are what make cold outreach
  worthless. Every sequence states the demo runs on synthetic data.
- **One-page proposal generator**, rendered to Markdown and downloadable, carrying the
  commercials, the ROI table, and the provenance of the incident figure.

## Files

```text
commercial_faozan/
  __init__.py
  engine.py       # pricing economics, client ROI, outreach sequences, pipeline, proposal
  ui.py           # self-contained render_ui()
  README.md
  data/outreach_pipeline.json
```

Tests: `week6/tests/test_commercial_faozan.py` (27 tests).

## How to Run

From `week6/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py        # sidebar -> BI Dashboard Monthly Reporting Service
pytest tests/test_commercial_faozan.py
```
