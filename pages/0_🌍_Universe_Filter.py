"""
Market-Wide Universe Filter Page
Filter all IDX stocks to create a quality universe for daily scanning
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from utils.theme import apply_app_theme

st.set_page_config(
    page_title="Universe Filter - Swing Trader",
    page_icon="🌍",
    layout="wide"
)

apply_app_theme()

st.title("🌍 Universe Filter - Market-Wide Screener")
st.markdown("**Tahap 1**: Filter seluruh saham IDX untuk membuat universe berkualitas")
st.markdown("**Tahap 2**: Scan Harian akan berjalan pada universe terfilter")

# Load IDX universe
@st.cache_data
def load_idx_universe():
    """Load all IDX stocks from CSV"""
    csv_path = Path(__file__).parent.parent / "idx_universe.csv"
    
    if not csv_path.exists():
        return None
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error loading universe: {str(e)}")
        return None

# Initialize session state
if "filtered_universe" not in st.session_state:
    st.session_state.filtered_universe = None
if "universe_filter_applied" not in st.session_state:
    st.session_state.universe_filter_applied = False

# Load universe
df_universe = load_idx_universe()

if df_universe is None:
    st.error("❌ File `idx_universe.csv` tidak ditemukan!")
    st.info("💡 Buat file `idx_universe.csv` dengan kolom: Symbol, Name, Sector, MarketCap, AvgVolume, LastPrice")
    st.stop()

# Show universe stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Saham IDX", len(df_universe))
with col2:
    sectors = df_universe['Sector'].nunique()
    st.metric("Jumlah Sektor", sectors)
with col3:
    if st.session_state.filtered_universe is not None:
        st.metric("Universe Terfilter", len(st.session_state.filtered_universe))
    else:
        st.metric("Universe Terfilter", "-")
with col4:
    if st.session_state.universe_filter_applied:
        st.success("✅ Filter Aktif")
    else:
        st.info("⚪ Filter Belum Aktif")

st.markdown("---")

# Filter Configuration
st.sidebar.header("⚙️ Konfigurasi Filter Universe")

# Market Cap Filter
st.sidebar.markdown("### 💰 Market Capitalization")
use_mcap_filter = st.sidebar.checkbox(
    "Filter Market Cap",
    value=True,
    help="Filter berdasarkan kapitalisasi pasar minimum"
)

min_market_cap = None
if use_mcap_filter:
    mcap_options = {
        "10 Triliun": 10e12,
        "5 Triliun": 5e12,
        "1 Triliun": 1e12,
        "500 Miliar": 500e9,
        "100 Miliar": 100e9,
        "50 Miliar": 50e9,
        "10 Miliar": 10e9,
    }
    selected_mcap = st.sidebar.selectbox(
        "Market Cap Minimum",
        options=list(mcap_options.keys()),
        index=3,  # Default 500 Miliar
        help="Kapitalisasi pasar minimum"
    )
    min_market_cap = mcap_options[selected_mcap]

# Volume Filter
st.sidebar.markdown("### 📊 Likuiditas (Volume)")
use_volume_filter = st.sidebar.checkbox(
    "Filter Volume Rata-rata",
    value=True,
    help="Filter berdasarkan volume trading harian rata-rata"
)

min_volume = None
if use_volume_filter:
    volume_options = {
        "10 Juta saham": 10_000_000,
        "5 Juta saham": 5_000_000,
        "2 Juta saham": 2_000_000,
        "1 Juta saham": 1_000_000,
        "500 Ribu saham": 500_000,
        "250 Ribu saham": 250_000,
        "100 Ribu saham": 100_000,
    }
    selected_volume = st.sidebar.selectbox(
        "Volume Harian Minimum",
        options=list(volume_options.keys()),
        index=3,  # Default 1M
        help="Volume rata-rata minimum untuk likuiditas"
    )
    min_volume = volume_options[selected_volume]

# Price Filter
st.sidebar.markdown("### 💵 Harga Saham")
use_price_filter = st.sidebar.checkbox(
    "Filter Harga Minimum",
    value=True,
    help="Hindari saham receh ekstrem"
)

min_price = None
max_price = None
if use_price_filter:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        min_price = st.number_input(
            "Harga Min (Rp)",
            min_value=0,
            value=200,
            step=50,
            help="Harga minimum untuk hindari saham receh"
        )
    with col2:
        use_max_price = st.checkbox("Atur Max", value=False)
        if use_max_price:
            max_price = st.number_input(
                "Harga Max (Rp)",
                min_value=int(min_price),
                value=50000,
                step=1000,
                help="Harga maksimum (opsional)"
            )

# Sector Filter
st.sidebar.markdown("### 🏢 Sektor Industri")
use_sector_filter = st.sidebar.checkbox(
    "Filter Sektor",
    value=False,
    help="Fokus pada sektor tertentu saja"
)

selected_sectors = None
if use_sector_filter:
    all_sectors = sorted(df_universe['Sector'].unique().tolist())
    selected_sectors = st.sidebar.multiselect(
        "Pilih Sektor",
        options=all_sectors,
        default=all_sectors,
        help="Pilih satu atau beberapa sektor untuk difokuskan"
    )

# Apply Filter Button
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
with col1:
    apply_filter = st.button("🔍 Terapkan Filter", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.filtered_universe = None
        st.session_state.universe_filter_applied = False
        st.rerun()

# Apply filters
if apply_filter:
    with st.spinner("🔍 Memfilter universe..."):
        filtered = df_universe.copy()
        
        # Apply Market Cap filter
        if use_mcap_filter and min_market_cap:
            filtered = filtered[filtered['MarketCap'] >= min_market_cap]
        
        # Apply Volume filter
        if use_volume_filter and min_volume:
            filtered = filtered[filtered['AvgVolume'] >= min_volume]
        
        # Apply Price filter
        if use_price_filter and min_price:
            filtered = filtered[filtered['LastPrice'] >= min_price]
            if max_price:
                filtered = filtered[filtered['LastPrice'] <= max_price]
        
        # Apply Sector filter
        if use_sector_filter and selected_sectors:
            filtered = filtered[filtered['Sector'].isin(selected_sectors)]
        
        # Store in session state
        st.session_state.filtered_universe = filtered
        st.session_state.universe_filter_applied = True
        
        st.success(f"✅ Filter berhasil! {len(filtered)} saham dari {len(df_universe)} saham lolos filter")
        st.rerun()

# Display results
st.markdown("---")

# Show current filters
if st.session_state.universe_filter_applied:
    st.markdown("### 🎯 Filter Aktif")
    filter_summary = []
    
    if use_mcap_filter and min_market_cap:
        filter_summary.append(f"💰 Market Cap ≥ Rp {min_market_cap:,.0f}")
    if use_volume_filter and min_volume:
        filter_summary.append(f"📊 Volume ≥ {min_volume:,} saham/hari")
    if use_price_filter and min_price:
        price_filter = f"💵 Harga ≥ Rp {min_price:,.0f}"
        if max_price:
            price_filter += f" dan ≤ Rp {max_price:,.0f}"
        filter_summary.append(price_filter)
    if use_sector_filter and selected_sectors:
        filter_summary.append(f"🏢 Sektor: {', '.join(selected_sectors)}")
    
    if filter_summary:
        for item in filter_summary:
            st.info(item)

# Display filtered universe
if st.session_state.filtered_universe is not None:
    filtered_df = st.session_state.filtered_universe
    
    st.markdown(f"### 📋 Universe Terfilter ({len(filtered_df)} saham)")
    
    # Format display
    display_df = filtered_df.copy()
    display_df['MarketCap'] = display_df['MarketCap'].apply(lambda x: f"Rp {x/1e12:.2f}T" if x >= 1e12 else f"Rp {x/1e9:.1f}M")
    display_df['AvgVolume'] = display_df['AvgVolume'].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x/1e3:.0f}K")
    display_df['LastPrice'] = display_df['LastPrice'].apply(lambda x: f"Rp {x:,.0f}")
    
    # Show dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": st.column_config.TextColumn("Symbol", width="small"),
            "Name": st.column_config.TextColumn("Nama Perusahaan", width="medium"),
            "Sector": st.column_config.TextColumn("Sektor", width="small"),
            "MarketCap": st.column_config.TextColumn("Market Cap", width="small"),
            "AvgVolume": st.column_config.TextColumn("Avg Volume", width="small"),
            "LastPrice": st.column_config.TextColumn("Harga", width="small"),
        }
    )
    
    # Sector distribution
    st.markdown("### 📊 Distribusi Sektor")
    sector_dist = filtered_df['Sector'].value_counts()
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.bar_chart(sector_dist)
    
    with col2:
        st.dataframe(
            sector_dist.reset_index(),
            column_config={
                "Sector": "Sektor",
                "count": "Jumlah"
            },
            hide_index=True,
            use_container_width=True
        )
    
    # Download buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Download filtered universe as CSV
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="filtered_universe.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Save as watchlist
        symbols = filtered_df['Symbol'].tolist()
        watchlist_text = "\n".join(symbols)
        st.download_button(
            label="📝 Download Watchlist",
            data=watchlist_text,
            file_name="watchlist_filtered.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download sebagai watchlist.txt"
        )
    
    # Info message
    st.info("💡 **Next Step**: Lanjutkan ke halaman **Scan Harian** untuk melakukan scanning teknikal pada universe terfilter ini!")
    
else:
    # Show full universe if no filter applied
    st.markdown(f"### 📋 Seluruh Saham IDX ({len(df_universe)} saham)")
    st.info("ℹ️ Belum ada filter diterapkan. Gunakan sidebar untuk mengatur filter dan klik **Terapkan Filter**")
    
    # Format display
    display_df = df_universe.copy()
    display_df['MarketCap'] = display_df['MarketCap'].apply(lambda x: f"Rp {x/1e12:.2f}T" if x >= 1e12 else f"Rp {x/1e9:.1f}M")
    display_df['AvgVolume'] = display_df['AvgVolume'].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x/1e3:.0f}K")
    display_df['LastPrice'] = display_df['LastPrice'].apply(lambda x: f"Rp {x:,.0f}")
    
    # Show first 50 rows
    st.dataframe(
        display_df.head(50),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": st.column_config.TextColumn("Symbol", width="small"),
            "Name": st.column_config.TextColumn("Nama Perusahaan", width="medium"),
            "Sector": st.column_config.TextColumn("Sektor", width="small"),
            "MarketCap": st.column_config.TextColumn("Market Cap", width="small"),
            "AvgVolume": st.column_config.TextColumn("Avg Volume", width="small"),
            "LastPrice": st.column_config.TextColumn("Harga", width="small"),
        }
    )
    st.caption(f"Menampilkan 50 dari {len(df_universe)} saham. Terapkan filter untuk melihat hasil yang lebih fokus.")

# Help section
with st.expander("ℹ️ Cara Menggunakan Universe Filter"):
    st.markdown("""
    ### 🎯 Tujuan Universe Filter
    
    Universe Filter adalah **Tahap 1** dari proses scanning 2-tahap:
    1. **Universe Filter** (halaman ini): Filter kasar untuk dapatkan saham berkualitas
    2. **Scan Harian** (halaman berikutnya): Scan teknikal + fundamental detail
    
    ### 📋 Langkah-langkah:
    
    1. **Atur Filter Market Cap**: Tentukan ukuran perusahaan minimum
    2. **Atur Filter Volume**: Pastikan likuiditas memadai
    3. **Atur Filter Harga**: Hindari saham receh atau terlalu mahal
    4. **[OPSIONAL] Filter Sektor**: Fokus pada industri tertentu
    5. **Klik Terapkan Filter**: Sistem akan memfilter seluruh IDX
    6. **Review Hasil**: Lihat distribusi sektor dan statistik
    7. **Lanjut ke Scan Harian**: Universe terfilter otomatis digunakan
    
    ### 🔍 Kriteria Filter:
    
    **Market Cap (Kapitalisasi Pasar)**
    - Large Cap (> 10T): Blue chips, likuid, stabil
    - Mid Cap (1-10T): Growth potential, moderat likuid
    - Small Cap (< 1T): High risk/reward, kurang likuid
    - **Recommended**: ≥ 500M untuk likuiditas baik
    
    **Volume Rata-rata**
    - > 5M: Very liquid, mudah entry/exit
    - 1-5M: Liquid, cukup untuk swing trading
    - < 1M: Kurang likuid, hati-hati slippage
    - **Recommended**: ≥ 1M saham/hari
    
    **Harga Saham**
    - > Rp 200: Hindari saham receh ekstrem
    - < Rp 50,000: Fokus pada range normal
    - **Recommended**: Rp 200 - Rp 50,000
    
    **Sektor**
    - Banking: Likuid, sensitif suku bunga
    - Consumer: Defensive, stabil
    - Energy/Materials: Cyclical, volatil
    - Technology: Growth, high risk/reward
    - **Tip**: Diversifikasi atau fokus sesuai expertise
    
    ### 💡 Strategi Recommended:
    
    **Conservative (Safe Trading)**
    - Market Cap ≥ 5T
    - Volume ≥ 5M
    - Fokus Banking & Consumer
    
    **Balanced (Recommended)**
    - Market Cap ≥ 500M
    - Volume ≥ 1M
    - Harga ≥ Rp 200
    - All sectors
    
    **Aggressive (High Risk/Reward)**
    - Market Cap ≥ 100M
    - Volume ≥ 500K
    - Include small caps & cyclicals
    
    ### 🚀 Workflow 2-Tahap:
    
    ```
    IDX Universe (100 saham)
           ↓
    [Universe Filter] - Filter kasar (market cap, volume, harga, sektor)
           ↓
    Filtered Universe (30 saham)
           ↓
    [Scan Harian] - Filter teknikal (EMA, RSI, ATR) + Fundamental
           ↓
    BUY Signals (5-10 saham)
    ```
    
    ### ✅ Keuntungan Sistem Ini:
    
    - **Cakupan Luas**: Scan seluruh IDX, tidak terbatas watchlist manual
    - **Efisien**: Filter bertahap, dari kasar ke detail
    - **Kualitas Tinggi**: Kombinasi filter likuiditas + teknikal + fundamental
    - **Fleksibel**: Bisa fokus sektor atau diversifikasi
    - **Transparan**: Tahu persis saham mana yang difilter dan kenapa
    
    ### 💡 Tips:
    
    - **Update idx_universe.csv** secara berkala dengan data terbaru
    - **Mulai konservatif** (filter ketat), relaksasi bertahap
    - **Review distribusi sektor** untuk pastikan diversifikasi
    - **Download filtered universe** untuk referensi
    - **Kombinasikan dengan Scan Harian** untuk hasil optimal!
    """)
