import streamlit as st
from src.modules.registry import MODULE_REGISTRY

def render_ui() -> None:
    metadata = MODULE_REGISTRY["week4"]["model_comparison_careem"]
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">⏳ Scaffolding Ready · Workspace Placeholder</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Developer: <strong>{metadata["developer"]}</strong> ({metadata["role"]}) · <code>{metadata["email"]}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.expander("📌 Module Specifications", expanded=True):
        st.write(f"**Objective**: {metadata['description']}")
        st.write(f"**Assigned Stack**: {' · '.join(metadata['tech'])}")
        st.write(f"**Status**: `{metadata['status']}`")

    st.info(f"Welcome, {metadata['developer']}! This module is ready for your Week 4 client-ready sprint submission. Place your engine logic in `engine.py` and build your Streamlit elements inside `render_ui()` in this file.")
