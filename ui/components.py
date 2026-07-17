"""Reusable UI component helpers."""

from __future__ import annotations

import html
from typing import Any


def esc(text: str) -> str:
    return html.escape(str(text))


def render_app_header(page_title: str, has_result: bool, pipeline_done: bool) -> None:
    import streamlit as st

    status_class = "live" if has_result and pipeline_done else "idle"
    status_label = "Analysis Ready" if has_result else "Awaiting Input"

    st.markdown(
        f"""
<div class="app-header">
    <div class="header-breadcrumb">
        <span>Nexus</span>
        <span>›</span>
        <span>{esc(page_title)}</span>
    </div>
    <div class="header-actions">
        <div class="status-pill {status_class}">
            <span class="status-dot-sm"></span>
            {status_label}
        </div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )


def render_brand() -> str:
    return """
<div class="brand-mark">
    <div class="brand-icon">◈</div>
    <div>
        <div class="brand-name">Nexus AI</div>
        <div class="brand-tagline">Meeting Intelligence</div>
    </div>
</div>"""


def render_nav_item(label: str, icon: str, page_key: str, active: bool, disabled: bool = False) -> str:
    classes = ["nav-item"]
    if active:
        classes.append("active")
    if disabled:
        classes.append("disabled")
    badge = '<span class="nav-badge">New</span>' if page_key == "insights" and not disabled else ""
    return f"""
<div class="{' '.join(classes)}">
    <span class="nav-icon">{icon}</span>
    <span>{label}</span>
    {badge}
</div>"""


def render_pipeline_stepper(steps: dict[str, str]) -> None:
    import streamlit as st

    pipeline = [
        ("audio", "🔊", "Audio"),
        ("transcript", "📝", "Transcribe"),
        ("title", "🏷️", "Title"),
        ("summary", "📋", "Summary"),
        ("extract", "🔍", "Extract"),
        ("rag", "🧠", "RAG"),
    ]

    items_html = ""
    for key, icon, label in pipeline:
        state = steps.get(key, "pending")
        items_html += f"""
<div class="pipeline-step {state}">
    <div class="step-circle">{icon}</div>
    <div class="step-label">{label}</div>
</div>"""

    st.markdown(
        f'<div class="pipeline-track">{items_html}</div>',
        unsafe_allow_html=True,
    )


def render_metric_grid(metrics: list[tuple[str, str, str]]) -> None:
    import streamlit as st

    cards = ""
    for value, label, _color in metrics:
        cards += f"""
<div class="metric-card">
    <div class="metric-value">{esc(value)}</div>
    <div class="metric-label">{esc(label)}</div>
</div>"""

    st.markdown(f'<div class="metric-grid">{cards}</div>', unsafe_allow_html=True)


def render_glass_card(title: str, content: str, accent: bool = False) -> None:
    import streamlit as st

    accent_class = " glass-card-accent" if accent else ""
    st.markdown(
        f"""
<div class="glass-card{accent_class}">
    <div class="card-label">{title}</div>
    <div class="card-body">{content}</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_insight_card(title: str, icon: str, content: str, variant: str = "actions") -> None:
    import streamlit as st

    st.markdown(
        f"""
<div class="insight-card {variant}">
    <div class="insight-header">
        <span>{icon}</span>
        <h4>{esc(title)}</h4>
    </div>
    <div class="card-body">{content}</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_empty_state(icon: str, title: str, description: str) -> None:
    import streamlit as st

    st.markdown(
        f"""
<div class="empty-state">
    <div class="empty-icon">{icon}</div>
    <div class="empty-title">{esc(title)}</div>
    <div class="empty-desc">{esc(description)}</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_chat_messages(messages: list[dict[str, str]]) -> None:
    import streamlit as st

    if not messages:
        return

    rows = ""
    for msg in messages:
        role = msg["role"]
        avatar = "👤" if role == "user" else "◈"
        rows += f"""
<div class="chat-row {role}">
    <div class="chat-avatar">{avatar}</div>
    <div class="chat-bubble">{esc(msg['content'])}</div>
</div>"""

    st.markdown(
        f'<div class="chat-messages">{rows}</div>',
        unsafe_allow_html=True,
    )


def render_chat_empty() -> None:
    import streamlit as st

    st.markdown(
        """
<div class="empty-state" style="padding:3rem 2rem;margin-bottom:1rem">
    <div class="empty-icon">◈</div>
    <div class="empty-title">Start a Conversation</div>
    <div class="empty-desc">Ask anything about your meeting — decisions, action items, or specific topics discussed.</div>
</div>
<div class="chat-suggestions">
    <span class="suggestion-chip">What were the main decisions?</span>
    <span class="suggestion-chip">Summarize action items</span>
    <span class="suggestion-chip">Who said what about the budget?</span>
    <span class="suggestion-chip">What questions remain open?</span>
</div>""",
        unsafe_allow_html=True,
    )


def render_timeline_entry(title: str, timestamp: str, source: str, index: int) -> None:
    import streamlit as st

    st.markdown(
        f"""
<div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-content">
        <div class="timeline-title">{esc(title)}</div>
        <div class="timeline-meta">{esc(timestamp)} · {esc(source[:60])}{'…' if len(source) > 60 else ''}</div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )


def compute_result_metrics(result: dict[str, Any]) -> list[tuple[str, str, str]]:
    transcript = result.get("transcript", "")
    word_count = len(transcript.split())
    char_count = len(transcript)
    summary_words = len(result.get("summary", "").split())
    action_lines = len([l for l in result.get("action_items", "").split("\n") if l.strip()])

    return [
        (f"{word_count:,}", "Words", "teal"),
        (f"{char_count:,}", "Characters", "indigo"),
        (f"{summary_words:,}", "Summary Words", "amber"),
        (str(max(action_lines, 1)), "Action Items", "green"),
    ]


def format_content_as_html(text: str) -> str:
    return esc(text).replace("\n", "<br>")
