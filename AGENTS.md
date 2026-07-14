# Rules & Guidelines for AI Coding Agents

This repository serves as a collaborative platform for SafeX Solutions' business intelligence and automation systems. To maintain codebase hygiene and align with developer workflows, all AI agents (e.g., LLM coding assistants, copilots, agentic scripts) must strictly adhere to the instructions defined in this document.

---

## 🛑 STRICT CRITICAL RULES (MUST READ FIRST)

> [!IMPORTANT]
> **NO UNAUTHORIZED IMPLEMENTATION OF ASSIGNED TASKS**
> * AI Agents **must never** write actual production code, business logic, calculations, or models for any assigned team member's Week 2+ tasks.
> * AI Agents **must never** write actual production code, business logic, calculations, or models for the Group Leader's individual tasks (e.g. Invoice Automation).
> * The **ONLY** exception is if the Group Leader explicitly commands the agent in a user prompt to write a specific implementation (e.g., *"Implement the invoice PDF extraction logic"*).

> [!WARNING]
> **LIMIT WORK TO SCAFFOLDING AND DOCUMENTATION**
> * Unless explicitly instructed by the Group Leader to implement a feature, AI agents must restrict all task-specific contributions to **scaffolding, templates, empty boilerplate, placeholder functions, interface definitions, and documentation stubs**.
> * Writing mocked consoles, dummy text inputs, and empty event trigger stubs in `ui.py` files is permitted to help verify frontend layout routing.

---

## 📁 Repository Modular Structure

AI agents must keep the codebase modular. Changes must be confined to correct namespaces:

* **`/src/core/`**: Shared core packages (FAQ Chatbot logic, similarity engines, shared loaders, global config). Avoid modifying files here unless fixing core bugs or adding global helpers.
* **`/src/modules/`**: Extensible workspace hub. Organized by week directories (e.g., `week1/`, `week2/`).
  * Each active task has a folder containing an `__init__.py`, `engine.py` (calculations, mock models, data processing), and `ui.py` (Streamlit rendering).
  * Agents must **only** make changes to the specific folder corresponding to the active task.
* **`/tests/`**: Contains pytest suites validating modules.

---

## 💻 Coding & Interface Standards

When creating or modifying scaffolding or authorized code, agents must follow these guidelines:

1. **Clean Code and Type Hinting:**
   * Write clean, idiomatic Python code.
   * Provide proper type annotations for all function and class signatures.
2. **Boilerplate Layouts:**
   * When writing module stubs, use the standard Class names matching the directory name (e.g. `AttendanceEngineStub` inside `modules/week2/attendance/engine.py`).
   * Provide clean docstrings explaining the class interfaces and arguments.
3. **Streamlit Component Encapsulation:**
   * Streamlit UI components for a module must be fully self-contained inside the module's `ui.py` file within a `def render_ui():` function.
   * Do not write global session state updates or page setups inside module sub-files; keep page configuration inside `/src/app.py`.
4. **Local Paths and Imports:**
   * Never hardcode absolute system paths. Use relative path references anchored to the root folder using `Path(__file__)` or import configurations from `src.config`.
   * Ensure namespace imports are formatted relative to the root directory (e.g., `from src.modules.registry import ...`).

---

## 📝 Documentation & Review Standards

1. **Keep Root Documentation Clean:**
   * Do not inject task-specific, developer-specific, or internship-specific comments into the root `README.md`.
   * Keep the root README generic, focusing on overall workspace description, setup instructions, structure, and contribution rules.
2. **Preserve Team Registry Metadata:**
   * Keep the `MODULE_REGISTRY` mapping in `src/modules/registry.py` accurate. Any new module must first be registered there before files are created.
3. **No Code Churn:**
   * Do not refactor existing, working code in `src/core/` or `src/modules/week1/` unless fixing a documented bug or explicitly requested. Preserve all docstrings and comments.
