"""AI Chat page — RAG-powered Q&A."""

import streamlit as st

from core.rag_engine import ask_question
from ui.components import render_chat_empty, render_chat_messages, render_empty_state


SUGGESTIONS = [
    "What were the main decisions made?",
    "List all action items",
    "What questions remain unanswered?",
    "Summarize the key discussion points",
]


def render() -> None:
    st.markdown('<h1 class="page-title">Ask AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Chat with your meeting using retrieval-augmented generation. Ask anything about the transcript.</p>',
        unsafe_allow_html=True,
    )

    if not st.session_state.result:
        render_empty_state(
            "💬",
            "Chat Unavailable",
            "Complete an analysis first to enable AI-powered Q&A on your meeting content.",
        )
        if st.button("⚡ Go to Studio", type="primary"):
            st.session_state.current_page = "studio"
            st.rerun()
        return

    r = st.session_state.result

    st.markdown(
        f"""
<div class="glass-card" style="margin-bottom:1.25rem;padding:1rem 1.25rem">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem">
        <div>
            <span class="badge badge-teal">Active Session</span>
            <span style="margin-left:0.75rem;font-weight:600;font-size:0.9rem">{r['title'][:60]}{'…' if len(r['title']) > 60 else ''}</span>
        </div>
        <span style="font-size:0.75rem;color:var(--text-muted)">{len(st.session_state.chat_history)} messages</span>
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            render_chat_messages(st.session_state.chat_history)
        else:
            render_chat_empty()

    st.markdown('<div class="chat-suggestions">', unsafe_allow_html=True)
    sug_cols = st.columns(len(SUGGESTIONS))
    suggested = None
    for col, suggestion in zip(sug_cols, SUGGESTIONS):
        with col:
            if st.button(suggestion, key=f"sug_{suggestion[:20]}", use_container_width=True, type="secondary"):
                suggested = suggestion
    st.markdown("</div>", unsafe_allow_html=True)

    input_col, send_col, clear_col = st.columns([6, 1, 1])
    with input_col:
        user_input = st.text_input(
            "Message",
            value=suggested or "",
            placeholder="Ask about decisions, action items, or specific topics…",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        st.markdown("<br>", unsafe_allow_html=True)
        send_btn = st.button("Send", use_container_width=True, type="primary")
    with clear_col:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("Clear", use_container_width=True, type="secondary")

    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    query = (suggested or user_input or "").strip()
    if (send_btn or suggested) and query:
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()
