"""
User-friendly first-use guide for the stock screener.
"""
import streamlit as st

from utils.theme import apply_app_theme


st.set_page_config(
    page_title="Panduan - Swing Trader",
    page_icon="📖",
    layout="wide",
)

apply_app_theme()

st.markdown(
    """
    <div class="hero-panel">
        <div class="status-pill">PANDUAN PENGGUNAAN &nbsp;•&nbsp; START HERE</div>
        <h1 style="margin:0;font-size:1.75rem;font-weight:800;letter-spacing:-0.025em;">📖 Panduan Screener Saham</h1>
        <p style="margin:0.5rem 0 0 0;font-size:0.95rem;color:var(--text-secondary);">Ikuti lima tahap singkat untuk menyiapkan universe, menjalankan scan, dan mencatat hasil trading.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "guide_step" not in st.session_state:
    st.session_state.guide_step = 0

steps = [
    ("1", "Kenali Alur", "Tinjau dua tahap utama aplikasi."),
    ("2", "Buat Universe", "Atur filter emiten IDX."),
    ("3", "Atur Risiko", "Tentukan modal dan target R/R."),
    ("4", "Jalankan Scan", "Temukan kandidat sinyal BUY."),
    ("5", "Evaluasi Trade", "Gunakan Backtest dan Journal."),
]

tab_content = [
    (
        "🌍",
        "Mulai dari universe yang relevan",
        "Screener mencari seluruh emiten IDX otomatis. Anda tidak perlu mengisi watchlist secara manual.",
        "Tidak perlu mengisi kode saham satu per satu.",
        "Lanjut ke Universe Filter",
        "pages/0_🌍_Universe_Filter.py",
    ),
    (
        "🎯",
        "Atur filter market-wide",
        "Di Universe Filter, pilih market cap minimum, volume harian, rentang harga, dan sektor. Setelah konfigurasi selesai, klik Terapkan Filter.",
        "Gunakan filter konservatif untuk mendapatkan emiten yang lebih likuid.",
        "Buka Universe Filter",
        "pages/0_🌍_Universe_Filter.py",
    ),
    (
        "⚖️",
        "Tentukan profil risiko",
        "Di Scan Harian, aktifkan Gunakan Filtered Universe lalu atur periode scan, RSI maksimum, target R/R, dan modal trading.",
        "Mulai dari modal kecil dan risiko yang dapat ditoleransi.",
        "Buka Scan Harian",
        "pages/1_📊_Scan_Harian.py",
    ),
    (
        "🔍",
        "Jalankan dan tinjau sinyal",
        "Klik Mulai Scan. Periksa emiten yang lolos, sinyal BUY, entry, stop loss, dan take profit sebelum mengambil keputusan.",
        "Sinyal aplikasi bukan rekomendasi mutlak; konfirmasikan kondisi chart dan pasar.",
        "Mulai Scan",
        "pages/1_📊_Scan_Harian.py",
    ),
    (
        "📓",
        "Catat dan evaluasi hasil",
        "Gunakan Journal untuk mencatat eksekusi dan hasil. Gunakan Backtest untuk menguji parameter strategi menggunakan data historis.",
        "Evaluasi disiplin dan kualitas keputusan secara rutin.",
        "Buka Backtest",
        "pages/2_📈_Backtest.py",
    ),
]

index = max(0, min(st.session_state.guide_step, len(tab_content) - 1))

dot_items = "".join(
    f'<span class="guide-dot {"guide-dot-active" if i == index else ""}{" guide-dot-done" if i < index else ""}">{i + 1}</span>'
    for i in range(len(tab_content))
)
st.markdown(
    f'<div class="guide-progress">{dot_items}</div>',
    unsafe_allow_html=True,
)
st.progress((index + 1) / len(tab_content))

icon, title, description, tip, action_label, target_page = tab_content[index]
main, side = st.columns([2.15, 1])
with main:
    st.markdown(
        f"""
        <div class="guide-content-card">
            <div class="guide-card-icon">{icon}</div>
            <p class="onboarding-eyebrow">Tahap {index + 1} dari 5</p>
            <h2 style="margin-top:0.15rem;">{title}</h2>
            <p class="guide-description">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with side:
    st.markdown(
        f"""
        <div class="workflow-box" style="height:100%; box-sizing:border-box;">
            <p style="font-weight:800;">Tips pengguna</p>
            <p class="micro-note">{tip}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("Lewati", key="guide_skip", use_container_width=True):
        st.session_state.guide_step = len(tab_content) - 1
        st.rerun()
with nav2:
    if index > 0:
        if st.button("← Sebelumnya", key="guide_previous", use_container_width=True):
            st.session_state.guide_step = index - 1
            st.rerun()
    else:
        st.button("← Sebelumnya", key="guide_previous_disabled", use_container_width=True, disabled=True)
with nav3:
    if index < len(tab_content) - 1:
        if st.button("Selanjutnya →", key="guide_next", type="primary", use_container_width=True):
            st.session_state.guide_step = index + 1
            st.rerun()
    else:
        if st.button(action_label, key="guide_action", type="primary", use_container_width=True):
            st.switch_page(target_page)
