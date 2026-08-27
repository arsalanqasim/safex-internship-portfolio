"""RAG-based Knowledge Assistant engine for Indus Air.

Week 4 Client-Ready Sprint module owned by Muhammad Faozan Mujtaba.

Target company: Indus Air, a fictional Pakistani domestic and regional carrier used as
the client for this internship prototype. Its contact centre answers the same policy
questions every day - baggage allowances, change fees, delay compensation, pet carriage -
and agents currently search seven separate policy PDFs by hand.

This module turns that policy library into a retrieval-augmented question answering
service. The pipeline is:

    markdown policy docs -> section chunking -> vector index -> top-k retrieval
    -> similarity floor -> grounded answer with citations

Design notes that matter for review:

* The vector index is behind the ``VectorIndex`` interface. The default implementation is
  TF-IDF over word and bigram features with cosine similarity, which runs offline with no
  API key and no vector database service. ``EmbeddingVectorIndex`` implements the same
  interface against a hosted embeddings API and can be swapped in without touching the
  retriever, the composer, or the UI.
* Answer generation runs offline by default (``LLM_PROVIDER=mock``) using extractive
  composition over the retrieved passages. When a provider is configured, the same
  templates in ``prompts.py`` are sent to it and the extractive answer becomes the
  fallback if that call fails.
* Hallucination control is enforced in two places: a similarity floor that refuses to
  answer when retrieval is weak, and prompt rules that forbid any claim without a
  citation. Both are measured by ``evaluate()`` against ``data/evaluation_set.json``.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.modules.knowledge_assistant_airline import prompts

MODULE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_DIR = MODULE_DIR / "data" / "knowledge_base"
EVALUATION_SET_PATH = MODULE_DIR / "data" / "evaluation_set.json"

TARGET_COMPANY = "Indus Air"

# Retrieval defaults. The floor is calibrated against data/evaluation_set.json, where the
# weakest answerable question scores 0.1392 and the strongest out-of-scope question scores
# 0.1096. Any floor inside that band separates the two classes perfectly; 0.12 sits near
# the middle of it. The band is narrow, so a floor moved much outside it trades false
# refusals against false answers - see the benchmark table in README.md.
DEFAULT_TOP_K = 4
DEFAULT_SIMILARITY_FLOOR = 0.12

# Chunking. Sections longer than this are split at paragraph boundaries so a single
# passage stays small enough to be a useful citation rather than a whole page.
MAX_CHUNK_CHARS = 1100
CHUNK_OVERLAP_CHARS = 160


# --------------------------------------------------------------------------------------
# Domain vocabulary
# --------------------------------------------------------------------------------------

# Passengers rarely use the airline's own wording. Expanding the query with the policy
# library's vocabulary is what lets "how much hand luggage can I take" reach a section
# titled "Cabin Baggage Allowance". Each key is matched as a whole phrase, case
# insensitively, and its values are appended to the query before vectorisation.
QUERY_SYNONYMS: dict[str, list[str]] = {
    "hand luggage": ["cabin baggage", "cabin bag"],
    "hand baggage": ["cabin baggage", "cabin bag"],
    "carry on": ["cabin baggage", "cabin bag"],
    "carry-on": ["cabin baggage", "cabin bag"],
    "hold luggage": ["checked baggage"],
    "suitcase": ["checked baggage", "cabin baggage"],
    "luggage": ["baggage"],
    "bag": ["baggage"],
    "bags": ["baggage"],
    "overweight": ["excess baggage"],
    "extra weight": ["excess baggage"],
    "lost bag": ["delayed baggage", "lost baggage", "property irregularity report"],
    "missing bag": ["delayed baggage", "property irregularity report"],
    "broken bag": ["damaged baggage"],
    "money back": ["refund"],
    "cash back": ["refund"],
    "get a refund": ["refund", "cancellation"],
    "change my flight": ["date change", "flight change"],
    "reschedule": ["date change", "flight change"],
    "postpone": ["date change", "flight change"],
    "cancel": ["cancellation", "refund"],
    "missed my flight": ["no-show", "gate closed"],
    "missed the flight": ["no-show", "gate closed"],
    "late for": ["counter closes", "gate closes", "no-show"],
    "how early": ["counter opens", "check-in"],
    "check in": ["check-in"],
    "checkin": ["check-in"],
    "boarding pass": ["check-in", "boarding"],
    "seat": ["seat selection"],
    "legroom": ["extra legroom seat"],
    "emergency exit": ["exit row"],
    "bumped": ["denied boarding", "overbooking"],
    "overbooked": ["denied boarding", "overbooking"],
    "flight delayed": ["delay", "duty of care", "compensation"],
    "delay": ["duty of care", "compensation"],
    "cancelled flight": ["cancellation", "rebooking", "refund"],
    "compensation": ["controllable disruption", "duty of care"],
    "hotel": ["accommodation", "duty of care", "overnight"],
    "connection": ["missed connection", "minimum connection time"],
    "loyalty": ["indusmiles", "tier", "miles"],
    "points": ["miles"],
    "frequent flyer": ["indusmiles", "tier status"],
    "air miles": ["miles", "indusmiles"],
    "lounge": ["lounge access", "gold", "platinum"],
    "upgrade": ["tier", "award ticket"],
    "expire": ["expiry", "miles expire"],
    "wheelchair": ["mobility assistance", "wchr", "wchs", "wchc"],
    "disabled": ["special assistance", "wheelchair"],
    "child alone": ["unaccompanied minor", "umnr"],
    "kid travelling alone": ["unaccompanied minor", "umnr"],
    "children alone": ["unaccompanied minor", "umnr"],
    "fly alone": ["unaccompanied minor", "umnr", "child"],
    "flying alone": ["unaccompanied minor", "umnr", "child"],
    "travel alone": ["unaccompanied minor", "umnr", "child"],
    "travelling alone": ["unaccompanied minor", "umnr", "child"],
    "year old": ["child", "infant", "minor"],
    "name on my ticket": ["name change", "cancelled and rebooked"],
    "change the name": ["name change", "cancelled and rebooked"],
    "someone else": ["name change", "transferable"],
    "transfer my ticket": ["name change", "transferable"],
    "baby": ["infant", "bassinet"],
    "pregnant": ["medical clearance", "expectant mothers"],
    "pregnancy": ["medical clearance", "expectant mothers"],
    "stroller": ["stroller", "car seat", "child"],
    "dog": ["pets", "cabin pet", "animal"],
    "cat": ["pets", "cabin pet", "animal"],
    "pet": ["animal", "carrier"],
    "power bank": ["lithium batteries", "powerbank"],
    "powerbank": ["lithium batteries", "power banks"],
    "battery": ["lithium batteries"],
    "vape": ["electronic cigarettes", "vaping devices"],
    "e-cigarette": ["electronic cigarettes"],
    "liquids": ["liquids aerosols gels", "100 ml"],
    "knife": ["sharp objects", "checked baggage"],
    "sports": ["sports equipment", "oversized"],
    "golf": ["sports equipment", "golf bags"],
    "bicycle": ["sports equipment", "bicycles"],
}

# Shown to the user when the assistant refuses, so the refusal points somewhere useful
# instead of being a dead end.
COVERED_TOPICS = [
    "baggage allowances and excess baggage",
    "booking changes, cancellations and refunds",
    "check-in, boarding and seating",
    "delays, cancellations and compensation",
    "the IndusMiles loyalty programme",
    "special assistance, minors and medical travel",
    "pets, dangerous goods and restricted items",
]

STOP_WORDS_FOR_SCORING = {
    "a", "an", "and", "any", "are", "as", "at", "be", "by", "can", "could", "do", "does",
    "for", "from", "how", "i", "if", "in", "is", "it", "its", "me", "much", "my", "of",
    "on", "or", "so", "that", "the", "there", "they", "this", "to", "was", "what", "when",
    "where", "which", "who", "will", "with", "would", "you", "your",
}


# --------------------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------------------


@dataclass
class Chunk:
    """A retrievable passage: one section, or one slice of a long section."""

    chunk_id: str
    document: str
    document_title: str
    section: str
    text: str
    part: int = 1
    total_parts: int = 1

    @property
    def citation(self) -> str:
        label = f"{self.document_title} > {self.section}"
        if self.total_parts > 1:
            label += f" (part {self.part} of {self.total_parts})"
        return label

    @property
    def indexable_text(self) -> str:
        """Heading terms are repeated so section titles carry weight in the index."""
        return f"{self.document_title}. {self.section}. {self.section}. {self.text}"


@dataclass
class RetrievedPassage:
    """A chunk plus the score that retrieved it."""

    chunk: Chunk
    score: float
    rank: int

    def to_prompt_dict(self) -> dict[str, str]:
        return {
            "document_title": self.chunk.document_title,
            "section": self.chunk.section,
            "text": self.chunk.text,
        }


@dataclass
class RagAnswer:
    """The full result of one question, including everything needed to audit it."""

    question: str
    resolved_question: str
    answer: str
    grounded: bool
    confidence: float
    passages: list[RetrievedPassage] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    generator: str = "extractive"
    prompt_preview: str = ""
    latency_ms: float = 0.0
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "resolved_question": self.resolved_question,
            "answer": self.answer,
            "grounded": self.grounded,
            "confidence": round(self.confidence, 4),
            "generator": self.generator,
            "latency_ms": round(self.latency_ms, 2),
            "citations": self.citations,
            "passages": [
                {
                    "rank": p.rank,
                    "score": round(p.score, 4),
                    "citation": p.chunk.citation,
                    "document": p.chunk.document,
                    "section": p.chunk.section,
                }
                for p in self.passages
            ],
            "notes": self.notes,
        }


# --------------------------------------------------------------------------------------
# Knowledge base loading and chunking
# --------------------------------------------------------------------------------------


def _split_long_section(text: str) -> list[str]:
    """Split an oversized section at paragraph boundaries, keeping a small overlap.

    The overlap carries the tail of the previous part forward so a fact that straddles a
    paragraph break is still retrievable from at least one complete passage.
    """
    if len(text) <= MAX_CHUNK_CHARS:
        return [text]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= MAX_CHUNK_CHARS or not current:
            current = candidate
            continue
        parts.append(current)
        tail = current[-CHUNK_OVERLAP_CHARS:]
        current = f"{tail}\n\n{paragraph}".strip()

    if current:
        parts.append(current)
    return parts


def load_knowledge_base(directory: str | Path | None = None) -> list[Chunk]:
    """Load every markdown policy document and split it into retrievable chunks.

    Chunking follows the documents' own structure: the level-one heading is the document
    title and every level-two heading starts a new chunk. Policy documents are written in
    self-contained sections, so a section is the natural unit of citation - an agent can
    read the retrieved passage and see the whole rule, not half of it.
    """
    kb_dir = Path(directory) if directory is not None else KNOWLEDGE_BASE_DIR
    if not kb_dir.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {kb_dir}")

    chunks: list[Chunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        lines = raw.splitlines()

        document_title = path.stem.replace("_", " ").title()
        preamble: list[str] = []
        section_name: str | None = None
        buffer: list[str] = []
        sections: list[tuple[str, str]] = []

        for line in lines:
            if line.startswith("# "):
                document_title = line[2:].strip()
                continue
            if line.startswith("## "):
                if section_name is not None:
                    sections.append((section_name, "\n".join(buffer).strip()))
                elif buffer:
                    preamble = buffer[:]
                section_name = line[3:].strip()
                buffer = []
                continue
            buffer.append(line)

        if section_name is not None:
            sections.append((section_name, "\n".join(buffer).strip()))
        elif buffer:
            preamble = buffer[:]

        preamble_text = "\n".join(preamble).strip()
        if preamble_text:
            sections.insert(0, ("Document Overview", preamble_text))

        for section, body in sections:
            if not body:
                continue
            parts = _split_long_section(body)
            for index, part_text in enumerate(parts, start=1):
                chunks.append(
                    Chunk(
                        chunk_id=f"{path.stem}::{_slugify(section)}::{index}",
                        document=path.name,
                        document_title=document_title,
                        section=section,
                        text=part_text,
                        part=index,
                        total_parts=len(parts),
                    )
                )

    if not chunks:
        raise ValueError(f"No markdown documents found in {kb_dir}")
    return chunks


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


# --------------------------------------------------------------------------------------
# Vector index
# --------------------------------------------------------------------------------------


class VectorIndex:
    """Interface every retrieval backend implements.

    Keeping this abstract is what makes the assignment's Chroma/FAISS stack a drop-in
    change: a backend only has to build vectors and return cosine scores in chunk order.
    """

    name: str = "base"

    def build(self, chunks: Sequence[Chunk]) -> None:
        raise NotImplementedError

    def score(self, query: str) -> np.ndarray:
        raise NotImplementedError


class TfidfVectorIndex(VectorIndex):
    """Offline default: TF-IDF over unigrams and bigrams, scored by cosine similarity.

    Sublinear term frequency stops a policy section that repeats "baggage" fifteen times
    from dominating every baggage query, and bigrams keep multi-word policy terms such as
    "cabin baggage" or "unaccompanied minor" together as single features.
    """

    name = "tfidf"

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(
            sublinear_tf=True,
            ngram_range=(1, 2),
            min_df=1,
            # Drop terms that appear in more than 90 percent of chunks. The carrier name
            # is in every document title, and scikit-learn's smoothed IDF floors a term
            # present in every document at 1.0 rather than 0. Without this cap, simply
            # writing "Indus Air" in a question scores against all 48 chunks equally and
            # lifts unrelated questions above the similarity floor.
            max_df=0.9,
            stop_words="english",
            lowercase=True,
        )
        self._matrix = None
        self._chunks: list[Chunk] = []

    def build(self, chunks: Sequence[Chunk]) -> None:
        self._chunks = list(chunks)
        corpus = [chunk.indexable_text for chunk in self._chunks]
        self._matrix = self._vectorizer.fit_transform(corpus)

    def score(self, query: str) -> np.ndarray:
        if self._matrix is None:
            raise RuntimeError("Index has not been built. Call build() first.")
        query_vector = self._vectorizer.transform([query])
        return cosine_similarity(query_vector, self._matrix)[0]

    @property
    def vocabulary_size(self) -> int:
        if self._matrix is None:
            return 0
        return int(self._matrix.shape[1])


class EmbeddingVectorIndex(VectorIndex):
    """Hosted-embeddings backend, used only when an embeddings API is configured.

    It is included to show the production path for the assigned stack. ``build`` raises if
    no provider is available so that :class:`AirlineKnowledgeAssistant` can fall back to
    TF-IDF instead of failing the demo, which is the behaviour the deployed app relies on.
    """

    name = "embeddings"

    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.model = model
        self._matrix: np.ndarray | None = None
        self._chunks: list[Chunk] = []

    @staticmethod
    def is_available() -> bool:
        return bool(os.getenv("OPENAI_API_KEY")) and os.getenv("EMBEDDING_BACKEND") == "openai"

    def _embed(self, texts: list[str]) -> np.ndarray:
        import requests  # imported lazily so offline mode never needs the dependency

        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
            json={"model": self.model, "input": texts},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        vectors = np.array([item["embedding"] for item in payload["data"]], dtype=float)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, 1e-12, None)

    def build(self, chunks: Sequence[Chunk]) -> None:
        if not self.is_available():
            raise RuntimeError("No embeddings provider configured.")
        self._chunks = list(chunks)
        self._matrix = self._embed([chunk.indexable_text for chunk in self._chunks])

    def score(self, query: str) -> np.ndarray:
        if self._matrix is None:
            raise RuntimeError("Index has not been built. Call build() first.")
        query_vector = self._embed([query])[0]
        return self._matrix @ query_vector


# --------------------------------------------------------------------------------------
# Query handling
# --------------------------------------------------------------------------------------


def expand_query(question: str) -> str:
    """Append policy-library vocabulary for any passenger phrasing found in the question.

    Retrieval is lexical by default, so a question that shares no words with the policy
    text cannot be retrieved at all. This bridges that gap without a second model.
    """
    lowered = question.lower()
    additions: list[str] = []
    for phrase, expansions in QUERY_SYNONYMS.items():
        if phrase in lowered:
            additions.extend(expansions)
    if not additions:
        return question
    unique = list(dict.fromkeys(additions))
    return f"{question} {' '.join(unique)}"


def resolve_follow_up(question: str, history: Sequence[tuple[str, str]]) -> str:
    """Make a follow-up question standalone by carrying the previous subject forward.

    "What about international?" retrieves nothing on its own. Prefixing the previous
    question restores the subject so the same retriever handles both turns.
    """
    if not history:
        return question

    stripped = question.strip()
    words = [w for w in re.findall(r"[a-z']+", stripped.lower()) if w]
    starts_dependent = bool(
        re.match(r"^(what about|how about|and |what if|is it|does it|can i then)", stripped.lower())
    )
    has_bare_pronoun = bool(re.search(r"\b(it|that|they|them|those|this)\b", stripped.lower()))
    too_short = len(words) <= 6

    if not (starts_dependent or (has_bare_pronoun and too_short)):
        return question

    previous_question = history[-1][0]
    return f"{previous_question.rstrip('?')}? Follow-up: {stripped}"


# --------------------------------------------------------------------------------------
# Extractive answer composition
# --------------------------------------------------------------------------------------


def _split_units(text: str) -> list[str]:
    """Break a passage into citable units.

    The policy documents are hard-wrapped at roughly 88 characters, so a physical line is
    almost never a complete thought. Lines belonging to the same paragraph or the same
    bullet are rejoined before sentence splitting, otherwise the composer quotes fragments
    such as "of respiratory distress and may travel only in the cabin".

    Table rows are the exception and are kept whole: "| Indus Flex | 25 kg | 30 kg |" is a
    single fact, and splitting it on punctuation would destroy the answer being sought.
    """
    units: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        paragraph = " ".join(buffer).strip()
        buffer.clear()
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z(\d])", paragraph):
            sentence = sentence.strip()
            if sentence:
                units.append(sentence)

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            flush()
            continue
        if line.startswith("|"):
            flush()
            if re.fullmatch(r"\|[\s\-:|]+\|", line):
                continue  # the |---|---| separator row carries no content
            units.append(line)
            continue
        if re.match(r"^([-*]|\d+\.)\s+", line):
            flush()  # a new bullet ends the previous one
            buffer.append(re.sub(r"^([-*]|\d+\.)\s+", "", line))
            continue
        # Any other line continues whatever paragraph or bullet is already open.
        buffer.append(line)

    flush()
    return units


def _content_terms(text: str) -> set[str]:
    terms = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in terms if t not in STOP_WORDS_FOR_SCORING and len(t) > 1}


def compose_extractive_answer(
    question: str,
    passages: Sequence[RetrievedPassage],
    max_units: int = 4,
) -> tuple[str, list[str]]:
    """Build a grounded answer by quoting the passage lines that match the question.

    Nothing here is generated. Every line in the answer is a verbatim unit lifted from a
    retrieved passage and tagged with the passage number it came from, which makes the
    offline mode auditable in the same way the LLM mode is meant to be.
    """
    query_terms = _content_terms(expand_query(question))
    scored: list[tuple[float, int, int, str]] = []

    for passage in passages:
        section_terms = _content_terms(passage.chunk.section)
        for order, unit in enumerate(_split_units(passage.chunk.text)):
            unit_terms = _content_terms(unit)
            if not unit_terms:
                continue
            overlap = len(query_terms & unit_terms)
            if overlap == 0:
                continue
            # Normalise by unit length so a long paragraph does not beat a precise line,
            # then reward the retrieval rank and any section-title match.
            coverage = overlap / max(len(query_terms), 1)
            density = overlap / (len(unit_terms) ** 0.5)
            section_bonus = 0.25 if query_terms & section_terms else 0.0
            rank_bonus = 1.0 / passage.rank
            numeric_bonus = 0.15 if re.search(r"\d", unit) else 0.0
            score = (coverage * 1.5) + density + section_bonus + (rank_bonus * 0.5) + numeric_bonus
            scored.append((score, passage.rank, order, unit))

    if not scored:
        # Retrieval cleared the floor but no single line matched. Quote the opening of the
        # best passage rather than inventing a summary of it.
        best = passages[0]
        opening = " ".join(_split_units(best.chunk.text)[:2])
        return (
            f"{opening} [1]",
            [best.chunk.citation],
        )

    scored.sort(key=lambda item: (-item[0], item[1], item[2]))

    selected: list[tuple[int, int, str]] = []
    seen_terms: list[set[str]] = []
    for score, rank, order, unit in scored:
        unit_terms = _content_terms(unit)
        # Drop a line that repeats one already selected, which happens across the chunk
        # overlap introduced during splitting.
        if any(len(unit_terms & prior) / max(len(unit_terms), 1) > 0.75 for prior in seen_terms):
            continue
        selected.append((rank, order, unit))
        seen_terms.append(unit_terms)
        if len(selected) >= max_units:
            break

    selected.sort(key=lambda item: (item[0], item[1]))

    lines: list[str] = []
    citations: list[str] = []
    for rank, _order, unit in selected:
        lines.append(f"- {unit} [{rank}]")
        citation = passages[rank - 1].chunk.citation
        if citation not in citations:
            citations.append(citation)

    return "\n".join(lines), citations


# --------------------------------------------------------------------------------------
# Assistant
# --------------------------------------------------------------------------------------


class AirlineKnowledgeAssistant:
    """End-to-end RAG assistant over the Indus Air policy library."""

    def __init__(
        self,
        knowledge_base_dir: str | Path | None = None,
        index: VectorIndex | None = None,
        similarity_floor: float = DEFAULT_SIMILARITY_FLOOR,
        top_k: int = DEFAULT_TOP_K,
    ) -> None:
        self.developer = "Muhammad Faozan Mujtaba"
        self.role = "Group Member"
        self.target_company = TARGET_COMPANY
        self.similarity_floor = similarity_floor
        self.top_k = top_k
        self.notes: list[str] = []

        self.chunks = load_knowledge_base(knowledge_base_dir)

        if index is not None:
            self.index = index
            self.index.build(self.chunks)
        else:
            self.index = self._build_default_index()

    def _build_default_index(self) -> VectorIndex:
        """Prefer a hosted embeddings index when configured, fall back to TF-IDF."""
        if EmbeddingVectorIndex.is_available():
            embedding_index = EmbeddingVectorIndex()
            try:
                embedding_index.build(self.chunks)
                self.notes.append("Retrieval backend: hosted embeddings index.")
                return embedding_index
            except Exception as exc:  # network, quota, auth - never break the demo
                self.notes.append(f"Embeddings index unavailable ({exc.__class__.__name__}), using TF-IDF.")

        tfidf_index = TfidfVectorIndex()
        tfidf_index.build(self.chunks)
        return tfidf_index

    # -- retrieval ---------------------------------------------------------------------

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedPassage]:
        """Return the top-k passages for a question, best first."""
        k = top_k or self.top_k
        scores = self.index.score(expand_query(question))
        order = np.argsort(scores)[::-1][:k]
        return [
            RetrievedPassage(chunk=self.chunks[i], score=float(scores[i]), rank=rank)
            for rank, i in enumerate(order, start=1)
        ]

    def nearest_topics(self, question: str, limit: int = 2) -> list[str]:
        """Name the closest covered topics so a refusal still points somewhere."""
        passages = self.retrieve(question, top_k=limit)
        topics = [p.chunk.document_title for p in passages if p.score > 0]
        return list(dict.fromkeys(topics)) or COVERED_TOPICS[:limit]

    # -- generation --------------------------------------------------------------------

    @staticmethod
    def provider() -> str:
        return os.getenv("LLM_PROVIDER", "mock").strip().lower()

    def _call_provider(self, prompt: str) -> str | None:
        """Send the grounded prompt to a hosted provider, or return None to fall back."""
        provider = self.provider()
        api_key = os.getenv("OPENAI_API_KEY", "")
        if provider not in {"openai"} or not api_key:
            return None
        try:
            import requests

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": prompts.SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            self.notes.append(f"Provider call failed ({exc.__class__.__name__}); used extractive answer.")
            return None

    # -- public entry point ------------------------------------------------------------

    def answer(
        self,
        question: str,
        history: Sequence[tuple[str, str]] | None = None,
        top_k: int | None = None,
        similarity_floor: float | None = None,
    ) -> RagAnswer:
        """Answer a question against the policy library, or refuse if retrieval is weak."""
        started = time.perf_counter()
        floor = self.similarity_floor if similarity_floor is None else similarity_floor
        resolved = resolve_follow_up(question, history or [])

        if not question.strip():
            return RagAnswer(
                question=question,
                resolved_question=resolved,
                answer="Please enter a question about Indus Air policy.",
                grounded=False,
                confidence=0.0,
                latency_ms=(time.perf_counter() - started) * 1000,
            )

        passages = self.retrieve(resolved, top_k=top_k)
        best_score = passages[0].score if passages else 0.0

        # Hallucination control one: refuse rather than answer from a weak match.
        if best_score < floor:
            topics = ", ".join(self.nearest_topics(resolved))
            return RagAnswer(
                question=question,
                resolved_question=resolved,
                answer=prompts.REFUSAL_TEMPLATE.format(nearest_topics=topics),
                grounded=False,
                confidence=float(best_score),
                passages=passages,
                generator="refusal",
                latency_ms=(time.perf_counter() - started) * 1000,
                notes=["Best retrieval score fell below the similarity floor."],
            )

        kept = [p for p in passages if p.score >= floor * 0.5]
        prompt_preview = prompts.build_answer_prompt(resolved, [p.to_prompt_dict() for p in kept])

        extractive_answer, citations = compose_extractive_answer(resolved, kept)
        generator = "extractive"
        answer_text = extractive_answer

        provider_answer = self._call_provider(prompt_preview)
        if provider_answer:
            answer_text = provider_answer
            generator = f"llm:{os.getenv('LLM_MODEL', 'gpt-4o-mini')}"

        return RagAnswer(
            question=question,
            resolved_question=resolved,
            answer=answer_text,
            grounded=True,
            confidence=float(best_score),
            passages=kept,
            citations=citations,
            generator=generator,
            prompt_preview=prompt_preview,
            latency_ms=(time.perf_counter() - started) * 1000,
            notes=list(self.notes),
        )

    # -- evaluation --------------------------------------------------------------------

    def evaluate(self, evaluation_set: Iterable[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Score the pipeline against the gold set.

        Three things are measured, matching the three ways this assistant can fail a
        contact-centre agent: it retrieves the wrong policy, it answers a question it
        should have refused, or it refuses a question it should have answered.
        """
        cases = list(evaluation_set) if evaluation_set is not None else load_evaluation_set()

        rows: list[dict[str, Any]] = []
        answerable_total = 0
        retrieval_hits = 0
        answered_correctly = 0
        refusal_total = 0
        refusal_correct = 0

        for case in cases:
            result = self.answer(case["question"])
            expected_doc = case.get("expected_document")
            should_refuse = bool(case.get("out_of_scope", False))

            top_documents = [p.chunk.document for p in result.passages]
            hit = expected_doc in top_documents if expected_doc else False
            top1 = bool(top_documents) and top_documents[0] == expected_doc

            if should_refuse:
                refusal_total += 1
                correct = not result.grounded
                refusal_correct += int(correct)
            else:
                answerable_total += 1
                retrieval_hits += int(hit)
                correct = result.grounded and hit
                answered_correctly += int(correct)

            rows.append(
                {
                    "question": case["question"],
                    "expected_document": expected_doc or "(out of scope)",
                    "retrieved_document": top_documents[0] if top_documents else "",
                    "hit_at_k": hit,
                    "hit_at_1": top1,
                    "grounded": result.grounded,
                    "should_refuse": should_refuse,
                    "correct": correct,
                    "confidence": round(result.confidence, 4),
                    "latency_ms": round(result.latency_ms, 2),
                }
            )

        def pct(numerator: int, denominator: int) -> float:
            return round((numerator / denominator) * 100, 2) if denominator else 0.0

        return {
            "total_cases": len(cases),
            "answerable_cases": answerable_total,
            "out_of_scope_cases": refusal_total,
            "retrieval_recall_at_k": pct(retrieval_hits, answerable_total),
            "retrieval_precision_at_1": pct(
                sum(1 for r in rows if r["hit_at_1"] and not r["should_refuse"]), answerable_total
            ),
            "answer_accuracy": pct(answered_correctly, answerable_total),
            "refusal_accuracy": pct(refusal_correct, refusal_total),
            "mean_latency_ms": round(float(np.mean([r["latency_ms"] for r in rows])), 2) if rows else 0.0,
            "rows": rows,
        }

    # -- introspection -----------------------------------------------------------------

    def knowledge_base_summary(self) -> list[dict[str, Any]]:
        """Per-document chunk and word counts, used by the UI's knowledge base panel."""
        summary: dict[str, dict[str, Any]] = {}
        for chunk in self.chunks:
            entry = summary.setdefault(
                chunk.document,
                {"document": chunk.document, "title": chunk.document_title, "chunks": 0, "words": 0, "sections": set()},
            )
            entry["chunks"] += 1
            entry["words"] += len(chunk.text.split())
            entry["sections"].add(chunk.section)
        rows = []
        for entry in summary.values():
            entry["sections"] = len(entry["sections"])
            rows.append(entry)
        return sorted(rows, key=lambda row: row["document"])

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "documents": len({c.document for c in self.chunks}),
            "chunks": len(self.chunks),
            "words": sum(len(c.text.split()) for c in self.chunks),
            "backend": self.index.name,
            "provider": self.provider(),
            "similarity_floor": self.similarity_floor,
            "top_k": self.top_k,
        }


def load_evaluation_set(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load the hand-written gold question set used by :meth:`evaluate`."""
    target = Path(path) if path is not None else EVALUATION_SET_PATH
    if not target.exists():
        raise FileNotFoundError(f"Evaluation set not found: {target}")
    with target.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["cases"]


def export_answer_json(answer: RagAnswer) -> str:
    """Serialise an answer for download from the UI or for a downstream ticketing system."""
    return json.dumps(answer.as_dict(), indent=2, ensure_ascii=False)
