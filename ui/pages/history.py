"""Analysis history page."""

import streamlit as st

from ui.components import render_empty_state, render_timeline_entry, esc


def render() -> None:
    st.markdown('<h1 class="page-title">Session History</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Review past analyses from this session. Each entry captures title, source, and timestamp.</p>',
        unsafe_allow_html=True,
    )

    history = st.session_state.analysis_history

    if not history:
        render_empty_state(
            "🕐",
            "No History Yet",
            "Your analysis history will appear here after you run your first video through the Studio pipeline.",
        )
        if st.button("⚡ Start First Analysis", type="primary"):
            st.session_state.current_page = "studio"
            st.rerun()
        return

    st.markdown(
        f"""
<div class="metric-grid" style="margin-bottom:2rem">
    <div class="metric-card">
        <div class="metric-value">{len(history)}</div>
        <div class="metric-label">Total Sessions</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{sum(h.get('word_count', 0) for h in history):,}</div>
        <div class="metric-label">Total Words</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{history[0]['timestamp'].split('·')[0].strip() if history else '—'}</div>
        <div class="metric-label">Latest Session</div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">📜 Timeline</div>', unsafe_allow_html=True)

    for i, entry in enumerate(history):
        render_timeline_entry(
            entry["title"],
            entry["timestamp"],
            entry["source"],
            i,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.result:
        st.markdown("---")
        st.info(f"Currently viewing: **{esc(st.session_state.result['title'])}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Current Insights", use_container_width=True, disabled=not st.session_state.result):
            st.session_state.current_page = "insights"
            st.rerun()
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state.analysis_history = []
            st.rerun()
