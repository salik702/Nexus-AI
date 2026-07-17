"""Welcome / Home page."""

import streamlit as st


def render() -> None:
    st.markdown(
        """
<div class="hero-section">
    <div class="hero-glow"></div>
    <div class="hero-title-xl">
        Transform Meetings into<br><span class="gradient-text">Actionable Intelligence</span>
    </div>
    <p class="hero-desc">
        Upload a video or paste a YouTube link. Nexus AI transcribes, summarizes,
        extracts insights, and lets you chat with your content — all in one workspace.
    </p>
</div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡  Launch Studio", use_container_width=True, type="primary"):
            st.session_state.current_page = "studio"
            st.rerun()

    st.markdown(
        """
<div class="feature-grid">
    <div class="feature-tile">
        <div class="feature-icon">🎙️</div>
        <div class="feature-title">Smart Transcription</div>
        <div class="feature-desc">Accurate speech-to-text with English & Hinglish support</div>
    </div>
    <div class="feature-tile">
        <div class="feature-icon">📋</div>
        <div class="feature-title">AI Summaries</div>
        <div class="feature-desc">Concise meeting summaries generated in seconds</div>
    </div>
    <div class="feature-tile">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Deep Extraction</div>
        <div class="feature-desc">Action items, decisions, and open questions pulled automatically</div>
    </div>
    <div class="feature-tile">
        <div class="feature-icon">◈</div>
        <div class="feature-title">RAG Chat</div>
        <div class="feature-desc">Ask natural language questions about any meeting</div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    if st.session_state.analysis_history:
        st.markdown("---")
        st.markdown('<p class="page-subtitle" style="margin-bottom:1rem">Recent Activity</p>', unsafe_allow_html=True)
        recent = st.session_state.analysis_history[:3]
        cols = st.columns(len(recent))
        for col, entry in zip(cols, recent):
            with col:
                st.markdown(
                    f"""
<div class="glass-card">
    <div class="card-label"><span class="badge badge-teal">Recent</span></div>
    <div style="font-weight:600;font-size:0.95rem;margin-bottom:0.35rem">{entry['title'][:50]}{'…' if len(entry['title']) > 50 else ''}</div>
    <div style="font-size:0.75rem;color:var(--text-muted)">{entry['timestamp']} · {entry['word_count']:,} words</div>
</div>""",
                    unsafe_allow_html=True,
                )
