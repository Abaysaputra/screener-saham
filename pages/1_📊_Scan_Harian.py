"""
Daily Signal Scanner Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from core.data import get_daily_history_for_scan, load_watchlist, normalize_symbol, merge_watchlist_and_universe
from core.config import Config
from utils.strategy import generate_signals
from utils.risk import position_size, calculate_stop_loss, calculate_take_profit
from utils.fundamental import get_fundamental_data, check_fundamental_criteria, get_fundamental_summary, format_fundamental_display
from utils.theme import apply_app_theme

st.set_page_config(
    page_title="Scan Harian - Swing Trader",
    page_icon="🔍",
    layout="wide"
)

apply_app_theme()

st.title("🔍 Scan Sinyal BUY Harian")

# Initialize session state
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None

# Sidebar configuration
st.sidebar.header("⚙️ Pengaturan Scan")

modal_per_saham = st.sidebar.number_input(
    "Modal per Saham (Default)",
    min_value=1_000,
    value=10_000,
    step=1_000,
    help="Modal default untuk setiap saham (bisa diubah manual di hasil scan)"
)

capital = st.sidebar.number_input(
    "Total Modal Trading (Rp)",
    min_value=1_000,
    value=int(Config.DEFAULT_CAPITAL),
    step=1_000,
    help="Total modal yang tersedia untuk trading (untuk validasi)"
)

lookback_signals = st.sidebar.slider(
    "Periode Scan (hari)",
    min_value=1,
    max_value=10,
    value=3,
    help="Jumlah hari terakhir untuk mencari sinyal BUY"
)

rsi_max = st.sidebar.slider(
    "RSI Maksimum",
    min_value=50.0,
    max_value=80.0,
    value=70.0,
    step=5.0,
    help="RSI maksimum untuk sinyal BUY (hindari overbought)"
)

# R/R Ratio selection
rr_ratio = st.sidebar.selectbox(
    "Risk/Reward Ratio Target",
    options=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
    index=2,  # Default 2.0
    help="Target Risk/Reward ratio untuk Take Profit (semakin tinggi semakin baik)"
)

st.sidebar.info(f"💡 Target R/R: **{rr_ratio}** (Take Profit = {rr_ratio}x risiko)")

signal_mode = st.sidebar.radio(
    "Mode Sinyal",
    options=["Crossover Saja", "Crossover + Trend Lanjutan"],
    index=1,
    help=(
        "Crossover Saja: hanya sinyal EMA cross-up baru. "
        "Crossover + Trend Lanjutan: juga izinkan trend bullish berlanjut (EMA fast > EMA slow, RSI sehat)."
    ),
)
enable_continuation_signal = signal_mode == "Crossover + Trend Lanjutan"

# Fundamental Filter section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Filter Fundamental")

enable_fundamental = st.sidebar.checkbox(
    "Aktifkan Filter Fundamental",
    value=False,
    help="Filter saham berdasarkan kriteria fundamental untuk menghindari saham berkualitas rendah"
)

fundamental_criteria = {}

if enable_fundamental:
    st.sidebar.info("🎯 Filter saham berdasarkan kualitas fundamental")
    
    # EPS Filter
    eps_positive = st.sidebar.checkbox(
        "EPS Positif (Profitable)",
        value=True,
        help="Hanya saham dengan EPS (Earning Per Share) positif"
    )
    if eps_positive:
        fundamental_criteria['eps_positive'] = True
    
    # PE Ratio Filter
    use_pe_filter = st.sidebar.checkbox(
        "Filter PE Ratio",
        value=False,
        help="Price to Earnings Ratio - valuasi harga"
    )
    if use_pe_filter:
        max_pe = st.sidebar.slider(
            "PE Ratio Maksimum",
            min_value=5.0,
            max_value=50.0,
            value=25.0,
            step=5.0,
            help="PE < 15 = undervalued, 15-25 = wajar, > 25 = mahal"
        )
        fundamental_criteria['max_pe'] = max_pe
    
    # PB Ratio Filter
    use_pb_filter = st.sidebar.checkbox(
        "Filter PB Ratio",
        value=False,
        help="Price to Book Ratio - harga vs nilai buku"
    )
    if use_pb_filter:
        max_pb = st.sidebar.slider(
            "PB Ratio Maksimum",
            min_value=0.5,
            max_value=5.0,
            value=3.0,
            step=0.5,
            help="PB < 1 = undervalued, 1-3 = wajar, > 3 = mahal"
        )
        fundamental_criteria['max_pb'] = max_pb
    
    # Profit Margin Filter
    use_margin_filter = st.sidebar.checkbox(
        "Filter Profit Margin",
        value=False,
        help="Margin keuntungan perusahaan"
    )
    if use_margin_filter:
        min_margin = st.sidebar.slider(
            "Profit Margin Minimum (%)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=1.0,
            help="Margin > 10% = sangat baik, 5-10% = baik"
        ) / 100
        fundamental_criteria['min_profit_margin'] = min_margin
    
    # Market Cap Filter
    use_mcap_filter = st.sidebar.checkbox(
        "Filter Market Cap",
        value=False,
        help="Kapitalisasi pasar minimum"
    )
    if use_mcap_filter:
        min_mcap = st.sidebar.selectbox(
            "Market Cap Minimum",
            options=[
                ("1 Triliun", 1e12),
                ("500 Miliar", 500e9),
                ("100 Miliar", 100e9),
                ("50 Miliar", 50e9)
            ],
            format_func=lambda x: x[0],
            help="Market cap untuk filter ukuran perusahaan"
        )
        fundamental_criteria['min_market_cap'] = min_mcap[1]

# Technical Health Filter section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Filter Teknikal (Kesehatan Trend)")

enable_technical_health = st.sidebar.checkbox(
    "Aktifkan Filter Teknikal Kesehatan",
    value=True,
    help="Filter saham berdasarkan kesehatan teknikal untuk hindari saham lemah"
)

technical_criteria = {}

if enable_technical_health:
    st.sidebar.info("🎯 Filter saham berdasarkan kesehatan teknikal")
    
    # EMA Slow Filter
    require_above_ema = st.sidebar.checkbox(
        "Wajib di Atas EMA Slow",
        value=True,
        help="Hanya saham yang close price di atas EMA slow (trend naik)"
    )
    if require_above_ema:
        technical_criteria['above_ema_slow'] = True
    
    # 52-week low filter
    use_52w_filter = st.sidebar.checkbox(
        "Filter 52-Week Low",
        value=True,
        help="Hindari saham yang baru rebound dari crash dalam"
    )
    if use_52w_filter:
        min_52w_pct = st.sidebar.slider(
            "Harga > 52W Low + X%",
            min_value=5.0,
            max_value=50.0,
            value=20.0,
            step=5.0,
            help="Harga saat ini minimal X% di atas 52-week low"
        )
        technical_criteria['min_52w_pct'] = min_52w_pct / 100
    
    # ATR/Volatility Filter
    use_atr_filter = st.sidebar.checkbox(
        "Filter Volatilitas (ATR)",
        value=True,
        help="Hindari saham terlalu datar (volatilitas rendah)"
    )
    if use_atr_filter:
        min_atr_pct = st.sidebar.slider(
            "ATR/Price Minimum (%)",
            min_value=0.5,
            max_value=5.0,
            value=1.5,
            step=0.5,
            help="Volatilitas minimum: ATR dibagi harga (1.5% = sehat)"
        )
        technical_criteria['min_atr_pct'] = min_atr_pct / 100
    
    # Volume Filter
    use_volume_filter = st.sidebar.checkbox(
        "Filter Volume Rata-rata",
        value=True,
        help="Hindari saham dengan volume trading rendah"
    )
    if use_volume_filter:
        min_volume = st.sidebar.selectbox(
            "Volume 20-Hari Minimum",
            options=[
                ("1 Juta saham", 1_000_000),
                ("500 Ribu saham", 500_000),
                ("250 Ribu saham", 250_000),
                ("100 Ribu saham", 100_000)
            ],
            index=2,  # Default 250K
            format_func=lambda x: x[0],
            help="Volume rata-rata minimum untuk likuiditas"
        )
        technical_criteria['min_avg_volume'] = min_volume[1]

# Universe/Watchlist Selection
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Sumber Data Scan")

use_universe = st.sidebar.checkbox(
    "Gunakan Filtered Universe",
    value=False,
    help="Gunakan hasil filter dari Universe Filter. Jika tidak aktif, gunakan watchlist.txt"
)

if use_universe:
    # Check if filtered universe exists in session state
    if "filtered_universe" in st.session_state and st.session_state.filtered_universe is not None:
        filtered_df = st.session_state.filtered_universe
        watchlist = filtered_df['Symbol'].tolist()
        st.sidebar.success(f"✅ {len(watchlist)} saham dari Filtered Universe")
        
        with st.sidebar.expander("Info Universe"):
            st.write(f"**Total Saham**: {len(watchlist)}")
            sector_counts = filtered_df['Sector'].value_counts()
            st.write("**Distribusi Sektor**:")
            for sector, count in sector_counts.head(5).items():
                st.write(f"• {sector}: {count}")
    else:
        st.sidebar.warning("⚠️ Filtered Universe belum ada!")
        st.sidebar.info("💡 Buka **Universe Filter** dulu untuk membuat filtered universe")
        watchlist = load_watchlist()  # Fallback
        if watchlist:
            st.sidebar.info(f"↩️ Menggunakan watchlist.txt ({len(watchlist)} saham)")
else:
    # Load watchlist
    watchlist = load_watchlist()
    
    st.sidebar.markdown("### 📋 Watchlist")
    if not watchlist:
        st.sidebar.warning("⚠️ Watchlist kosong! Tambahkan kode saham di `watchlist.txt`")
    else:
        st.sidebar.success(f"✅ {len(watchlist)} saham di watchlist")
        with st.sidebar.expander("Lihat Watchlist"):
            for sym in watchlist:
                st.write(f"• {sym}")

# Main content
if not watchlist:
    st.error("❌ Tidak ada saham untuk di-scan!")
    st.info("💡 **Pilihan untuk mendapatkan saham:**\n\n"
            "**Opsi 1: Universe Filter (Recommended)**\n"
            "1. Buka halaman **Universe Filter** (sidebar kiri)\n"
            "2. Terapkan filter market cap, volume, harga, sektor\n"
            "3. Kembali ke halaman ini\n"
            "4. Aktifkan 'Gunakan Filtered Universe'\n\n"
            "**Opsi 2: Watchlist Manual**\n"
            "1. Buka file `watchlist.txt` di folder aplikasi\n"
            "2. Tambahkan kode saham (satu per baris)\n"
            "3. Contoh: BBCA, BBRI, TLKM\n"
            "4. Refresh halaman ini")
    st.stop()

# Scan button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    scan_button = st.button("🔍 Mulai Scan", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.scan_results = None
        st.rerun()

# Run scan
if scan_button:
    with st.spinner(f"🔍 Scanning {len(watchlist)} saham..."):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        scan_stats = {
            "total": 0,
            "passed_fundamental": 0,
            "insufficient_data": 0,
            "failed_technical": 0,
            "no_signal": 0,
            "errors": 0,
        }
        
        # Apply fundamental filter if enabled
        filtered_watchlist = watchlist.copy()
        
        if enable_fundamental and fundamental_criteria:
            st.info("🔍 Applying fundamental filters...")
            filter_status = st.empty()
            
            temp_filtered = []
            for idx, sym in enumerate(watchlist):
                filter_status.text(f"Checking fundamentals for {sym}... ({idx+1}/{len(watchlist)})")
                
                yf_symbol = normalize_symbol(sym)
                fundamentals = get_fundamental_data(yf_symbol)
                
                if check_fundamental_criteria(fundamentals, fundamental_criteria):
                    temp_filtered.append(sym)
            
            filtered_watchlist = temp_filtered
            filter_status.empty()
            scan_stats["passed_fundamental"] = len(filtered_watchlist)
            
            if not filtered_watchlist:
                st.error("❌ Tidak ada saham yang memenuhi kriteria fundamental!")
                st.info("💡 Coba relaksasi kriteria fundamental filter")
                st.stop()
            
            st.success(f"✅ {len(filtered_watchlist)} dari {len(watchlist)} saham memenuhi kriteria fundamental")
        
        for idx, sym in enumerate(filtered_watchlist):
            scan_stats["total"] += 1
            status_text.text(f"Scanning {sym}... ({idx+1}/{len(filtered_watchlist)})")
            progress_bar.progress((idx + 1) / len(filtered_watchlist))
            
            try:
                # Fetch data
                df = get_daily_history_for_scan(sym)
                
                if df.empty or len(df) < lookback_signals + 50:
                    scan_stats["insufficient_data"] += 1
                    continue
                
                # Generate signals
                df_sig = generate_signals(df, rsi_max=rsi_max)
                
                # Apply technical health filters if enabled
                if enable_technical_health and technical_criteria:
                    # Check latest data point for technical health
                    latest = df_sig.iloc[-1]
                    
                    # Filter 1: Must be above EMA slow
                    if technical_criteria.get('above_ema_slow'):
                        if latest['close'] < latest['ema_slow']:
                            scan_stats["failed_technical"] += 1
                            continue  # Skip this stock
                    
                    # Filter 2: 52-week low filter
                    if 'min_52w_pct' in technical_criteria:
                        # Calculate 52-week low (252 trading days)
                        lookback_52w = min(252, len(df_sig))
                        low_52w = df_sig['low'].tail(lookback_52w).min()
                        min_price_threshold = low_52w * (1 + technical_criteria['min_52w_pct'])
                        
                        if latest['close'] < min_price_threshold:
                            scan_stats["failed_technical"] += 1
                            continue  # Price too close to 52-week low
                    
                    # Filter 3: ATR/Volatility filter
                    if 'min_atr_pct' in technical_criteria:
                        # Calculate ATR (14-period)
                        if 'atr' in df_sig.columns:
                            atr = latest['atr']
                        else:
                            # Calculate ATR if not present
                            high_low = df_sig['high'] - df_sig['low']
                            high_close = abs(df_sig['high'] - df_sig['close'].shift())
                            low_close = abs(df_sig['low'] - df_sig['close'].shift())
                            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                            atr = true_range.rolling(window=14).mean().iloc[-1]
                        
                        atr_pct = atr / latest['close']
                        if atr_pct < technical_criteria['min_atr_pct']:
                            scan_stats["failed_technical"] += 1
                            continue  # Volatility too low (stock too flat)
                    
                    # Filter 4: Volume filter
                    if 'min_avg_volume' in technical_criteria:
                        avg_volume_20 = df_sig['volume'].tail(20).mean()
                        if avg_volume_20 < technical_criteria['min_avg_volume']:
                            scan_stats["failed_technical"] += 1
                            continue  # Volume too low
                
                # Check recent signals
                recent = df_sig.tail(lookback_signals)
                buys = recent[recent["signal"] == "BUY"]

                signal_type = "BUY (Crossover)"
                selected_signal_row = buys.iloc[-1] if not buys.empty else None

                if selected_signal_row is None and enable_continuation_signal:
                    continuation = recent[
                        (recent["ema_fast"] > recent["ema_slow"]) &
                        (recent["rsi"] < rsi_max) &
                        (recent["close"] > recent["ema_fast"])
                    ]
                    if not continuation.empty:
                        selected_signal_row = continuation.iloc[-1]
                        signal_type = "BUY (Trend Lanjutan)"

                if selected_signal_row is None:
                    scan_stats["no_signal"] += 1
                    continue

                # Get selected buy signal row
                last_buy = selected_signal_row
                entry_price = float(last_buy["close"])
                sl_price = calculate_stop_loss(entry_price)
                tp_price = calculate_take_profit(entry_price, sl_price, r_multiple=rr_ratio)
                
                # Use default modal from sidebar
                results.append({
                    "Symbol": sym,
                    "Tanggal Sinyal": last_buy.name.date(),
                    "Entry Price": round(entry_price, 2),
                    "Stop Loss": round(sl_price, 2),
                    "Take Profit": round(tp_price, 2),
                    "Modal Dialokasikan": modal_per_saham,  # Default from sidebar, user can edit
                    "RSI": round(last_buy["rsi"], 2),
                    "Target R/R": rr_ratio,  # Store target R/R
                    "Tipe Sinyal": signal_type,
                })
                
            except Exception as e:
                st.sidebar.error(f"Error pada {sym}: {str(e)}")
                scan_stats["errors"] += 1
                continue
        
        progress_bar.empty()
        status_text.empty()
        
        # Store results in session state
        st.session_state.scan_results = results
        st.session_state.scan_stats = scan_stats

# Display results
if st.session_state.scan_results is not None:
    results = st.session_state.scan_results
    scan_stats = st.session_state.get("scan_stats", {})
    
    if not results:
        st.info(f"ℹ️ Tidak ada sinyal BUY dalam {lookback_signals} hari terakhir di watchlist.")
        if scan_stats:
            st.warning("Diagnostik scan: banyak saham tersaring sebelum menghasilkan sinyal.")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Diproses", scan_stats.get("total", 0))
            with c2:
                st.metric("Data Kurang", scan_stats.get("insufficient_data", 0))
            with c3:
                st.metric("Gagal Filter Teknikal", scan_stats.get("failed_technical", 0))
            with c4:
                st.metric("Tanpa Sinyal", scan_stats.get("no_signal", 0))
            with c5:
                st.metric("Error Data", scan_stats.get("errors", 0))

            st.info(
                "Tips cepat: aktifkan mode 'Crossover + Trend Lanjutan', perbesar 'Periode Scan' ke 5-10 hari, "
                "atau nonaktifkan sementara filter teknikal 52W/ATR/Volume untuk melihat kandidat lebih banyak."
            )
    else:
        st.success(f"✅ Ditemukan {len(results)} sinyal BUY!")
        
        # Convert to DataFrame
        df_results = pd.DataFrame(results)
        
        # Results table with editable capital
        st.markdown("### 📋 Hasil Scan (Edit Kolom 'Modal Dialokasikan' sesuai keinginan)")
        
        # Create editable dataframe
        edited_df = st.data_editor(
            df_results,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol", width="small", disabled=True),
                "Tanggal Sinyal": st.column_config.DateColumn("Tanggal", disabled=True),
                "Entry Price": st.column_config.NumberColumn("Entry", format="%.2f", disabled=True),
                "Stop Loss": st.column_config.NumberColumn("Stop Loss", format="%.2f", disabled=True),
                "Take Profit": st.column_config.NumberColumn("Take Profit", format="%.2f", disabled=True),
                "Modal Dialokasikan": st.column_config.NumberColumn(
                    "Modal Dialokasikan",
                    format="Rp %d",
                    help="Edit nilai ini untuk menentukan modal per saham",
                    min_value=0,
                    step=1000000
                ),
                "RSI": st.column_config.NumberColumn("RSI", format="%.2f", disabled=True),
                "Target R/R": st.column_config.NumberColumn("Target R/R", format="%.1f", disabled=True),
            },
            num_rows="fixed"
        )
        
        # Calculate metrics based on user input
        total_capital_allocated = 0
        total_potential_profit = 0
        total_potential_loss = 0
        
        # Calculate for each row based on user's allocated capital
        calculated_rows = []
        for idx, row in edited_df.iterrows():
            modal = row["Modal Dialokasikan"]
            entry = row["Entry Price"]
            sl = row["Stop Loss"]
            tp = row["Take Profit"]
            
            # Calculate size based on allocated capital
            size = int(modal / entry) if entry > 0 else 0
            
            # Calculate potential profit and loss
            potential_loss = (entry - sl) * size
            potential_profit = (tp - entry) * size
            rr = potential_profit / potential_loss if potential_loss > 0 else 0
            
            total_capital_allocated += modal
            total_potential_profit += potential_profit
            total_potential_loss += potential_loss
            
            calculated_rows.append({
                "Symbol": row["Symbol"],
                "Size (shares)": size,
                "Modal": int(modal),
                "Potential Loss": int(potential_loss),
                "Potential Profit": int(potential_profit),
                "Risk/Reward": round(rr, 2)
            })
        
        # Summary metrics
        st.markdown("### 📊 Ringkasan")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Sinyal", len(results))
        with col2:
            st.metric("Total Modal Dialokasikan", f"Rp {total_capital_allocated:,.0f}")
        with col3:
            st.metric("Total Potential Profit", f"Rp {total_potential_profit:,.0f}")
        with col4:
            avg_rr = total_potential_profit / total_potential_loss if total_potential_loss > 0 else 0
            st.metric("Avg R/R Actual", f"{avg_rr:.2f}")
        with col5:
            st.metric("Target R/R", f"{rr_ratio:.1f}", help="R/R ratio yang Anda pilih")
        
        # Show calculated metrics
        st.markdown("### 📈 Detail Perhitungan")
        df_calculated = pd.DataFrame(calculated_rows)
        
        # Format display
        df_calc_display = df_calculated.copy()
        df_calc_display["Modal"] = df_calc_display["Modal"].apply(lambda x: f"Rp {x:,.0f}")
        df_calc_display["Potential Loss"] = df_calc_display["Potential Loss"].apply(lambda x: f"Rp {x:,.0f}")
        df_calc_display["Potential Profit"] = df_calc_display["Potential Profit"].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(
            df_calc_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol", width="small"),
                "Risk/Reward": st.column_config.NumberColumn("R/R", format="%.2f"),
            }
        )
        
        # Download button - combine both dataframes
        df_export = edited_df.merge(df_calculated, on="Symbol")
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
        
        # Show fundamental analysis if enabled
        if enable_fundamental:
            st.markdown("---")
            st.markdown("### 📊 Analisa Fundamental Saham Terfilter")
            
            # Select stock to view fundamentals
            selected_symbol = st.selectbox(
                "Pilih saham untuk melihat detail fundamental:",
                options=edited_df["Symbol"].tolist()
            )
            
            if selected_symbol:
                yf_symbol = normalize_symbol(selected_symbol)
                fundamentals = get_fundamental_data(yf_symbol)
                
                if fundamentals:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Quality rating
                        quality = get_fundamental_summary(fundamentals)
                        st.info(f"**Kualitas Fundamental:**\n\n{quality}")
                        
                        # Show fundamental table
                        df_fund = format_fundamental_display(fundamentals)
                        st.dataframe(df_fund, use_container_width=True, hide_index=True)
                    
                    with col2:
                        # Explanation
                        st.markdown("#### 💡 Interpretasi Fundamental")
                        
                        eps = fundamentals.get('eps')
                        pe = fundamentals.get('pe_ratio')
                        pb = fundamentals.get('pb_ratio')
                        margin = fundamentals.get('profit_margin')
                        roe = fundamentals.get('roe')
                        
                        if eps is not None:
                            if eps > 0:
                                st.success(f"✅ **EPS Positif** ({eps:.2f}): Perusahaan profitable")
                            else:
                                st.error(f"❌ **EPS Negatif** ({eps:.2f}): Perusahaan rugi")
                        
                        if pe is not None and pe > 0:
                            if pe < 15:
                                st.success(f"✅ **PE Ratio {pe:.2f}**: Valuasi undervalued")
                            elif pe < 25:
                                st.info(f"ℹ️ **PE Ratio {pe:.2f}**: Valuasi wajar")
                            else:
                                st.warning(f"⚠️ **PE Ratio {pe:.2f}**: Valuasi tinggi/mahal")
                        
                        if pb is not None and pb > 0:
                            if pb < 1:
                                st.success(f"✅ **PB Ratio {pb:.2f}**: Trading di bawah nilai buku")
                            elif pb < 3:
                                st.info(f"ℹ️ **PB Ratio {pb:.2f}**: Valuasi wajar")
                            else:
                                st.warning(f"⚠️ **PB Ratio {pb:.2f}**: Valuasi tinggi")
                        
                        if margin is not None:
                            margin_pct = margin * 100
                            if margin_pct > 10:
                                st.success(f"✅ **Profit Margin {margin_pct:.2f}%**: Sangat baik")
                            elif margin_pct > 5:
                                st.info(f"ℹ️ **Profit Margin {margin_pct:.2f}%**: Baik")
                            else:
                                st.warning(f"⚠️ **Profit Margin {margin_pct:.2f}%**: Rendah")
                        
                        if roe is not None:
                            roe_pct = roe * 100
                            if roe_pct > 15:
                                st.success(f"✅ **ROE {roe_pct:.2f}%**: Excellent")
                            elif roe_pct > 10:
                                st.info(f"ℹ️ **ROE {roe_pct:.2f}%**: Good")
                            else:
                                st.warning(f"⚠️ **ROE {roe_pct:.2f}%**: Below average")
                else:
                    st.warning(f"⚠️ Data fundamental untuk {selected_symbol} tidak tersedia")
        
        # Warnings
        if total_capital_allocated > capital:
            st.warning(f"⚠️ **Peringatan**: Total modal dialokasikan (Rp {total_capital_allocated:,.0f}) "
                      f"melebihi modal tersedia (Rp {capital:,.0f})")

# Info box
with st.expander("ℹ️ Cara Menggunakan"):
    st.markdown("""
    ### Workflow 2-Tahap (Recommended):
    
    **Tahap 1: Universe Filter**
    1. Buka halaman **Universe Filter** (di sidebar)
    2. Atur filter market cap, volume, harga, sektor
    3. Terapkan filter untuk dapatkan universe berkualitas
    4. Universe tersimpan otomatis di session
    
    **Tahap 2: Scan Harian (halaman ini)**
    1. Aktifkan **"Gunakan Filtered Universe"** di sidebar
    2. Atur filter teknikal dan fundamental (opsional)
    3. Atur target R/R ratio
    4. Klik **Mulai Scan**
    
    ### Atau Gunakan Watchlist Manual:
    
    1. **Atur Modal Default**: Masukkan modal per saham default di sidebar
    2. **Atur Total Modal**: Masukkan total modal trading untuk validasi
    3. **Atur Target R/R**: Pilih Risk/Reward ratio target (1.0 - 4.0)
    4. **Atur Periode**: Pilih berapa hari ke belakang untuk mencari sinyal
    5. **[OPSIONAL] Filter Fundamental**: Aktifkan untuk filter saham berkualitas fundamental
    6. **[OPSIONAL] Filter Teknikal**: Aktifkan untuk filter kesehatan teknikal trend
    7. **Klik Scan**: Tekan tombol "Mulai Scan" untuk memulai
    7. **Edit Modal**: Sesuaikan kolom "Modal Dialokasikan" untuk setiap saham sesuai keinginan
    8. **Lihat Perhitungan**: Sistem otomatis menghitung potential profit dari modal Anda
    9. **Analisa Fundamental**: Jika aktif, lihat kualitas fundamental setiap saham
    10. **Download**: Unduh hasil dalam format CSV jika diperlukan
    
    ### Interpretasi Hasil:
    
    - **Modal Dialokasikan**: Modal yang Anda alokasikan untuk setiap saham (bisa diedit)
    - **Entry Price**: Harga untuk masuk posisi
    - **Stop Loss**: Harga untuk cut loss otomatis
    - **Take Profit**: Target harga berdasarkan R/R ratio yang Anda pilih
    - **Target R/R**: Risk/Reward ratio yang Anda tentukan (1.0 = 1:1, 2.0 = 1:2, dst)
    - **Avg R/R Actual**: R/R ratio aktual berdasarkan modal yang dialokasikan
    - **Size**: Jumlah saham yang bisa dibeli dengan modal yang dialokasikan
    - **Potential Profit**: Potensi profit berdasarkan modal yang Anda masukkan
    - **Potential Loss**: Potensi loss jika hit stop loss
    - **Risk/Reward**: Rasio potensi profit vs risiko (> 2 lebih baik)
    - **RSI**: Relative Strength Index (< 70 tidak overbought)
    
    ### Filter Fundamental:
    
    **Mengapa Penting?**
    - Menghindari saham gorengan/berkualitas rendah
    - Kombinasi teknikal + fundamental = strategi lebih robust
    - Filter saham dengan kondisi keuangan sehat
    
    **Kriteria Filter:**
    - **EPS Positif**: Perusahaan profitable (tidak rugi)
    - **PE Ratio**: Valuasi harga (< 15 undervalued, 15-25 wajar, > 25 mahal)
    - **PB Ratio**: Harga vs nilai buku (< 1 undervalued, 1-3 wajar, > 3 mahal)
    - **Profit Margin**: Margin keuntungan (> 10% excellent, 5-10% good)
    - **Market Cap**: Ukuran perusahaan (larger = lebih stabil)
    
    **Recommended Settings:**
    - EPS Positif: ✅ Aktifkan (hindari perusahaan rugi)
    - PE < 25: Hindari valuasi terlalu mahal
    - PB < 3: Hindari valuasi premium berlebihan
    - Market Cap > 1T: Fokus pada large cap (lebih likuid)
    
    ### Filter Teknikal (Kesehatan Trend):
    
    **Mengapa Penting?**
    - Hindari saham dengan trend lemah atau sideways
    - Pastikan momentum dan likuiditas memadai
    - Kombinasi dengan filter fundamental = hasil sangat berkualitas
    - Mengurangi false signals dan meningkatkan win rate
    
    **Kriteria Filter:**
    - **Di Atas EMA Slow**: Harga di atas EMA slow = trend naik (bullish)
    - **52-Week Low**: Hindari saham yang baru rebound dari crash dalam
    - **ATR/Volatilitas**: Pastikan pergerakan harga sehat (tidak terlalu datar)
    - **Volume Rata-rata**: Pastikan likuiditas memadai untuk entry/exit mudah
    
    **Recommended Settings (DEFAULT):**
    - ✅ Di Atas EMA Slow: WAJIB (pastikan trend naik)
    - ✅ Harga > 52W Low + 20%: Hindari catch falling knife
    - ✅ ATR/Price > 1.5%: Pastikan volatilitas sehat
    - ✅ Volume > 250K: Pastikan likuiditas cukup
    
    **Interpretasi:**
    - Filter teknikal akan **mengurangi jumlah sinyal** tapi **meningkatkan kualitas**
    - Saham yang lolos filter = trend kuat + volatilitas sehat + likuid
    - **Kombinasi 3 filter (Fundamental + Teknikal + Sinyal) = POWER COMBO!**
    
    ### Pilihan R/R Ratio:
    
    - **1.0 - 1.5**: Conservative (risk averse), Take Profit dekat
    - **2.0 - 2.5**: Balanced (recommended), rasio seimbang
    - **3.0 - 4.0**: Aggressive, Take Profit tinggi tapi butuh waktu lebih lama
    
    ### Tips:
    
    - **[BEST PRACTICE] Gunakan Universe Filter** untuk cakupan luas
    - Universe Filter menghasilkan 20-50 saham berkualitas
    - Kombinasi Universe + Teknikal + Fundamental = ULTRA QUALITY!
    - **Atur modal default** di sidebar sesuai strategi Anda
    - **Aktifkan filter fundamental** untuk hasil lebih berkualitas
    - **Pilih R/R ratio** berdasarkan kondisi market dan risk tolerance
    - **Edit manual** di tabel untuk menyesuaikan modal per saham
    - Sistem menghitung potential profit berdasarkan modal yang Anda input
    - Prioritaskan saham dengan R/R ratio > 2
    - R/R ratio lebih tinggi = profit lebih besar, tapi butuh waktu lebih lama
    - Perhatikan RSI, hindari yang terlalu tinggi (> 70)
    - Pastikan total modal dialokasikan tidak melebihi modal tersedia
    - **Fundamental + Teknikal** = kombinasi powerful!
    - Selalu gunakan stop loss!
    """)

