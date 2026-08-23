# Week 4 Progress Report - RAG-based Knowledge Assistant

**Member**: Muhammad Faozan Mujtaba
**Role**: Group Member, SafeX Solutions Group 54
**Module**: `week4/src/modules/knowledge_assistant_airline/`
**Assignment**: RAG-based Knowledge Assistant (Client-Ready Sprint)
**Report date**: 2026-08-24
**Status**: Ready for review

---

## 1. Assignment

Build a Retrieval-Augmented Generation assistant that answers questions over a customised
operational document set (FAQ/policies), package it as a standalone deployable app, and
register the live URL in `week4/src/modules/registry.py`.

## 2. Client and Problem

The chosen client is **Indus Air**, a fictional Pakistani domestic and regional carrier
created for this prototype. Its contact centre answers the same policy questions all day
from seven separate documents, searched by hand while a passenger waits.

Two failures follow. Agents are slow, because finding a rule means scrolling the right
document. Agents are inconsistent, because when they cannot find it quickly they answer
from memory, and a passenger gets quoted the wrong excess baggage rate.

A general chatbot makes the second failure worse: it answers fluently whether or not it
knows. **A confident wrong answer is the specific failure this module is built to
prevent**, and that shaped every design decision below.

## 3. What Was Delivered

| Deliverable | Status |
|---|---|
| Module engine, prompts, UI under the required shape | Complete |
| Knowledge base: 7 synthetic policy documents, 48 chunks, ~3,960 words | Complete |
| Gold evaluation set: 38 questions (33 answerable, 5 out-of-scope) | Complete |
| Automated test suite: 31 tests | Complete, all passing |
| Standalone deployment package + packaging script | Complete, verified running |
| Registry entry updated (status, tech stack) | Complete |
| Outreach tracker: 3 target records | Prepared, awaiting send |
| Live deployment URL registered | **Blocked - see section 7** |
| Demo and explanation videos | **Not recorded - see section 7** |

## 4. How It Works

```
markdown policy docs -> section chunking -> vector index -> top-k retrieval
    -> similarity floor -> grounded answer with citations
```

1. **Chunking** at each document's own level-two headings, so a retrieved passage is a
   complete rule an agent can act on. Long sections split at paragraph boundaries with
   overlap so a fact crossing a break stays retrievable whole.
2. **Query expansion** - passengers say "hand luggage", the policy says "cabin baggage".
   A domain synonym map bridges that gap before vectorisation.
3. **Vector index** - TF-IDF over unigrams and bigrams with cosine similarity, behind a
   `VectorIndex` interface so a hosted embeddings backend swaps in without touching
   anything downstream.
4. **Similarity floor** - weak retrieval becomes an explicit refusal naming the closest
   covered topic.
5. **Grounded composition** - the answer quotes matching passage lines, each tagged with
   its passage number.

## 5. Results

Measured against `data/evaluation_set.json`, written in passenger phrasing from the
agent's point of view **before** the retriever was tuned.

| Metric | Result |
|---|---|
| Retrieval recall@4 | 100.00% |
| Retrieval precision@1 | 93.94% |
| Answer accuracy | 100.00% |
| Refusal accuracy (out-of-scope correctly refused) | 100.00% |
| Mean latency | ~0.6 ms per question |

**Similarity floor calibration.** The weakest answerable question scores 0.1392; the
strongest out-of-scope question scores 0.1096. Any floor inside that band separates the
two classes perfectly, and the default 0.12 sits near its middle. The band is narrow, and
the app exposes the floor as a slider so a reviewer can see both failure modes directly.

## 6. Problems Found and Fixed

Three findings are documented rather than quietly tuned away. Full detail in
`problems_encountered.md`.

1. **The carrier name carried fake retrieval signal.** `indus` and `air` appear in all 48
   chunks, and scikit-learn's smoothed IDF floors a term present in every document at 1.0
   rather than 0. Simply naming the airline scored against every chunk equally and lifted
   out-of-scope questions above the floor. Capping the vectoriser at `max_df=0.9` fixed it
   and raised refusal accuracy from 80% to 100%. A regression test guards it.
2. **Hard-wrapped markdown produced fragment answers**, such as "of respiratory distress
   and may travel only in the cabin". Lines in one paragraph or bullet are now rejoined
   before sentence splitting; table rows are kept whole.
3. **Precision@1 is 93.94%, not 100%,** and is left visible. Two questions retrieve the
   baggage policy first where the gold label says the restricted-items policy. Both are
   arguably right - the baggage policy does state that power banks are barred from the
   hold. Recall@4 is 100%, so the correct document is always retrieved and cited.

## 7. Blockers and Open Items

- **Live deployment URL.** Deploying to Streamlit Community Cloud requires signing in to
  my personal GitHub and Streamlit accounts, which cannot be done from the build
  environment. The standalone package is built and verified running at
  `week4/knowledge_assistant_deploy_package/`, so deployment is a push-and-connect step.
  `deployed_url` is left as `None` until the live link exists; setting it to a guessed URL
  would show a broken green "Live" badge on the master dashboard.
- **Demo and explanation videos.** Not recorded. Full scripts with timings are prepared in
  `demo_video_script.md` and `explanation_video_script.md`.
- **Outreach.** The 3 target records are prepared with drafted messages but not yet sent,
  since the messages reference the live demo URL. Follow-up date 2026-08-28.
- **`week4/data/outreach_tracker.xlsx` is listed in `week4/.gitignore`,** so the workbook
  will not appear in the pull request. A committed mirror is at `outreach_log.md` in this
  folder. Flagging for the group leader in case the ignore rule was meant only for the
  runtime-generated copy.

## 8. Deviation From the Assigned Stack

The registry listed Chroma/FAISS and an embeddings API. What ships is a TF-IDF cosine
index, for two deliberate reasons: the deployed demo must run on Streamlit Community Cloud
free tier with no API key and no vector database service so a reviewer can just open the
link; and `week4/requirements.txt` is shared by all nine members, so adding `chromadb` or
`faiss-cpu` would affect everyone's deployment.

The production path is kept open rather than closed off. `EmbeddingVectorIndex` already
implements the same `VectorIndex` interface against a hosted embeddings API, and swapping
it in is a one-line change covered by a test.

## 9. How to Verify

From `week4/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py        # sidebar -> RAG Knowledge Assistant
pytest src/modules/knowledge_assistant_airline/     # 31 tests
```
