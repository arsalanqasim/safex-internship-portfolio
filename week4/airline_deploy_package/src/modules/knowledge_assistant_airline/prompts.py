"""Prompt templates for the Indus Air RAG knowledge assistant.

These templates are used when a hosted LLM provider is configured through
``LLM_PROVIDER``. In the default offline mode the deterministic composer in
``engine.py`` produces the answer instead, but the templates are still rendered and
surfaced in the UI so reviewers can inspect exactly what would be sent to a provider.

Every template is written to constrain the model to the retrieved context. The
grounding rules below are the prompt-side half of the hallucination controls; the
retrieval-side half is the similarity floor enforced in ``engine.py``.
"""

from __future__ import annotations

SYSTEM_PROMPT = """You are the Indus Air policy assistant. You answer questions from
passengers and from Indus Air contact-centre agents.

You must obey these rules without exception:

1. Answer only from the numbered context passages supplied in the user message. Treat
   them as the complete and only source of truth.
2. Never use general knowledge about airlines, other carriers, or industry norms. If the
   context does not contain the answer, you do not know it.
3. If the context does not answer the question, reply with exactly:
   "I could not find this in the Indus Air policy documents." Then name the closest
   related topic that is covered, and stop.
4. Cite the passage number for every factual claim, in the form [1] or [2][3].
5. Quote figures, fees, weights and time limits exactly as written in the context. Never
   round, convert, average or infer a number that is not present.
6. If two passages conflict, say so and cite both rather than choosing one.
7. Keep the answer under 120 words. Use short sentences. Do not add greetings, apologies
   or invitations to ask more questions."""

ANSWER_PROMPT = """Question from the passenger:
{question}

Context passages retrieved from the Indus Air policy library:
{context_block}

Write the answer now, following every rule in your instructions. Cite passage numbers."""

CONTEXT_PASSAGE_TEMPLATE = """[{index}] Source: {document} > {section}
{text}"""

# Used when the retriever returns nothing above the similarity floor. The model is not
# called at all in that case, but the template is kept so the refusal wording stays
# identical across offline mode and provider mode.
REFUSAL_TEMPLATE = """I could not find this in the Indus Air policy documents.

The closest topics covered in the current knowledge base are: {nearest_topics}.

If this question should be answerable, the policy library may need a new document or an
update to an existing one."""

FOLLOW_UP_PROMPT = """Earlier turns in this conversation:
{history_block}

The passenger has now asked:
{question}

Rewrite the passenger's latest question as a single standalone question that can be
understood without the earlier turns. Resolve pronouns such as "it", "that" and "they"
using the earlier turns. Change nothing else and add no new facts. Return only the
rewritten question."""


def build_context_block(passages: list[dict]) -> str:
    """Render retrieved passages into the numbered block the answer prompt expects."""
    rendered = []
    for index, passage in enumerate(passages, start=1):
        rendered.append(
            CONTEXT_PASSAGE_TEMPLATE.format(
                index=index,
                document=passage["document_title"],
                section=passage["section"],
                text=passage["text"].strip(),
            )
        )
    return "\n\n".join(rendered)


def build_answer_prompt(question: str, passages: list[dict]) -> str:
    """Render the full user-side prompt for a grounded answer."""
    return ANSWER_PROMPT.format(
        question=question.strip(),
        context_block=build_context_block(passages),
    )
