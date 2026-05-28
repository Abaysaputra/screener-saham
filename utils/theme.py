"""
Global app theme utilities for professional Streamlit UI.
"""

import streamlit as st


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
    return st.session_state.dark_mode
