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

# ─── Page-specific CSS ───
st.markdown("""
<style>
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0.25rem 0 0.6rem 0;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 0.95rem;
    line-height: 1.65;
    margin: 0;
    color: var(--text-secondary);
    max-width: 540px;
}
.micro-note {
    font-size: 0.78rem;
    color: var(--text-muted) !important;
    margin-top: 0.75rem !important;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border-color);
}
.quick-action-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}
.data-badge {
    font-family: var(--mono-font, monospace);
    font-size: 0.75rem;
    color: var(--text-muted);
    background: var(--bg-card-soft, rgba(255,255,255,0.05));
    border: 1px solid var(--border-color);
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    display: inline-block;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Data ───
watchlist_count = 0
watchlist_path = Path("watchlist.txt")
if watchlist_path.exists():
    watchlist_count = len([x for x in watchlist_path.read_text().splitlines() if x.strip()])

filtered_universe = st.session_state.get("filtered_universe")
filtered_count = len(filtered_universe) if filtered_universe is not None else 0

# ─── Hero + Metrics ───
hero_col, stats_col = st.columns([1.65, 1.0], gap="large")

with hero_col:
    st.markdown(
        """
        <div class="hero-panel">
            <div class="status-pill">IDX SWING SCANNER &nbsp;•&nbsp; LIVE READY</div>
            <p class="hero-title">📈 Swing Trading Assistant</p>
            <p class="hero-subtitle">Platform analisis swing trading profesional dengan alur kerja 2 tahap:
            <strong>Universe Filter → Scan Harian</strong>. Fokus pada kualitas sinyal,
            manajemen risiko terukur, dan dokumentasi performa yang terstruktur.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="callout-tip" style="margin-top:0;">
        ✅ &nbsp;<strong>100% Gratis</strong> — Powered by Yahoo Finance. Tanpa API key, langsung siap pakai.
        </div>""",
        unsafe_allow_html=True,
    )

with stats_col:
    st.markdown('<p class="section-label">Statistik Sesi</p>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Watchlist", watchlist_count)
    with m2:
        st.metric("Universe", filtered_count if filtered_count else "—")
    st.metric("Workflow", "2-Stage", delta="Universe → Scan")

# ─── Quick Access ───
st.markdown('<p class="section-label" style="margin-top:1.5rem;">Akses Cepat</p>', unsafe_allow_html=True)
quick1, quick2, quick3, quick4 = st.columns(4)
with quick1:
    if st.button("🌍 Buat Universe", use_container_width=True, type="primary"):
        st.switch_page("pages/0_🌍_Universe_Filter.py")
with quick2:
    if st.button("🔍 Jalankan Scan", use_container_width=True):
        st.switch_page("pages/1_📊_Scan_Harian.py")
with quick3:
    if st.button("📓 Buka Journal", use_container_width=True):
        st.switch_page("pages/3_📓_Journal.py")
with quick4:
    if st.button("📖 Panduan", use_container_width=True):
        st.session_state.guide_step = 0
        st.switch_page("pages/5_📖_Panduan.py")

st.markdown("<hr/>", unsafe_allow_html=True)

# ─── Feature Cards ───
st.markdown('<p class="section-label">Fitur Utama</p>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4, gap="small")

with f1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🌍 Universe Filter</h4>
            <p>Screen seluruh IDX dan saring berdasar market cap, volume, harga, serta sektor secara otomatis.</p>
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
            <p>Filter teknikal dan fundamental untuk menghasilkan sinyal BUY yang lebih selektif dan terukur.</p>
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

st.markdown("<hr/>", unsafe_allow_html=True)

# ─── Quick Start Workflow ───
st.markdown('<p class="section-label">Quick Start Workflow</p>', unsafe_allow_html=True)

w1, w2 = st.columns(2, gap="medium")

with w1:
    st.markdown(
        """
        <div class="workflow-box">
            <h4>Stage 1 · Universe Filter</h4>
            <ol>
                <li>Buka menu Universe Filter.</li>
                <li>Set filter market cap, volume, harga, dan sektor.</li>
                <li>Klik <strong>Terapkan Filter</strong> untuk membuat daftar saham terpilih.</li>
            </ol>
            <p class="micro-note">Target output: 20–50 saham yang lebih liquid dan layak dianalisis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with w2:
    st.markdown(
        """
        <div class="workflow-box">
            <h4>Stage 2 · Scan Harian</h4>
            <ol>
                <li>Aktifkan opsi <strong>Gunakan Filtered Universe</strong>.</li>
                <li>Tentukan parameter teknikal + fundamental.</li>
                <li>Atur modal dan target risk/reward.</li>
                <li>Mulai scan untuk menemukan kandidat sinyal BUY.</li>
            </ol>
            <p class="micro-note">Target output: 5–15 ide trading dengan kualitas sinyal lebih tinggi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """<div class="callout-info" style="margin-top:0.5rem;">
    💡 &nbsp;<strong>Power combo:</strong> Universe Filter + Technical Filter + Fundamental Filter
    untuk menjaga kualitas sinyal tetap premium.
    </div>""",
    unsafe_allow_html=True,
)

st.markdown("<hr/>", unsafe_allow_html=True)

# ─── Data & Docs ───
st.markdown('<p class="section-label">Data & Dokumentasi</p>', unsafe_allow_html=True)

doc1, doc2 = st.columns([1.2, 1])

with doc1:
    st.markdown(
        """
        <div class="info-panel">
            <div class="info-title">📡 Sumber Data</div>
            <ul style="margin:0;padding-left:1.2rem;font-size:0.875rem;line-height:1.75;">
                <li>Yahoo Finance — data historis multi-tahun, gratis & stabil.</li>
                <li>Delay ~15–20 menit tidak menjadi kendala untuk swing trading.</li>
                <li>Historical data tersedia untuk validasi strategi via backtest.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with doc2:
    st.markdown(
        """
        <div class="info-panel">
            <div class="info-title">📄 Referensi</div>
            <ul style="margin:0;padding-left:1.2rem;font-size:0.875rem;line-height:1.9;">
                <li><a href="./README.md">README.md</a></li>
                <li><a href="./ARCHITECTURE.md">ARCHITECTURE.md</a></li>
                <li><a href="./YFINANCE_MIGRATION.md">YFINANCE_MIGRATION.md</a></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Footer ───
st.markdown(
    """
    <div class="footer-note">
        Dibuat dengan Streamlit &amp; Yahoo Finance &nbsp;|&nbsp; © 2026 Swing Trader IDX<br>
        <span style="opacity:0.6;">Disclaimer: aplikasi ini untuk edukasi. Selalu lakukan riset mandiri sebelum trading.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar Content ───
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown(
        """
- 🏠 Home
- 🌍 Universe Filter
- 📊 Scan Harian
- 📈 Backtest
- 📓 Journal
- ⚙️ Settings
"""
    )

    st.markdown("### ⏰ Waktu Scan Optimal")
    st.markdown(
        """
- **15:30 – 16:00** WIB (menjelang close)
- **16:00 – 17:00** WIB (setelah close)
"""
    )

    st.markdown("### 🎯 Tips Modal")
    st.markdown(
        """
- Diversifikasi ke beberapa saham
- Prioritaskan R/R ≥ 2
- Sisakan 10–20% dana cadangan
"""
    )
