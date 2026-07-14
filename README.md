# SafeX AI & Automation Suite

Welcome to the **SafeX AI & Automation Suite** repository. This platform serves as a unified workspace for SafeX Solutions' business intelligence, client onboarding, and operations automation systems. It integrates diverse modular toolkits, predictive analytics, and automated workflows into a single interface.

---

## 📖 Platform Overview

The platform is designed to house multiple modular tools. It facilitates:
* **Information Assistants:** Locally running knowledge bases and semantic search tools.
* **Business Automation Modules:** Extensible scripts and interfaces for document extraction, workflows, scheduling, and analytics.
* **Operations Dashboards:** Visual management systems and team contribution summaries.

The codebase is built on **Python** and served locally through an interactive web-based interface using **Streamlit**.

---

## 📁 Repository Structure

The project uses a modular folder structure to ensure code segregation, allowing multiple developers to work independently without overlapping changes:

```text
safex-platform/
├── requirements.txt            # System dependencies
├── README.md                   # Platform documentation
├── AGENTS.md                   # Instructions and rules for AI coding assistants
│
├── data/                       # Shared datasets, logs, and files
│   └── faq.json                # Verified information database
│
├── docs/                       # Written reports, summaries, and guides
│   └── Meeting_Notes.md        # Templates for alignments
│
├── src/                        # Platform source code
│   ├── app.py                  # Main dashboard dashboard, styling, and navigation
│   ├── config.py               # Shared constants and settings
│   │
│   ├── core/                   # Shared backend algorithms, search, and loading scripts
│   │   ├── chatbot.py          
│   │   ├── similarity.py       
│   │   └── knowledge_base.py   
│   │
│   └── modules/                # Workspace extension modules organized by category
│       ├── registry.py         # Metadata directory mapping files to features
│       ├── week1/              # Week 1 project extensions
│       └── week2/              # Week 2 project extensions
│
└── tests/                      # Pytest unit testing suite
```

---

## ⚙️ Setup Instructions

Follow these steps to run the platform locally:

### 1. Prerequisites
* Python 3.9 or higher installed.
* Git installed.

### 2. Set Up Virtual Environment
Initialize and activate a virtual environment to manage dependencies cleanly:

```bash
# Initialize venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install all required platform libraries:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Set up your local configuration settings:
```bash
# Copy template env
cp .env.example .env
```

### 5. Run the Platform
Start the local Streamlit development server:
```bash
streamlit run src/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 6. Run Unit Tests
To execute automated tests validating core utilities:
```bash
python -m pytest
```

---

## 🤝 Contribution Guidelines

To maintain code quality and prevent version control conflicts, all contributors must follow these rules:

1. **Keep Code Modulated:** Avoid writing code in shared files like `src/app.py` or `src/config.py` unless coordinating layout changes.
2. **Develop in Modules:** Place all code, assets, and tests inside your assigned subdirectory under `src/modules/`.
3. **Use Namespace Imports:** Ensure all local imports are referenced from the project root directory (e.g. `from src.core.chatbot import ...`).
4. **Git Branching Policy:**
   * Never push changes directly to the `main` branch.
   * Create a feature branch for your work: `feature/<module_name>-<developer_name>` (e.g., `feature/ocr-hammad`).
   * Once code is tested locally, open a Pull Request (PR) to `main` and request a review from the Group Leader.
5. **No Placeholders in Production:** Do not push non-functional placeholders or stubs once your feature is complete. Fully document your classes and functions.
