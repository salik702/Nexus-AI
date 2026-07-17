"""Global stylesheet for the premium SaaS dashboard UI."""


def inject_global_styles() -> None:
    import streamlit as st

    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

:root {
    --bg-deep: #06080f;
    --bg-base: #0b0f1a;
    --bg-elevated: rgba(16, 22, 38, 0.72);
    --bg-glass: rgba(255, 255, 255, 0.04);
    --bg-glass-hover: rgba(255, 255, 255, 0.07);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(20, 184, 166, 0.35);
    --accent-primary: #14b8a6;
    --accent-secondary: #6366f1;
    --accent-warm: #f59e0b;
    --accent-rose: #f43f5e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --success: #22c55e;
    --warning: #eab308;
    --danger: #ef4444;
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --shadow-soft: 0 4px 24px rgba(0, 0, 0, 0.25);
    --shadow-glow: 0 0 40px rgba(20, 184, 166, 0.12);
    --font-display: 'Outfit', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    --nav-width: 260px;
    --header-height: 64px;
}

html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15), transparent),
        radial-gradient(ellipse 60% 40% at 100% 100%, rgba(20, 184, 166, 0.08), transparent),
        var(--bg-deep) !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* ── App Shell ── */
.app-shell {
    display: flex;
    min-height: 100vh;
}

.app-nav {
    width: var(--nav-width);
    min-width: var(--nav-width);
    background: var(--bg-elevated);
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-subtle);
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 100;
    overflow-y: auto;
}

.app-main {
    margin-left: var(--nav-width);
    flex: 1;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.app-header {
    height: var(--header-height);
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-subtle);
    background: rgba(6, 8, 15, 0.6);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 50;
}

.app-content {
    padding: 2rem 2.5rem 3rem;
    flex: 1;
}

/* ── Brand ── */
.brand-mark {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    margin-bottom: 2rem;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    box-shadow: var(--shadow-glow);
}

.brand-name {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-primary);
    line-height: 1.2;
}

.brand-tagline {
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

/* ── Navigation ── */
.nav-section-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.7rem 0.85rem;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    cursor: default;
    transition: all 0.2s ease;
    margin-bottom: 0.15rem;
    border: 1px solid transparent;
}

.nav-item:hover {
    background: var(--bg-glass-hover);
    color: var(--text-primary);
}

.nav-item.active {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.15), rgba(99, 102, 241, 0.1));
    border-color: var(--border-glow);
    color: var(--accent-primary);
}

.nav-item.disabled {
    opacity: 0.4;
    pointer-events: none;
}

.nav-icon {
    font-size: 1.1rem;
    width: 1.5rem;
    text-align: center;
}

.nav-badge {
    margin-left: auto;
    font-size: 0.6rem;
    padding: 0.15rem 0.45rem;
    border-radius: 20px;
    background: rgba(20, 184, 166, 0.2);
    color: var(--accent-primary);
    font-weight: 600;
}

.nav-footer {
    margin-top: auto;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-subtle);
}

/* ── Header ── */
.header-breadcrumb {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.header-breadcrumb span:last-child {
    color: var(--text-primary);
    font-weight: 600;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
}

.status-pill.live {
    border-color: rgba(34, 197, 94, 0.4);
    color: var(--success);
}

.status-pill.idle {
    color: var(--text-muted);
}

.status-dot-sm {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
}

.status-pill.live .status-dot-sm {
    animation: blink 2s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Typography ── */
.page-title {
    font-family: var(--font-display);
    font-size: clamp(1.75rem, 3vw, 2.25rem);
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.02em;
}

.page-subtitle {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin: 0 0 2rem 0;
    line-height: 1.6;
}

.gradient-text {
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-warm) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Glass Cards ── */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow: var(--shadow-soft);
    transform: translateY(-2px);
}

.glass-card-accent::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.card-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-body {
    font-size: 0.9rem;
    line-height: 1.75;
    color: var(--text-primary);
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    text-align: center;
    transition: all 0.2s;
}

.metric-card:hover {
    border-color: var(--border-glow);
}

.metric-value {
    font-family: var(--font-display);
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--accent-primary);
    line-height: 1;
}

.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}

.badge-teal { background: rgba(20, 184, 166, 0.15); color: var(--accent-primary); border: 1px solid rgba(20, 184, 166, 0.3); }
.badge-indigo { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
.badge-amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-warm); border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-green { background: rgba(34, 197, 94, 0.15); color: var(--success); border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-rose { background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.3); }

/* ── Pipeline Stepper ── */
.pipeline-track {
    display: flex;
    align-items: center;
    gap: 0;
    padding: 1.25rem;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    overflow-x: auto;
}

.pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    min-width: 80px;
    position: relative;
}

.pipeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: calc(50% + 20px);
    width: calc(100% - 40px);
    height: 2px;
    background: var(--border-subtle);
}

.pipeline-step.done:not(:last-child)::after {
    background: var(--accent-primary);
}

.pipeline-step.active:not(:last-child)::after {
    background: linear-gradient(90deg, var(--accent-primary), var(--border-subtle));
}

.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    border: 2px solid var(--border-subtle);
    background: var(--bg-base);
    z-index: 1;
    transition: all 0.3s;
}

