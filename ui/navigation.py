"""Application navigation shell."""

from __future__ import annotations

import streamlit as st

from services.session import PAGES, has_result
from ui.components import render_brand


def render_shell_start() -> tuple[str | None, object]:
    """Open the app shell and render navigation. Returns selected page if changed."""
    current = st.session_state.current_page
    result_available = has_result()
    selected = None

    st.markdown(
        """
<style>
[data-testid="column"]:first-child {
    background: var(--bg-elevated);
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-subtle);
    min-height: 100vh;
    padding: 1.5rem 0.75rem !important;
    position: sticky;
    top: 0;
    align-self: flex-start;
}

[data-testid="column"]:first-child .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text-secondary) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    padding: 0.65rem 0.85rem !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 0.88rem !important;
}

[data-testid="column"]:first-child .stButton > button:hover {
    background: var(--bg-glass-hover) !important;
    color: var(--text-primary) !important;
    transform: none !important;
    box-shadow: none !important;
}

[data-testid="column"]:first-child .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.15), rgba(99, 102, 241, 0.1)) !important;
    border-color: var(--border-glow) !important;
    color: var(--accent-primary) !important;
}

[data-testid="column"]:last-child {
    padding: 0 !important;
}

.nav-section-label-inline {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0.75rem 0.85rem 0.35rem;
}
</style>""",
        unsafe_allow_html=True,
    )

    nav_col, main_col = st.columns([1, 4.2], gap="small")

    with nav_col:
        st.markdown(render_brand(), unsafe_allow_html=True)

        last_section = None
        for page_key, meta in PAGES.items():
            section = meta.get("section", "Main")
            if section != last_section:
                st.markdown(f'<div class="nav-section-label-inline">{section}</div>', unsafe_allow_html=True)
                last_section = section

            requires = meta.get("requires_result", False)
            if requires and not result_available:
                st.markdown(
                    f'<div class="nav-item disabled"><span class="nav-icon">{meta["icon"]}</span><span>{meta["label"]}</span></div>',
                    unsafe_allow_html=True,
                )
                continue

            label = f'{meta["icon"]}  {meta["label"]}'
            is_active = current == page_key
            if st.button(label, key=f"nav_{page_key}", use_container_width=True, type="primary" if is_active else "secondary"):
                selected = page_key

        st.markdown(
            """
<div class="nav-footer" style="margin-top:2rem">
    <div style="font-size:0.7rem;color:var(--text-muted);padding:0.5rem 0.85rem;line-height:1.5">
        Nexus AI v2.0<br>Meeting Intelligence
    </div>
</div>""",
            unsafe_allow_html=True,
        )

    return selected, main_col


def close_content() -> None:
    st.markdown("</div>", unsafe_allow_html=True)
