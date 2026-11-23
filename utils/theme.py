"""
Global app theme utilities — Fintech Dark Terminal UI.
Redesigned for professional, institutional-grade aesthetics.
Zero functional changes — only CSS & layout styling.
"""

import streamlit as st


ONBOARDING_STEPS = [
    {
        "icon": "✦",
        "eyebrow": "Selamat datang",
        "title": "Mulai dari universe yang relevan",
        "description": (
            "Screener akan mencari emiten IDX secara otomatis. Anda hanya perlu "
            "memilih kriteria kualitas, likuiditas, harga, dan sektor."
        ),
        "tip": "Tidak perlu mengisi kode saham satu per satu.",
    },
    {
        "icon": "01",
        "eyebrow": "Langkah 1",
        "title": "Buat Filter Universe",
        "description": (
            "Buka Universe Filter, atur market cap minimum, volume harian, "
            "rentang harga, lalu pilih sektor apabila diperlukan."
        ),
        "tip": "Klik Terapkan Filter untuk menyimpan daftar emiten yang lolos.",
    },
    {
        "icon": "02",
        "eyebrow": "Langkah 2",
        "title": "Atur sumber dan profil risiko",
        "description": (
            "Di Scan Harian, gunakan Filtered Universe. Lalu atur periode scan, "
            "maksimum RSI, R/R target, serta modal trading."
        ),
        "tip": "Mulai dengan kriteria konservatif, lalu evaluasi hasilnya.",
    },
    {
        "icon": "03",
        "eyebrow": "Langkah 3",
        "title": "Jalankan scan dan pilih sinyal",
        "description": (
            "Klik Mulai Scan untuk memeriksa emiten secara otomatis. "
            "Tinjau sinyal BUY, harga entry, stop loss, dan target profit."
        ),
        "tip": "Gunakan chart dan kondisi pasar sebagai konfirmasi tambahan.",
    },
    {
        "icon": "04",
        "eyebrow": "Langkah terakhir",
        "title": "Catat dan evaluasi trade",
        "description": (
            "Gunakan Journal untuk mencatat eksekusi, hasil, serta win rate. "
            "Gunakan Backtest untuk menguji strategi sebelum dipakai."
        ),
        "tip": "Panduan ini selalu bisa dibuka kembali dari sidebar.",
    },
]


