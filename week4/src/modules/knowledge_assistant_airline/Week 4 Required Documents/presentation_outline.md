# Week 4 Slide Deck Outline - RAG-based Knowledge Assistant

Member: Muhammad Faozan Mujtaba
Module: `week4/src/modules/knowledge_assistant_airline/`
Target length: 10 slides, 6-8 minutes

---

## Slide 1 - Title

**RAG-based Knowledge Assistant**
Grounded policy answers for airline contact centres

Muhammad Faozan Mujtaba · SafeX Solutions Group 54 · Week 4 Client-Ready Sprint
Client: Indus Air (fictional carrier built for this prototype)

*Footer: live demo link*

---

## Slide 2 - The problem

Indus Air's contact centre answers the same policy questions all day, from **seven
separate documents**, searched by hand while a passenger waits.

- **Slow** - finding a rule means scrolling the right document.
- **Inconsistent** - when agents cannot find it fast, they answer from memory.

*Speaker note: the second one is what costs money - a wrong excess baggage rate quoted on
a call becomes a refund later.*

---

## Slide 3 - Why not just use a chatbot

A general chatbot **answers fluently whether or not it knows**. On policy questions that
makes the problem worse, not better.

> A confident wrong answer is the specific failure this module is built to prevent.

*Speaker note: this single line drove every design decision in the deck that follows.*

---

## Slide 4 - The pipeline

```
policy docs -> section chunking -> vector index -> top-k retrieval
    -> similarity floor -> grounded answer with citations
```

| Stage | Decision |
|---|---|
| Chunking | Split at the documents' own headings, so a passage is a complete rule |
| Query expansion | Passengers say "hand luggage", policy says "cabin baggage" |
| Index | TF-IDF + cosine, behind a swappable `VectorIndex` interface |
| Floor | Below it, refuse instead of guessing |
| Composition | Quote the matching lines, cite every one |

---

## Slide 5 - Four hallucination controls

1. **Similarity floor** - weak retrieval becomes an explicit refusal naming the closest
   covered topic.
2. **Extractive composition** - every line is verbatim from a retrieved passage. There is
   no free text to invent. A test asserts this.
3. **Prompt rules** - no outside knowledge, a citation per claim, figures quoted exactly.
4. **Visible citations and scores** - the agent can check the source before repeating it.

---

## Slide 6 - Live demo

*Switch to the app. Three questions, ninety seconds:*

1. "How much hand luggage can I take?" - answers despite the wording mismatch.
2. "Can my pug travel in the hold?" - finds the snub-nosed breed exclusion.
3. "What is the wifi password on board?" - **refuses**, and names the closest topic.

---

## Slide 7 - Results

| Metric | Result |
|---|---|
| Retrieval recall@4 | 100.00% |
| Retrieval precision@1 | 93.94% |
| Answer accuracy | 100.00% |
| Refusal accuracy | 100.00% |
| Mean latency | ~0.6 ms |

38 questions: 33 answerable, 5 out-of-scope. Written in passenger phrasing **before** the
retriever was tuned.

---

## Slide 8 - The bug worth showing

`indus` and `air` appear in **48 of 48 chunks**. scikit-learn's smoothed IDF floors a
universal term at **1.0, not 0** - so naming the airline scored against every chunk and
lifted out-of-scope questions over the floor.

`max_df=0.9` → **refusal accuracy 80% → 100%**.

*Speaker note: only an out-of-scope question that sounded like a company question exposed
this. "Who won the cricket match" scored 0.0 and never would have.*

---

## Slide 9 - Honest limits

- **Precision@1 is 93.94%, not 100%** - two questions retrieve the baggage policy where
  the label says restricted items. Both are arguably correct. Recall@4 is 100%.
- **The synonym map is manual** and will not cover wording nobody anticipated. That is the
  real argument for the embeddings backend in production.
- **The floor's separation band is narrow** (0.1096 to 0.1392). The app exposes it as a
  slider so you can see both failure modes.

---

## Slide 10 - Production path and close

Retrieval sits behind an interface, so the assigned Chroma/FAISS stack is a one-line swap:

```python
assistant = AirlineKnowledgeAssistant(index=EmbeddingVectorIndex())
```

TF-IDF ships because the demo must run on free hosting with no API key - so a reviewer can
just open the link.

**Live demo:** *(URL)* · **Repo:** `week4/src/modules/knowledge_assistant_airline/`

---

## Screenshots to capture

Capture by hand from the running app - Streamlit renders over a websocket, so headless
screenshots capture only the loading skeleton.

1. `01_ask_answer.png` - hand luggage answer with citations and confidence metrics.
2. `02_retrieved_passages.png` - an expanded passage showing source file and score.
3. `03_refusal.png` - the wifi question refused, naming the closest topic.
4. `04_benchmark.png` - benchmark tab with the four metric tiles.
5. `05_knowledge_base.png` - indexed document table.
6. `06_how_it_works.png` - the system prompt with its grounding rules.
