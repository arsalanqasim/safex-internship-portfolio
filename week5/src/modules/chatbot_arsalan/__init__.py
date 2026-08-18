"""Client-Ready AI Customer Support Chatbot Module (Arsalan Qasim - Week 5)."""

from .engine import (
    load_faq_knowledge_base,
    save_faq_knowledge_base,
    generate_chat_response,
    run_benchmark_tests,
    calculate_kpis,
)
from .ui import render_ui

__all__ = [
    "load_faq_knowledge_base",
    "save_faq_knowledge_base",
    "generate_chat_response",
    "run_benchmark_tests",
    "calculate_kpis",
    "render_ui",
]
