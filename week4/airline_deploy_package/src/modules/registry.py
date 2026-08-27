"""Trimmed registry for the standalone deployment of this module."""

MODULE_REGISTRY = {
    "week4": {
        "knowledge_assistant_airline": {
            "title": "RAG-based Knowledge Assistant",
            "developer": "Muhammad Faozan Mujtaba",
            "role": "Group Member",
            "status": "Submission Ready",
            "tech": ["Python", "scikit-learn", "TF-IDF Retrieval", "RAG Pipeline", "Streamlit"],
            "description": (
                "Retrieval-Augmented Generation assistant answering Q&A queries over a "
                "customised operational document set (FAQ/policies) with citations and "
                "an explicit refusal path for out-of-scope questions."
            ),
            "import_path": "src.modules.knowledge_assistant_airline.ui",
            "icon": "\U0001F4DA",
            "deployed_url": None,
        }
    }
}
