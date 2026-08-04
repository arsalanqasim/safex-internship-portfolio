"""AI Customer Support Chatbot Deployment Engine.

Handles intent classification, error validation, dynamic brand configuration,
and human escalation triggers for client-ready deployment.
"""

from __future__ import annotations

import json
import re
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ base with template variable for brand name
FAQ_TEMPLATE_KB = [
    {
        "id": "order_tracking",
        "category": "Logistics & Orders",
        "intent": "Track Order Status",
        "patterns": [
            "Where is my order",
            "Where is my package",
            "How can I track my shipment",
            "Track my package status",
            "When will my order arrive",
            "Check my delivery status",
            "My tracking link is not updating"
        ],
        "response": "You can track your package in real-time by entering your 8-digit Order ID in the '{brand_name}' portal. Standard delivery takes 3-5 business days.",
        "requires_escalation": False
    },
    {
        "id": "returns_refunds",
        "category": "Policies",
        "intent": "Return & Refund Policy",
        "patterns": [
            "What is your return policy",
            "How to exchange an item for another size",
            "I want a refund on my order",
            "How many days do I have to return an item",
            "Can I get money back if it doesn't fit"
        ],
        "response": "We offer a 14-day hassle-free return and exchange policy for unused items with tags intact. Returns can be initiated online or at any '{brand_name}' retail store.",
        "requires_escalation": False
    },
    {
        "id": "sizing_fit",
        "category": "Product Info",
        "intent": "Sizing & Fit Guide",
        "patterns": [
            "How do I choose the right size",
            "Is your clothing true to size",
            "Do you have a size chart",
            "What size should I order",
            "Are your shirts slim fit or regular fit"
        ],
        "response": "Our products run true to size. Please check our interactive Size Guide on every product page. For '{brand_name}' apparel, we recommend checking the size chart before checking out.",
        "requires_escalation": False
    },
    {
        "id": "shipping_delivery",
        "category": "Logistics & Orders",
        "intent": "Shipping Rates & Delivery",
        "patterns": [
            "How much is shipping",
            "Is delivery free",
            "What are your delivery charges",
            "Do you offer free shipping",
            "How long does shipping take"
        ],
        "response": "Flat shipping applies to all standard orders. Orders over our threshold qualify for FREE standard shipping nationwide! Deliveries take 3-5 business days.",
        "requires_escalation": False
    },
    {
        "id": "payment_discounts",
        "category": "Payments & Offers",
        "intent": "Payment Methods & Promo Codes",
        "patterns": [
            "What payment options do you accept",
            "Can I pay with Cash on Delivery",
            "How to apply promo code",
            "Do you accept credit card payments",
            "Cash on delivery available"
        ],
        "response": "We accept Cash on Delivery (COD), credit/debit cards, and mobile wallets. Enter promo codes at checkout in the 'Discount Code' field of '{brand_name}'.",
        "requires_escalation": False
    },
    {
        "id": "damaged_goods",
        "category": "Support Escalation",
        "intent": "Damaged or Wrong Item Received",
        "patterns": [
            "I received a damaged item",
            "You sent me the wrong item",
            "Stain on my clothes when opened",
            "Ripped seam on new trousers",
            "Wrong item in my parcel"
        ],
        "response": "We sincerely apologize for this inconvenience! We have logged your issue as urgent. A support representative from '{brand_name}' will contact you immediately to dispatch a free replacement.",
        "requires_escalation": True
    },
    {
        "id": "store_locations",
        "category": "Store Info",
        "intent": "Store Locations & Hours",
        "patterns": [
            "Where are your stores located",
            "Do you have a physical branch",
            "What are your store operating hours",
            "Where is your outlet",
            "Is your outlet open today"
        ],
        "response": "Our stores are open daily from 11:00 AM to 10:00 PM. Please visit the 'Stores' section on the '{brand_name}' website to find your nearest outlet.",
        "requires_escalation": False
    }
]

ESCALATION_KEYWORDS = [
    "scam", "fraud", "lawsuit", "legal action", "fake", "stole my money",
    "manager", "supervisor", "complain", "terrible service", "sue",
    "damaged", "broken", "wrong item", "ruined", "dispute", "refund", "cheated"
]

BENCHMARK_TEST_SUITE = [
    {"query": "Where is my order package?", "expected_intent": "Track Order Status"},
    {"query": "Can I return a shirt after 10 days?", "expected_intent": "Return & Refund Policy"},
    {"query": "What size should I get if my chest is 38?", "expected_intent": "Sizing & Fit Guide"},
    {"query": "Is shipping free if I purchase a lot?", "expected_intent": "Shipping Rates & Delivery"},
    {"query": "Do you accept Cash on Delivery?", "expected_intent": "Payment Methods & Promo Codes"},
    {"query": "My dress arrived torn and stained!", "expected_intent": "Damaged or Wrong Item Received"},
    {"query": "Where is your store located?", "expected_intent": "Store Locations & Hours"}
]


