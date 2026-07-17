"""Help and documentation page."""

import streamlit as st

from ui.components import render_glass_card


def render() -> None:
    st.markdown('<h1 class="page-title">Help Center</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Everything you need to get the most out of Nexus AI Meeting Intelligence.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="glass-card glass-card-accent" style="margin-bottom:1.5rem">
    <div class="card-label">🚀 Quick Start</div>
    <div class="card-body">
        <ol style="margin:0;padding-left:1.25rem;line-height:2">
            <li>Navigate to <strong>Studio</strong> from the sidebar</li>
            <li>Paste a YouTube URL or local video file path</li>
            <li>Select your transcription language (English or Hinglish)</li>
            <li>Click <strong>Run Analysis</strong> and watch the pipeline progress</li>
            <li>Explore results in <strong>Insights</strong> or chat in <strong>Ask AI</strong></li>
        </ol>
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    faqs = [
        (
            "What video sources are supported?",
            "YouTube URLs and local file paths (MP4, MP3, and other formats supported by the audio processor). "
            "Paste the full URL or absolute path to your file.",
        ),
        (
            "What is the difference between English and Hinglish?",
            "English mode transcribes standard English speech. Hinglish mode handles Hindi-English code-mixed speech "
            "common in Indian meetings and conversations.",
        ),
        (
            "How does the AI Chat work?",
            "After analysis, a RAG (Retrieval-Augmented Generation) engine indexes your transcript. "
            "When you ask a question, relevant sections are retrieved and used to generate accurate, context-aware answers.",
        ),
        (
            "What gets extracted automatically?",
            "The pipeline extracts action items, key decisions, and open questions from your meeting transcript "
            "using specialized AI prompts — no manual tagging required.",
        ),
        (
            "Is my data stored permanently?",
            "All data exists only in your current browser session. Closing the tab clears everything unless you download exports.",
        ),
    ]

    st.markdown('<div class="card-label">❓ Frequently Asked Questions</div>', unsafe_allow_html=True)
    for question, answer in faqs:
        st.markdown(
            f"""
<div class="faq-item">
    <div class="faq-q">{question}</div>
    <div class="faq-a">{answer}</div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        render_glass_card(
            "📋 Supported Outputs",
            "• Full transcript<br>• Executive summary<br>• Action items<br>• Key decisions<br>• Open questions<br>• Interactive Q&A",
        )
    with col2:
        render_glass_card(
            "⚙️ Pipeline Stages",
            "1. Audio processing<br>2. Transcription<br>3. Title generation<br>4. Summarization<br>5. Insight extraction<br>6. RAG initialization",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Get Started in Studio", type="primary"):
        st.session_state.current_page = "studio"
        st.rerun()
