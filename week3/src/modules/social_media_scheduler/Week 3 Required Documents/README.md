# SafeX Group 54 — Week 3 AI Agent Automation Proposal Suite

This directory is the self-contained workspace for Group 54's Week 3 project: **AI Agent Automation Proposal Suite**.

The suite contains interactive AI agent prototypes designed to automate high-priority workflows for target companies across various industries.

---

## 📂 Repository Structure

```text
week3/
  README.md                 # Setup, running instructions, and architecture overview
  requirements.txt          # Python packages required for the project
  src/
    app.py                  # Streamlit shared portal shell with premium styling
    config.py               # Shared platform configuration parameters
    modules/
      registry.py           # Team roster registry, tracking emails, roles, and statuses
      customer_support_chatbot/   # Arsalan Qasim: E-commerce clothing customer support agent
      social_media_scheduler/     # Ali Ammar Haider: Tutoring platform content scheduling agent
      # [Other member scaffolding stubs]
  tests/
    conftest.py             # pytest configurations
    test_app.py             # Streamlit shell integration test
    test_customer_support_chatbot.py
    test_social_media_scheduler.py
  docs/
    Meeting_Notes.md        # Week 3 team sync notes
    Self_Initiative.md      # Case study: AI Customer Support Chatbot (Arsalan Qasim)
    social_media_scheduler.md # Case study: AI Social Media Scheduler (Ali Ammar Haider)
    daily_work_log.md       # Individual work progress tracking
    research_notes.md       # API references, prompt engineering, and scheduling models
    demo_video_script.md    # Video recording narrative and walkthrough timeline
    presentation_slides.md  # Slide outline for presentation compiling
    weekly_progress_report.md # Print-ready weekly progress status report
```

---

## ⚡ Setup & Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run unit tests to verify the integrity of the codebase:
   ```bash
   python -m pytest tests/
   ```

---

## 🚀 Running the Web Portal

Run the Streamlit application shell to access all active member prototypes:
```bash
streamlit run src/app.py
```
- Navigate to **💬 AI Customer Support Chatbot** (Arsalan Qasim) to try the local NLP classifier.
- Navigate to **📅 AI Social Media Scheduler & Caption Generator** (Ali Ammar Haider) to test the automated content planner.


