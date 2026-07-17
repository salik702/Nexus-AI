"""Insights dashboard — results display."""

import streamlit as st

from ui.components import (
    compute_result_metrics,
    format_content_as_html,
    render_empty_state,
    render_insight_card,
    render_metric_grid,
    esc,
)


def render() -> None:
    st.markdown('<h1 class="page-title">Insights Dashboard</h1>', unsafe_allow_html=True)

    if not st.session_state.result:
        render_empty_state(
            "📊",
            "No Analysis Yet",
            "Run an analysis in the Studio to unlock your insights dashboard with summaries, extractions, and metrics.",
        )
        if st.button("⚡ Go to Studio", type="primary"):
            st.session_state.current_page = "studio"
            st.rerun()
        return

    r = st.session_state.result

    st.markdown(
        f"""
<div class="glass-card glass-card-accent" style="margin-bottom:1.5rem">
    <div class="card-label"><span class="badge badge-teal">Session</span></div>
    <div style="font-family:var(--font-display);font-size:1.5rem;font-weight:700;line-height:1.3">
        {esc(r['title'])}
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    render_metric_grid(compute_result_metrics(r))

    tab_overview, tab_transcript, tab_extract = st.tabs(
        ["📋 Overview", "📝 Transcript", "🔍 Extractions"]
    )

    with tab_overview:
        st.markdown(
            f"""
<div class="glass-card">
    <div class="card-label">📋 Executive Summary</div>
    <div class="card-body">{format_content_as_html(r['summary'])}</div>
</div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            render_insight_card(
                "Action Items",
                "✅",
                format_content_as_html(r["action_items"]),
                "actions",
            )
        with c2:
            render_insight_card(
                "Key Decisions",
                "🔑",
                format_content_as_html(r["key_decisions"]),
                "decisions",
            )
        with c3:
            render_insight_card(
                "Open Questions",
                "❓",
                format_content_as_html(r["open_questions"]),
                "questions",
            )

    with tab_transcript:
        with st.expander("🔎 Search & Read Full Transcript", expanded=True):
            search = st.text_input("Filter transcript", placeholder="Type to highlight sections…", label_visibility="collapsed")
            transcript = r["transcript"]
            if search.strip():
                lines = transcript.split("\n")
                filtered = [l for l in lines if search.lower() in l.lower()]
                display = "\n".join(filtered) if filtered else "No matching sections found."
            else:
                display = transcript

            st.markdown(
                f'<div class="transcript-viewer">{esc(display)}</div>',
                unsafe_allow_html=True,
            )

        st.download_button(
            "⬇️ Download Transcript",
            data=r["transcript"],
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with tab_extract:
        extract_tabs = st.tabs(["✅ Actions", "🔑 Decisions", "❓ Questions"])
        with extract_tabs[0]:
            st.markdown(
                f'<div class="glass-card"><div class="card-body">{format_content_as_html(r["action_items"])}</div></div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download Actions",
                data=r["action_items"],
                file_name="action_items.txt",
                mime="text/plain",
            )
        with extract_tabs[1]:
            st.markdown(
                f'<div class="glass-card"><div class="card-body">{format_content_as_html(r["key_decisions"])}</div></div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download Decisions",
                data=r["key_decisions"],
                file_name="key_decisions.txt",
                mime="text/plain",
            )
        with extract_tabs[2]:
            st.markdown(
                f'<div class="glass-card"><div class="card-body">{format_content_as_html(r["open_questions"])}</div></div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download Questions",
                data=r["open_questions"],
                file_name="open_questions.txt",
                mime="text/plain",
            )

    st.markdown("---")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("💬 Chat with this Meeting", use_container_width=True, type="primary"):
            st.session_state.current_page = "chat"
            st.rerun()
    with action_col2:
        if st.button("⚡ Run New Analysis", use_container_width=True, type="secondary"):
            st.session_state.current_page = "studio"
            st.rerun()
