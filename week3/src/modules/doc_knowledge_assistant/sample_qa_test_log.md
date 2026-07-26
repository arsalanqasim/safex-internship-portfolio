# QuickBite Knowledge Assistant — Sample Q&A Test Log

**Overall retrieval accuracy: 100.0% (14/14)**

Each question below was run through the live `DocKnowledgeAssistantEngine.answer()` pipeline. "Expected source" is the document a human would consider correct for that question; "Retrieved source" is what the engine actually matched. The last two questions are deliberately out-of-scope, to test whether the assistant correctly abstains instead of guessing.

---

## 1. How long does standard delivery usually take?
- **Status:** PASS
- **Expected source:** QuickBite Delivery Policy
- **Retrieved source:** QuickBite Delivery Policy (score 0.273)
- **Abstained:** False
- **Answer given:**

  > Most orders are delivered within 30-45 minutes of order confirmation during normal hours (10 AM - 11 PM). During peak hours (12-2 PM and 7-9 PM) or bad weather, delivery may take up to 60 minutes. The app shows a live estimated delivery time that updates as your rider moves.
  > 
  > _Source: QuickBite Delivery Policy — "Standard Delivery Times"_

## 2. What happens if my order is late?
- **Status:** PASS
- **Expected source:** QuickBite Delivery Policy
- **Retrieved source:** QuickBite Delivery Policy (score 0.217)
- **Abstained:** False
- **Answer given:**

  > If your order arrives more than 20 minutes after the estimated delivery time shown at checkout, you are automatically eligible for a QuickBite Credit equal to your delivery fee, added to your account within 24 hours. No claim form is required — this is applied automatically based on the rider's GPS-logged delivery timestamp.
  > 
  > _Source: QuickBite Delivery Policy — "Late Delivery Compensation"_

## 3. Can I cancel my order for free right after placing it?
- **Status:** PASS
- **Expected source:** QuickBite Refund and Cancellation Policy
- **Retrieved source:** QuickBite Refund and Cancellation Policy (score 0.4)
- **Abstained:** False
- **Answer given:**

  > You can cancel any order for free within 60 seconds of placing it, before the restaurant has accepted it. Go to "My Orders," select the active order, and tap "Cancel Order." The full amount is refunded automatically to your original payment method or QuickBite Wallet.
  > 
  > _Source: QuickBite Refund and Cancellation Policy — "Cancelling an Order Before Restaurant Acceptance"_

## 4. How do I get a refund if an item is missing from my order?
- **Status:** PASS
- **Expected source:** QuickBite Refund and Cancellation Policy
- **Retrieved source:** QuickBite Refund and Cancellation Policy (score 0.276)
- **Abstained:** False
- **Answer given:**

  > If any item is missing or incorrect when your order arrives, report it within 24 hours via "Help" > "Order Issue" in the app. Attach a photo of what you received if possible. Approved claims are refunded as QuickBite Credit within minutes, or to your original payment method within 3-5 business days if you request a cash refund instead of credit.
  > 
  > Related: If a customer reports an issue with food quality or a missing item, the restaurant is notified and given 48 hours to respond with their side before a refund decision is finalized. Restaurants with a complaint rate above 5% of total orders in a rolling 30-day window are flagged for a quality review call with the Partner Success team.
  > 
  > _Source: QuickBite Refund and Cancellation Policy — "Refunds for Missing or Incorrect Items"_

## 5. What payment methods do you accept?
- **Status:** PASS
- **Expected source:** QuickBite Payment Methods FAQ
- **Retrieved source:** QuickBite Payment Methods FAQ (score 0.295)
- **Abstained:** False
- **Answer given:**

  > QuickBite accepts Cash on Delivery (COD), Visa/Mastercard debit and credit cards, JazzCash, EasyPaisa, and the in-app QuickBite Wallet. Bank transfers and cheques are not supported for order payments.
  > 
  > Related: Card details are tokenized and stored securely by our PCI-DSS compliant payment partner; QuickBite does not store your full card number. You can remove a saved card anytime from "Payment Methods" in your account settings.
  > 
  > _Source: QuickBite Payment Methods FAQ — "Accepted Payment Methods"_

## 6. Is there a limit on cash on delivery orders?
- **Status:** PASS
- **Expected source:** QuickBite Payment Methods FAQ
- **Retrieved source:** QuickBite Payment Methods FAQ (score 0.329)
- **Abstained:** False
- **Answer given:**

  > Cash on Delivery is available for orders up to PKR 10,000. For orders above this amount, you must pay with a card, wallet, JazzCash, or EasyPaisa. Riders carry limited change, so please try to have close to the exact amount ready.
  > 
  > Related: - QuickBite Wallet / Credit: instant to 1 hour
  > - Debit/Credit card: 3-7 business days
  > - JazzCash / EasyPaisa: 1-3 business days
  > - Cash on Delivery orders: refunded as QuickBite Credit only, since no original payment method exists to refund to
  > 
  > _Source: QuickBite Payment Methods FAQ — "Cash on Delivery Limits"_

