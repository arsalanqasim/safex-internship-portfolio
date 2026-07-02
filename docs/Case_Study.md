# Portfolio Case Study: SafeX AI FAQ Chatbot

*Instructions: Replace the placeholders `[bracketed text]` with your team's specific contributions, details, and evaluation results. Address the guiding questions in each section to build a professional-grade portfolio case study.*

---

## 1. Project Overview & Context
- **Company Name:** SafeX Solutions
- **Project Duration:** [e.g. 1 Week, Week 1 Internship Task]
- **Team Name/Cohort ID:** [e.g. Cohort Group 54]
- **Core Technology Stack:** Python, Streamlit, Scikit-learn, Numpy, Pandas

### Guiding Questions:
*What was the corporate background of this task? Why did the company want to build this chatbot? What was the overall role of your team?*

---

## 2. Problem Statement
- **Context:** [Describe the scenario, e.g. intern onboarding friction]
- **The Challenge:** [Describe the problem, e.g. static documents, missing information, user confusion]

### Guiding Questions:
*What are the specific pain points of using static FAQ files? How does a semantic query interface improve team onboarding?*

---

## 3. Objectives & Key Deliverables
- **Objective 1:** [e.g. Build a modular query tool]
- **Objective 2:** [e.g. Implement semantic keyword retrieval without external APIs]
- **Objective 3:** [e.g. Enforce threshold guardrails to control false answers]

### Guiding Questions:
*What key performance indicators (accuracy, latency, user satisfaction) did the team aim to achieve?*

---

## 4. Technical Architecture
*Instructions: Explain the decoupling of database loading, feature vector calculations, workflow orchestration, and visualization UI.*

### System Dataflow Design:
```text
  [ User Query ]
        │
        ▼
  [ Preprocessing & Normalization ] (utils.py)
        │
        ▼
  [ Vector Space Representation ] (similarity.py: TF-IDF Vectorizer)
        │
        ▼
  [ Similarity Calculation ] (similarity.py: Cosine Similarity matrix math)
        │
        ▼
  [ Decision Boundary Threshold Check ] (chatbot.py)
   ├── Score >= Threshold ➔ Return Verified FAQ Answer
   └── Score < Threshold  ➔ Return Fallback Warning
```

---

## 5. Implementation Process
*Instructions: Outline the specific development phases, what each team member built, and how components were integrated.*

- **Data Engineering:** [Describe how the FAQ dataset JSON structure was designed and validated]
- **Retrieval Engine:** [Describe the mathematical vector space calculation steps]
- **User Interface:** [Describe how the Streamlit dashboard layout was styled]
- **Integration & Testing:** [Describe the Git feature-branch workflow and unit tests]

---

## 6. Benchmarking & Evaluation
*Instructions: Fill in the benchmarking metrics recorded by the testing framework on your test question set.*

| Evaluation Metric | Target Value | Achieved Value | Target Met? (Yes/No) |
| :--- | :--- | :--- | :--- |
| **Retrieval Accuracy** | [e.g. > 90%] | [Insert %] | [Yes/No] |
| **Response Latency** | [e.g. < 50ms] | [Insert ms] | [Yes/No] |
| **Fallback Success Rate** | [e.g. 100%] | [Insert %] | [Yes/No] |

### Guiding Questions:
*Describe how the decision threshold value was tuned. How did you balance true positives against false positives?*

---

## 7. Engineering Challenges & Solutions
- **Challenge 1 (Keyword Overlap / Stop Words):** [Describe issue and how stop word filtering resolved it]
- **Challenge 2 (Vocabulary Mismatch / Synonyms):** [Describe issue and how expanding database questions with synonyms resolved it]

---

## 8. Lessons Learned & Key Takeaways
1. [Key takeaway about choosing local algorithm implementations over heavy external API networks]
2. [Key takeaway about using a decoupled OOP architecture for team collaboration]
3. [Key takeaway about the importance of benchmarking performance empirically]

---

## 9. Media Showcase
- **App Dashboard Screenshot:** `[Insert screenshot path/url here]`
- **Evaluation Console Logs:** `[Insert screenshot path/url here]`
- **Interactive App Demo:** `[Insert GIF path/url here]`
