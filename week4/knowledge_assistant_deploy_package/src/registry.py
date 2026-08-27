"""Standalone registry stub for the deployed Knowledge Assistant.
Mirrors the metadata shape the module's ui.py expects from the full
monorepo's registry.py, so this module runs identically when deployed
on its own."""

MODULE_REGISTRY = {
    "week4": {
        "knowledge_assistant_foodpanda": {
            "title": "RAG-based Knowledge Assistant",
            "developer": "Ali Zaib",
            "role": "Group Member",
            "email": "aliofficialzaib@gmail.com",
            "status": "Deployed",
            "tech": ["Python", "TF-IDF Vector Retrieval", "RAG Pipeline", "Streamlit"],
            "description": "Retrieval-augmented Q&A assistant retrieving policy contexts to answer user queries with hallucination controls.",
            "icon": "📚",
        }
    }
}