class CustomerSupportEngine:
    """Client-ready NLP chatbot engine with custom branding, LLM APIs, and error fallbacks."""

    def __init__(
        self,
        brand_name: str = "ThreadStyle Co.",
        confidence_threshold: float = 0.20,
        api_provider: str = None,
        api_key: str = None
    ):
        self.brand_name = brand_name
        self.confidence_threshold = confidence_threshold
        self.api_provider = api_provider
        self.api_key = api_key.strip().replace(" ", "").replace("\n", "").replace("\r", "") if api_key else None
        self._prepare_knowledge_base()
        self._prepare_vectorizer()

    def _prepare_knowledge_base(self) -> None:
        """Inject the user's custom brand name into the template responses."""
        self.knowledge_base = []
        for item in FAQ_TEMPLATE_KB:
            new_item = item.copy()
            new_item["response"] = item["response"].format(brand_name=self.brand_name)
            self.knowledge_base.append(new_item)

    def _prepare_vectorizer(self) -> None:
        """Fit TF-IDF vectorizer over all FAQ patterns."""
        self.documents = []
        self.intent_indices = []

        for idx, item in enumerate(self.knowledge_base):
            for pattern in item["patterns"]:
                self.documents.append(pattern)
                self.intent_indices.append(idx)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def _call_gemini_api(self, user_query: str) -> str:
        """Call Google Gemini API using direct requests."""
        if not self.api_key:
            raise ValueError("Gemini API Key is missing.")

        faq_data = json.dumps(self.knowledge_base, indent=2)
        system_prompt = (
            f"You are a professional, helpful customer support representative for the e-commerce clothing brand '{self.brand_name}'.\n"
            f"Here is the official store policy knowledge base (FAQ):\n{faq_data}\n\n"
            "Guidelines:\n"
            "1. Answer the customer's query accurately using the knowledge base policies where applicable.\n"
            "2. Adopt a helpful, warm, and professional tone.\n"
            f"3. Refer to the store as '{self.brand_name}'.\n"
            "4. If the query is outside the scope of the store policies, state that you cannot assist with that specific request and politely offer to escalate the customer to a live human agent.\n"
            "5. Keep responses concise (under 3-4 sentences).\n"
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_prompt}\n\nCustomer: {user_query}\nSupport Representative:"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 200
            }
        }

        response = requests.post(url, headers=headers, json=payload, timeout=8)
        response.raise_for_status()
        resp_json = response.json()

        try:
            return resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            raise ValueError("Failed to parse Gemini API response structure.")

    def _call_openai_api(self, user_query: str) -> str:
        """Call OpenAI Chat Completions API using direct requests."""
        if not self.api_key:
            raise ValueError("OpenAI API Key is missing.")

        faq_data = json.dumps(self.knowledge_base, indent=2)
        system_prompt = (
            f"You are a professional, helpful customer support representative for the e-commerce clothing brand '{self.brand_name}'.\n"
            f"Here is the official store policy knowledge base (FAQ):\n{faq_data}\n\n"
            "Guidelines:\n"
            "1. Answer the customer's query accurately using the knowledge base policies where applicable.\n"
            "2. Adopt a helpful, warm, and professional tone.\n"
            f"3. Refer to the store as '{self.brand_name}'.\n"
            "4. If the query is outside the scope of the store policies, state that you cannot assist with that specific request and politely offer to escalate the customer to a live human agent.\n"
            "5. Keep responses concise (under 3-4 sentences).\n"
        )

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            "temperature": 0.3,
            "max_tokens": 200
        }

        response = requests.post(url, headers=headers, json=payload, timeout=8)
        response.raise_for_status()
        resp_json = response.json()

        try:
            return resp_json["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            raise ValueError("Failed to parse OpenAI API response structure.")

    def classify_query(self, user_query: str) -> dict:
        """Classify user query intent, check error states, check escalation rules, and generate response."""
        cleaned_query = user_query.strip()

        # 1. Error Handling: Empty query check
        if not cleaned_query:
            return {
                "intent": "Error: Empty Input",
                "category": "Error Handling",
                "confidence": 0.0,
                "response": "It looks like you didn't type anything. Please ask a question so I can assist you!",
                "escalated": False,
                "escalation_reason": "Empty text submission"
            }

        # 2. Error Handling: Query length check
        if len(cleaned_query) > 300:
            return {
                "intent": "Error: Input Too Long",
                "category": "Error Handling",
                "confidence": 0.0,
                "response": "Your question is a bit too long for me to read (limit is 300 characters). Please shorten your inquiry or ask to speak to a human!",
                "escalated": False,
                "escalation_reason": f"Input length ({len(cleaned_query)} chars) exceeded limit"
            }

        # 3. Error Handling: Gibberish/Junk filter (Checks if short text has no vowels)
        if len(cleaned_query) >= 3 and not any(v in cleaned_query.lower() for v in ["a", "e", "i", "o", "u", "y"]):
            return {
                "intent": "Error: Gibberish Detected",
                "category": "Error Handling",
                "confidence": 0.0,
                "response": "I didn't quite catch that. It looks like random text. Could you please rephrase your question using full words?",
                "escalated": False,
                "escalation_reason": "No vowels detected in short query"
            }

        cleaned_query_lower = cleaned_query.lower()

        # Check for explicit priority keywords forcing human handoff
        forced_escalation = any(kw in cleaned_query_lower for kw in ESCALATION_KEYWORDS)

        query_vec = self.vectorizer.transform([cleaned_query_lower])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        max_idx = int(np.argmax(similarities))
        max_score = float(similarities[max_idx])

        faq_item = self.knowledge_base[self.intent_indices[max_idx]]
        intent_detected = faq_item["intent"] if max_score >= self.confidence_threshold else "Out of Scope / Unmapped"
        category_detected = faq_item["category"] if max_score >= self.confidence_threshold else "Fallback Support"
        matched_pattern_text = self.documents[max_idx] if max_score >= self.confidence_threshold else None

        # Generate Response: Generative LLM vs Local TF-IDF Fallback
        response_text = ""
        engine_used = "Local TF-IDF"
        api_error = None

        if self.api_provider and self.api_key:
            try:
                if self.api_provider == "Gemini":
                    response_text = self._call_gemini_api(cleaned_query)
                    engine_used = "Generative AI (Gemini)"
                elif self.api_provider == "OpenAI":
                    response_text = self._call_openai_api(cleaned_query)
                    engine_used = "Generative AI (OpenAI)"
                else:
                    raise ValueError(f"Unknown API provider: {self.api_provider}")
            except Exception as e:
                api_error = str(e)
                # Fall back to TF-IDF response
                engine_used = f"Local TF-IDF (Fallback - API Error: {type(e).__name__})"

        # Use TF-IDF response if local is selected, or if API call failed/was bypassed
        if not response_text:
            if max_score < self.confidence_threshold:
                response_text = f"I'm sorry, I couldn't find an exact match for your inquiry about '{cleaned_query}'. I am transferring your session to a live '{self.brand_name}' agent who will help you shortly."
            else:
                response_text = faq_item["response"]

        should_escalate = forced_escalation or (max_score < self.confidence_threshold) or faq_item["requires_escalation"]

        escalation_reason = None
        if forced_escalation:
            escalation_reason = "Priority keyword triggered escalation"
        elif max_score < self.confidence_threshold:
            escalation_reason = f"Similarity score ({max_score:.2f}) below threshold ({self.confidence_threshold})"
        elif faq_item["requires_escalation"]:
            escalation_reason = "Policy trigger: Damaged/wrong goods issues require human agent care"

        if should_escalate:
            ticket_id = f"TK-{hash(cleaned_query) % 100000:05d}"
            if "Human Support Handoff Triggered" not in response_text:
                response_text += f"\n\n🚨 **Human Support Handoff Triggered**: A support ticket ({ticket_id}) has been created. A representative from '{self.brand_name}' will contact you shortly."

        return {
            "intent": intent_detected,
            "category": category_detected,
            "confidence": round(max_score, 3),
            "response": response_text,
            "escalated": should_escalate,
            "escalation_reason": escalation_reason,
            "matched_pattern": matched_pattern_text,
            "engine_used": engine_used,
            "api_error": api_error
        }

    def run_benchmark(self) -> dict:
        """Run benchmark evaluation over standard customer test queries."""
        results = []
        correct_count = 0

        for sample in BENCHMARK_TEST_SUITE:
            query = sample["query"]
            expected = sample["expected_intent"]
            prediction = self.classify_query(query)
            is_correct = (prediction["intent"] == expected)

            if is_correct:
                correct_count += 1

            results.append({
                "query": query,
                "expected": expected,
                "predicted": prediction["intent"],
                "confidence": prediction["confidence"],
                "escalated": prediction["escalated"],
                "passed": is_correct
            })

        total = len(BENCHMARK_TEST_SUITE)
        accuracy = (correct_count / total) * 100.0 if total > 0 else 0.0

        return {
            "total_queries": total,
            "passed_queries": correct_count,
            "accuracy_percent": round(accuracy, 2),
            "test_results": results
        }

    def export_test_report_json(self) -> str:
        """Export full benchmark test report in JSON format."""
        benchmark_data = self.run_benchmark()
        return json.dumps(benchmark_data, indent=2)
