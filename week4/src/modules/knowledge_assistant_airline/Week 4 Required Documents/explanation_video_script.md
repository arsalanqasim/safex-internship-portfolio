# Technical Explanation Video Script (5-10 minutes, HD)

Module: RAG-based Knowledge Assistant · Muhammad Faozan Mujtaba · Week 4
Audience: SafeX internship evaluators and the group leader
Record at 1080p minimum. Editor font 16pt+ so code is readable at full-screen.

**Setup**: editor with `engine.py` open, app running in a second tab, terminal ready in
`week4/`.

---

## 0:00-0:40 - What was assigned and what shipped

> "Week 4, my module is the RAG-based knowledge assistant. The client is Indus Air, a
> fictional carrier I created for this prototype, with seven policy documents - baggage,
> changes and refunds, check-in, disruption, loyalty, assistance, and restricted items.
>
> The goal isn't just to answer questions. It's to never answer confidently when it
> shouldn't. Everything I'll show you follows from that."

---

## 0:40-1:40 - Chunking

Show `load_knowledge_base` in `engine.py`.

> "First decision: how to cut the documents. I split at each document's own level-two
> headings, because policy documents are already written in self-contained sections. That
> means a retrieved passage is a whole rule - an agent reads it and can act on it, rather
> than getting half a rule.
>
> Sections over 1,100 characters split at paragraph boundaries with a 160-character
> overlap, so a fact that straddles a paragraph break still appears complete in at least
> one passage. Seven documents become 48 chunks."

---

## 1:40-2:40 - Query expansion

Show `QUERY_SYNONYMS`.

> "Second problem: passengers say 'hand luggage'. The policy says 'cabin baggage' - the
> phrase 'hand luggage' appears nowhere in the corpus. Lexical retrieval cannot match a
> word that doesn't exist in the documents.
>
> So before vectorising I expand the query with policy vocabulary. I keep the original
> wording too, so a question that's already precise doesn't get diluted.
>
> I'll be straight about the trade-off: this map is manual, and it won't cover phrasing I
> didn't anticipate. That's the strongest argument for the embeddings backend in
> production, and I'll come back to it."

---

## 2:40-3:40 - The index and the interface

Show `VectorIndex`, `TfidfVectorIndex`, `EmbeddingVectorIndex`.

> "Retrieval is TF-IDF over unigrams and bigrams with cosine similarity. Bigrams matter
> here - 'cabin baggage' and 'unaccompanied minor' need to stay single features.
>
> But notice it's behind an interface. My assignment listed Chroma or FAISS with an
> embeddings API. I didn't ship that, for two concrete reasons: the deployed demo has to
> run on Streamlit free tier with no API key so a reviewer can just open the link, and
> `week4/requirements.txt` is shared by all nine of us - adding faiss or chromadb changes
> everyone's deployment.
>
> So instead of ignoring the assigned stack, I built the seam for it. `EmbeddingVectorIndex`
> implements the same interface against a hosted embeddings API. Swapping is one line, and
> there's a test that injects a custom index to prove the seam works."

---

## 3:40-5:10 - The bug worth explaining

Show the diagnostic output.

> "Now the part I'd most want you to see. My first full benchmark gave 100% recall but only
> **80% refusal accuracy**. The question 'what is the share price of Indus Air today?'
> scored 0.1392 - above my 0.12 floor - so it answered from the check-in policy.
>
> I inspected the fitted vectoriser and found this: `indus` and `air` appear in 48 out of
> 48 chunks, with an IDF of 1.0. `baggage` appears in 17 chunks with an IDF of 2.0.
>
> Now, TF-IDF is supposed to give a term that appears everywhere no discriminating power.
> But scikit-learn's default `smooth_idf` computes log of (1+n) over (1+df), **plus one**.
> That plus one floors a universal term at 1.0 instead of zero. Every document title starts
> with 'Indus Air', so the carrier name was contributing real weight to all 48 chunks
> equally - and any question that merely mentioned the airline cleared my floor.
>
> The fix is `max_df=0.9`: drop terms in more than 90% of chunks. Refusal accuracy went
> from 80% to 100%, and there's a regression test named after the failure.
>
> The lesson generalises. My unrelated question - 'who won the cricket match' - scored 0.0
> and would never have caught this. Only an out-of-scope question that *sounded* like a
> company question exposed it. If you build one of these, put in-domain out-of-scope
> questions in your eval set."

