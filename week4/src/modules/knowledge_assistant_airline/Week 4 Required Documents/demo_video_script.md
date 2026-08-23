# Client Demo Video Script (3-5 minutes)

Module: RAG-based Knowledge Assistant · Muhammad Faozan Mujtaba · Week 4
Audience: the client - an airline operations or customer-experience manager
Tone: business outcome first. No code on screen at any point.

**Setup before recording**: app open on the *Ask the assistant* tab, question box empty,
conversation history cleared, browser zoom ~110%, notifications off.

---

## 0:00-0:35 - The problem

> "Your contact centre answers the same questions all day. What is my baggage allowance,
> what does it cost to change my ticket, my flight was delayed - what am I owed. Those
> answers live across seven separate policy documents, and right now an agent searches
> them by hand while the passenger waits on the line.
>
> That costs you twice. Handling time goes up. And when an agent can't find the rule
> quickly, they answer from memory - so two passengers with the same question get two
> different answers, and the wrong one comes back later as a refund."

---

## 0:35-1:00 - What this is

> "This is a knowledge assistant that reads your own policy documents and answers from
> them - only from them. Every answer shows the exact passage it came from, so an agent
> can check the source before repeating it to a passenger.
>
> Let me show you three questions."

---

## 1:00-1:45 - Demo 1: it understands passenger wording

Type: **How much hand luggage can I take on board?**

> "Notice the passenger said 'hand luggage'. Your policy document never uses that phrase -
> it says 'cabin baggage' throughout. The assistant bridges that gap and returns the
> answer: seven kilos, 55 by 40 by 20 centimetres.
>
> And beside it, the source." *(expand passage 1)* "That is your baggage policy, the cabin
> allowance section. The agent can see the rule, not just the answer."

---

## 1:45-2:30 - Demo 2: it finds the exception

Type: **Can my pug travel in the hold?**

> "This is the one that matters. A general answer would be 'yes, animals over eight kilos
> travel in the hold' - and that would be wrong.
>
> Look what it found: snub-nosed breeds, including pugs, are refused in the hold on all
> routes, because of the respiratory risk. It surfaced the exception, not just the general
> rule. That is a booking your team would otherwise have taken and then had to cancel at
> the airport."

---

## 2:30-3:15 - Demo 3: it says when it does not know

Type: **What is the wifi password on board?**

> "Now the important one. This isn't in the policy library - and the assistant says so. It
> doesn't invent a plausible answer, it tells the agent it can't find it, and points at the
> closest topic that is covered.
>
> That is the difference between this and a general chatbot. A chatbot answers fluently
> whether or not it knows. On policy questions, a confident wrong answer is worse than no
> answer at all - and this refuses instead."

---

## 3:15-3:50 - Results

Switch to the **Benchmark** tab, click *Run benchmark*.

> "This is tested, not asserted. Thirty-eight questions written in passenger wording:
> thirty-three it should answer, five it shouldn't.
>
> It answered all thirty-three from the correct policy document, and refused all five it
> should have refused. Answers come back in under a millisecond, and it runs on ordinary
> hosting with no per-question model cost."

---

## 3:50-4:30 - Close

> "To point this at your own policies, we replace the documents - the pipeline doesn't
> change. That is a short piece of work, and you'd get an assistant that answers from your
> published terms with the passage cited beside every answer.
>
> The demo is live at this link and you're welcome to try your own questions. I'd suggest
> deliberately asking it something your policies don't cover, and watching it decline."

---

## Recording checklist

- [ ] Clear conversation history before starting
- [ ] Type questions at readable speed; pause on each answer
- [ ] Expand at least one passage on camera
- [ ] Never show code, file paths or the terminal
- [ ] Say "your policies", not "the knowledge base"
- [ ] End on the live URL, held on screen
