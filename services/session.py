"""Session state initialization and helpers."""

from __future__ import annotations

import streamlit as st


DEFAULTS: dict = {
    "current_page": "home",
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
    "analysis_history": [],
    "default_language": "english",
    "source_input": "",
}


def init_session_state() -> None:
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def has_result() -> bool:
    return st.session_state.result is not None


def add_to_history(result: dict, source: str) -> None:
    import time

    entry = {
        "title": result["title"],
        "source": source,
        "timestamp": time.strftime("%b %d, %Y · %H:%M"),
        "word_count": len(result.get("transcript", "").split()),
    }
    history = st.session_state.analysis_history
    history.insert(0, entry)
    st.session_state.analysis_history = history[:20]


PAGES = {
    "home": {"label": "Home", "icon": "🏠", "section": "Main"},
    "studio": {"label": "Studio", "icon": "⚡", "section": "Main"},
    "insights": {"label": "Insights", "icon": "📊", "section": "Analysis", "requires_result": True},
    "chat": {"label": "Ask AI", "icon": "💬", "section": "Analysis", "requires_result": True},
    "history": {"label": "History", "icon": "🕐", "section": "Analysis"},
    "settings": {"label": "Settings", "icon": "⚙️", "section": "System"},
    "help": {"label": "Help", "icon": "❓", "section": "System"},
}
