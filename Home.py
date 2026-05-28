"""
Swing Trading Assistant - IDX
Main application entry point
"""
import streamlit as st
from pathlib import Path
from utils.theme import apply_app_theme

# Page configuration
st.set_page_config(
    page_title="Swing Trader IDX",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_app_theme()

st.markdown("""
<style>
.hero-title {
    font-size: 2.45rem;
    font-weight: 800;
    line-height: 1.18;
    margin: 0;
}

.hero-subtitle {
    font-size: 1rem;
    margin-top: 0.5rem;
    opacity: 0.92;
}

.status-pill {
    display: inline-block;
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    font-weight: 700;
    font-size: 0.82rem;
    margin-bottom: 0.75rem;
    background: rgba(95, 180, 255, 0.18);
    border: 1px solid rgba(95, 180, 255, 0.35);
}

.section-label {
    font-weight: 800;
    font-size: 1.08rem;
    margin-top: 0.15rem;
    margin-bottom: 0.65rem;
}

.micro-note {
    font-size: 0.88rem;
    opacity: 0.86;
}
</style>
""", unsafe_allow_html=True)

watchlist_count = 0
watchlist_path = Path("watchlist.txt")
if watchlist_path.exists():
    watchlist_count = len([x for x in watchlist_path.read_text().splitlines() if x.strip()])

filtered_universe = st.session_state.get("filtered_universe")
filtered_count = len(filtered_universe) if filtered_universe is not None else 0

left, right = st.columns([1.55, 1.0])

with left:
    st.markdown(
        """
        <div class="hero-panel">
            <div class="status-pill">PRO EDITION • MARKET-WIDE SWING SCANNER</div>
            <p class="hero-title">📈 Swing Trading Assistant - IDX</p>
            <p class="hero-subtitle">Platform analisis swing trading dengan alur kerja 2 tahap: Universe Filter → Scan Harian.
            Fokus pada kualitas sinyal, manajemen risiko, dan dokumentasi performa secara terstruktur.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.success("Gratis 100% dengan Yahoo Finance. Tanpa API key, langsung siap pakai.")

with right:
    st.metric("Watchlist Aktif", watchlist_count)
    st.metric("Filtered Universe", filtered_count if filtered_count else "Belum dibuat")
    st.metric("Workflow", "2-Stage")

st.markdown("<p class='section-label'>Fitur Utama</p>", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🌍 Universe Filter</h4>
            <p>Screen seluruh IDX dan saring berdasar market cap, volume, harga, serta sektor.</p>
            <p class="micro-note">Output: universe berkualitas untuk proses scan berikutnya.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📊 Scan Harian</h4>
            <p>Filter teknikal dan fundamental untuk menghasilkan sinyal BUY yang lebih selektif.</p>
            <p class="micro-note">Modal per saham bisa diatur manual sesuai preferensi risiko.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📈 Backtest</h4>
            <p>Uji strategi menggunakan data historis multi-tahun dengan metrik performa lengkap.</p>
            <p class="micro-note">Validasi objektif sebelum strategi dipakai di market nyata.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f4:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📓 Journal</h4>
            <p>Lacak trade, hitung win rate dan R/R, serta monitor equity curve secara berkala.</p>
            <p class="micro-note">Membantu evaluasi disiplin dan kualitas eksekusi trading.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("<p class='section-label'>Quick Start Workflow</p>", unsafe_allow_html=True)

w1, w2 = st.columns(2)

with w1:
    st.markdown(
        """
        <div class="workflow-box">
            <h4>Stage 1 • Universe Filter</h4>
            <ol>
                <li>Buka menu Universe Filter.</li>
                <li>Set filter market cap, volume, harga, dan sektor.</li>
                <li>Klik Terapkan Filter untuk membuat daftar saham terpilih.</li>
            </ol>
            <p class="micro-note">Target output: 20-50 saham yang lebih liquid dan layak dianalisis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with w2:
    st.markdown(
        """
        <div class="workflow-box">
            <h4>Stage 2 • Scan Harian</h4>
            <ol>
                <li>Aktifkan opsi Gunakan Filtered Universe.</li>
                <li>Tentukan parameter teknikal + fundamental.</li>
                <li>Atur modal dan target risk/reward.</li>
                <li>Mulai scan untuk menemukan kandidat sinyal BUY.</li>
            </ol>
            <p class="micro-note">Target output: 5-15 ide trading dengan kualitas sinyal lebih tinggi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.info(
    "Power combo: Universe Filter + Technical Filter + Fundamental Filter untuk menjaga kualitas sinyal tetap premium."
)

st.markdown("---")
st.markdown("<p class='section-label'>Data & Dokumentasi</p>", unsafe_allow_html=True)

st.markdown(
    """
- Yahoo Finance digunakan sebagai data source utama: gratis, stabil, dan cukup untuk swing trading harian.
- Historical data multi-tahun tersedia untuk validasi strategi melalui backtest.
- Delay data sekitar 15-20 menit umumnya tidak menjadi kendala untuk gaya trading swing.

Baca dokumentasi:
- [README.md](./README.md)
- [YFINANCE_MIGRATION.md](./YFINANCE_MIGRATION.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
"""
)

st.markdown(
    """
    <div style='text-align:center; padding:1rem 0 0.25rem 0; opacity:0.88;'>
        <small>Dibuat dengan Streamlit & Yahoo Finance | © 2026 Swing Trader IDX</small><br>
        <small>Disclaimer: aplikasi ini untuk edukasi. Selalu lakukan riset mandiri sebelum trading.</small>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🚀 Navigation")
    st.markdown(
        """
- Home
- 🌍 Universe Filter
- 📊 Scan Harian
- 📈 Backtest
- 📓 Journal
- ⚙️ Settings
"""
    )

    st.markdown("### 💡 Waktu Scan Disarankan")
    st.markdown(
        """
- 15:30-16:00 WIB (menjelang close)
- 16:00-17:00 WIB (setelah close)
"""
    )

    st.markdown("### 🎯 Strategi Modal")
    st.markdown(
        """
- Diversifikasi ke beberapa saham
- Prioritaskan kandidat R/R di atas 2
- Sisakan 10-20% dana untuk fleksibilitas
"""
    )
