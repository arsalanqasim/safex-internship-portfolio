# RAG-based Knowledge Assistant (Indus Air)

Week 4 Client-Ready Sprint module for SafeX Solutions Group 54.

## Developer Metadata

- **Developer**: Muhammad Faozan Mujtaba
- **Role**: Group Member (Group 54)
- **Module path**: `week4/src/modules/knowledge_assistant_airline/`
- **Sprint**: Week 4 Client-Ready Sprint

## The Client Problem

**Indus Air** is a fictional Pakistani domestic and regional carrier used as the client for
this prototype. Its contact centre answers the same policy questions all day: baggage
allowances, change fees, delay compensation, pet carriage, assistance for minors. Those
rules live in seven separate policy documents, and agents search them by hand while a
passenger waits on the line.

Two things go wrong today. Agents are slow, because finding the rule means scrolling the
right document. And agents are inconsistent, because when they cannot find the rule
quickly they answer from memory, which is how a passenger gets quoted the wrong excess
baggage rate.

A general chatbot makes the second problem worse: it answers fluently whether or not it
knows. This module is built so that a confident wrong answer is the specific failure it
is designed to prevent.

## What This Module Does

It turns the policy library into a retrieval-augmented question answering service that
answers **only** from the loaded documents, shows the passage behind every answer, and
refuses when it does not have the rule.

```
markdown policy docs -> section chunking -> vector index -> top-k retrieval
    -> similarity floor -> grounded answer with citations
```

### Pipeline stages

1. **Chunking** - each document is split at its own level-two headings, so a retrieved
   passage is a complete rule an agent can read and act on rather than half a rule.
   Sections over 1,100 characters are split at paragraph boundaries with a 160-character
   overlap, so a fact straddling a paragraph break stays retrievable in one whole passage.
2. **Query expansion** - passengers say "hand luggage"; the policy says "cabin baggage".
   A domain synonym map bridges that vocabulary gap before vectorisation. This is what
   lets lexical retrieval work well without paying for an embeddings service.
3. **Vector index** - TF-IDF over unigrams and bigrams, scored by cosine similarity,
   behind a `VectorIndex` interface.
4. **Similarity floor** - if the best passage scores below the floor, the assistant
   refuses and names the closest covered topic instead of answering from a weak match.
5. **Grounded composition** - the answer quotes the passage lines that match the question,
   each tagged with the passage number it came from.

## Knowledge Base

Seven synthetic Indus Air policy documents, 48 indexed chunks, ~3,960 words:

| File | Covers |
|---|---|
| `baggage_policy.md` | Cabin and checked allowances, excess rates, sports gear, lost baggage |
| `booking_changes_and_refunds.md` | Fare families, change fees, refunds, no-show, travel credit |
| `check_in_and_boarding.md` | Check-in windows, counter and gate timings, seating, denied boarding |
| `disruptions_and_compensation.md` | Duty of care, compensation, cancellations, missed connections |
| `indusmiles_loyalty_program.md` | Tiers, earning and spending miles, expiry, family pooling |
| `special_assistance_and_minors.md` | Wheelchair codes, unaccompanied minors, infants, medical clearance |
| `pets_and_restricted_items.md` | Cabin and hold pets, lithium batteries, prohibited items, liquids |

*All documents are synthetic, written for this internship prototype. Indus Air is not a
real airline and no real carrier's policy text is reproduced.*

## Hallucination Controls

The assignment calls for hallucination controls, so they are stated explicitly and each
one is measured:

1. **Similarity floor** - weak retrieval becomes an explicit refusal that names the
   closest covered topic, rather than a confident-sounding guess. Measured by
   `refusal_accuracy`.
2. **Extractive composition** - in offline mode every line of the answer is verbatim text
   lifted from a retrieved passage. There is no free text for the system to invent. A test
   asserts every quoted line appears in the retrieved passages.
3. **Prompt rules** - `prompts.py` forbids outside knowledge, requires a citation per
   claim, requires figures to be quoted exactly, and specifies the exact refusal wording.
4. **Visible citations and scores** - every answer shows its passages, source file and
   retrieval score, so an agent can check the source before repeating it to a passenger.

## Benchmark Results

Measured against `data/evaluation_set.json`: 38 questions, 33 answerable and 5
out-of-scope. Questions were written from the agent's point of view in passenger phrasing
**before** the retriever was tuned.