---

## 5:10-6:10 - The similarity floor

Show the app's floor slider; drag it to 0.

> "The floor is the main hallucination control. Below it, the assistant refuses rather than
> answering from a weak match.
>
> On my gold set the weakest answerable question scores 0.1392 and the strongest
> out-of-scope question scores 0.1096. Any floor in that band separates them perfectly, and
> I default to 0.12, near the middle. That band is narrow, so I've exposed it as a slider -
> drag it to zero and it will answer the cricket question, which is exactly the failure the
> floor exists to stop."

---

## 6:10-7:00 - Grounded composition

Show `compose_extractive_answer`.

> "In offline mode nothing is generated. I score each line of the retrieved passages
> against the question and quote the best ones verbatim, each tagged with its passage
> number. There's no free text for the system to invent, and a test asserts every quoted
> line appears in the retrieved passages.
>
> One bug here: my first version split passages on physical newlines. My documents are
> hard-wrapped at 88 characters, so I was quoting fragments like 'of respiratory distress
> and may travel only in the cabin'. I now rejoin paragraph and bullet lines before
> sentence splitting, but keep table rows whole - a row like 'Indus Flex, 25 kilos, 30
> kilos' is a single fact."

---

## 7:00-7:50 - Prompts and the provider path

Show `prompts.py`, then the *How it works* tab.

> "When a provider is configured, these templates are what gets sent: answer only from the
> numbered passages, never use general airline knowledge, cite a passage number per claim,
> quote figures exactly, and if two passages conflict say so rather than picking one.
>
> The app renders that prompt even in offline mode, so the grounding rules can be reviewed
> without an API key. And if a provider call fails, the extractive answer is the fallback -
> the demo never breaks."

---

## 7:50-8:50 - Results and honest limits

Run `pytest src/modules/knowledge_assistant_airline/` on camera, then the Benchmark tab.

> "Thirty-one tests, all passing. On the gold set: recall@4 100%, answer accuracy 100%,
> refusal accuracy 100%, precision@1 93.94%.
>
> That last number isn't 100 and I've left it visible. Two questions - the power bank one
> and the cabin liquids one - retrieve the baggage policy first where my label says
> restricted items. Both are arguably correct; the baggage policy genuinely does say power
> banks are never permitted in the hold. My gold set only allows one label per question, so
> they score as misses. Recall@4 is 100%, so the right document is always retrieved and
> always cited.
>
> I'd rather report that than quietly relabel the question."

---

## 8:50-9:30 - Deployment and close

Show `deploy_prep.py` output and the package folder.

> "For deployment, the shared `deploy_prep.py` is hardcoded to the group leader's chatbot
> module, and it's a shared file other members' PRs touch. So I wrote a module-local
> packager, following the precedent from the tutor deploy package.
>
> It copies the module with its import paths unchanged - the deployed code is byte-identical
> to the reviewed code, so no import rewriting can silently change behaviour between them.
> I verified the standalone package runs on its own before deploying.
>
> That's the module: seven documents, 48 chunks, four hallucination controls, and a
> benchmark that measures all three ways it could fail an agent. Thanks for watching."

---

## Recording checklist

- [ ] 1080p or better; editor font 16pt+
- [ ] Run the test suite live on camera, don't just claim it passes
- [ ] Drag the floor slider to zero on camera - show the failure
- [ ] State the precision@1 limitation out loud
- [ ] Keep total length between 5 and 10 minutes