def render_onboarding() -> None:
    """Show a first-run, dismissible onboarding dialog."""
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0

    if not st.session_state.onboarding_complete:
        st.session_state.onboarding_open = True
    if not st.session_state.get("onboarding_open", False):
        return
    if not hasattr(st, "dialog"):
        return

    @st.dialog("Panduan Penggunaan Screener", width="large")
    def onboarding_dialog():
        step = st.session_state.onboarding_step
        item = ONBOARDING_STEPS[step]

        dot_labels = "".join(
            f'<span class="guide-dot {"guide-dot-active" if i == step else ""}{ " guide-dot-done" if i < step else ""}">{i + 1}</span>'
            for i in range(len(ONBOARDING_STEPS))
        )
        st.markdown(
            f'<div class="guide-progress">{dot_labels}</div>',
            unsafe_allow_html=True,
        )
        st.progress((step + 1) / len(ONBOARDING_STEPS))
        st.markdown(
            f"""
            <div class="onboarding-shell">
                <div class="onboarding-step-badge">{item["icon"]}</div>
                <p class="onboarding-eyebrow">{item["eyebrow"]}</p>
                <h2 class="onboarding-title">{item["title"]}</h2>
                <p class="onboarding-description">{item["description"]}</p>
                <div class="onboarding-tip">💡 {item["tip"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        left, middle, right = st.columns(3)
        with left:
            if st.button("Lewati", key="onboarding_skip", use_container_width=True):
                st.session_state.onboarding_complete = True
                st.session_state.onboarding_open = False
                st.rerun()
        with middle:
            if step > 0:
                if st.button("Kembali", key="onboarding_back", use_container_width=True):
                    st.session_state.onboarding_step = max(0, step - 1)
                    st.rerun()
        with right:
            if step < len(ONBOARDING_STEPS) - 1:
                if st.button("Selanjutnya", key="onboarding_next", type="primary", use_container_width=True):
                    st.session_state.onboarding_step = step + 1
                    st.rerun()
            else:
                if st.button("Mulai Screener", key="onboarding_finish", type="primary", use_container_width=True):
                    st.session_state.onboarding_complete = True
                    st.session_state.onboarding_open = False
                    st.rerun()

    onboarding_dialog()


def _build_theme_css(is_dark: bool) -> str:
    if is_dark:
        return """
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-main: #0B0F17;
            --bg-gradient: radial-gradient(ellipse 1400px 900px at 60% -20%, rgba(37,99,235,0.12) 0%, #0B0F17 60%);
            --bg-card: rgba(17, 24, 39, 0.85);
            --bg-card-hover: rgba(22, 32, 52, 0.95);
            --bg-card-soft: rgba(255, 255, 255, 0.04);
            --bg-sidebar: rgba(9, 14, 24, 0.97);
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --border-color: rgba(255, 255, 255, 0.07);
            --border-accent: rgba(59, 130, 246, 0.35);
            --accent: #3B82F6;
            --accent-2: #2563EB;
            --accent-glow: rgba(59, 130, 246, 0.25);
            --success: #10B981;
            --success-bg: rgba(16, 185, 129, 0.12);
            --danger: #EF4444;
            --danger-bg: rgba(239, 68, 68, 0.12);
            --warning: #F59E0B;
            --warning-bg: rgba(245, 158, 11, 0.12);
            --mono-font: 'JetBrains Mono', 'Roboto Mono', monospace;
            --ui-font: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }

        /* ─── Global ─── */
        .stApp {
            font-family: var(--ui-font);
            color: var(--text-primary);
            background: var(--bg-gradient);
            background-attachment: fixed;
            min-height: 100vh;
        }

        /* ─── Scrollbar ─── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.3); border-radius: 99px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(59,130,246,0.55); }

        /* ─── Header ─── */
        [data-testid="stHeader"] {
            background: rgba(7, 11, 20, 0.80) !important;
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
        }

        /* ─── Sidebar ─── */
        section[data-testid="stSidebar"] {
            background: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-color) !important;
            backdrop-filter: blur(20px);
        }
        section[data-testid="stSidebar"] .stMarkdown h3 {
            font-size: 0.72rem !important;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
            margin: 1.2rem 0 0.5rem 0 !important;
        }
        section[data-testid="stSidebar"] .stMarkdown hr {
            border-color: var(--border-color) !important;
            margin: 0.75rem 0 !important;
        }

        /* ─── Typography ─── */
        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
            letter-spacing: -0.025em;
            font-family: var(--ui-font);
        }
        h1 { font-size: 1.75rem !important; font-weight: 800 !important; }
        h2 { font-size: 1.35rem !important; font-weight: 700 !important; }
        h3 { font-size: 1.1rem !important; font-weight: 700 !important; }

        .stApp, .stApp p, .stApp li, .stApp label, .stApp span,
        .stMarkdown,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stMarkdownContainer"] strong,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] label,
        div[data-testid="stMetricValue"] div,
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] label {
            color: var(--text-secondary) !important;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        div[data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
        }

        .stApp a, .stApp a:visited { color: #60A5FA !important; }

        /* ─── Metric Cards ─── */
        .stMetric {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 1rem 1.1rem !important;
            backdrop-filter: blur(8px);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .stMetric:hover {
            border-color: var(--border-accent) !important;
            box-shadow: 0 0 0 1px var(--accent-glow), 0 8px 24px rgba(0,0,0,0.3);
        }
        [data-testid="stMetricValue"] {
            font-family: var(--mono-font) !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            font-variant-numeric: tabular-nums;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.72rem !important;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: var(--mono-font) !important;
            font-variant-numeric: tabular-nums;
        }

        /* ─── Alerts ─── */
        .stAlert {
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--border-color) !important;
            backdrop-filter: blur(4px);
        }
        .stAlert[data-baseweb="notification"][kind="positive"] {
            background: var(--success-bg) !important;
            border-color: rgba(16,185,129,0.3) !important;
        }
        .stAlert[data-baseweb="notification"][kind="warning"] {
            background: var(--warning-bg) !important;
            border-color: rgba(245,158,11,0.3) !important;
        }
        .stAlert[data-baseweb="notification"][kind="negative"] {
            background: var(--danger-bg) !important;
            border-color: rgba(239,68,68,0.3) !important;
        }

        /* ─── Buttons ─── */
        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            border-radius: var(--radius-sm) !important;
            font-family: var(--ui-font) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            transition: all 0.18s cubic-bezier(.4,0,.2,1) !important;
            border: 1px solid var(--border-color) !important;
            background: rgba(255,255,255,0.05) !important;
            color: var(--text-secondary) !important;
        }
        .stButton > button:hover {
            background: rgba(255,255,255,0.09) !important;
            border-color: rgba(255,255,255,0.15) !important;
            color: var(--text-primary) !important;
            transform: translateY(-1px);
        }
        .stButton > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
            border-color: transparent !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
        }
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(37,99,235,0.55) !important;
            transform: translateY(-2px);
        }

        /* ─── Form Inputs ─── */
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stNumberInput > div > div > input,
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stDateInput > div > div > input {
            background: rgba(17, 24, 39, 0.9) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: var(--radius-sm) !important;
            font-family: var(--ui-font) !important;
        }
        .stSelectbox > div > div:focus-within,
        .stNumberInput > div > div > input:focus,
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus {
            border-color: var(--border-accent) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }

        /* ─── Tabs ─── */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-card) !important;
            border-radius: var(--radius-md) !important;
            padding: 4px !important;
            border: 1px solid var(--border-color) !important;
            gap: 2px !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            color: var(--text-secondary) !important;
            background: transparent !important;
            padding: 0.45rem 1.1rem !important;
            transition: all 0.15s ease !important;
        }
        .stTabs [aria-selected="true"] {
            background: var(--accent) !important;
            color: #ffffff !important;
            box-shadow: 0 2px 10px rgba(37,99,235,0.4) !important;
        }
        .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

        /* ─── Expander ─── */
        [data-testid="stExpander"] {
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg-card) !important;
            overflow: hidden !important;
        }
        [data-testid="stExpander"] summary {
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            padding: 0.75rem 1rem !important;
        }
        [data-testid="stExpander"] summary:hover { color: var(--text-primary) !important; }

        /* ─── DataFrame ─── */
        [data-testid="stDataFrame"] {
            border-radius: var(--radius-md) !important;
            overflow: hidden !important;
            border: 1px solid var(--border-color) !important;
        }

        /* ─── Progress Bar ─── */
        [data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, var(--accent), var(--success)) !important;
            border-radius: 99px !important;
        }
        [data-testid="stProgress"] > div > div {
            border-radius: 99px !important;
            background: rgba(255,255,255,0.06) !important;
        }

        /* ─── Slider ─── */
        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
            background: var(--accent) !important;
            color: white !important;
            border-radius: 6px !important;
            font-family: var(--mono-font) !important;
            font-size: 0.75rem !important;
        }
        [data-baseweb="slider"] [role="slider"] {
            background: var(--accent) !important;
            border: 2px solid var(--accent) !important;
            box-shadow: 0 0 0 4px var(--accent-glow) !important;
        }

        /* ─── Dialog (Onboarding) ─── */
        [data-testid="stDialog"],
        [data-testid="stDialog"] > div,
        [role="dialog"] {
            background: #0D1626 !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-xl) !important;
        }
        [role="dialog"] h1, [role="dialog"] h2, [role="dialog"] h3,
        [role="dialog"] p, [role="dialog"] li, [role="dialog"] span, [role="dialog"] strong,
        [data-testid="stDialog"] h1, [data-testid="stDialog"] h2, [data-testid="stDialog"] h3,
        [data-testid="stDialog"] p, [data-testid="stDialog"] li, [data-testid="stDialog"] strong {
            color: var(--text-secondary) !important;
        }
        [role="dialog"] h1, [role="dialog"] h2, [role="dialog"] h3,
        [data-testid="stDialog"] h1, [data-testid="stDialog"] h2, [data-testid="stDialog"] h3,
        [role="dialog"] .onboarding-title,
        [data-testid="stDialog"] .onboarding-title {
            color: var(--text-primary) !important;
        }
        [role="dialog"] .onboarding-description,
        [role="dialog"] .onboarding-tip,
        [data-testid="stDialog"] .onboarding-description,
        [data-testid="stDialog"] .onboarding-tip {
            color: var(--text-secondary) !important;
            background: var(--bg-card-soft) !important;
            text-align: center !important;
        }

        /* ─── Hero Panel ─── */
        .hero-panel {
            border-radius: var(--radius-xl);
            padding: 1.75rem 2rem;
            background: linear-gradient(135deg, rgba(37,99,235,0.18) 0%, rgba(17,24,39,0.6) 60%, rgba(16,185,129,0.1) 100%);
            border: 1px solid rgba(59,130,246,0.25);
            box-shadow: 0 1px 0 rgba(255,255,255,0.05) inset, 0 20px 40px rgba(0,0,0,0.4);
            margin-bottom: 1.25rem;
            position: relative;
            overflow: hidden;
        }
        .hero-panel::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(59,130,246,0.6), transparent);
        }

        /* ─── Status Pill ─── */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border-radius: 999px;
            padding: 0.3rem 0.9rem;
            font-weight: 700;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1rem;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.4);
            color: #93C5FD !important;
        }
        .status-pill::before {
            content: '';
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 6px #10B981;
        }

        /* ─── Feature Cards ─── */
        .feature-card {
            border-radius: var(--radius-md);
            padding: 1.25rem;
            min-height: 180px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            backdrop-filter: blur(8px);
            transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
            cursor: default;
        }
        .feature-card:hover {
            border-color: var(--border-accent);
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.4), 0 0 0 1px var(--accent-glow);
        }
        .feature-card h4 {
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.6rem !important;
            color: var(--text-primary) !important;
        }
        .feature-card p {
            font-size: 0.84rem !important;
            line-height: 1.6 !important;
            color: var(--text-secondary) !important;
        }
        .feature-card .micro-note {
            font-size: 0.76rem !important;
            color: var(--text-muted) !important;
            margin-top: 0.75rem !important;
            padding-top: 0.75rem !important;
            border-top: 1px solid var(--border-color) !important;
        }

        /* ─── Workflow Box ─── */
        .workflow-box {
            border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            background: rgba(37,99,235,0.07);
            border: 1px solid rgba(59,130,246,0.2);
            transition: border-color 0.2s ease;
        }
        .workflow-box:hover { border-color: rgba(59,130,246,0.4); }
        .workflow-box h4 {
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            color: #60A5FA !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.75rem !important;
        }
        .workflow-box ol, .workflow-box li {
            font-size: 0.875rem !important;
            color: var(--text-secondary) !important;
            line-height: 1.8 !important;
        }

        /* ─── Section Label ─── */
        .section-label {
            font-weight: 700 !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* ─── Mono Numbers ─── */
        .mono-num {
            font-family: var(--mono-font) !important;
            font-variant-numeric: tabular-nums;
            font-size: 0.95rem;
        }

        /* ─── Ticker Badge ─── */
        .ticker-badge {
            font-family: var(--mono-font) !important;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.3);
            color: #93C5FD !important;
            border-radius: 6px;
            padding: 0.15rem 0.5rem;
            display: inline-block;
        }

        /* ─── Signal Badges ─── */
        .signal-buy {
            background: var(--success-bg);
            border: 1px solid rgba(16,185,129,0.4);
            color: #34D399 !important;
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .signal-warning {
            background: var(--warning-bg);
            border: 1px solid rgba(245,158,11,0.4);
            color: #FCD34D !important;
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
        }

        /* ─── Stat Card ─── */
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1.1rem 1.25rem;
            transition: border-color 0.2s ease;
        }
        .stat-card:hover { border-color: var(--border-accent); }
        .stat-card-label {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
            margin-bottom: 0.4rem;
        }
        .stat-card-value {
            font-family: var(--mono-font);
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary) !important;
            font-variant-numeric: tabular-nums;
            line-height: 1;
        }
        .stat-card-value.positive { color: var(--success) !important; }
        .stat-card-value.negative { color: var(--danger) !important; }
        .stat-card-value.warning { color: var(--warning) !important; }

        /* ─── RR Box ─── */
        .rr-box {
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            border: 1px solid rgba(16,185,129,0.25);
            background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(5,150,105,0.05));
        }
        .rr-label {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
            margin-bottom: 0.3rem;
        }
        .rr-value {
            font-family: var(--mono-font);
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--success) !important;
        }

        /* ─── Info Panel ─── */
        .info-panel {
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            background: rgba(59,130,246,0.07);
            border: 1px solid rgba(59,130,246,0.2);
            font-size: 0.875rem;
            line-height: 1.65;
        }
        .info-panel .info-title {
            font-weight: 700;
            color: #60A5FA !important;
            margin-bottom: 0.4rem;
        }

        /* ─── Callout Boxes ─── */
        .callout-tip {
            border-radius: var(--radius-sm);
            padding: 0.9rem 1.1rem;
            background: rgba(16,185,129,0.08);
            border-left: 3px solid var(--success);
            margin: 0.75rem 0;
        }
        .callout-warn {
            border-radius: var(--radius-sm);
            padding: 0.9rem 1.1rem;
            background: rgba(245,158,11,0.08);
            border-left: 3px solid var(--warning);
            margin: 0.75rem 0;
        }
        .callout-info {
            border-radius: var(--radius-sm);
            padding: 0.9rem 1.1rem;
            background: rgba(59,130,246,0.08);
            border-left: 3px solid var(--accent);
            margin: 0.75rem 0;
        }

        /* ─── Divider ─── */
        hr {
            border: none !important;
            border-top: 1px solid var(--border-color) !important;
            margin: 1.25rem 0 !important;
        }

        /* ─── Onboarding Dialog ─── */
        .onboarding-shell {
            min-height: 240px;
            text-align: center;
            padding: 0.5rem 1.5rem 1rem 1.5rem;
        }
        .onboarding-step-badge {
            width: 56px; height: 56px;
            margin: 0 auto 1rem auto;
            display: grid; place-items: center;
            border-radius: 16px;
            font-size: 1.1rem; font-weight: 800;
            color: #ffffff;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 8px 24px rgba(37,99,235,0.4);
            font-family: var(--mono-font);
        }
        .onboarding-eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.7rem !important;
            font-weight: 800;
            color: var(--accent) !important;
            margin-bottom: 0.4rem !important;
        }
        .onboarding-title { margin: 0 0 0.9rem 0; font-size: 1.55rem !important; }
        .onboarding-description {
            max-width: 580px; margin: 0 auto 1.1rem auto;
            line-height: 1.7; font-size: 0.95rem;
            color: var(--text-secondary) !important;
        }
        .onboarding-tip {
            max-width: 560px; margin: 0 auto;
            border-radius: var(--radius-sm);
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-color);
            background: var(--bg-card-soft);
            color: var(--text-secondary) !important;
            font-size: 0.875rem;
        }

        /* ─── Guide Progress Dots ─── */
        .guide-progress {
            display: flex; align-items: center;
            justify-content: center;
            gap: 0.5rem; margin: 0.2rem 0 0.9rem 0;
        }
        .guide-dot {
            width: 28px; height: 28px;
            display: inline-grid; place-items: center;
            border-radius: 50%;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-muted) !important;
            font-size: 0.72rem; font-weight: 800;
            font-family: var(--mono-font);
        }
        .guide-dot-active {
            color: #ffffff !important;
            background: var(--accent);
            border-color: transparent;
            box-shadow: 0 4px 14px rgba(37,99,235,0.45);
        }
        .guide-dot-done { color: var(--success) !important; border-color: var(--success); }

        /* ─── Guide Content ─── */
        .guide-content-card {
            min-height: 200px; border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
        }
        .guide-card-icon {
            width: 48px; height: 48px;
            display: grid; place-items: center;
            margin-bottom: 0.75rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            background: var(--bg-card-soft);
            font-size: 1.35rem;
        }
        .guide-description {
            max-width: 680px; line-height: 1.75;
            font-size: 0.95rem; text-align: center;
            color: var(--text-secondary) !important;
            margin: 0 auto;
        }

        /* ─── Footer ─── */
        .footer-note {
            text-align: center;
            color: var(--text-muted) !important;
            font-size: 0.8rem;
            padding: 1.5rem 0 0.5rem 0;
        }
        """

    # ─── Light Theme ───
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-main: #F0F4FF;
        --bg-gradient: radial-gradient(ellipse 1200px 800px at 50% -10%, #DBEAFE 0%, #F0F4FF 55%);
        --bg-card: rgba(255, 255, 255, 0.92);
        --bg-card-soft: rgba(239, 246, 255, 0.7);
        --bg-sidebar: rgba(248, 251, 255, 0.97);
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
        --border-color: rgba(0, 0, 0, 0.08);
        --border-accent: rgba(37, 99, 235, 0.4);
        --accent: #2563EB;
        --accent-2: #1D4ED8;
        --accent-glow: rgba(37, 99, 235, 0.15);
        --success: #059669;
        --success-bg: rgba(5, 150, 105, 0.1);
        --danger: #DC2626;
        --danger-bg: rgba(220, 38, 38, 0.08);
        --warning: #D97706;
        --warning-bg: rgba(217, 119, 6, 0.1);
        --mono-font: 'JetBrains Mono', 'Roboto Mono', monospace;
        --ui-font: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        --radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px; --radius-xl: 20px;
    }

    .stApp {
        font-family: var(--ui-font);
        color: var(--text-primary);
        background: var(--bg-gradient);
        background-attachment: fixed;
    }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(37,99,235,0.25); border-radius: 99px; }

    [data-testid="stHeader"] {
        background: rgba(240,244,255,0.75) !important;
        backdrop-filter: blur(16px);
        border-bottom: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.72rem !important; font-weight: 700;
        letter-spacing: 0.1em; text-transform: uppercase;
        color: var(--text-muted) !important;
        margin: 1.2rem 0 0.5rem 0 !important;
    }

    h1, h2, h3, h4 { color: var(--text-primary) !important; letter-spacing: -0.025em; }
    h1 { font-size: 1.75rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.35rem !important; font-weight: 700 !important; }

    .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stMarkdown,
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span, div[data-testid="stMarkdownContainer"] strong,
    div[data-testid="stMetricLabel"] p, div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricValue"] div, div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span, section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li, section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    div[data-testid="stMetricValue"] { color: var(--text-primary) !important; }
    .stApp a, .stApp a:visited { color: var(--accent) !important; }

    .stMetric {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.1rem !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        transition: box-shadow 0.2s ease !important;
    }
    .stMetric:hover { box-shadow: 0 4px 16px rgba(37,99,235,0.1) !important; }
    [data-testid="stMetricValue"] {
        font-family: var(--mono-font) !important; font-size: 1.5rem !important;
        font-weight: 600 !important; font-variant-numeric: tabular-nums;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.72rem !important; font-weight: 600;
        letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--text-muted) !important;
    }

    .stButton > button, div[data-testid="stFormSubmitButton"] button {
        border-radius: var(--radius-sm) !important; font-weight: 600 !important;
        font-size: 0.875rem !important; transition: all 0.18s ease !important;
        border: 1px solid var(--border-color) !important;
        background: rgba(0,0,0,0.04) !important;
        color: var(--text-secondary) !important;
    }
    .stButton > button:hover { background: rgba(0,0,0,0.07) !important; color: var(--text-primary) !important; }
    .stButton > button[kind="primary"] {
        background: var(--accent) !important; border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 18px rgba(37,99,235,0.45) !important; transform: translateY(-1px);
    }

    .stSelectbox > div > div, .stMultiSelect > div > div,
    .stNumberInput > div > div > input, .stTextInput > div > div > input,
    .stTextArea textarea {
        border: 1px solid rgba(0,0,0,0.12) !important;
        border-radius: var(--radius-sm) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,0,0,0.04) !important; border-radius: var(--radius-md) !important;
        padding: 4px !important; border: 1px solid var(--border-color) !important; gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important; font-weight: 600 !important;
        font-size: 0.84rem !important; color: var(--text-secondary) !important;
        background: transparent !important; padding: 0.45rem 1.1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: white !important; color: var(--accent) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

    [data-testid="stExpander"] {
        border: 1px solid var(--border-color) !important; border-radius: var(--radius-md) !important;
        background: var(--bg-card) !important; overflow: hidden !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stDataFrame"] { border-radius: var(--radius-md) !important; overflow: hidden !important; }
    [data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--success)) !important;
    }

    [data-testid="stDialog"], [data-testid="stDialog"] > div, [role="dialog"] {
        background: #ffffff !important; border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-xl) !important;
    }
    [role="dialog"] h1, [role="dialog"] h2, [role="dialog"] h3,
    [role="dialog"] p, [role="dialog"] li, [role="dialog"] strong,
    [data-testid="stDialog"] h1, [data-testid="stDialog"] h2, [data-testid="stDialog"] h3,
    [data-testid="stDialog"] p, [data-testid="stDialog"] li, [data-testid="stDialog"] strong {
        color: var(--text-secondary) !important;
    }
    [role="dialog"] h1, [role="dialog"] h2, [role="dialog"] h3,
    [data-testid="stDialog"] h1, [data-testid="stDialog"] h2, [data-testid="stDialog"] h3,
    [role="dialog"] .onboarding-title, [data-testid="stDialog"] .onboarding-title {
        color: var(--text-primary) !important;
    }
    [role="dialog"] .onboarding-description, [role="dialog"] .onboarding-tip,
    [data-testid="stDialog"] .onboarding-description, [data-testid="stDialog"] .onboarding-tip {
        color: var(--text-secondary) !important; background: rgba(0,0,0,0.03) !important;
    }

    .hero-panel {
        border-radius: var(--radius-xl); padding: 1.75rem 2rem;
        background: linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(255,255,255,0.8) 60%, rgba(5,150,105,0.08) 100%);
        border: 1px solid rgba(37,99,235,0.2);
        box-shadow: 0 4px 24px rgba(37,99,235,0.1); margin-bottom: 1.25rem;
    }
    .status-pill {
        display: inline-flex; align-items: center; gap: 0.4rem;
        border-radius: 999px; padding: 0.3rem 0.9rem;
        font-weight: 700; font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase;
        margin-bottom: 1rem;
        background: rgba(37,99,235,0.1); border: 1px solid rgba(37,99,235,0.3);
        color: var(--accent) !important;
    }
    .status-pill::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--success); }
    .feature-card {
        border-radius: var(--radius-md); padding: 1.25rem; min-height: 180px;
        background: var(--bg-card); border: 1px solid var(--border-color);
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .feature-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,99,235,0.12); }
    .feature-card h4 { font-size: 0.95rem !important; font-weight: 700 !important; margin-bottom: 0.6rem !important; }
    .workflow-box {
        border-radius: var(--radius-md); padding: 1.25rem 1.5rem;
        background: rgba(37,99,235,0.05); border: 1px solid rgba(37,99,235,0.18);
    }
    .workflow-box h4 { font-size: 0.88rem !important; font-weight: 700 !important; color: var(--accent) !important; }
    .section-label {
        font-weight: 700 !important; font-size: 0.72rem !important;
        letter-spacing: 0.1em; text-transform: uppercase;
        color: var(--text-muted) !important; margin-bottom: 0.75rem !important;
    }
    .stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.1rem; }
    .stat-card-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted) !important; }
    .stat-card-value { font-family: var(--mono-font); font-size: 1.5rem; font-weight: 600; color: var(--text-primary) !important; }
    .stat-card-value.positive { color: var(--success) !important; }
    .stat-card-value.negative { color: var(--danger) !important; }
    .rr-box { border-radius: var(--radius-md); padding: 1rem 1.25rem; border: 1px solid rgba(5,150,105,0.25); background: rgba(5,150,105,0.06); }
    .rr-value { font-family: var(--mono-font); font-size: 1.75rem; font-weight: 700; color: var(--success) !important; }
    .callout-tip { border-radius: var(--radius-sm); padding: 0.9rem 1.1rem; background: rgba(5,150,105,0.07); border-left: 3px solid var(--success); margin: 0.75rem 0; }
    .callout-warn { border-radius: var(--radius-sm); padding: 0.9rem 1.1rem; background: rgba(217,119,6,0.07); border-left: 3px solid var(--warning); margin: 0.75rem 0; }
    .callout-info { border-radius: var(--radius-sm); padding: 0.9rem 1.1rem; background: rgba(37,99,235,0.07); border-left: 3px solid var(--accent); margin: 0.75rem 0; }
    hr { border: none !important; border-top: 1px solid var(--border-color) !important; margin: 1.25rem 0 !important; }
    .footer-note { text-align: center; color: var(--text-muted) !important; font-size: 0.8rem; padding: 1.5rem 0 0.5rem 0; }
    .onboarding-shell { min-height: 240px; text-align: center; padding: 0.5rem 1.5rem 1rem; }
    .onboarding-step-badge { width: 56px; height: 56px; margin: 0 auto 1rem; display: grid; place-items: center; border-radius: 16px; font-size: 1.1rem; font-weight: 800; color: #fff; background: linear-gradient(135deg, var(--accent), var(--accent-2)); box-shadow: 0 8px 20px rgba(37,99,235,0.3); font-family: var(--mono-font); }
    .onboarding-eyebrow { text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.7rem !important; font-weight: 800; color: var(--accent) !important; margin-bottom: 0.4rem !important; }
    .onboarding-title { margin: 0 0 0.9rem 0; font-size: 1.55rem !important; }
    .onboarding-description { max-width: 580px; margin: 0 auto 1.1rem; line-height: 1.7; font-size: 0.95rem; color: var(--text-secondary) !important; }
    .onboarding-tip { max-width: 560px; margin: 0 auto; border-radius: var(--radius-sm); padding: 0.75rem 1rem; border: 1px solid var(--border-color); background: rgba(0,0,0,0.03); color: var(--text-secondary) !important; }
    .guide-progress { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin: 0.2rem 0 0.9rem; }
    .guide-dot { width: 28px; height: 28px; display: inline-grid; place-items: center; border-radius: 50%; border: 1px solid var(--border-color); background: rgba(0,0,0,0.04); color: var(--text-muted) !important; font-size: 0.72rem; font-weight: 800; }
    .guide-dot-active { color: #fff !important; background: var(--accent); border-color: transparent; box-shadow: 0 4px 12px rgba(37,99,235,0.35); }
    .guide-dot-done { color: var(--success) !important; border-color: var(--success); }
    .guide-content-card { border-radius: var(--radius-md); padding: 1.25rem 1.5rem; border: 1px solid var(--border-color); background: var(--bg-card); }
    .guide-description { max-width: 680px; line-height: 1.75; font-size: 0.95rem; text-align: center; color: var(--text-secondary) !important; margin: 0 auto; }
    """


def apply_app_theme() -> bool:
    """
    Render theme toggle in sidebar and inject global CSS.

    Returns:
        bool: True if dark mode is active.
    """
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    with st.sidebar:
        st.markdown("### 🎨 Appearance")
        dark_mode = st.toggle(
            "Dark mode",
            value=st.session_state.dark_mode,
            help="Aktifkan mode gelap untuk tampilan terminal profesional",
        )
        st.session_state.dark_mode = dark_mode
        st.markdown("---")

    st.markdown(f"<style>{_build_theme_css(st.session_state.dark_mode)}</style>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 1.75rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    [data-testid="stMetric"] { box-shadow: none; }
    </style>
    """, unsafe_allow_html=True)
    render_onboarding()
    return st.session_state.dark_mode