| Metric | Result |
|---|---|
| Retrieval recall@4 | 100.00% |
| Retrieval precision@1 | 93.94% |
| Answer accuracy | 100.00% |
| Refusal accuracy (out-of-scope refused) | 100.00% |
| Mean latency | ~0.6 ms per question |

Reproduce with `pytest src/modules/knowledge_assistant_airline/`, or open the **Benchmark**
tab in the app and press *Run benchmark*.

### How the similarity floor was calibrated

On this gold set the weakest answerable question scores **0.1392** and the strongest
out-of-scope question scores **0.1096**. Any floor inside that band separates the two
classes perfectly, and the default of `0.12` sits near the middle. That band is narrow.
A floor moved much above it starts refusing legitimate questions; moved much below it
starts answering out-of-scope ones. The **Ask** tab exposes the floor as a slider so a
reviewer can see both failure modes directly.

### Findings kept visible rather than tuned away

- **Precision@1 is 93.94%, not 100%.** Two questions retrieve `baggage_policy.md` first
  when the gold label says `pets_and_restricted_items.md`: the power-bank question and the
  cabin-liquids question. Both are arguably correct - the baggage policy genuinely does
  state that power banks are never permitted in the hold. The gold label allows only one
  document, so these score as misses. Recall@4 is 100%, so the correct document is always
  retrieved and always cited.
- **The carrier name carried fake retrieval signal.** `indus` and `air` appear in all 48
  chunks. scikit-learn's smoothed IDF floors a term present in every document at 1.0
  rather than 0, so simply naming the airline scored against every chunk equally and
  lifted out-of-scope questions above the floor. Capping the vectoriser at `max_df=0.9`
  removed it, and raised refusal accuracy from 80% to 100%. A regression test guards it.
- **Hard-wrapped markdown produced fragment answers.** The first composer split passages on
  physical newlines, quoting fragments such as "of respiratory distress and may travel
  only in the cabin". Lines belonging to one paragraph or bullet are now rejoined before
  sentence splitting, while table rows are kept whole.

## Assigned Stack vs Built Stack

The registry lists Chroma/FAISS and an embeddings API for this module. What ships is a
TF-IDF cosine index, for two deliberate reasons:

- The deployed demo has to run on Streamlit Community Cloud free tier with **no API key
  and no vector database service**, so a reviewer can open the link and it works.
- `week4/requirements.txt` is a shared file used by all nine members, so adding
  `chromadb` or `faiss-cpu` to it would affect everyone else's deployment.

The production path is kept open rather than closed off. Retrieval sits behind the
`VectorIndex` interface, and `EmbeddingVectorIndex` already implements that interface
against a hosted embeddings API. Swapping backends touches no other code:

```python
assistant = AirlineKnowledgeAssistant(index=EmbeddingVectorIndex())
```

Answer generation follows the same pattern the group used in Week 3: offline
`LLM_PROVIDER=mock` by default, with `prompts.py` sent to a hosted provider when one is
configured, and the extractive answer as the fallback if that call fails.

## Files

```text
knowledge_assistant_airline/
  __init__.py
  engine.py            # chunking, vector index, retrieval, grounding, evaluation
  prompts.py           # system prompt, answer prompt, refusal template
  ui.py                # self-contained render_ui()
  deploy_prep.py       # builds the standalone deployment package
  README.md
  data/
    knowledge_base/    # 7 synthetic Indus Air policy documents
    evaluation_set.json
  tests/
    test_knowledge_assistant_airline.py
  Week 4 Required Documents/
```

## How to Run

From the `week4/` folder:

```bash
pip install -r requirements.txt
streamlit run src/app.py          # then pick "RAG Knowledge Assistant" in the sidebar
pytest src/modules/knowledge_assistant_airline/
```

Optional environment variables (all unset by default; the app runs fully offline):

```bash
LLM_PROVIDER=openai        # default "mock" - offline extractive answers
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=...         # never commit this
EMBEDDING_BACKEND=openai   # switches retrieval to the hosted embeddings index
```

## Deployment

`python src/modules/knowledge_assistant_airline/deploy_prep.py` builds a self-contained
folder at `week4/knowledge_assistant_deploy_package/` with its own `app.py`,
`requirements.txt` and a copy of the knowledge base, ready to push to a personal GitHub
repo and deploy on Streamlit Community Cloud.

The live URL is registered in `week4/src/modules/registry.py` under `deployed_url`.
