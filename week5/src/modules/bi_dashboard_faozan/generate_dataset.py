"""Deterministic synthetic dataset generator for the Chinar Cart BI dashboard.

Week 5 module owned by Muhammad Faozan Mujtaba.

Run from the week5 folder to regenerate the committed CSV:

    python src/modules/bi_dashboard_faozan/generate_dataset.py

Why a committed CSV instead of generating at runtime:

The scaffold generated its data inside the render path with an unseeded ``np.random``,
so every widget interaction reshuffled the whole dataset - revenue totals changed while
the user was reading them, and no insight could be checked twice. A dashboard whose
numbers move when you touch a filter cannot be demoed or tested. The data is therefore
generated once, deterministically, and read from disk.

The series is not pure noise. Four events are deliberately embedded so the analytics have
something real to find, and so the narrative generator and anomaly detector can be
evaluated against a known answer:

1. Eid promotion (days 96-99): large session and order lift, AOV falls as discounting bites.
2. Checkout outage (days 128-131): conversion rate collapses while traffic is unaffected.
   This is the anomaly the detector is expected to catch.
3. Paid-social scale-up (from day 110): spend climbs steadily with diminishing returns,
   so blended CAC worsens even as revenue grows.
4. Slow AOV erosion across the whole window, hidden underneath revenue growth.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

MODULE_DIR = Path(__file__).resolve().parent
DATA_PATH = MODULE_DIR / "data" / "chinar_cart_daily.csv"

COMPANY = "Chinar Cart"
DAYS = 180
SEED = 20260828

CHANNELS = ["Organic Search", "Paid Social", "Email", "Direct", "Marketplace"]

# Event windows, as day offsets from the start of the series.
EID_PROMO = range(96, 100)
CHECKOUT_OUTAGE = range(128, 132)
PAID_SOCIAL_SCALE_START = 110


def build_dataset(days: int = DAYS, seed: int = SEED, end: pd.Timestamp | None = None) -> pd.DataFrame:
    """Build the daily e-commerce series. Same seed always yields the same frame."""
    rng = np.random.default_rng(seed)
    end_date = pd.Timestamp("2026-08-28") if end is None else end
    dates = pd.date_range(end=end_date, periods=days, freq="D")
    t = np.arange(days)

    # Traffic: gentle organic growth, weekly seasonality, lognormal noise.
    # Friday and Saturday are the browsing peak for this market.
    weekday = dates.dayofweek.to_numpy()
    weekly = np.select(
        [weekday == 4, weekday == 5, weekday == 6, weekday < 4],
        [1.18, 1.22, 1.05, 0.95],
    )
    base_sessions = 2400 + 9.5 * t
    sessions = base_sessions * weekly * rng.lognormal(mean=0.0, sigma=0.06, size=days)

    # Conversion rate: slowly improving as the funnel is tuned.
    conversion = 0.0225 + 0.000035 * t + rng.normal(0, 0.0011, size=days)

    # Average order value erodes gradually - the trend the narrative should surface,
    # because revenue growth otherwise hides it.
    aov = 5850 - 3.1 * t + rng.normal(0, 95, size=days)

    marketing_spend = 42000 + 60 * t + rng.normal(0, 2600, size=days)

    # --- embedded events -------------------------------------------------------------
    for day in EID_PROMO:
        sessions[day] *= rng.uniform(2.5, 3.1)
        conversion[day] *= 1.35
        aov[day] *= 0.78          # heavy discounting
        marketing_spend[day] *= 2.4

    for day in CHECKOUT_OUTAGE:
        conversion[day] *= 0.28   # traffic unaffected, checkout broken
        aov[day] *= 0.97

    scale = np.clip((t - PAID_SOCIAL_SCALE_START) / 40.0, 0, None)
    marketing_spend = marketing_spend * (1 + 0.55 * scale)
    sessions = sessions * (1 + 0.12 * np.sqrt(scale))   # diminishing returns on spend

    sessions = np.maximum(sessions, 400).round().astype(int)
    conversion = np.clip(conversion, 0.002, None)
    aov = np.maximum(aov, 1200)

    orders = np.maximum((sessions * conversion).round(), 1).astype(int)
    revenue = (orders * aov).round(2)

    # Refunds lag demand slightly and rise after the promo.
    refund_rate = np.clip(0.031 + rng.normal(0, 0.006, size=days), 0.005, None)
    for day in EID_PROMO:
        for lag in range(1, 8):
            if day + lag < days:
                refund_rate[day + lag] *= 1.6
    refunds = (revenue * refund_rate).round(2)

    returning_share = np.clip(0.38 + 0.0007 * t + rng.normal(0, 0.03, size=days), 0.1, 0.85)
    returning_customers = (orders * returning_share).round().astype(int)
    new_customers = orders - returning_customers

    frame = pd.DataFrame(
        {
            "Date": dates,
            "Sessions": sessions,
            "Orders": orders,
            "Revenue": revenue,
            "Refunds": refunds,
            "Marketing_Spend": marketing_spend.round(2),
            "New_Customers": new_customers,
            "Returning_Customers": returning_customers,
        }
    )

    # Channel split of sessions. Paid Social grows its share during the scale-up.
    paid_share = 0.20 + 0.10 * np.clip(scale, 0, 1)
    shares = np.vstack(
        [
            0.34 - 0.05 * np.clip(scale, 0, 1),   # Organic Search
            paid_share,                            # Paid Social
            0.14 + rng.normal(0, 0.008, size=days),
            0.19 + rng.normal(0, 0.010, size=days),
            0.13 + rng.normal(0, 0.008, size=days),
        ]
    )
    shares = np.clip(shares, 0.02, None)
    shares = shares / shares.sum(axis=0)
    for i, channel in enumerate(CHANNELS):
        frame[f"Sessions_{channel.replace(' ', '_')}"] = (sessions * shares[i]).round().astype(int)

    return frame


def write_dataset(path: Path = DATA_PATH) -> Path:
    frame = build_dataset()
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, date_format="%Y-%m-%d")
    return path


if __name__ == "__main__":
    written = write_dataset()
    df = pd.read_csv(written)
    print(f"Wrote {len(df)} rows to {written}")
    print(f"Date range      : {df['Date'].min()} -> {df['Date'].max()}")
    print(f"Total revenue   : PKR {df['Revenue'].sum():,.0f}")
    print(f"Total orders    : {df['Orders'].sum():,}")
    print(f"Mean conversion : {(df['Orders'].sum() / df['Sessions'].sum()) * 100:.2f}%")
