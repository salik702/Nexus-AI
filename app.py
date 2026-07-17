"""Nexus AI — Premium Meeting Intelligence Dashboard."""

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from services.session import PAGES, has_result, init_session_state
from ui.components import render_app_header
from ui.navigation import close_content, render_shell_start
from ui.pages import chat, help, history, home, insights, settings, studio
from ui.styles import inject_global_styles

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus AI · Meeting Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_styles()
init_session_state()

PAGE_RENDERERS = {
    "home": home.render,
    "studio": studio.render,
    "insights": insights.render,
    "chat": chat.render,
    "history": history.render,
    "settings": settings.render,
    "help": help.render,
}

selected_page, main_col = render_shell_start()

if selected_page:
    st.session_state.current_page = selected_page
    st.rerun()

current = st.session_state.current_page
page_label = PAGES.get(current, {}).get("label", "Home")

with main_col:
    render_app_header(page_label, has_result(), st.session_state.pipeline_done)
    st.markdown('<div class="app-content">', unsafe_allow_html=True)
    PAGE_RENDERERS.get(current, home.render)()
    close_content()