## 7. How do loyalty points work?
- **Status:** PASS
- **Expected source:** QuickBite Payment Methods FAQ
- **Retrieved source:** QuickBite Payment Methods FAQ (score 0.477)
- **Abstained:** False
- **Answer given:**

  > Every paid order (excluding delivery fees) earns 1 loyalty point per PKR 100 spent. Points can be redeemed for discount vouchers starting at 200 points = PKR 100 off. Points expire 12 months after being earned if unused.
  > 
  > _Source: QuickBite Payment Methods FAQ — "Loyalty Points"_

## 8. What do I need to become a delivery rider?
- **Status:** PASS
- **Expected source:** QuickBite Rider Partner FAQ
- **Retrieved source:** QuickBite Rider Partner FAQ (score 0.182)
- **Abstained:** False
- **Answer given:**

  > Riders are rated by customers after each delivery. A rider whose rating falls below 4.0 (out of 5) over their last 100 deliveries will receive a warning and access to a coaching session. Ratings below 3.5, or serious violations (safety issues, order tampering, fraud), can result in temporary suspension or permanent deactivation after review.
  > 
  > _Source: QuickBite Rider Partner FAQ — "Rider Rating and Deactivation Policy"_

## 9. How much do riders get paid per delivery?
- **Status:** PASS
- **Expected source:** QuickBite Rider Partner FAQ
- **Retrieved source:** QuickBite Rider Partner FAQ (score 0.286)
- **Abstained:** False
- **Answer given:**

  > Riders earn a base fee per delivery (distance-based, PKR 60-140) plus 100% of any customer tip. Peak-hour deliveries (12-2 PM, 7-9 PM) earn an additional PKR 20-40 surge bonus per order. Weekly earnings are deposited directly to the rider's bank account or JazzCash/EasyPaisa account every Monday for the previous Monday-Sunday period.
  > 
  > _Source: QuickBite Rider Partner FAQ — "How Riders Are Paid"_

## 10. How can my restaurant join QuickBite?
- **Status:** PASS
- **Expected source:** QuickBite Restaurant Partner FAQ
- **Retrieved source:** QuickBite Restaurant Partner FAQ (score 0.204)
- **Abstained:** False
- **Answer given:**

  > Restaurants can apply to join QuickBite through the "Partner with Us" page by submitting a valid business/food license, NTN (National Tax Number), bank account details, and a sample menu with prices. Onboarding review typically takes 5-7 business days, followed by a menu photography session (provided free of charge in major cities).
  > 
  > _Source: QuickBite Restaurant Partner FAQ — "Becoming a Partner Restaurant"_

## 11. What commission does QuickBite charge restaurants?
- **Status:** PASS
- **Expected source:** QuickBite Restaurant Partner FAQ
- **Retrieved source:** QuickBite Restaurant Partner FAQ (score 0.184)
- **Abstained:** False
- **Answer given:**

  > QuickBite charges a commission of 18-25% per order, depending on the restaurant's category, order volume tier, and whether the restaurant participates in QuickBite marketing promotions. New restaurants receive a reduced commission rate of 15% for their first 60 days on the platform.
  > 
  > Related: If a card payment fails but money was deducted from your account, it is automatically reversed by your bank within 5-7 business days; QuickBite does not hold these funds. If you were charged twice for the same order due to a network issue, contact support with both transaction IDs and the duplicate charge will be refunded within 3 business days after verification.
  > 
  > _Source: QuickBite Restaurant Partner FAQ — "Commission Structure"_

## 12. When are restaurant payouts made?
- **Status:** PASS
- **Expected source:** QuickBite Restaurant Partner FAQ
- **Retrieved source:** QuickBite Restaurant Partner FAQ (score 0.316)
- **Abstained:** False
- **Answer given:**

  > Restaurant payouts (order value minus commission) are transferred weekly, every Wednesday, for the previous Monday-Sunday sales period, directly to the restaurant's registered bank account. Detailed order-level statements are available for download from the Partner Dashboard at any time.
  > 
  > _Source: QuickBite Restaurant Partner FAQ — "Payouts to Restaurants"_

## 13. What is the weather like in Islamabad today?
- **Status:** PASS
- **Expected source:** (none — out of scope)
- **Retrieved source:** QuickBite Delivery Policy (score 0.087)
- **Abstained:** True
- **Answer given:**

  > I don't have information about that in the QuickBite knowledge base I was given. Please contact support directly for this question, or rephrase it if you think it should be covered.

## 14. Can you recommend a good stock to invest in?
- **Status:** PASS
- **Expected source:** (none — out of scope)
- **Retrieved source:** QuickBite Rider Partner FAQ (score 0.0)
- **Abstained:** True
- **Answer given:**

  > I don't have information about that in the QuickBite knowledge base I was given. Please contact support directly for this question, or rephrase it if you think it should be covered.

---
## Summary
- Total questions: 14
- Passed: 14
- Accuracy: 100.0%
- 12 answerable questions (2-3 per document) plus 2 deliberately out-of-scope questions to test abstention behavior.