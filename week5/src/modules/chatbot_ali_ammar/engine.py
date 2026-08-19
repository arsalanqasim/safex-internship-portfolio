"""
ShopEase AI Customer Support Chatbot Engine
Developer: Ali Ammar Haider
Institution: COMSATS University Islamabad

Core AI & Logic Engine for:
- Hybrid TF-IDF / NLP similarity matching
- Dynamic confidence scoring (0.0 to 1.0)
- Explicit and confidence-threshold human escalation handoff
- Real-time conversation logging with latency metrics
- Safe fallback messaging preventing hallucinated policies
- No-code Admin CRUD (Create, Read, Update, Delete) & factory reset
- Analytics KPI calculations
- Automated benchmark test suite execution
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FAQ_FILE = DATA_DIR / "faq_knowledge_base.json"
LOG_FILE = DATA_DIR / "chat_logs.json"


DEFAULT_BUSINESS_INFO = {
    "name": "ShopEase",
    "industry": "E-commerce & Retail",
    "description": "ShopEase is a leading online retail store offering fashion, electronics, home accessories, and lifestyle products.",
    "support_hours": "Monday to Saturday, 9:00 AM to 6:00 PM EST",
    "support_email": "support@shopease-demo.com",
    "support_phone": "+1 (800) 555-EASE",
}

DEFAULT_FAQS: List[Dict[str, Any]] = [
    {
        "id": "FAQ001",
        "category": "Orders",
        "question": "How can I track my order or package?",
        "answer": "You can track your order using the tracking link sent to your email after dispatch. You can also view live status in your ShopEase Account under 'My Orders'.",
        "keywords": ["track order", "order tracking", "where is my order", "package status", "parcel location", "delivery status", "check order"]
    },
    {
        "id": "FAQ002",
        "category": "Shipping",
        "question": "How long does delivery take?",
        "answer": "Standard delivery usually takes 3 to 5 business days. Express shipping arrives in 1 to 2 business days depending on your location.",
        "keywords": ["delivery time", "shipping time", "how long delivery", "when will my order arrive", "shipping duration", "transit time"]
    },
    {
        "id": "FAQ003",
        "category": "Shipping",
        "question": "How much does shipping cost?",
        "answer": "Standard shipping is FREE for orders over $50. Orders under $50 incur a flat standard shipping fee of $5.00.",
        "keywords": ["shipping cost", "delivery charges", "shipping fee", "delivery fee", "free shipping", "shipping rates"]
    },
    {
        "id": "FAQ004",
        "category": "Returns",
        "question": "What is your return policy?",
        "answer": "ShopEase offers a 30-day hassle-free return policy. Unused items in original packaging with tags attached can be returned for a full refund.",
        "keywords": ["return policy", "return item", "can I return", "product return", "how to return", "return period", "30 days return"]
    },
    {
        "id": "FAQ005",
        "category": "Refunds",
        "question": "How long does a refund take to process?",
        "answer": "Once our warehouse receives and inspects your returned package, refunds are issued to your original payment method within 5 to 7 business days.",
        "keywords": ["refund", "refund time", "money back", "when refund", "reimbursement", "refund status"]
    },
    {
        "id": "FAQ006",
        "category": "Exchanges",
        "question": "Can I exchange an item for a different size or color?",
        "answer": "Yes! Exchanges are free within 30 days of delivery. You can start an exchange request through your account or by contacting support.",
        "keywords": ["exchange", "replace product", "change size", "change color", "swap item", "product exchange"]
    },
    {
        "id": "FAQ007",
        "category": "Cancellation",
        "question": "Can I cancel or modify my order after placing it?",
        "answer": "Orders can be cancelled or updated within 1 hour of placement. After 1 hour, processing begins and orders cannot be cancelled prior to delivery.",
        "keywords": ["cancel order", "order cancellation", "stop order", "cancel purchase", "modify order", "change address"]
    },
    {
        "id": "FAQ008",
        "category": "Payments",
        "question": "What payment methods do you accept?",
        "answer": "ShopEase accepts Visa, MasterCard, American Express, PayPal, Apple Pay, Google Pay, and Cash on Delivery (COD) in eligible regions.",
        "keywords": ["payment methods", "how can I pay", "payment options", "credit card", "debit card", "paypal", "apple pay"]
    },
    {
        "id": "FAQ009",
        "category": "Payments",
        "question": "Do you offer Cash on Delivery (COD)?",
        "answer": "Yes, Cash on Delivery is available for eligible domestic shipping addresses. Availability is confirmed at checkout.",
        "keywords": ["cash on delivery", "COD", "pay on delivery", "pay cash"]
    },
    {
        "id": "FAQ010",
        "category": "Problems",
        "question": "What should I do if I receive a damaged or incorrect item?",
        "answer": "We sincerely apologize! Please take clear photos of the damaged/wrong item and contact support within 48 hours for an immediate free replacement.",
        "keywords": ["damaged item", "wrong item", "incorrect product", "broken product", "defective item", "missing item"]
    },
    {
        "id": "FAQ011",
        "category": "Products",
        "question": "How can I check if an item is in stock?",
        "answer": "Product availability is shown live on each product detail page. If an item is sold out, click 'Notify Me' to receive an email alert upon restocking.",
        "keywords": ["product availability", "in stock", "stock status", "available product", "sold out", "restock"]
    },
    {
        "id": "FAQ012",
        "category": "Products",
        "question": "Where can I find size charts and product specifications?",
        "answer": "Detailed sizing charts, dimensions, material composition, and care instructions are located in the 'Specifications' tab on each product page.",
        "keywords": ["size chart", "specifications", "product details", "dimensions", "measurements", "fit guide"]
    },
    {
        "id": "FAQ013",
        "category": "Shipping",
        "question": "Do you offer international shipping?",
        "answer": "Yes, ShopEase ships to over 50 countries worldwide. International shipping fees and estimated delivery times are calculated at checkout.",
        "keywords": ["international shipping", "ship internationally", "overseas delivery", "global shipping", "foreign delivery"]
    },
    {
        "id": "FAQ014",
        "category": "Support",
        "question": "How can I contact ShopEase customer support?",
        "answer": "Reach out to our support team via email at support@shopease-demo.com or call +1 (800) 555-EASE during business hours (Mon-Sat, 9AM-6PM EST).",
        "keywords": ["contact support", "customer service", "support email", "phone number", "help desk", "talk to support"]
    },
    {
        "id": "FAQ015",
        "category": "Account",
        "question": "Do I need an account to place an order?",
        "answer": "No, you can check out as a guest. However, creating a free ShopEase account allows you to track orders faster, save wishlists, and store addresses.",
        "keywords": ["create account", "guest checkout", "register account", "sign up", "login", "account benefits"]
    }
]

BENCHMARK_TEST_CASES: List[Dict[str, Any]] = [
    {"query": "Where is my order right now?", "expected_faq": "FAQ001", "intent": "Order Tracking"},
    {"query": "Can I track my package location?", "expected_faq": "FAQ001", "intent": "Order Tracking"},
    {"query": "How long will delivery take to arrive?", "expected_faq": "FAQ002", "intent": "Shipping Duration"},
    {"query": "How much do I need to pay for shipping?", "expected_faq": "FAQ003", "intent": "Shipping Cost"},
    {"query": "What is the return policy window?", "expected_faq": "FAQ004", "intent": "Return Policy"},
    {"query": "When will my refund show up in my bank?", "expected_faq": "FAQ005", "intent": "Refund Processing"},
    {"query": "Can I exchange this shirt for a larger size?", "expected_faq": "FAQ006", "intent": "Exchanges"},
    {"query": "I want to cancel my order immediately", "expected_faq": "FAQ007", "intent": "Order Cancellation"},
    {"query": "Do you accept credit cards and PayPal?", "expected_faq": "FAQ008", "intent": "Payment Methods"},
    {"query": "Can I pay with cash on delivery?", "expected_faq": "FAQ009", "intent": "Cash on Delivery"},
    {"query": "My product arrived damaged and broken", "expected_faq": "FAQ010", "intent": "Damaged Product"},
    {"query": "Is this item available in stock?", "expected_faq": "FAQ011", "intent": "Product Stock"},
    {"query": "Where is the sizing chart and measurements?", "expected_faq": "FAQ012", "intent": "Size Guide"},
    {"query": "Do you ship packages internationally?", "expected_faq": "FAQ013", "intent": "International Shipping"},
    {"query": "How can I email customer service?", "expected_faq": "FAQ014", "intent": "Contact Support"},
    {"query": "I need to talk to a real human agent", "expected_faq": "HUMAN_HANDOFF", "intent": "Explicit Escalation"},
    {"query": "Do you sell commercial diesel aircraft engines?", "expected_faq": "FALLBACK", "intent": "Out of Scope"}
]


class CustomerSupportEngine:
    """Core AI engine for ShopEase customer support chatbot."""

    def __init__(self, confidence_threshold: float = 0.42) -> None:
        self.confidence_threshold = confidence_threshold
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.knowledge_base = self._load_or_create_kb()
        self.faqs: List[Dict[str, Any]] = self.knowledge_base.get("faqs", DEFAULT_FAQS)
        self.business_info: Dict[str, Any] = self.knowledge_base.get("business", DEFAULT_BUSINESS_INFO)
        self._ensure_log_file()
        self._build_vectorizer()

    # ------------------------------------------------------------------
    # Knowledge Base Persistence & Vectorizer
    # ------------------------------------------------------------------

    def _load_or_create_kb(self) -> Dict[str, Any]:
        """Load knowledge base from JSON or initialize default."""
        if FAQ_FILE.exists():
            try:
                with FAQ_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "faqs" in data and len(data["faqs"]) > 0:
                        return data
            except Exception:
                pass
        kb = {"business": DEFAULT_BUSINESS_INFO, "faqs": DEFAULT_FAQS}
        self._save_kb(kb)
        return kb

    def _save_kb(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Save active knowledge base to JSON file."""
        if data is None:
            data = {"business": self.business_info, "faqs": self.faqs}
        with FAQ_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _ensure_log_file(self) -> None:
        """Ensure conversation log JSON file exists."""
        if not LOG_FILE.exists():
            with LOG_FILE.open("w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def _build_vectorizer(self) -> None:
        """Construct TF-IDF Matrix over questions & keywords."""
        self.corpus: List[str] = []
        for faq in self.faqs:
            q_text = faq.get("question", "")
            kw_text = " ".join(faq.get("keywords", []))
            cat_text = faq.get("category", "")
            combined = f"{q_text} {kw_text} {cat_text} {q_text}"
            self.corpus.append(combined.lower())

        if self.corpus:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.vectorizer = None
            self.tfidf_matrix = None

    # ------------------------------------------------------------------
    # Query Matching & TF-IDF Similarity
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Clean and normalize string."""
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text)

    def _calculate_hybrid_confidence(self, query: str, faq: Dict[str, Any], vector_idx: int) -> float:
        """Calculate hybrid confidence blending TF-IDF cosine similarity, token overlap & keyword matching."""
        norm_query = self._normalize_text(query)
        stop_words = {"a", "an", "the", "is", "are", "am", "i", "my", "me", "to", "of", "for", "on", "in", "and", "can", "do", "you", "your", "how", "what", "when", "where", "does", "it", "this", "that", "there", "with", "much", "many", "will"}

        query_tokens = {w for w in norm_query.split() if w not in stop_words and len(w) > 1}

        # 1. TF-IDF Cosine Similarity
        tfidf_score = 0.0
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                q_vec = self.vectorizer.transform([norm_query])
                sim = cosine_similarity(q_vec, self.tfidf_matrix[vector_idx])[0][0]
                tfidf_score = float(sim)
            except Exception:
                tfidf_score = 0.0

        # 2. Exact match check
        norm_question = self._normalize_text(faq.get("question", ""))
        if norm_query == norm_question or norm_query in norm_question or norm_question in norm_query:
            return round(max(0.95, tfidf_score), 3)

        # 3. Token Overlap Score
        faq_text = f"{faq.get('question', '')} {' '.join(faq.get('keywords', []))}"
        faq_tokens = {w for w in self._normalize_text(faq_text).split() if w not in stop_words and len(w) > 1}

        overlap_score = 0.0
        if query_tokens and faq_tokens:
            overlap = len(query_tokens & faq_tokens)
            overlap_score = overlap / len(query_tokens)

        # 4. Keyword Match Boost
        keywords = faq.get("keywords", [])
        kw_hits = 0.0
        for kw in keywords:
            norm_kw = self._normalize_text(kw)
            if norm_kw in norm_query or norm_query in norm_kw:
                kw_hits += 2.0
            else:
                kw_words = {w for w in norm_kw.split() if w not in stop_words}
                if kw_words and kw_words.intersection(query_tokens):
                    kw_hits += 1.0

        kw_score = min(kw_hits / 2.0, 1.0)

        # Combined score taking maximum of component strengths
        blend = (tfidf_score * 0.35) + (overlap_score * 0.45) + (kw_score * 0.20)
        final_score = max(tfidf_score, overlap_score, blend)
        return round(min(max(final_score, 0.0), 1.0), 3)

    def find_best_faq(self, user_query: str) -> Optional[Dict[str, Any]]:
        """Find FAQ with highest confidence score."""
        if not user_query.strip() or not self.faqs:
            return None

        best_faq: Optional[Dict[str, Any]] = None
        best_score = 0.0

        for idx, faq in enumerate(self.faqs):
            score = self._calculate_hybrid_confidence(user_query, faq, idx)
            if score > best_score:
                best_score = score
                best_faq = {**faq, "confidence": score}

        return best_faq

    # ------------------------------------------------------------------
    # Human Escalation Detection
    # ------------------------------------------------------------------

    @staticmethod
    def _needs_human_handoff(user_query: str) -> bool:
        """Detect explicit requests to speak with a human support agent."""
        norm = CustomerSupportEngine._normalize_text(user_query)
        phrases = [
            "human", "real person", "agent", "representative",
            "talk to someone", "speak to someone", "speak with someone", "manager",
            "escalate", "operator", "person", "support staff", "help desk guy"
        ]
        return any(phrase in norm for phrase in phrases)

    def _human_handoff_response(self) -> str:
        """Format human escalation notification message."""
        return (
            "Connecting you to ShopEase Priority Support...\n\n"
            f"An agent will be with you shortly. You can also contact us directly at "
            f"**{self.business_info.get('support_email')}** or call **{self.business_info.get('support_phone')}** "
            f"({self.business_info.get('support_hours')})."
        )

    @staticmethod
    def _fallback_response() -> str:
        """Safe fallback message when inquiry is out-of-scope or below confidence threshold."""
        return (
            "I'm sorry, I don't have enough information to answer that accurately. "
            "I don't want to give you incorrect information. "
            "Please contact ShopEase support at **support@shopease-demo.com** or call **+1 (800) 555-EASE**, "
            "and our team will be delighted to assist you!"
        )

    # ------------------------------------------------------------------
    # Main Chat Generator
    # ------------------------------------------------------------------

    def get_response(self, user_query: str) -> Dict[str, Any]:
        """
        Process customer inquiry and return structured response.

        Returns dict with keys:
        - response (str)
        - confidence (float)
        - matched_faq (str or None)
        - category (str)
        - human_handoff (bool)
        - response_time_ms (float)
        """
        start_time = time.perf_counter()
        cleaned_query = user_query.strip()

        if not cleaned_query:
            result = {
                "response": "Hello! Welcome to ShopEase. How can I help you today?",
                "confidence": 1.0,
                "matched_faq": None,
                "category": "Greeting",
                "human_handoff": False,
            }
            self._log_conversation(cleaned_query, result, start_time)
            return result

        # 1. Explicit Human Request Check
        if self._needs_human_handoff(cleaned_query):
            result = {
                "response": self._human_handoff_response(),
                "confidence": 1.0,
                "matched_faq": "HUMAN_HANDOFF",
                "category": "Human Escalation",
                "human_handoff": True,
            }
            self._log_conversation(cleaned_query, result, start_time)
            return result

        # 2. FAQ Matching
        best_faq = self.find_best_faq(cleaned_query)

        if best_faq is None:
            result = {
                "response": self._fallback_response(),
                "confidence": 0.0,
                "matched_faq": None,
                "category": "Out of Scope",
                "human_handoff": True,
            }
            self._log_conversation(cleaned_query, result, start_time)
            return result

        confidence = best_faq["confidence"]

        # 3. Threshold Check
        if confidence >= self.confidence_threshold:
            result = {
                "response": best_faq["answer"],
                "confidence": confidence,
                "matched_faq": best_faq["id"],
                "category": best_faq.get("category", "General"),
                "human_handoff": False,
            }
        else:
            result = {
                "response": self._fallback_response(),
                "confidence": confidence,
                "matched_faq": best_faq["id"],
                "category": best_faq.get("category", "Low Confidence"),
                "human_handoff": True,
            }

        self._log_conversation(cleaned_query, result, start_time)
        return result

    # ------------------------------------------------------------------
    # Conversation Logging
    # ------------------------------------------------------------------

    def _log_conversation(
        self,
        user_query: str,
        result: Dict[str, Any],
        start_time: float,
    ) -> None:
        """Append interaction log to chat_logs.json."""
        end_time = time.perf_counter()
        response_time_ms = round((end_time - start_time) * 1000, 2)
        result["response_time_ms"] = response_time_ms

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_query": user_query,
            "bot_response": result["response"],
            "confidence": result["confidence"],
            "matched_faq": result["matched_faq"],
            "category": result.get("category", "General"),
            "human_handoff": result["human_handoff"],
            "response_time_ms": response_time_ms,
        }

        try:
            with LOG_FILE.open("r", encoding="utf-8") as f:
                logs = json.load(f)
            if not isinstance(logs, list):
                logs = []
        except Exception:
            logs = []

        logs.append(log_entry)

        try:
            with LOG_FILE.open("w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get_chat_logs(self) -> List[Dict[str, Any]]:
        """Retrieve conversation log history."""
        if not LOG_FILE.exists():
            return []
        try:
            with LOG_FILE.open("r", encoding="utf-8") as f:
                logs = json.load(f)
                return logs if isinstance(logs, list) else []
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Admin CRUD Operations
    # ------------------------------------------------------------------

    def add_faq(self, category: str, question: str, answer: str, keywords: List[str]) -> Tuple[bool, str]:
        """Add a new FAQ entry to knowledge base."""
        if not question.strip() or not answer.strip():
            return False, "Question and Answer cannot be empty."

        next_num = len(self.faqs) + 1
        faq_id = f"FAQ{next_num:03d}"
        while any(f["id"] == faq_id for f in self.faqs):
            next_num += 1
            faq_id = f"FAQ{next_num:03d}"

        new_faq = {
            "id": faq_id,
            "category": category.strip() or "General",
            "question": question.strip(),
            "answer": answer.strip(),
            "keywords": [k.strip() for k in keywords if k.strip()],
        }

        self.faqs.append(new_faq)
        self._save_kb()
        self._build_vectorizer()
        return True, f"Successfully created FAQ `{faq_id}`."

    def update_faq(self, faq_id: str, category: str, question: str, answer: str, keywords: List[str]) -> Tuple[bool, str]:
        """Update an existing FAQ entry by ID."""
        for idx, faq in enumerate(self.faqs):
            if faq["id"] == faq_id:
                self.faqs[idx] = {
                    "id": faq_id,
                    "category": category.strip() or "General",
                    "question": question.strip(),
                    "answer": answer.strip(),
                    "keywords": [k.strip() for k in keywords if k.strip()],
                }
                self._save_kb()
                self._build_vectorizer()
                return True, f"Successfully updated `{faq_id}`."
        return False, f"FAQ with ID `{faq_id}` not found."

    def delete_faq(self, faq_id: str) -> Tuple[bool, str]:
        """Delete an FAQ entry by ID."""
        initial_count = len(self.faqs)
        self.faqs = [f for f in self.faqs if f["id"] != faq_id]
        if len(self.faqs) < initial_count:
            self._save_kb()
            self._build_vectorizer()
            return True, f"Successfully deleted FAQ `{faq_id}`."
        return False, f"FAQ with ID `{faq_id}` not found."

    def reset_factory_faqs(self) -> Tuple[bool, str]:
        """Reset knowledge base to factory default FAQs."""
        self.faqs = list(DEFAULT_FAQS)
        self.business_info = dict(DEFAULT_BUSINESS_INFO)
        self._save_kb()
        self._build_vectorizer()
        return True, "Knowledge Base reset to default 15 FAQs."

    # ------------------------------------------------------------------
    # Analytics & KPIs
    # ------------------------------------------------------------------

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate live analytics KPIs from interaction logs."""
        logs = self.get_chat_logs()
        total_queries = len(logs)

        if total_queries == 0:
            return {
                "total_conversations": 0,
                "avg_confidence_pct": 0.0,
                "handoff_rate_pct": 0.0,
                "resolution_rate_pct": 100.0,
                "avg_latency_ms": 0.0,
                "low_confidence_count": 0,
            }

        confidences = [l.get("confidence", 0.0) for l in logs]
        handoffs = [1 for l in logs if l.get("human_handoff")]
        latencies = [l.get("response_time_ms", 0.0) for l in logs]

        avg_conf = float(np.mean(confidences)) * 100.0 if confidences else 0.0
        handoff_rate = (len(handoffs) / total_queries) * 100.0
        resolution_rate = 100.0 - handoff_rate
        avg_latency = float(np.mean(latencies)) if latencies else 0.0
        low_conf_count = len([c for c in confidences if c < self.confidence_threshold])

        return {
            "total_conversations": total_queries,
            "avg_confidence_pct": round(avg_conf, 1),
            "handoff_rate_pct": round(handoff_rate, 1),
            "resolution_rate_pct": round(resolution_rate, 1),
            "avg_latency_ms": round(avg_latency, 2),
            "low_confidence_count": low_conf_count,
        }

    # ------------------------------------------------------------------
    # Benchmark Runner
    # ------------------------------------------------------------------

    def run_benchmark_suite(self) -> Dict[str, Any]:
        """Execute automated benchmark test suite against current model."""
        test_results = []
        passed_count = 0
        latencies = []

        for item in BENCHMARK_TEST_CASES:
            query = item["query"]
            expected = item["expected_faq"]
            intent = item["intent"]

            start_t = time.perf_counter()
            res = self.get_response(query)
            latency = round((time.perf_counter() - start_t) * 1000, 2)
            latencies.append(latency)

            matched_id = res["matched_faq"]
            is_pass = False

            if expected == "HUMAN_HANDOFF":
                is_pass = res["human_handoff"] and (matched_id == "HUMAN_HANDOFF" or res["confidence"] == 1.0)
            elif expected == "FALLBACK":
                is_pass = res["human_handoff"] and (matched_id is None or res["confidence"] < self.confidence_threshold)
            else:
                is_pass = (matched_id == expected) and (res["confidence"] >= self.confidence_threshold)

            if is_pass:
                passed_count += 1

            test_results.append({
                "query": query,
                "intent": intent,
                "expected": expected,
                "actual": matched_id or ("FALLBACK" if res["human_handoff"] else "UNKNOWN"),
                "confidence": res["confidence"],
                "status": "PASS" if is_pass else "FAIL",
                "latency_ms": latency,
                "human_handoff": res["human_handoff"],
            })

        total_tests = len(BENCHMARK_TEST_CASES)
        accuracy = round((passed_count / total_tests) * 100.0, 1) if total_tests > 0 else 0.0
        avg_lat = round(float(np.mean(latencies)), 2) if latencies else 0.0

        return {
            "total_tests": total_tests,
            "passed_tests": passed_count,
            "accuracy_pct": accuracy,
            "avg_latency_ms": avg_lat,
            "results": test_results,
        }


if __name__ == "__main__":
    engine = CustomerSupportEngine()
    print("\nShopEase AI Customer Support Engine — Test Run")
    print("=" * 60)

    sample_queries = [
        "Where is my order right now?",
        "How much does shipping cost?",
        "Can I return an item?",
        "I want to speak with a human support agent",
        "Do you sell quantum teleportation devices?"
    ]

    for q in sample_queries:
        out = engine.get_response(q)
        print(f"\nQuery: '{q}'")
        print(f"Confidence: {out['confidence']:.2f} | Handoff: {out['human_handoff']} | FAQ: {out['matched_faq']}")
        print(f"Response: {out['response'][:100]}...")
