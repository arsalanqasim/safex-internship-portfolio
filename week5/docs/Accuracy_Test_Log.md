# SafeX Week 5 · Chatbot Accuracy Benchmark & Test Log

**Test Suite:** 15-Question E-Commerce Customer Support Benchmark  
**Chatbot Version:** v1.0.0 (Hybrid TF-IDF & LLM)  
**Evaluator:** Automated Pytest / Streamlit Benchmark Runner  
**Overall Accuracy:** 100.0% (15 / 15 Inquiries Successfully Resolved)  

---

## Benchmark Results Log

| # | Customer Test Query | Expected Intent | Target FAQ ID | Predicted FAQ ID | Confidence | Status | Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | "How long does shipping take to Canada?" | Shipping Time | `faq_01` | `faq_01` | 88% | **PASS** | 42 ms |
| 2 | "How much do I need to spend for free shipping?" | Free Shipping Minimum | `faq_02` | `faq_02` | 85% | **PASS** | 38 ms |
| 3 | "Do you deliver to Dubai or Saudi Arabia?" | International Shipping | `faq_03` | `faq_03` | 81% | **PASS** | 35 ms |
| 4 | "Where can I enter my tracking number to see package status?" | Order Tracking | `faq_04` | `faq_04` | 91% | **PASS** | 39 ms |
| 5 | "I made a typo in my address, can I change it before shipment?" | Modify/Cancel Order | `faq_05` | `faq_05` | 76% | **PASS** | 44 ms |
| 6 | "What is the return window if the shirt does not fit?" | Return Policy Window | `faq_06` | `faq_06` | 89% | **PASS** | 41 ms |
| 7 | "When will the refund money be returned to my bank card?" | Refund Processing Time | `faq_07` | `faq_07` | 84% | **PASS** | 37 ms |
| 8 | "Where is your size guide and measurements chart?" | Size Guide | `faq_08` | `faq_08` | 92% | **PASS** | 36 ms |
| 9 | "Can I wash this organic cotton hoodie in a washing machine?" | Garment Care & Material | `faq_09` | `faq_09` | 79% | **PASS** | 40 ms |
| 10 | "Do you accept Apple Pay or Klarna installment plans?" | Payment Methods | `faq_10` | `faq_10` | 87% | **PASS** | 38 ms |
| 11 | "My discount coupon code is not applying at checkout" | Promo Code Usage | `faq_11` | `faq_11` | 83% | **PASS** | 43 ms |
| 12 | "I received a defective t-shirt with a torn stitch" | Damaged/Wrong Item | `faq_12` | `faq_12` | 80% | **PASS** | 39 ms |
| 13 | "Please connect me to a human representative right now" | Human Support Escalation | `faq_13` | `faq_13` | 94% | **PASS** | 28 ms |
| 14 | "Can our corporate company order 100 hoodies in bulk?" | Wholesale / Bulk Orders | `faq_14` | `faq_14` | 86% | **PASS** | 41 ms |
| 15 | "Do you offer digital e-gift cards and do they expire?" | Gift Cards | `faq_15` | `faq_15` | 90% | **PASS** | 35 ms |

---

## Edge Case & Stress Testing Observations

1. **Negative Sentiment Stress Test:**
   * *Query:* *"Your service is terrible and I am extremely angry, my package is late!"*
   * *Result:* Correctly flagged as negative sentiment, bypassed standard FAQ retrieval, and immediately triggered the priority human support escalation protocol with empathy acknowledgment.
2. **Out-of-Scope Gibberish Test:**
   * *Query:* *"Quantum physics relativity astronaut engine"*
   * *Result:* Score below confidence threshold (0.28). Triggered polite fallback message informing user of supported topics and offering human connection.
