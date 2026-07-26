# Document Analysis & Knowledge-Base Assistant (RAG)

**Module:** `week3/src/modules/doc_knowledge_assistant/`
**Developer:** Ali Zaib (AI/ML Intern)
**Part of:** SafeX Solutions — AI Agent Automation Proposal, Week 3

## What this is

A Retrieval-Augmented Generation (RAG) assistant that answers questions
over a small set of company policy/FAQ documents, instead of guessing or
relying on a language model's general knowledge.

**Target company:** QuickBite — an original, fictional food-delivery
company standing in for Foodpanda (per the assignment's explicit
substitution note). All 5 knowledge-base documents were written from
scratch for this exercise; none are copied from any real company's actual
policies.

## Architecture

```
5 Markdown documents
      |
      v
Chunking (by '## ' section heading)
      |
      v
TF-IDF Embedding  (heading text boosted into each chunk's embedding)
      |
      v
In-memory Vector Store  (TF-IDF matrix + chunk metadata)
      |
      v
User Query --> Top-K Retrieval (cosine similarity)
      |
      +---> best score < threshold (0.12)? --> Abstain: "I don't know"
      |
      v
Answer Synthesis
      +-- mock (default): extractive answer directly from top chunk(s)
      +-- openai / gemini (optional): LLM call grounded in retrieved context
      |
      v
Response + cited source shown to user
```

See `architecture_diagram.svg` for the rendered version of this diagram.

### Why TF-IDF instead of a real embedding model / vector DB?

This repo's own established convention (see the Week 1 FAQ chatbot and the
Week 3 `customer_support_chatbot` module) is local, dependency-light NLP —
TF-IDF + cosine similarity, no external API required to run. `requirements.txt`
doesn't include an embeddings library or a vector database, and
`week3/.env.example` already scaffolds an `LLM_PROVIDER=mock` default,
confirming the team's intended pattern: a working local default, with real
LLM/embedding providers as an optional upgrade path. This module follows
that same pattern:

- **"Vector DB"** here is an in-memory TF-IDF matrix + chunk list. At this
  scale (5 documents, 35 chunks) this is a completely adequate vector
  store, and the retrieval interface (`engine.retrieve()`) wouldn't need to
  change if this were swapped for FAISS/Chroma later — only `_build_index()`
  would.
- **"LLM API"** — `engine.py` implements an `openai` and `gemini` provider
  behind the same `answer()` interface (see `_synthesize_with_llm`), but
  neither is used for the graded deliverable below, since no API key is
  available in the evaluation environment. The default `mock` mode
  (extractive answer synthesis, directly from retrieved text) is what's
  actually tested and reported.

## How it works

1. **Chunking:** each document is split by its `## ` section headings; each
   section becomes one chunk, tagged with its document title and section
   name.
2. **Embedding:** all chunks are vectorized with `TfidfVectorizer`
   (unigrams+bigrams, English stopwords removed, `sublinear_tf=True`).
   Each chunk's section heading is repeated into its embedding text before
   vectorizing — see "Development finding" below for why.
3. **Retrieval:** a query is vectorized the same way, and the top-K chunks
   by cosine similarity are returned.
4. **Abstention:** if the best similarity score is below `0.12`
   (`SIMILARITY_THRESHOLD` in `engine.py`), the assistant returns "I don't
   have information about that" instead of guessing — this is the module's
   main hallucination-mitigation control.
5. **Answer synthesis:** in the default `mock` mode, the top chunk's own
   text is returned directly (plus a second related chunk, if it also
   clears the threshold), with its source cited. This keeps every answer
   grounded — the assistant can only ever say what's actually written in a
   retrieved chunk.

## Development finding: heading-boosting improved accuracy from 71.4% to 100%

The first version of this pipeline embedded only each chunk's raw body
text. On the 14-question test suite, that scored **71.4%** — several
answerable questions matched the *wrong* document. The cause: "delivery"
appears in nearly every chunk across all 5 documents (the whole knowledge
base is about a delivery company), so TF-IDF gives it very little
discriminating weight, and paraphrased questions (*"how long does delivery
**usually take**"*) shared little other vocabulary with the correct
chunk's actual wording (*"delivered **within 30-45 minutes**"*).

Repeating each chunk's section heading into its embedding text (a standard
technique for short, single-topic documents) raised accuracy to 100%. This
finding, and the reasoning behind it, is documented in full in the
notebook and directly informed the "Known limitations" section below — it's
a genuine TF-IDF weakness, not something the heading boost fully solves.

## Files

| File | Purpose |
|---|---|
| `engine.py` | Chunking, embedding, retrieval, abstention, and answer synthesis. No Streamlit code. |
| `ui.py` | Streamlit tabs: Ask a Question, Knowledge Base browser, Evaluation Log, Architecture. |
| `data/knowledge_base/*.md` | The 5 original QuickBite policy/FAQ documents. |
| `test_suite.py` | 14 labeled test questions (12 answerable + 2 deliberately out-of-scope). |
| `sample_qa_test_log.md` | The required Q&A test log — all 14 questions run through the live pipeline with full answers and pass/fail status. |
| `doc_knowledge_assistant_rag_study.ipynb` | Notebook walkthrough with sample input/output, the heading-boost finding, and limitations discussion. |
| `architecture_diagram.svg` | Rendered version of the pipeline diagram above. |
| `../../../tests/test_doc_knowledge_assistant.py` | 9 unit tests covering indexing, retrieval, answering, abstention, and evaluation. |

## How to run

**Unit tests:**
```bash
cd week3
python -m pytest tests/test_doc_knowledge_assistant.py -v
```

**Notebook:**
Open `doc_knowledge_assistant_rag_study.ipynb` in Jupyter/VS Code and run
all cells (the first code cell adds the repo root to `sys.path`
automatically).

**Full Streamlit suite** (this module is one tab inside it):
```bash
cd week3
pip install -r requirements.txt
streamlit run src/app.py
```
Then select **"Document Analysis & Knowledge-Base Assistant"** from the
sidebar. The **Ask a Question** tab lets you query the knowledge base
live; the **Evaluation Log** tab re-runs the 14-question test suite and
shows the same limitations discussion as this README.

## Known limitations

- **Lexical, not semantic, matching.** TF-IDF only recognizes shared words
  and phrases; it has no real concept of synonyms or paraphrase. A true
  embedding model (e.g. sentence-transformers) would generalize much
  better — see the development finding above for a concrete example of
  this failing (and partially being mitigated).
- **Abstention is a similarity-score heuristic, not true uncertainty
  estimation.** A borderline or ambiguous question could still score above
  the threshold against the *wrong* document, producing a confident but
  irrelevant answer rather than an abstention. This is the main residual
  hallucination-adjacent risk in this design.
- **Extractive answers only, by default.** Answers are always the
  retrieved chunk's own text, not a generated summary — this limits
  hallucination risk but also limits how naturally the assistant can
  combine information across chunks.
- **Small knowledge base (5 documents, 35 chunks).** 100% accuracy on this
  14-question test suite doesn't guarantee the same performance on a
  larger, more topically overlapping document set, where more chunks would
  compete for similar vocabulary.
- **The optional LLM generation path (`openai`/`gemini`) is implemented but
  untested against a live API** in this evaluation environment, since no
  API key was available. Only the default `mock` (extractive) path has
  been run and evaluated.
