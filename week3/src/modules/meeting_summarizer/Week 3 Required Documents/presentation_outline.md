# Presentation Outline — AI Meeting Summarizer & Action-Item Extractor

**Member:** Muhammad Faozan Mujtaba · **Target company:** Meridian Softworks
**Suggested length:** 10 slides, 8–10 minutes

---

### Slide 1 — Title

AI Meeting Summarizer & Action-Item Extractor
Muhammad Faozan Mujtaba · Group 54 · SafeX Solutions Summer Internship
Target company: Meridian Softworks (software house, Islamabad)

### Slide 2 — The problem

Three recurring meeting types a week. Notes taken in about half.

> "I'll chase the client for credentials by tomorrow" — said out loud, written down nowhere.

Consequences: blockers rediscovered a week later; clients told about slips after they happen;
actions nobody remembers owning.

**The gap is not note-taking. It is the structure of the notes: who owns what, by when.**

### Slide 3 — What the agent produces

Transcript in → structured record out.

Summary · Decisions made · **Action items (owner + absolute deadline + priority)** ·
Blockers · Open questions

*Visual: side-by-side raw transcript excerpt → generated action-item table.*

### Slide 4 — Architecture

Use `architecture_diagram.svg`.

Parser → segmentation → four extractors (decision / action / risk / summary) →
owner resolver + deadline resolver → `MeetingReport` → Markdown / JSON / PDF-ready HTML.

Optional hosted-LLM seam on the same prompt templates, with the offline pipeline as fallback.

### Slide 5 — Design rules enforced in code

1. Never invent an owner → `Unassigned`, flagged in the UI
2. Deadlines resolve against the **meeting date**, not today → reproducible
3. A decision is not a task
4. A question is only open if the reply defers it
5. A commitment needs a marker **and** a work verb

*Point to make: a wrong owner is worse than no owner — it makes the whole document
untrustworthy.*

### Slide 6 — Deadline resolution

`"by Friday"` → `2026-07-31` · `"next Wednesday"` → `2026-08-05` ·
`"in five business days"` → `2026-08-04` · `"end of the month"` → `2026-07-31`

Hard case worth showing:

> "If the icons land **this week** I can ship it **by next Wednesday**"

Two date phrases, one deadline. Explicit weekday constructions win over vague ones.

### Slide 7 — Accuracy

16 action items hand-annotated **before** the rules were tuned.

| Recall | Precision | F1 | Owner | Deadline |
|---|---|---|---|---|
| 100.00% | 94.12% | 96.97% | 100.00% | 93.75% |

38 tests · 54/54 pass across the Week 3 workspace.

### Slide 8 — What it gets wrong

Be direct about both:

1. **Cross-turn deadlines.** "I'll draft it" … three turns later … "In five business days."
   Needs coreference across turns. Reports `null` rather than guessing.
2. **Restated tasks double-counted.** Deduplication risks merging genuinely distinct tasks —
   a worse failure, because a dropped commitment is invisible.

*Framing: both are visible in the numbers rather than tuned away.*

### Slide 9 — Live demo

1. Open the Week 3 app → sidebar → AI Meeting Summarizer
2. Sprint review sample → **Generate Minutes**
3. Show the action-item table, then the `Unassigned` warning
4. Download the Markdown minutes
5. **Accuracy Benchmark** tab → Run Benchmark

*Runs entirely offline — no API key, no network.*

### Slide 10 — What I learned & next steps

The hard part was deciding **what not to output**. Four correct action items beat fifteen
items where four are real — a reader who finds noise stops trusting the document. Most tuning
removed output rather than adding it.

Next: cross-turn deadline attachment · larger gold set · `.ics` calendar export.

---

## Delivery notes

- Lead with the problem, not the pipeline. The architecture slide means nothing until the
  audience feels the lost-follow-up pain.
- Slide 8 is the credibility slide. Do not skip it — stating limitations precisely is what
  makes the accuracy figures believable.
- Have the app already running before you start; the demo is fast when it works and awkward
  when Streamlit is still booting.
