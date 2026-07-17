"""Settings page."""

import streamlit as st

from ui.components import render_glass_card


def render() -> None:
    st.markdown('<h1 class="page-title">Settings</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Configure defaults and manage your workspace preferences.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="settings-group">
    <div class="settings-group-title">🌐 Language Preferences</div>
</div>""",
        unsafe_allow_html=True,
    )

    default_lang = st.selectbox(
        "Default Transcription Language",
        ["english", "hinglish"],
        index=0 if st.session_state.default_language == "english" else 1,
        help="This language will be pre-selected when you open the Studio.",
    )

    if default_lang != st.session_state.default_language:
        st.session_state.default_language = default_lang
        st.toast("Language preference saved.")

    st.markdown(
        """
<div class="settings-group">
    <div class="settings-group-title">📊 Session Data</div>
</div>""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Analyses This Session", len(st.session_state.analysis_history))
    with col2:
        st.metric("Chat Messages", len(st.session_state.chat_history))

    st.markdown("<br>", unsafe_allow_html=True)

    reset_col1, reset_col2 = st.columns(2)
    with reset_col1:
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.toast("Chat history cleared.")
            st.rerun()
    with reset_col2:
        if st.button("🔄 Reset All Session Data", use_container_width=True, type="secondary"):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.session_state.pipeline_done = False
            st.session_state.pipeline_steps = {}
            st.session_state.analysis_history = []
            st.session_state.source_input = ""
            st.toast("Session data reset.")
            st.rerun()

    st.markdown("---")

    render_glass_card(
        "ℹ️ About Configuration",
        "API keys and model settings are managed via your <code>.env</code> file. "
        "Ensure your environment variables are configured before running analyses.",
    )
