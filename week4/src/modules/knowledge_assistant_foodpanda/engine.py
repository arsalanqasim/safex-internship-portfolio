# RAG-based Knowledge Assistant - Engine
# Developer: Ali Zaib (Group Member)
# For SafeX Solutions Week 4 Client-Ready AI & Automation Suite
#
# This is the same proven RAG pipeline built and evaluated in Week 3
# (100% retrieval accuracy on a 14-question test log — see
# week3/src/modules/doc_knowledge_assistant/README.md for the full
# development writeup), repackaged here as a client-facing, deployable
# module for Week 4:
#
#   Documents -> Chunking -> TF-IDF Embedding -> In-Memory Vector Store
#             -> Query -> Top-K Retrieval (cosine similarity)
#             -> Answer Synthesis (extractive by default; optional LLM API)
#
# Target company: "QuickBite" (an original, fictional food-delivery
# company standing in for a Foodpanda-style client per the assignment's
# substitution note — see README.md). All knowledge-base documents are
# original content written for this exercise, not sourced from any real
# company's actual policies, so there is no copyright/reproduction concern.
#
# Retrieval and embedding are fully local (TF-IDF + cosine similarity),
# consistent with this repo's established pattern (see the Week 1 FAQ
# chatbot and Week 3 customer_support_chatbot modules) and matching the
# `LLM_PROVIDER=mock` default already scaffolded in week3/.env.example.
# Generation is a pluggable step: the default "mock" mode assembles an
# answer directly from the retrieved chunks (no external API needed, so
# the module always runs standalone); "openai" and "gemini" modes are
# also implemented for anyone who configures a real API key later.

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_DOCS_DIR = Path(__file__).parent / "data" / "knowledge_base"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.12  # below this, we abstain rather than guess


class DocKnowledgeAssistantError(ValueError):
    """Raised for invalid inputs (empty query, unknown provider, etc.)."""


@dataclass
class Chunk:
    chunk_id: str
    doc_title: str
    source_file: str
    section: str
    text: str


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass
class AnswerResult:
    query: str
    answer: str
    abstained: bool
    retrieved: list[RetrievedChunk] = field(default_factory=list)


def _split_into_chunks(raw_text: str, doc_title: str, source_file: str) -> list[Chunk]:
    """Chunk a markdown document by its '## ' section headers, then by
    paragraph if a section is still long. Each chunk keeps its section
    heading as light metadata/context for more readable citations."""
    sections = re.split(r"\n(?=## )", raw_text.strip())
    chunks: list[Chunk] = []
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        heading_match = re.match(r"^#{1,2}\s*(.+)", section)
        heading = heading_match.group(1).strip() if heading_match else doc_title
        body = re.sub(r"^#{1,2}\s*.+\n?", "", section, count=1).strip()
        if not body:
            continue
        chunks.append(Chunk(
            chunk_id=f"{source_file}::{i}",
            doc_title=doc_title,
            source_file=source_file,
            section=heading,
            text=body,
        ))
    return chunks