.pipeline-step.pending .step-circle { color: var(--text-muted); }
.pipeline-step.active .step-circle {
    border-color: var(--accent-primary);
    background: rgba(20, 184, 166, 0.15);
    color: var(--accent-primary);
    box-shadow: 0 0 20px rgba(20, 184, 166, 0.3);
    animation: stepPulse 1.5s infinite;
}

.pipeline-step.done .step-circle {
    border-color: var(--success);
    background: rgba(34, 197, 94, 0.15);
    color: var(--success);
}

@keyframes stepPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(20, 184, 166, 0.3); }
    50% { box-shadow: 0 0 30px rgba(20, 184, 166, 0.5); }
}

.step-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    text-align: center;
    font-weight: 500;
}

.pipeline-step.active .step-label,
.pipeline-step.done .step-label {
    color: var(--text-secondary);
}

/* ── Hero Section ── */
.hero-section {
    text-align: center;
    padding: 3rem 2rem 4rem;
    position: relative;
}

.hero-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(20, 184, 166, 0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-title-xl {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 5vw, 3.75rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}

.hero-desc {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    max-width: 900px;
    margin: 0 auto;
}

.feature-tile {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.75rem 1.25rem;
    text-align: center;
    transition: all 0.25s;
}

.feature-tile:hover {
    border-color: var(--border-glow);
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
}

.feature-title {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.4rem;
}

.feature-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.5;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: var(--bg-glass);
    border: 1px dashed var(--border-subtle);
    border-radius: var(--radius-lg);
}

.empty-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    opacity: 0.8;
}

.empty-title {
    font-family: var(--font-display);
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.empty-desc {
    color: var(--text-muted);
    font-size: 0.9rem;
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Chat Interface ── */
.chat-panel {
    display: flex;
    flex-direction: column;
    height: calc(100vh - var(--header-height) - 280px);
    min-height: 400px;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
}

.chat-row {
    display: flex;
    margin-bottom: 1.25rem;
    animation: fadeUp 0.3s ease;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-row.user { justify-content: flex-end; }
.chat-row.assistant { justify-content: flex-start; }

.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

.chat-row.user .chat-avatar {
    background: linear-gradient(135deg, var(--accent-secondary), #4f46e5);
    margin-left: 0.75rem;
    order: 2;
}

.chat-row.assistant .chat-avatar {
    background: linear-gradient(135deg, var(--accent-primary), #0d9488);
    margin-right: 0.75rem;
}

.chat-bubble {
    max-width: 75%;
    padding: 0.85rem 1.15rem;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.65;
}

.chat-row.user .chat-bubble {
    background: rgba(99, 102, 241, 0.18);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-bottom-right-radius: 4px;
}

.chat-row.assistant .chat-bubble {
    background: rgba(20, 184, 166, 0.12);
    border: 1px solid rgba(20, 184, 166, 0.2);
    border-bottom-left-radius: 4px;
}

.chat-suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.suggestion-chip {
    padding: 0.4rem 0.85rem;
    border-radius: 20px;
    font-size: 0.78rem;
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    cursor: default;
}

/* ── Transcript ── */
.transcript-viewer {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 1.5rem;
    font-size: 0.85rem;
    line-height: 1.85;
    color: var(--text-secondary);
    max-height: 480px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Sans', monospace;
}

/* ── History Timeline ── */
.timeline-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-subtle);
}

.timeline-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-primary);
    margin-top: 0.4rem;
    flex-shrink: 0;
    box-shadow: 0 0 10px rgba(20, 184, 166, 0.4);
}

.timeline-content { flex: 1; }

.timeline-title {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
}

.timeline-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* ── Insight Cards ── */
.insight-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    height: 100%;
    border-top: 3px solid var(--accent-primary);
}

.insight-card.decisions { border-top-color: var(--accent-secondary); }
.insight-card.questions { border-top-color: var(--accent-warm); }

.insight-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.insight-header h4 {
    font-family: var(--font-display);
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
}

/* ── Workspace Layout ── */
.workspace-split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.upload-zone {
    border: 2px dashed var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 3rem 2rem;
    text-align: center;
    background: var(--bg-glass);
    transition: all 0.25s;
}

.upload-zone:hover {
    border-color: var(--accent-primary);
    background: rgba(20, 184, 166, 0.04);
}

.upload-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
}

/* ── Settings ── */
.settings-group {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.settings-group-title {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
}

/* ── Help / FAQ ── */
.faq-item {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

.faq-q {
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
}

.faq-a {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* ── Streamlit Overrides ── */
.stButton > button {
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s !important;
    border: none !important;
}

.stButton > button[kind="primary"],
.stButton > button:not([kind="secondary"]) {
    background: linear-gradient(135deg, var(--accent-primary), #0d9488) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button:not([kind="secondary"]):hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(20, 184, 166, 0.35) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.15) !important;
}

[data-testid="stTabs"] button {
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent-primary) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
}

.stSpinner > div {
    border-top-color: var(--accent-primary) !important;
}

[data-testid="stExpander"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
}

label, .stCaption {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-subtle); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

/* Hide default streamlit nav buttons styling in our layout */
div[data-testid="column"] .stButton > button {
    width: 100%;
}

.nav-btn-hidden label { display: none; }
</style>
""",
        unsafe_allow_html=True,
    )
