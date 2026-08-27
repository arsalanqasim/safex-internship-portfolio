# Problems Encountered - Week 4 RAG Knowledge Assistant

Owner: Muhammad Faozan Mujtaba
Module: `week4/src/modules/knowledge_assistant_airline/`
Date: 2026-08-24

---

## 1. Naming the airline made unrelated questions look answerable

**Symptom.** Refusal accuracy sat at 80%. The question *"What is the share price of Indus
Air today?"* scored 0.1392, above the 0.12 similarity floor, so the assistant answered it
from the check-in policy instead of refusing.

**Investigation.** Inspecting the fitted vectoriser showed the cause:

```
'indus':     appears in 48/48 chunks, idf=1.000
'air':       appears in 48/48 chunks, idf=1.000
'indus air': appears in 48/48 chunks, idf=1.000
'baggage':   appears in 17/48 chunks, idf=2.001
```

Every document title starts with "Indus Air", so the carrier name is in every chunk. TF-IDF
should give a term like that no discriminating power, but scikit-learn's default
`smooth_idf=True` computes `ln((1+n)/(1+df)) + 1`, which **floors the IDF of a universal
term at 1.0 rather than 0**. The name therefore contributed real weight to every chunk
equally, and any question merely mentioning the airline cleared the floor.

**Fix.** Cap the vectoriser at `max_df=0.9`, dropping terms present in more than 90% of
chunks. On this corpus that removes exactly the ubiquitous branding terms.

**Result.** Refusal accuracy 80% -> 100%. Out-of-scope scores dropped to a maximum of
0.1096 while answerable questions stayed at 0.1392 and above, opening a clean separation
band around the floor.

**Guarded by.** `test_carrier_name_alone_does_not_produce_a_confident_match`.

**Lesson.** A RAG evaluation set needs out-of-scope questions that use in-domain
vocabulary. A generic unrelated question ("who won the cricket match") scored 0.0 and would
never have exposed this. Only a question that *sounded* like a company question did.

---

## 2. Hard-wrapped markdown produced fragment answers

**Symptom.** Answers contained sentence fragments that read as broken:

```
- duty of care. [1]
- Compensation claims must be filed within 60 days of the disrupted flight through [1]
- of respiratory distress and may travel only in the cabin if within the 8 kg limit. [1]
```

**Cause.** The extractive composer split each passage on physical newlines. The policy
documents are hard-wrapped at roughly 88 characters, so a physical line is almost never a
complete sentence. Every quoted "unit" was really a wrapped fragment.

**Fix.** Rewrote `_split_units` to rejoin lines belonging to the same paragraph or the same
bullet before sentence splitting, while still keeping markdown table rows whole - a row
like `| Indus Flex | 25 kg | 30 kg |` is a single fact and splitting it on punctuation
would destroy the answer being asked for.

**Result.** Same passage now yields complete statements:

```
- Snub nosed breeds, including Persian and Himalayan cats, and Pug, Bulldog, Boxer and
  Shih Tzu dogs, are refused in the hold on all routes. [1]
```

**Guarded by.** `test_split_units_rejoins_hard_wrapped_lines` and
`test_split_units_keeps_table_rows_whole_and_drops_separators`.

---

## 3. Passenger vocabulary does not match policy vocabulary

**Symptom.** *"How much hand luggage can I take?"* retrieved poorly. The policy never uses
the phrase "hand luggage" - it says "cabin baggage" throughout. Lexical retrieval cannot
match words that do not exist in the corpus.

**Fix.** A domain synonym map applied to the query before vectorisation, mapping passenger
phrasing onto policy vocabulary. The original wording is kept alongside the expansion so an
already-precise question is not diluted.

Two gaps in this map caused the only false refusals in the first full benchmark run:
*"Can my 7 year old fly alone?"* (0.1121) and *"Can I put my brother's name on my ticket?"*
(0.0982). Adding `fly alone -> unaccompanied minor` and `name on my ticket -> name change`
lifted both above the floor.

**Trade-off, stated plainly.** A synonym map is manual and does not generalise to wording
nobody anticipated. This is the clearest argument for the embeddings backend in production,
where semantic similarity handles unseen phrasing without a hand-maintained list. The
`VectorIndex` interface exists so that swap costs one line.

---

## 4. The assigned stack could not be deployed as specified

**Constraint.** The registry assigned Chroma/FAISS plus an embeddings API. Neither could
ship: the deployed demo has to run on Streamlit Community Cloud free tier with no API key
so a reviewer can simply open the link, and `week4/requirements.txt` is shared by all nine
members, so adding `chromadb` or `faiss-cpu` would change everyone else's deployment.

**Resolution.** Build against the `VectorIndex` interface. TF-IDF is the default that runs
anywhere; `EmbeddingVectorIndex` implements the same interface against a hosted embeddings
API for production. Documented in the README and section 8 of the progress report rather
than left as a silent substitution.

---

## 5. Deployment and video deliverables could not be completed in-session

**Deployment.** Streamlit Community Cloud requires interactive sign-in to personal GitHub
and Streamlit accounts, which is not possible from the build environment. The standalone
package is built and verified running, so the remaining work is push-and-connect.
`deployed_url` is deliberately left `None`: a guessed URL would light a green "Live" badge
on the master dashboard pointing at nothing.

**Videos.** Screen recording with narration cannot be produced here. Both scripts are
written with per-section timings so recording is a read-through.

---

## 6. Repeat of a Week 3 constraint

Streamlit renders over a websocket, so headless browser screenshots capture only the
loading skeleton. As in Week 3, UI verification was done with `streamlit.testing.v1.AppTest`
- driving the real widgets and asserting on rendered output - and screenshots have to be
captured by hand from a running app.