class DocKnowledgeAssistantEngine:
    """
    RAG-style knowledge-base assistant.

    Loads markdown documents from `docs_dir`, chunks them by section,
    embeds every chunk with TF-IDF, and answers questions by retrieving
    the most similar chunks and synthesizing a response from them.
    """

    def __init__(self, docs_dir: Path | str = DEFAULT_DOCS_DIR, llm_provider: str | None = None):
        self.docs_dir = Path(docs_dir)
        self.llm_provider = (llm_provider or os.getenv("LLM_PROVIDER", "mock")).lower()
        self.chunks: list[Chunk] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.chunk_matrix = None
        self._build_index()

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------
    def _build_index(self) -> None:
        """Load every .md file in docs_dir, chunk it, and fit the TF-IDF
        vectorizer over all chunks (this is the "embed + store in a
        vector DB" step — the vectorizer + matrix act as an in-memory
        vector store, appropriate at this small scale; the retrieval
        interface below would not need to change if this were swapped
        for FAISS/Chroma later)."""
        if not self.docs_dir.exists():
            raise DocKnowledgeAssistantError(f"Knowledge base directory not found: {self.docs_dir}")

        self.chunks = []
        for path in sorted(self.docs_dir.glob("*.md")):
            raw = path.read_text(encoding="utf-8")
            title_match = re.match(r"^#\s*(.+)", raw.strip())
            doc_title = title_match.group(1).strip() if title_match else path.stem
            self.chunks.extend(_split_into_chunks(raw, doc_title, path.name))

        if not self.chunks:
            raise DocKnowledgeAssistantError(f"No documents found in {self.docs_dir}")

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
        # Boost each chunk's section heading into its embedding text (repeated,
        # not just once) so short, topical headings carry real weight in the
        # TF-IDF space — this matters a lot for small, single-topic documents
        # like these, where the body text alone often shares generic words
        # ("delivery", "order") across many unrelated chunks. The heading
        # boost is used only for embedding/retrieval; chunk.text (returned to
        # the user) stays exactly as written in the source document.
        embedding_texts = [f"{c.section}. {c.section}. {c.text}" for c in self.chunks]
        self.chunk_matrix = self.vectorizer.fit_transform(embedding_texts)

    def document_titles(self) -> list[str]:
        return sorted({c.doc_title for c in self.chunks})

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = TOP_K) -> list[RetrievedChunk]:
        if not query or not query.strip():
            raise DocKnowledgeAssistantError("Query must not be empty.")

        query_vec = self.vectorizer.transform([query.strip()])
        scores = cosine_similarity(query_vec, self.chunk_matrix).flatten()
        order = np.argsort(scores)[::-1][:top_k]
        return [RetrievedChunk(chunk=self.chunks[i], score=round(float(scores[i]), 3)) for i in order]

    # ------------------------------------------------------------------
    # Answer synthesis
    # ------------------------------------------------------------------
    def answer(self, query: str, top_k: int = TOP_K) -> AnswerResult:
        """Retrieve relevant chunks and synthesize an answer. If the top
        match is below SIMILARITY_THRESHOLD, abstain instead of guessing
        — this is the module's main hallucination-mitigation control."""
        retrieved = self.retrieve(query, top_k=top_k)

        if not retrieved or retrieved[0].score < SIMILARITY_THRESHOLD:
            return AnswerResult(
                query=query,
                answer=(
                    "I don't have information about that in the QuickBite knowledge base "
                    "I was given. Please contact support directly for this question, or "
                    "rephrase it if you think it should be covered."
                ),
                abstained=True,
                retrieved=retrieved,
            )

        if self.llm_provider == "mock":
            answer_text = self._synthesize_extractive(query, retrieved)
        elif self.llm_provider in {"openai", "gemini"}:
            answer_text = self._synthesize_with_llm(query, retrieved)
        else:
            raise DocKnowledgeAssistantError(
                f"Unknown LLM_PROVIDER '{self.llm_provider}'. Use 'mock', 'openai', or 'gemini'."
            )

        return AnswerResult(query=query, answer=answer_text, abstained=False, retrieved=retrieved)

    @staticmethod
    def _synthesize_extractive(query: str, retrieved: list[RetrievedChunk]) -> str:
        """Default, API-free answer synthesis: return the best-matching
        chunk's own text (original content written for this module),
        with its source cited. This keeps the module fully runnable
        without any API key, and keeps answers grounded — the assistant
        can only ever say what's actually written in the source chunk."""
        best = retrieved[0]
        answer = best.chunk.text
        if len(retrieved) > 1 and retrieved[1].score >= SIMILARITY_THRESHOLD:
            answer += f"\n\nRelated: {retrieved[1].chunk.text}"
        answer += f"\n\n_Source: {best.chunk.doc_title} — \"{best.chunk.section}\"_"
        return answer

    def _synthesize_with_llm(self, query: str, retrieved: list[RetrievedChunk]) -> str:
        """Optional real-LLM generation path. Not required for the
        graded deliverable (no API key is available in this evaluation
        environment), but implemented so the pipeline is genuinely
        pluggable, matching the LLM_PROVIDER switch already scaffolded
        in week3/.env.example."""
        context = "\n\n".join(f"[{r.chunk.section}] {r.chunk.text}" for r in retrieved)
        prompt = (
            "Answer the question using ONLY the context below. "
            "If the context doesn't contain the answer, say so — do not guess.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        )

        if self.llm_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise DocKnowledgeAssistantError("OPENAI_API_KEY is not set in the environment.")
            try:
                import openai
            except ImportError:
                raise DocKnowledgeAssistantError("The 'openai' package is not installed.")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        if self.llm_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise DocKnowledgeAssistantError("GEMINI_API_KEY is not set in the environment.")
            try:
                import google.generativeai as genai
            except ImportError:
                raise DocKnowledgeAssistantError("The 'google-generativeai' package is not installed.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model.generate_content(prompt).text

        raise DocKnowledgeAssistantError(f"Unsupported LLM provider: {self.llm_provider}")

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
    def run_evaluation(self, test_suite: list[dict]) -> dict:
        """Run a labeled test suite of {"query", "expected_doc" or None}
        items and report retrieval accuracy: for answerable questions,
        did we retrieve/answer from the correct document? For
        deliberately out-of-scope questions (expected_doc=None), did we
        correctly abstain instead of hallucinating?"""
        results = []
        correct = 0

        for case in test_suite:
            query = case["query"]
            expected_doc = case.get("expected_doc")
            result = self.answer(query)

            if expected_doc is None:
                passed = result.abstained
            else:
                passed = (not result.abstained) and result.retrieved and \
                    result.retrieved[0].chunk.doc_title == expected_doc

            if passed:
                correct += 1

            results.append({
                "query": query,
                "expected_doc": expected_doc,
                "abstained": result.abstained,
                "top_doc": result.retrieved[0].chunk.doc_title if result.retrieved else None,
                "top_score": result.retrieved[0].score if result.retrieved else 0.0,
                "passed": passed,
            })

        total = len(test_suite)
        accuracy = round(100.0 * correct / total, 1) if total else 0.0
        return {"total": total, "correct": correct, "accuracy_percent": accuracy, "results": results}
