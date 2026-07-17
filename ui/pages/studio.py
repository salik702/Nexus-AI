"""Analysis Studio — input and pipeline execution."""

import streamlit as st

from services.pipeline import run_analysis_pipeline
from ui.components import render_pipeline_stepper


def render() -> None:
    st.markdown('<h1 class="page-title">Analysis Studio</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Configure your source, select language, and launch the intelligence pipeline.</p>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown(
            """
<div class="upload-zone">
    <div class="upload-icon">📁</div>
    <div style="font-family:var(--font-display);font-weight:600;font-size:1.1rem;margin-bottom:0.5rem">
        Video Source
    </div>
    <div style="font-size:0.85rem;color:var(--text-muted)">
        YouTube URL or local file path
    </div>
</div>""",
            unsafe_allow_html=True,
        )

        source = st.text_input(
            "Source URL or Path",
            value=st.session_state.source_input,
            placeholder="https://youtube.com/watch?v=... or C:/videos/meeting.mp4",
            label_visibility="collapsed",
        )

        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            language = st.selectbox(
                "Transcription Language",
                ["english", "hinglish"],
                index=0 if st.session_state.default_language == "english" else 1,
            )
        with lang_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_btn = st.button("🚀  Run Analysis", use_container_width=True, type="primary")

    with right:
        st.markdown(
            """
<div class="glass-card glass-card-accent">
    <div class="card-label">⚙️ Pipeline Overview</div>
    <div class="card-body" style="font-size:0.85rem;color:var(--text-secondary)">
        <p style="margin:0 0 0.75rem 0">Six-stage AI pipeline processes your video end-to-end:</p>
        <div style="display:flex;flex-direction:column;gap:0.5rem">
            <span><span class="badge badge-teal">1</span> Audio extraction & chunking</span>
            <span><span class="badge badge-indigo">2</span> Speech transcription</span>
            <span><span class="badge badge-amber">3</span> Title generation</span>
            <span><span class="badge badge-teal">4</span> Intelligent summarization</span>
            <span><span class="badge badge-rose">5</span> Insight extraction</span>
            <span><span class="badge badge-green">6</span> RAG engine initialization</span>
        </div>
    </div>
</div>""",
            unsafe_allow_html=True,
        )

        if st.session_state.pipeline_steps:
            st.markdown('<div class="card-label" style="margin-top:1.5rem">Live Progress</div>', unsafe_allow_html=True)
            render_pipeline_stepper(st.session_state.pipeline_steps)

    progress_placeholder = st.empty()

    if run_btn:
        if not source.strip():
            st.error("Please enter a YouTube URL or file path.")
        else:
            st.session_state.processing = True
            success = run_analysis_pipeline(source.strip(), language, progress_placeholder)
            st.session_state.processing = False
            if success:
                st.session_state.current_page = "insights"
                st.rerun()

    if st.session_state.pipeline_done and st.session_state.pipeline_steps:
        st.markdown("---")
        st.markdown('<div class="card-label">Completed Pipeline</div>', unsafe_allow_html=True)
        render_pipeline_stepper(st.session_state.pipeline_steps)

        nav_col1, nav_col2, nav_col3 = st.columns(3)
        with nav_col1:
            if st.button("📊 View Insights", use_container_width=True):
                st.session_state.current_page = "insights"
                st.rerun()
        with nav_col2:
            if st.button("💬 Open Chat", use_container_width=True):
                st.session_state.current_page = "chat"
                st.rerun()
        with nav_col3:
            if st.button("🔄 New Analysis", use_container_width=True, type="secondary"):
                st.session_state.current_page = "studio"
                st.rerun()
