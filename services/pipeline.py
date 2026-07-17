"""Video analysis pipeline — backend logic unchanged from original app."""

from __future__ import annotations

import time

import streamlit as st

from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain
from core.summarizer import generate_title, summarize
from core.transcriber import transcribe_all
from services.session import add_to_history
from utils.audio_processor import process_input


def update_step(key: str, state: str) -> None:
    st.session_state.pipeline_steps[key] = state


def run_analysis_pipeline(source: str, language: str, progress_placeholder) -> bool:
    """Execute the full analysis pipeline. Returns True on success."""
    st.session_state.pipeline_done = False
    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.pipeline_steps = {}

    try:
        with progress_placeholder.container():
            st.info("Pipeline running — track progress below…")

        update_step("audio", "active")
        chunks = process_input(source)
        update_step("audio", "done")

        update_step("transcript", "active")
        transcript = transcribe_all(chunks, language)
        update_step("transcript", "done")

        update_step("title", "active")
        title = generate_title(transcript)
        update_step("title", "done")

        update_step("summary", "active")
        summary = summarize(transcript)
        update_step("summary", "done")

        update_step("extract", "active")
        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)
        update_step("extract", "done")

        update_step("rag", "active")
        rag_chain = build_rag_chain(transcript)
        update_step("rag", "done")

        result = {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain": rag_chain,
        }

        st.session_state.result = result
        st.session_state.pipeline_done = True
        st.session_state.source_input = source
        add_to_history(result, source)

        progress_placeholder.success("Analysis complete!")
        time.sleep(0.5)
        progress_placeholder.empty()
        return True

    except Exception as e:
        for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
            if st.session_state.pipeline_steps.get(k) == "active":
                st.session_state.pipeline_steps[k] = "pending"
        progress_placeholder.error(f"Error: {e}")
        return False
