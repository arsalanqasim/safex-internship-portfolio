"""Executive narrative generation for the Chinar Cart BI dashboard.

Week 5 module owned by Muhammad Faozan Mujtaba.

This is the "AI auto-generated weekly insights" half of the assignment. It runs offline by
default, in the same ``LLM_PROVIDER=mock`` convention the group used in Weeks 3 and 4: the
narrative is composed deterministically from facts the engine actually computed, and a
hosted model is used only when one is configured.

The reason for building it this way is not cost. A language model handed a table of
numbers will write a fluent paragraph whether or not the numbers support it, and the
failure mode - a confident sentence about a trend that is not in the data - is exactly
what a founder would act on. Every sentence produced here is emitted by a rule that first
checked a threshold against a real figure, so the narrative cannot claim something the
data does not show.

The scaffold this replaces always reported "strong upward momentum" when revenue rose,
which on this dataset is true and useless: revenue rose while margin quietly eroded and
acquisition cost climbed. The rules below are written to surface that kind of divergence
rather than restate the headline.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .engine import AnomalyEpisode, ForecastResult, Kpi

# Thresholds below which a movement is treated as noise rather than a finding. Daily
# e-commerce metrics move a few percent on their own; without these the narrative reports
# a "decline" every time a number ticks down.
MATERIAL_CHANGE_PCT = 5.0
STRONG_CHANGE_PCT = 15.0
MARGIN_WATCH_PCT = 2.0


@dataclass
class Insight:
    """One statement, with the evidence that produced it."""

    severity: str  # "positive" | "watch" | "risk"
    headline: str
    detail: str
    evidence: str

    def as_markdown(self) -> str:
        icon = {"positive": "🟢", "watch": "🟡", "risk": "🔴"}.get(self.severity, "•")
        return f"{icon} **{self.headline}** {self.detail}  \n<small>{self.evidence}</small>"


def _find(kpis: list["Kpi"], label: str) -> "Kpi | None":
    return next((k for k in kpis if k.label == label), None)


def build_insights(
    kpis: list["Kpi"],
    forecast: "ForecastResult",
    anomalies: dict[str, Any],
    channels: Any,
    window_days: int = 30,
) -> list[Insight]:
    """Derive the findings worth putting in front of a founder, most important first."""
    insights: list[Insight] = []

    revenue = _find(kpis, "Revenue")
    orders = _find(kpis, "Orders")
    sessions = _find(kpis, "Sessions")
    aov = _find(kpis, "Average Order Value")
    cac = _find(kpis, "Blended CAC")
    roas = _find(kpis, "ROAS")
    conversion = _find(kpis, "Conversion Rate")
    refund = _find(kpis, "Refund Rate")

    # --- 1. Headline movement -------------------------------------------------------
    if revenue and abs(revenue.delta_pct) >= MATERIAL_CHANGE_PCT:
        direction = "grew" if revenue.delta_pct > 0 else "fell"
        insights.append(
            Insight(
                severity="positive" if revenue.delta_pct > 0 else "risk",
                headline=f"Revenue {direction} {abs(revenue.delta_pct):.1f}%",
                detail=(
                    f"against the previous {window_days} days, to {revenue.formatted()}."
                ),
                evidence=(
                    f"Previous window {revenue.previous:,.0f}; comparison is like-for-like "
                    f"over two {window_days}-day windows."
                ),
            )
        )

    # --- 2. Growth quality: is revenue growing for a good reason? --------------------
    # This is the check the scaffold could not make. Revenue rising on volume alone while
    # order value falls is a different business situation from revenue rising on both.
    if revenue and aov and revenue.delta_pct > MATERIAL_CHANGE_PCT and aov.delta_pct < -MARGIN_WATCH_PCT:
        insights.append(
            Insight(
                severity="watch",
                headline="Growth is coming from volume, not basket size",
                detail=(
                    f"Orders are up {orders.delta_pct:+.1f}% but average order value is "
                    f"down {abs(aov.delta_pct):.1f}% to {aov.formatted()}. "
                    "Revenue growth is masking a falling basket."
                ),
                evidence=(
                    "Flagged because revenue rose more than "
                    f"{MATERIAL_CHANGE_PCT:.0f}% while AOV fell more than {MARGIN_WATCH_PCT:.0f}%."
                ),
            )
        )

    # --- 3. Acquisition efficiency ---------------------------------------------------
    if cac and cac.delta_pct > MATERIAL_CHANGE_PCT:
        roas_note = f" ROAS moved to {roas.formatted()} ({roas.delta_pct:+.1f}%)." if roas else ""
        insights.append(
            Insight(
                severity="risk" if cac.delta_pct > STRONG_CHANGE_PCT else "watch",
                headline=f"Customer acquisition cost rose {cac.delta_pct:.1f}%",
                detail=f"Blended CAC is now {cac.formatted()} per new customer.{roas_note}",
                evidence="Blended CAC = total marketing spend / new customers acquired in the window.",
            )
        )

    # --- 4. Funnel ------------------------------------------------------------------
    if conversion and sessions:
        if conversion.delta_pct >= MATERIAL_CHANGE_PCT:
            insights.append(
                Insight(
                    severity="positive",
                    headline=f"Conversion rate improved {conversion.delta_pct:.1f}%",
                    detail=(
                        f"now {conversion.formatted()}, on {sessions.value:,.0f} sessions "
                        f"({sessions.delta_pct:+.1f}%)."
                    ),
                    evidence="Conversion rate = orders / sessions across the window.",
                )
            )
        elif conversion.delta_pct <= -MATERIAL_CHANGE_PCT:
            insights.append(
                Insight(
                    severity="risk",
                    headline=f"Conversion rate dropped {abs(conversion.delta_pct):.1f}%",
                    detail=(
                        f"to {conversion.formatted()} while sessions moved "
                        f"{sessions.delta_pct:+.1f}%. Traffic is arriving but converting less."
                    ),
                    evidence="Conversion rate = orders / sessions across the window.",
                )
            )

    # --- 5. Refunds -----------------------------------------------------------------
    if refund and refund.delta_pct >= STRONG_CHANGE_PCT:
        insights.append(
            Insight(
                severity="watch",
                headline=f"Refund rate up {refund.delta_pct:.1f}%",
                detail=f"now {refund.formatted()} of gross revenue.",
                evidence="Refund rate = refunds / gross revenue in the window.",
            )
        )

    # --- 6. Operational anomalies ----------------------------------------------------
    # Only episodes that overlap the reporting window belong in this week's summary. The
    # dataset also contains a checkout outage from seven weeks earlier; reporting it here
    # would present a resolved, stale incident as if it were current news. Older episodes
    # stay available in the anomaly view, which is explicitly historical.
    episodes: list["AnomalyEpisode"] = anomalies.get("episodes", [])
    window_start = anomalies.get("window_start")
    if window_start is not None:
        episodes = [e for e in episodes if e.end >= window_start]

    for episode in episodes[:3]:
        severity = "risk" if episode.change_pct < 0 else "watch"
        insights.append(
            Insight(
                severity=severity,
                headline="Unusual activity detected",
                detail=episode.describe(),
                evidence=(
                    f"Modified z-score {episode.peak_z:+.1f} against a threshold of "
                    f"{anomalies.get('threshold', 3.5)}, using median and MAD."
                ),
            )
        )

    # --- 7. Channel mix --------------------------------------------------------------
    if channels is not None and len(channels):
        top = channels.iloc[0]
        movers = channels.sort_values("Change_Pct", ascending=False)
        best, worst = movers.iloc[0], movers.iloc[-1]
        detail = (
            f"{top['Channel']} carries {top['Share_Pct']:.0f}% of sessions. "
            f"Fastest growing is {best['Channel']} ({best['Change_Pct']:+.1f}%); "
            f"weakest is {worst['Channel']} ({worst['Change_Pct']:+.1f}%)."
        )
        insights.append(
            Insight(
                severity="watch" if worst["Change_Pct"] < -MATERIAL_CHANGE_PCT else "positive",
                headline="Channel mix",
                detail=detail,
                evidence=f"Session counts, latest {window_days} days vs the {window_days} before.",
            )
        )

    # --- 8. Forecast -----------------------------------------------------------------
    confidence = "usable" if forecast.mape < 10 else "indicative only"
    insights.append(
        Insight(
            severity="positive",
            headline=f"Next {forecast.forecast_days} days projected at "
            f"PKR {forecast.forecast_total:,.0f}",
            detail=(
                f"Underlying trend is {forecast.trend_per_day:+.2f}% per day compounding. "
                f"Forecast is {confidence}."
            ),
            evidence=(
                f"Backtested on a {forecast.holdout_days}-day holdout the model never saw: "
                f"MAPE {forecast.mape:.1f}%, R-squared {forecast.r2:+.2f}."
            ),
        )
    )

    return insights


def compose_summary(
    insights: list[Insight],
    kpis: list["Kpi"],
    forecast: "ForecastResult",
    company: str,
    window_days: int = 30,
) -> str:
    """Write the paragraph a founder reads first, from the insights already derived."""
    revenue = _find(kpis, "Revenue")
    orders = _find(kpis, "Orders")

    risks = [i for i in insights if i.severity == "risk"]
    watches = [i for i in insights if i.severity == "watch"]

    if revenue is None:
        return f"Not enough data to summarise the last {window_days} days for {company}."

    direction = "up" if revenue.delta_pct >= 0 else "down"
    opening = (
        f"Over the last {window_days} days {company} took **{revenue.formatted()}** across "
        f"**{orders.value:,.0f} orders**, {direction} **{abs(revenue.delta_pct):.1f}%** on the "
        f"previous {window_days} days."
    )

    # Lead the caveat with the most actionable finding. Lowercasing the source headline
    # was tried first and mangled month abbreviations into "8 jul", so the clause is
    # assembled from the parts instead.
    lead = risks[0] if risks else (watches[0] if watches else None)
    if lead is not None:
        middle = f" The headline is not the whole picture. {lead.headline}: {lead.detail.rstrip('.')}."
    else:
        middle = " No metric moved far enough this period to require attention."

    closing = (
        f" The next {forecast.forecast_days} days are projected at "
        f"**PKR {forecast.forecast_total:,.0f}**, from a model backtested at "
        f"{forecast.mape:.1f}% mean absolute percentage error on unseen data."
    )

    return opening + middle + closing


def provider() -> str:
    """Active generation provider. ``mock`` means fully offline, which is the default."""
    return os.getenv("LLM_PROVIDER", "mock").strip().lower()


def build_llm_prompt(company: str, kpis: list["Kpi"], insights: list[Insight]) -> str:
    """Render the prompt that would be sent to a hosted model.

    Surfaced in the UI even in offline mode so the grounding rules can be reviewed. The
    rules mirror the ones used in the Week 4 module: the model may only restate figures it
    was given, and may not introduce a trend that is not in the supplied facts.
    """
    kpi_lines = "\n".join(
        f"- {k.label}: {k.formatted()} ({k.delta_pct:+.1f}% vs previous window)" for k in kpis
    )
    finding_lines = "\n".join(f"- [{i.severity}] {i.headline} {i.detail}" for i in insights)
    return f"""You are writing the weekly executive summary for {company}.

Rules:
1. Use only the figures and findings below. Introduce no metric that is not listed.
2. Never describe a trend that is not evidenced by a figure you were given.
3. Quote numbers exactly as supplied. Do not round, convert or infer.
4. Lead with the finding that most changes what the business should do, which is not
   always the largest number.
5. Maximum 150 words. No greetings, no closing pleasantries.

Metrics for the period:
{kpi_lines}

Findings already derived from the data:
{finding_lines}

Write the summary now."""
