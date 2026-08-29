# AI Business Intelligence & Forecasting Suite (Chinar Cart)

Week 5 AI Products Suite module for SafeX Solutions Group 54.

- **Developer**: Muhammad Faozan Mujtaba
- **Role**: Team Member (Group 54), NUST H-12
- **Module path**: `week5/src/modules/bi_dashboard_faozan/`

## The Client Problem

**Chinar Cart** is a fictional Pakistani direct-to-consumer e-commerce store selling
apparel and digital products, used as the client for this prototype.

Its founder exports a spreadsheet once a week, sees that revenue is up, and stops reading.
That single habit is the problem this module addresses. Revenue is the easiest number to
look at and the least informative on its own: it can rise while basket size shrinks,
acquisition cost climbs, and margin quietly erodes. Those changes only become visible when
a month closes badly.

On the shipped dataset this is exactly what is happening. Revenue is **up 23.6%** over the
last 30 days — and in the same window average order value is **down**, blended CAC is **up
10.3%**, and ROAS is **down 8.2%**. A dashboard that reports the first number and not the
other three is worse than no dashboard, because it is reassuring.

## What It Does

Five tabs, built around what a weekly review actually needs:

| Tab | Answers |
|---|---|
| Executive summary | What happened, what it means, what to look at |
| Performance | Revenue, conversion, order value and channel mix over time |
| Forecast | What next month looks like, and whether to trust the number |
| Anomalies | Which days were abnormal, grouped into episodes |
| Data & method | Where every figure comes from |

## Dataset

180 days of daily operating data for Chinar Cart, generated **deterministically** by
`generate_dataset.py` and committed as `data/chinar_cart_daily.csv`:

- Sessions, orders, revenue, refunds, marketing spend, new/returning customers
- Session counts split across five channels
- Derived: conversion rate, AOV, net revenue, refund rate, blended CAC, ROAS

Four events are deliberately embedded so the analytics can be checked against a known
answer rather than assumed correct:

| Event | Window | Effect |
|---|---|---|
| Eid promotion | 6–9 Jun | Sessions ~3x, AOV down on discounting |
| Post-promo refund wave | 7–16 Jun | Refund rate ~4x normal |
| **Checkout outage** | 8–11 Jul | Conversion −70% with traffic unaffected |
| Paid-social scale-up | from day 110 | Spend nearly doubles, CAC worsens |

*All data is synthetic. Chinar Cart is not a real company.*

## Results

### Forecast accuracy — measured on a holdout the model never saw

| Metric | Value |
|---|---|
| MAPE | **6.70%** |
| MAE | PKR 47,186 |
| R² (30-day holdout) | **+0.4474** |
| R² (in-sample) | +0.3796 |
| 95% interval coverage | 93% (nominal 95%) |

The in-sample figure is published beside the holdout one deliberately. Here it is *lower*,
which is the honest signature of a robust loss: the model refuses to chase the eight event
days, so it fits the training data slightly worse and generalises better.

### Anomaly detection — validated against the embedded events

The detector recovers **all four** embedded events and finds nothing spurious. 22 flagged
days collapse into 4 readable episodes:

| Episode | Detected | Ground truth |
|---|---|---|
| Refund rate +333%, 10 days from 7 Jun | ✅ | Post-promo refund wave |
| Conversion −70%, 4 days from 8 Jul | ✅ | Checkout outage |
| Revenue +210%, 4 days from 6 Jun | ✅ | Eid promotion |
| Conversion +38%, 4 days from 6 Jun | ✅ | Eid promotion |

## Three Findings Worth Reading

### 1. The forecast was worse than useless before it was fixed

The first working model scored **R² −2.40** on the holdout — worse than predicting the
mean — and under-predicted *every single* holdout day by an average of PKR 134,000.

The cause was not the algorithm. The training window contains a promotion at ~3x normal
revenue and an outage at ~⅓ normal conversion. Least squares has no way to know those
eight days were exceptional, so it bends the trend line to accommodate them — and because
the outage sits near the *end* of the training window, that bend drags the extrapolation
down.

Two fixes were measured:

| Model | MAPE | R² |
|---|---|---|
| Ridge (least squares) | 18.73% | **−2.40** |
| Ridge + explicit event indicators | 6.44% | +0.4895 |
| **Huber loss on log revenue** | **6.19%** | **+0.4903** |

Huber was chosen over event indicators despite near-identical scores, because it needs no
hand-maintained list of event dates and therefore still works when pointed at a client's
own data. Log target because revenue is `sessions × conversion × AOV` — multiplicative,
so logs make it additive and keep predictions positive.

*An earlier attempt to fix this with feature scaling alone made it worse (R² −2.40), which
is what pointed at the real cause.*

### 2. Mean and standard deviation cannot find the outage

Anomaly detection uses the **modified z-score** (median and MAD), not mean and standard
deviation. The promotion is extreme enough that it inflates both the mean and the standard
deviation, raising the threshold far enough that the checkout outage stops looking unusual.
Median and MAD are barely moved by it.

### 3. A stale incident is not news

Episodes are grouped and filtered against the reporting window. The checkout outage is
real, but it is seven weeks old; presenting it in an August summary would report a resolved
incident as current. The summary therefore leads with the in-window basket-size finding
instead, and the anomaly tab labels each episode as current or historical.

## Why the Narrative Is Not Generated by an LLM

The summary is composed deterministically from facts the engine computed, in the same
`LLM_PROVIDER=mock` convention the group used in Weeks 3 and 4.

The reason is not cost. A language model handed a table of numbers will write a fluent
paragraph whether or not the numbers support it, and a confident sentence about a trend
that is not in the data is exactly what a founder would act on. Every sentence here is
emitted by a rule that first checked a threshold against a real figure.

The prompt that *would* be sent to a hosted provider is rendered in the **Data & method**
tab even in offline mode, so the grounding rules can be reviewed without an API key.

## Files

```text
bi_dashboard_faozan/
  __init__.py
  engine.py             # KPIs, forecasting, anomaly detection, channel analysis
  narrative.py          # insight rules and executive summary composition
  ui.py                 # self-contained render_ui()
  generate_dataset.py   # deterministic dataset generator
  deploy_prep.py        # builds the standalone deployment package
  data/chinar_cart_daily.csv
  README.md
```

Tests: `week5/tests/test_bi_dashboard_faozan.py` (29 tests).

## How to Run

From `week5/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py        # sidebar -> AI Business Intelligence & Forecasting Suite
pytest tests/test_bi_dashboard_faozan.py
python src/modules/bi_dashboard_faozan/generate_dataset.py   # regenerate the CSV
```

Optional (unset by default; the dashboard runs fully offline):

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=...        # never commit this
```

## Deployment

`python src/modules/bi_dashboard_faozan/deploy_prep.py` builds a self-contained folder at
`week5/bi_dashboard_deploy_package/`, verified running standalone. The live URL is
registered in `week5/src/modules/registry.py` under `deployed_url`.
