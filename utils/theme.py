"""
Global app theme utilities for professional Streamlit UI.
"""

import streamlit as st


ONBOARDING_STEPS = [
    {
        "icon": "1",
        "eyebrow": "Selamat datang",
        "title": "Mulai dari universe yang relevan",
        "description": (
            "Screener akan mencari emiten IDX secara otomatis. Anda hanya perlu "
            "memilih kriteria kualitas, likuiditas, harga, dan sektor."
        ),
        "tip": "Tidak perlu mengisi kode saham satu per satu.",
    },
    {
        "icon": "2",
        "eyebrow": "Langkah 1",
        "title": "Buat Filter Universe",
        "description": (
            "Buka Universe Filter, atur market cap minimum, volume harian, "
            "rentang harga, lalu pilih sektor apabila diperlukan."
        ),
        "tip": "Klik Terapkan Filter untuk menyimpan daftar emiten yang lolos.",
    },
    {
        "icon": "3",
        "eyebrow": "Langkah 2",
        "title": "Atur sumber dan profil risiko",
        "description": (
            "Di Scan Harian, gunakan Filtered Universe. Lalu atur periode scan, "
            "maksimum RSI, R/R target, serta modal trading."
        ),
        "tip": "Mulai dengan kriteria konservatif, lalu evaluasi hasilnya.",
    },
    {
        "icon": "4",
        "eyebrow": "Langkah 3",
        "title": "Jalankan scan dan pilih sinyal",
        "description": (
            "Klik Mulai Scan untuk memeriksa emiten secara otomatis. "
            "Tinjau sinyal BUY, harga entry, stop loss, dan target profit."
        ),
        "tip": "Gunakan chart dan kondisi pasar sebagai konfirmasi tambahan.",
    },
    {
        "icon": "5",
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
            f'<span class="guide-dot {"guide-dot-active" if i == step else ""}{" guide-dot-done" if i < step else ""}">{i + 1}</span>'
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
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --bg-main: radial-gradient(1200px 700px at 20% -10%, #1f3a5b 0%, #0b1521 45%, #070d14 100%);
            --bg-card: rgba(17, 25, 40, 0.72);
            --bg-card-soft: rgba(255, 255, 255, 0.04);
            --text-primary: #ecf2ff;
            --text-secondary: #b8c7e0;
            --border-color: rgba(154, 181, 255, 0.22);
            --accent: #5fb4ff;
            --accent-2: #4f7cff;
            --success: #28c58b;
            --warning: #ffb84d;
        }

        .stApp {
            font-family: 'Manrope', 'Segoe UI', sans-serif;
            color: var(--text-primary);
            background: var(--bg-main);
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: rgba(7, 13, 20, 0.55);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border-color);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(9, 16, 27, 0.95), rgba(5, 10, 18, 0.92));
            border-right: 1px solid var(--border-color);
        }

        [data-testid="stDialog"],
        [data-testid="stDialog"] > div,
        [role="dialog"] {
            background: #111927 !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }

        [role="dialog"] h1,
        [role="dialog"] h2,
        [role="dialog"] h3,
        [role="dialog"] p,
        [role="dialog"] li,
        [role="dialog"] span,
        [role="dialog"] strong,
        [data-testid="stDialog"] h1,
        [data-testid="stDialog"] h2,
        [data-testid="stDialog"] h3,
        [data-testid="stDialog"] p,
        [data-testid="stDialog"] li,
        [data-testid="stDialog"] strong {
            color: var(--text-secondary) !important;
        }

        [role="dialog"] h1,
        [role="dialog"] h2,
        [role="dialog"] h3,
        [data-testid="stDialog"] h1,
        [data-testid="stDialog"] h2,
        [data-testid="stDialog"] h3,
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
            text-wrap: balance;
        }

        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }

        .stApp,
        .stApp p,
        .stApp li,
        .stApp label,
        .stApp span,
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

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        div[data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
        }

        .stApp a,
        .stApp a:visited {
            color: #8fc6ff !important;
        }

        .stMetric {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 0.7rem;
            backdrop-filter: blur(4px);
        }

        .stAlert {
            border-radius: 14px;
            border: 1px solid var(--border-color);
            background: var(--bg-card-soft);
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            border-radius: 10px;
            border: 1px solid rgba(104, 166, 255, 0.35);
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: #f5f9ff;
            font-weight: 700;
            transition: transform 0.16s ease, box-shadow 0.16s ease;
            box-shadow: 0 8px 18px rgba(43, 113, 210, 0.3);
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 22px rgba(43, 113, 210, 0.4);
        }

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stNumberInput > div > div > input,
        .stTextInput > div > div > input,
        .stTextArea textarea {
            background: rgba(21, 31, 46, 0.8) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
        }

        .hero-panel {
            border-radius: 18px;
            padding: 1.3rem 1.4rem;
            background: linear-gradient(130deg, rgba(95, 180, 255, 0.2), rgba(79, 124, 255, 0.12), rgba(40, 197, 139, 0.13));
            border: 1px solid var(--border-color);
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25);
            margin-bottom: 0.9rem;
        }

        .feature-card {
            border-radius: 14px;
            padding: 1rem;
            min-height: 170px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            backdrop-filter: blur(4px);
        }

        .workflow-box {
            border-radius: 14px;
            padding: 0.9rem 1rem;
            background: rgba(95, 180, 255, 0.09);
            border: 1px solid rgba(95, 180, 255, 0.35);
        }
        """

    return """
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: radial-gradient(1000px 600px at 15% -10%, #f6fbff 0%, #eef4ff 42%, #f8fbff 100%);
        --bg-card: rgba(255, 255, 255, 0.86);
        --bg-card-soft: rgba(255, 255, 255, 0.65);
        --text-primary: #0e2240;
        --text-secondary: #41506a;
        --border-color: rgba(34, 88, 164, 0.2);
        --accent: #1f7de6;
        --accent-2: #2f6fff;
        --success: #10986a;
        --warning: #cc7d16;
    }

    .stApp {
        font-family: 'Manrope', 'Segoe UI', sans-serif;
        color: var(--text-primary);
        background: var(--bg-main);
        background-attachment: fixed;
    }

    [data-testid="stHeader"] {
        background: rgba(244, 249, 255, 0.65);
        backdrop-filter: blur(8px);
        border-bottom: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(247, 251, 255, 0.95), rgba(236, 244, 255, 0.92));
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stDialog"],
    [data-testid="stDialog"] > div,
    [role="dialog"] {
        background: #ffffff !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    [role="dialog"] h1,
    [role="dialog"] h2,
    [role="dialog"] h3,
    [role="dialog"] p,
    [role="dialog"] li,
    [role="dialog"] strong,
    [data-testid="stDialog"] h1,
    [data-testid="stDialog"] h2,
    [data-testid="stDialog"] h3,
    [data-testid="stDialog"] p,
    [data-testid="stDialog"] li,
    [data-testid="stDialog"] strong {
        color: var(--text-secondary) !important;
    }

    [role="dialog"] h1,
    [role="dialog"] h2,
    [role="dialog"] h3,
    [data-testid="stDialog"] h1,
    [data-testid="stDialog"] h2,
    [data-testid="stDialog"] h3,
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
        text-wrap: balance;
    }

    h1, h2, h3, h4 {
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }

    .stApp,
    .stApp p,
    .stApp li,
    .stApp label,
    .stApp span,
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

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6,
    div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }

    .stApp a,
    .stApp a:visited {
        color: #1f66c7 !important;
    }

    .stMetric {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 0.7rem;
        box-shadow: 0 10px 20px rgba(32, 75, 140, 0.07);
    }

    .stAlert {
        border-radius: 14px;
        border: 1px solid var(--border-color);
        background: var(--bg-card-soft);
    }

    .stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 10px;
        border: 1px solid rgba(31, 125, 230, 0.35);
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        color: #f7fbff;
        font-weight: 700;
        transition: transform 0.16s ease, box-shadow 0.16s ease;
        box-shadow: 0 8px 16px rgba(31, 125, 230, 0.2);
    }

    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 22px rgba(31, 125, 230, 0.3);
    }

    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border: 1px solid rgba(52, 110, 192, 0.28) !important;
        border-radius: 10px !important;
    }

    .hero-panel {
        border-radius: 18px;
        padding: 1.3rem 1.4rem;
        background: linear-gradient(140deg, rgba(31, 125, 230, 0.18), rgba(47, 111, 255, 0.12), rgba(16, 152, 106, 0.12));
        border: 1px solid var(--border-color);
        box-shadow: 0 14px 26px rgba(35, 89, 166, 0.12);
        margin-bottom: 0.9rem;
    }

    .feature-card {
        border-radius: 14px;
        padding: 1rem;
        min-height: 170px;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 20px rgba(22, 61, 121, 0.08);
    }

    .workflow-box {
        border-radius: 14px;
        padding: 0.9rem 1rem;
        background: rgba(31, 125, 230, 0.08);
        border: 1px solid rgba(31, 125, 230, 0.28);
    }
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
            help="Aktifkan mode gelap untuk tampilan yang lebih nyaman",
        )
        st.session_state.dark_mode = dark_mode
        st.markdown("---")

    st.markdown(f"<style>{_build_theme_css(st.session_state.dark_mode)}</style>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    [data-testid="stMetric"] {
        box-shadow: 0 10px 24px rgba(15, 49, 96, 0.08);
    }
    [data-testid="stExpander"] {
        border: 1px solid var(--border-color);
        border-radius: 14px;
        background: var(--bg-card);
        overflow: hidden;
    }
    [data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--success));
    }
    .onboarding-shell {
        min-height: 240px;
        text-align: center;
        padding: 0.4rem 1.5rem 0.8rem 1.5rem;
    }
    .onboarding-step-badge {
        width: 54px;
        height: 54px;
        margin: 0 auto 0.8rem auto;
        display: grid;
        place-items: center;
        border-radius: 18px;
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        box-shadow: 0 12px 26px rgba(47, 111, 255, 0.28);
    }
    .onboarding-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem !important;
        font-weight: 800;
        color: var(--accent) !important;
        margin-bottom: 0.35rem !important;
    }
    .onboarding-title {
        margin: 0 0 0.75rem 0;
        font-size: 1.65rem;
    }
    .onboarding-description {
        max-width: 620px;
        margin: 0 auto 1rem auto;
        line-height: 1.65;
        font-size: 0.98rem;
        text-align: center;
        text-wrap: balance;
        color: var(--text-secondary) !important;
    }
    .onboarding-tip {
        max-width: 620px;
        margin: 0 auto;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: 1px solid var(--border-color);
        background: var(--bg-card-soft);
        text-align: center;
        color: var(--text-secondary) !important;
    }
    .guide-progress {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.55rem;
        margin: 0.15rem 0 0.8rem 0;
    }
    .guide-dot {
        width: 30px;
        height: 30px;
        display: inline-grid;
        place-items: center;
        border-radius: 50%;
        border: 1px solid var(--border-color);
        background: var(--bg-card);
        color: var(--text-secondary) !important;
        font-size: 0.78rem;
        font-weight: 800;
    }
    .guide-dot-active {
        color: #ffffff !important;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border-color: transparent;
        box-shadow: 0 8px 18px rgba(47, 111, 255, 0.25);
    }
    .guide-dot-done {
        color: var(--success) !important;
        border-color: var(--success);
    }
    .guide-content-card {
        min-height: 220px;
        box-sizing: border-box;
        border-radius: 16px;
        padding: 1.35rem 1.5rem;
        border: 1px solid var(--border-color);
        background: var(--bg-card);
        box-shadow: 0 12px 26px rgba(15, 49, 96, 0.08);
    }
    .guide-card-icon {
        width: 52px;
        height: 52px;
        display: grid;
        place-items: center;
        margin-bottom: 0.8rem;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        background: var(--bg-card-soft);
        font-size: 1.45rem;
    }
    .guide-description {
        max-width: 700px;
        line-height: 1.7;
        font-size: 1rem;
        text-align: center;
        text-wrap: balance;
        color: var(--text-secondary) !important;
        margin-left: auto;
        margin-right: auto;
    }
    .footer-note {
        text-align: center;
        color: var(--text-secondary) !important;
        opacity: 0.88;
    }
    </style>
    """, unsafe_allow_html=True)
    render_onboarding()
    return st.session_state.dark_mode
