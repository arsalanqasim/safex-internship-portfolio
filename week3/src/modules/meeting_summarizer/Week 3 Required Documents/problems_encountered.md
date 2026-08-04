# Problems Encountered — AI Meeting Summarizer & Action-Item Extractor

**Member:** Muhammad Faozan Mujtaba

Five problems shaped the final design. Four were solved; two limitations remain and are
reported in the accuracy numbers rather than hidden.

---

## 1. "Will" is not a commitment

**Problem.** The first extraction pass treated any sentence containing `will`, `I'll`,
`please` or `need to` as an action item. On the client kickoff transcript that produced
tasks like *"Our legal team will have a view on that"* and *"We will keep it on the open
list"* — grammatically commitments, but no work is described. The action list filled with
conversational filler, which is exactly what makes generated minutes get ignored.

**Fix.** A sentence now needs **two** signals: a commitment marker *and* a verb from a
curated list of work verbs (`chase`, `draft`, `circulate`, `deploy`, `confirm`, …). "Will
have a view" has the marker and no verb, so it is dropped. "Will chase Orchard for
credentials" has both.

**Result.** Precision rose without any loss of recall — the work-verb requirement removed
only sentences that described no work.

---

## 2. Most questions in a meeting are not open questions

**Problem.** Treating every sentence ending in `?` as an open question produced five
"open questions" for the sprint review, of which one was genuinely open. *"How much more time
do you need?"* was answered in the next breath. *"Hina, can you prepare the regression
report?"* is a task, not a question.

**Fix.** Two rules. A directed request (`can you`, `could you`, `please`) is never an open
question — it belongs to the action pipeline. And a genuine question is only kept if the
**next one or two turns defer it** (`to be decided`, `open question`, `don't know yet`).

**Result.** Five open questions down to two, both correct.

---

## 3. Relative deadlines are ambiguous, and one sentence can carry two

**Problem.** *"If the final icons land **this week** I can ship the order tracking screen
**by next Wednesday**."* Two date phrases; only the second is the deadline. The first
matched earlier in the resolver's ordering and won, dating the task to Friday instead of the
following Wednesday.

Separately, "next Wednesday" said on a Tuesday is genuinely ambiguous in English — the naive
"next occurrence" reading gives *tomorrow*, which nobody means.

**Fix.** Explicit `by/next/this <weekday>` constructions are resolved **before** vague phrases
like "this week", because a preposition plus a weekday is a much stronger deadline signal.
And "next \<weekday\>" resolves to that weekday in the following Monday–Sunday week, which
matches how people actually use it. Every deadline resolves against the **meeting date**, so
re-running an old transcript reproduces the same dates rather than drifting with the clock.

---

## 4. Speakers and attendees are the same people under different names

**Problem.** The transcript header lists `Ayesha Rauf (Delivery Lead)` while her turns are
labelled `Ayesha:`. The participant list came out with both, so the same person appeared
twice and owner attribution was inconsistent between full and short names. A related bug:
splitting the attendee line on commas broke `Nadia Sheikh (Orchard Foods, Head of Digital)`
into two "people" on the comma inside the parentheses.

**Fix.** Role parentheticals are stripped before splitting, and entries sharing a first name
are merged with the fuller form kept. Every owner, decision attribution and blocker
attribution then reports the canonical full name.

---

## 5. Deadlines stated in a later turn — **unresolved**

**Problem.** In the kickoff call:

> **Bilal:** I'll draft an integration options document covering both real time and batch.
> **Ayesha:** Good idea. When can you have it?
> **Bilal:** In five business days.

The deadline is three turns away from the task. The engine dates the task `null`.

**Why it is not fixed.** Attaching it requires resolving "it" back to the earlier commitment
— coreference across speaker turns. That is a genuine NLP problem, not a regex gap, and
faking it with "attach any nearby date to the nearest recent task" would produce confidently
wrong deadlines. Given design rule 1 (never invent), an honest `null` is better than a
plausible guess.

**Cost:** 1 of 16 deadlines — the entire gap between 93.75% and 100% deadline accuracy.

---

## 6. Restated tasks are double-counted — **unresolved**

**Problem.** In the hiring sync, Ayesha commits to sharing a weekly shortlist, and Sana then
adds *"Please send the shortlist before Tuesday lunchtime."* The second sentence refines the
first; the engine emits both as separate action items.

**Why it is not fixed.** Deduplicating them requires deciding that two differently-worded
sentences describe one task. Simple text-similarity thresholds are unreliable at this length
and would start merging genuinely distinct tasks that share vocabulary — a worse failure,
because a dropped commitment is invisible.

**Cost:** the single precision miss — 17 items extracted against 16 in the gold set.

---

## Reflection

The hardest part was not extraction, it was deciding **what not to output**. A minutes
document with four correct action items is more useful than one with fifteen items where
four are real, because a reader who finds noise stops trusting the whole document. Most of
the tuning work removed output rather than adding it.

Annotating the gold standard *before* tuning the rules mattered more than expected. It made
regressions visible immediately, and it kept the reported accuracy honest — the two
limitations above showed up as numbers I could not explain away rather than as behaviour I
never looked at.
