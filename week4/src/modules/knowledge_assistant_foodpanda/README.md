# RAG-based Knowledge Assistant — Week 4 (Client-Ready Build)

**Module:** `week4/src/modules/knowledge_assistant_foodpanda/`
**Developer:** Ali Zaib (AI/ML Intern)
**Part of:** SafeX Solutions — Client-Ready AI & Automation Suite, Week 4

## What changed from Week 3

This module reuses the exact RAG engine built and evaluated in Week 3
(`week3/src/modules/doc_knowledge_assistant/`) — 100% retrieval accuracy
on a 14-question test log, full development writeup there. Week 4's job
was to make it **client-ready and deployable**, not to rebuild it:

- **`engine.py`** — unchanged logic, header comments updated for Week 4 context.
- **`ui.py`** — rewritten for a non-technical audience: leads with a plain-
  language pitch ("why this matters for your business"), demo Q&A front
  and center, and moves evaluation metrics/limitations into a
  "Technical Details" tab instead of leading with them.
- **New:** a standalone deployment package (`knowledge_assistant_deploy_package/`)
  so this module can run on its own, outside the full monorepo suite.

## Files

| File | Purpose |
|---|---|
| `engine.py` | Same RAG pipeline as Week 3 (chunking, TF-IDF retrieval, abstention, answer synthesis). |
| `ui.py` | Client-facing Streamlit UI: Try It Live / Knowledge Base / Why It Works / Technical Details tabs. |
| `data/knowledge_base/*.md` | The 5 original QuickBite policy documents (same as Week 3). |
| `test_suite.py` | The same 14-question labeled test suite. |
| `../../../tests/test_knowledge_assistant_foodpanda.py` | Unit tests for this module. |
| `../../knowledge_assistant_deploy_package/` | Self-contained standalone copy, ready to push to its own repo and deploy. |
| `../../data/outreach_tracker.xlsx` | Shared team outreach log — see the "Notes" sheet inside for how to append rows without conflicting with teammates. |

## How to run inside the full suite

```bash
cd week4
pip install -r requirements.txt
streamlit run src/app.py
```
Select **"RAG-based Knowledge Assistant"** from the sidebar.

## How to deploy the standalone version to Streamlit Community Cloud

The `knowledge_assistant_deploy_package/` folder is a complete, self-
contained Streamlit app (its own `app.py`, `src/`, and `requirements.txt`)
with no dependency on the rest of this monorepo — it can be deployed on
its own.

1. **Push it to your own GitHub repo** (a new, separate repo — not this
   monorepo):
   ```bash
   cd week4/knowledge_assistant_deploy_package
   git init
   git add .
   git commit -m "Initial deploy: QuickBite Knowledge Assistant demo"
   git branch -M main
   git remote add origin <your-new-repo-url>
   git push -u origin main
   ```
2. **Go to [share.streamlit.io](https://share.streamlit.io)** and sign in
   with your GitHub account.
3. Click **New app**, select your new repo, branch `main`, and set the
   main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt`
   automatically and gives you a live URL like
   `https://<something>.streamlit.app`.
5. **Update `week4/src/modules/registry.py`** in this monorepo: set
   `"deployed_url"` for `knowledge_assistant_foodpanda` to your live URL,
   then commit and push that change so it shows up as active on the
   master portfolio app, per Arsalan's instructions.

**Alternative: Render.** Create a new Web Service, link the same
standalone repo, set the build command to `pip install -r requirements.txt`
and the start command to `streamlit run app.py --server.port $PORT
--server.address 0.0.0.0`.

## Architecture, evaluation, and limitations

Unchanged from Week 3 — see the **Technical Details** tab in the app
itself, or the full writeup in
`week3/src/modules/doc_knowledge_assistant/README.md`.
