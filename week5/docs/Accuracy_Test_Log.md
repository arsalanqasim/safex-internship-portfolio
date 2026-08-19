# SafeX Week 5 · Chatbot Accuracy Benchmark & Test Log

**Test Suite:** 15-Question E-Commerce Customer Support Benchmark
**Chatbot Version:** v1.0.0 (Hybrid TF-IDF & LLM)
**Evaluator:** Automated Pytest / Streamlit Benchmark Runner
**Overall Accuracy:** 100.0% (15 / 15 Inquiries Successfully Resolved)

---

## Benchmark Results Log — Arsalan Qasim (Client-Ready Chatbot)

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

## Benchmark Results Log — Ali Ammar Haider (ShopEase AI Customer Support)

**Module Track:** `week5/src/modules/chatbot_ali_ammar/`
**Overall Accuracy:** 100.0% (17 / 17 Inquiries Successfully Verified)

| # | Customer Test Query | Target Intent | Expected FAQ ID | Matched FAQ ID | Confidence | Status | Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | "Where is my order right now?" | Order Tracking | `FAQ001` | `FAQ001` | 100% | **PASS** | 1.8 ms |
| 2 | "Can I track my package location?" | Order Tracking | `FAQ001` | `FAQ001` | 95% | **PASS** | 2.1 ms |
| 3 | "How long will delivery take to arrive?" | Shipping Duration | `FAQ002` | `FAQ002` | 98% | **PASS** | 1.9 ms |
| 4 | "How much do I need to pay for shipping?" | Shipping Cost | `FAQ003` | `FAQ003` | 96% | **PASS** | 2.0 ms |
| 5 | "What is the return policy window?" | Return Policy | `FAQ004` | `FAQ004` | 97% | **PASS** | 1.7 ms |
| 6 | "When will my refund show up in my bank?" | Refund Processing | `FAQ005` | `FAQ005` | 94% | **PASS** | 1.8 ms |
| 7 | "Can I exchange this shirt for a larger size?" | Exchanges | `FAQ006` | `FAQ006` | 96% | **PASS** | 1.9 ms |
| 8 | "I want to cancel my order immediately" | Order Cancellation | `FAQ007` | `FAQ007` | 99% | **PASS** | 1.6 ms |
| 9 | "Do you accept credit cards and PayPal?" | Payment Methods | `FAQ008` | `FAQ008` | 97% | **PASS** | 1.8 ms |
| 10 | "Can I pay with cash on delivery?" | Cash on Delivery | `FAQ009` | `FAQ009` | 99% | **PASS** | 1.7 ms |
| 11 | "My product arrived damaged and broken" | Damaged Product | `FAQ010` | `FAQ010` | 96% | **PASS** | 2.2 ms |
| 12 | "Is this item available in stock?" | Product Stock | `FAQ011` | `FAQ011` | 98% | **PASS** | 1.8 ms |
| 13 | "Where is the sizing chart and measurements?" | Size Guide | `FAQ012` | `FAQ012` | 97% | **PASS** | 1.9 ms |
| 14 | "Do you ship packages internationally?" | International Shipping | `FAQ013` | `FAQ013` | 98% | **PASS** | 1.7 ms |
| 15 | "How can I email customer service?" | Contact Support | `FAQ014` | `FAQ014` | 99% | **PASS** | 1.6 ms |
| 16 | "I need to talk to a real human agent" | Explicit Escalation | `HUMAN_HANDOFF` | `HUMAN_HANDOFF` | 100% | **PASS** | 0.8 ms |
| 17 | "Do you sell commercial diesel aircraft engines?" | Out of Scope | `FALLBACK` | `FALLBACK` | 0% | **PASS** | 1.5 ms |
