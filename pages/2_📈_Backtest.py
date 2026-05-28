"""
Backtest Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from itertools import product

from core.data import get_history_yf, normalize_symbol, load_watchlist
from core.config import Config
from utils.strategy import generate_signals
from utils.backtest import backtest_risk_based, calculate_backtest_metrics
from utils.fundamental import get_fundamental_data, check_fundamental_criteria, format_fundamental_display, get_fundamental_summary
from utils.journal import log_trades
from utils.theme import apply_app_theme

st.set_page_config(
    page_title="Backtest - Swing Trader",
    page_icon="📈",
    layout="wide"
)

apply_app_theme()

st.title("📈 Backtest Strategi Trading")

# Initialize session state
if "backtest_results" not in st.session_state:
    st.session_state.backtest_results = None
if "backtest_df" not in st.session_state:
    st.session_state.backtest_df = None
if "optimization_results" not in st.session_state:
    st.session_state.optimization_results = None

# Main tabs
tab1, tab2 = st.tabs(["📊 Single Backtest", "🔍 Parameter Optimization"])

# TAB 1: Single Backtest
with tab1:
    # Sidebar configuration
    st.sidebar.header("⚙️ Pengaturan Backtest")
    
    # Stock selection
    watchlist = load_watchlist()
    if not watchlist:
        st.error("❌ Watchlist kosong! Tambahkan kode saham di `watchlist.txt`")
        st.stop()
    
    symbol = st.sidebar.selectbox(
        "Pilih Saham",
        watchlist,
        help="Pilih saham untuk backtest"
    )

    # Time period
    years = st.sidebar.slider(
        "Period (Tahun)",
        min_value=1,
        max_value=5,
        value=2,
        help="Durasi data historis untuk backtest"
    )
    
    # Capital
    capital = st.sidebar.number_input(
        "Modal Awal (Rp)",
        min_value=1_000,
        value=int(Config.DEFAULT_CAPITAL),
        step=1_000,
        help="Modal awal untuk backtest"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Parameter Trading")
    
    # Risk parameters
    risk_pct = st.sidebar.slider(
        "Risk per Trade (%)",
        min_value=0.5,
        max_value=5.0,
        value=Config.DEFAULT_RISK_PER_TRADE * 100,
        step=0.5,
        help="Persentase risiko modal per trade"
    ) / 100
    
    sl_pct = st.sidebar.slider(
        "Stop Loss (%)",
        min_value=1.0,
        max_value=5.0,
        value=Config.DEFAULT_SL_PCT * 100,
        step=0.5,
        help="Stop loss dari entry price"
    ) / 100
    
    tp_r_multiple = st.sidebar.slider(
        "Take Profit (R-Multiple)",
        min_value=1.0,
        max_value=5.0,
        value=Config.DEFAULT_TP_R_MULTIPLE,
        step=0.5,
        help="Target profit dalam kelipatan R (risk)"
    )
    
    rsi_max = st.sidebar.slider(
        "RSI Maksimum",
        min_value=50.0,
        max_value=80.0,
        value=70.0,
        step=5.0,
        help="RSI maksimum untuk entry"
    )
    
    # Fundamental Filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Filter Fundamental")
    
    enable_fundamental = st.sidebar.checkbox(
        "Cek Fundamental Saham",
        value=False,
        help="Tampilkan analisa fundamental sebelum backtest"
    )
    
    # Run backtest button
    col1, col2 = st.columns([1, 1])
    with col1:
        run_button = st.button("🚀 Jalankan Backtest", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.backtest_results = None
            st.session_state.backtest_df = None
            st.rerun()
    
    # Show fundamental analysis before backtest if enabled
    if enable_fundamental:
        st.markdown("---")
        st.markdown("### 📊 Analisa Fundamental")
        
        yf_symbol = normalize_symbol(symbol)
        fundamentals = get_fundamental_data(yf_symbol)
        
        if fundamentals:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                quality = get_fundamental_summary(fundamentals)
                st.info(f"**Kualitas Fundamental:**\n\n{quality}")
                
                df_fund = format_fundamental_display(fundamentals)
                st.dataframe(df_fund, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("#### 💡 Interpretasi")
                
                eps = fundamentals.get('eps')
                pe = fundamentals.get('pe_ratio')
                pb = fundamentals.get('pb_ratio')
                margin = fundamentals.get('profit_margin')
                
                if eps is not None:
                    if eps > 0:
                        st.success(f"✅ EPS Positif ({eps:.2f}): Profitable")
                    else:
                        st.error(f"❌ EPS Negatif ({eps:.2f}): Rugi")
                
                if pe is not None and pe > 0:
                    if pe < 15:
                        st.success(f"✅ PE {pe:.2f}: Undervalued")
                    elif pe < 25:
                        st.info(f"ℹ️ PE {pe:.2f}: Wajar")
                    else:
                        st.warning(f"⚠️ PE {pe:.2f}: Mahal")
                
                if pb is not None and pb > 0:
                    if pb < 1:
                        st.success(f"✅ PB {pb:.2f}: Below book value")
                    elif pb < 3:
                        st.info(f"ℹ️ PB {pb:.2f}: Fair")
                    else:
                        st.warning(f"⚠️ PB {pb:.2f}: Premium")
                
                if margin is not None:
                    margin_pct = margin * 100
                    if margin_pct > 10:
                        st.success(f"✅ Margin {margin_pct:.2f}%: Excellent")
                    elif margin_pct > 5:
                        st.info(f"ℹ️ Margin {margin_pct:.2f}%: Good")
                    else:
                        st.warning(f"⚠️ Margin {margin_pct:.2f}%: Low")
                
                st.info("💡 Fundamental baik + strategi teknikal = kombinasi powerful!")
        else:
            st.warning("⚠️ Data fundamental tidak tersedia untuk saham ini")
        
        st.markdown("---")

    # Run backtest
    if run_button:
        with st.spinner(f"⏳ Menjalankan backtest untuk {symbol}..."):
            try:
                # Calculate date range
                end = datetime.today()
                start = end - timedelta(days=365 * years)
                yf_symbol = normalize_symbol(symbol)
                
                # Fetch historical data
                df = get_history_yf(
                    yf_symbol,
                    start=start.strftime("%Y-%m-%d"),
                    end=end.strftime("%Y-%m-%d")
                )
                
                if df.empty:
                    st.error("❌ Gagal mengambil data historis")
                    st.stop()
                
                # Prepare data
                df = df.rename_axis("date").reset_index()
                df.set_index("date", inplace=True)
                
                # Generate signals
                df_sig = generate_signals(df, rsi_max=rsi_max)
                
                # Run backtest
                trades = backtest_risk_based(
                    df_sig,
                    capital=capital,
                    risk_pct=risk_pct,
                    sl_pct=sl_pct,
                    tp_r_multiple=tp_r_multiple
                )
                
                # Store results
                st.session_state.backtest_results = trades
                st.session_state.backtest_df = df_sig

                # Sync with Journal automatically when trades exist
                if not trades.empty:
                    if log_trades(trades):
                        st.success("✅ Hasil backtest otomatis tersimpan ke Journal")
                    else:
                        st.warning("⚠️ Backtest selesai, tapi gagal simpan ke Journal. Cek format data journal atau file CSV lama.")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    # Display results
    if st.session_state.backtest_results is not None:
        trades = st.session_state.backtest_results
        df_sig = st.session_state.backtest_df
        
        if trades.empty:
            st.warning("⚠️ Tidak ada trade yang terjadi untuk parameter ini.")
            st.info("💡 Coba ubah parameter atau pilih periode yang lebih panjang")
        else:
            # Calculate metrics
            metrics = calculate_backtest_metrics(trades)
            
            # Display metrics
            st.markdown("### 📊 Performa Backtest")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Trades", metrics["total_trades"])
            with col2:
                color = "normal" if metrics["win_rate"] >= 50 else "inverse"
                st.metric("Win Rate", f"{metrics['win_rate']}%")
            with col3:
                st.metric("Avg R-Multiple", f"{metrics['avg_r_multiple']}R")
            with col4:
                pnl_pct = (metrics["total_pnl"] / capital) * 100
                st.metric("Total PnL", f"Rp {metrics['total_pnl']:,.0f}", f"{pnl_pct:+.2f}%")
            with col5:
                st.metric("Max Drawdown", f"{metrics['max_drawdown']}%")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Winning Trades", metrics["winning_trades"])
            with col2:
                st.metric("Losing Trades", metrics["losing_trades"])
            with col3:
                st.metric("Avg Win", f"Rp {metrics['avg_win']:,.0f}")
            with col4:
                st.metric("Profit Factor", f"{metrics['profit_factor']}")
            
            # Equity curve
            st.markdown("### 📈 Equity Curve")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trades["exit_time"],
                y=trades["equity_after"],
                mode='lines+markers',
                name='Equity',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=6)
            ))
            
            # Add starting capital line
            fig.add_hline(
                y=capital,
                line_dash="dash",
                line_color="gray",
                annotation_text="Starting Capital"
            )
            
            fig.update_layout(
                title="Equity Growth Over Time",
                xaxis_title="Date",
                yaxis_title="Equity (Rp)",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Trade distribution
            st.markdown("### 📊 Distribusi R-Multiple")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # R-multiple histogram
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(
                    x=trades["r_multiple"],
                    nbinsx=20,
                    marker_color='#1f77b4',
                    name='R-Multiple'
                ))
                fig_hist.update_layout(
                    title="Distribusi R-Multiple",
                    xaxis_title="R-Multiple",
                    yaxis_title="Frequency",
                    height=300
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Win/Loss pie chart
                fig_pie = go.Figure()
                fig_pie.add_trace(go.Pie(
                    labels=['Winning Trades', 'Losing Trades'],
                    values=[metrics["winning_trades"], metrics["losing_trades"]],
                    marker_colors=['#2ecc71', '#e74c3c'],
                    hole=0.4
                ))
                fig_pie.update_layout(
                    title="Win/Loss Ratio",
                    height=300
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Trade list
            st.markdown("### 📋 Daftar Trade")
            
            # Format trades for display
            trades_display = trades.copy()
            trades_display["entry_time"] = pd.to_datetime(trades_display["entry_time"]).dt.strftime("%Y-%m-%d")
            trades_display["exit_time"] = pd.to_datetime(trades_display["exit_time"]).dt.strftime("%Y-%m-%d")
            
            # Color code based on profit/loss
            def highlight_pnl(row):
                if row["pnl"] > 0:
                    return ['background-color: #d4edda'] * len(row)
                else:
                    return ['background-color: #f8d7da'] * len(row)
            
            st.dataframe(
                trades_display.style.apply(highlight_pnl, axis=1),
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = trades.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Trades CSV",
                data=csv,
                file_name=f"backtest_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
            
            # Price chart with signals
            st.markdown("### 📊 Price Chart dengan Signals")
            
            # Create subplots
            fig_chart = make_subplots(
                rows=2, cols=1,
                row_heights=[0.7, 0.3],
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=('Price & Signals', 'RSI')
            )
            
            # Candlestick
            fig_chart.add_trace(
                go.Candlestick(
                    x=df_sig.index,
                    open=df_sig['open'],
                    high=df_sig['high'],
                    low=df_sig['low'],
                    close=df_sig['close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # EMAs
            fig_chart.add_trace(
                go.Scatter(x=df_sig.index, y=df_sig['ema_fast'],
                          name=f'EMA {Config.DEFAULT_EMA_FAST}',
                          line=dict(color='blue', width=1)),
                row=1, col=1
            )
            fig_chart.add_trace(
                go.Scatter(x=df_sig.index, y=df_sig['ema_slow'],
                          name=f'EMA {Config.DEFAULT_EMA_SLOW}',
                          line=dict(color='red', width=1)),
                row=1, col=1
            )
            
            # Buy signals
            buy_signals = df_sig[df_sig['signal'] == 'BUY']
            fig_chart.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['close'],
                    mode='markers',
                    name='BUY',
                    marker=dict(color='green', size=10, symbol='triangle-up')
                ),
                row=1, col=1
            )
            
            # Sell signals
            sell_signals = df_sig[df_sig['signal'] == 'SELL']
            fig_chart.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['close'],
                    mode='markers',
                    name='SELL',
                    marker=dict(color='red', size=10, symbol='triangle-down')
                ),
                row=1, col=1
            )
            
            # RSI
            fig_chart.add_trace(
                go.Scatter(x=df_sig.index, y=df_sig['rsi'],
                          name='RSI',
                          line=dict(color='purple', width=1)),
                row=2, col=1
            )
            
            # RSI levels
            fig_chart.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig_chart.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            fig_chart.update_layout(
                height=800,
                showlegend=True,
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig_chart, use_container_width=True)
    # Info section
    with st.expander("ℹ️ Cara Menggunakan"):
        st.markdown("""
        ### Langkah-langkah:
        
        1. **Pilih Saham**: Pilih saham dari watchlist di sidebar
        2. **Atur Periode**: Tentukan berapa tahun data historis
        3. **Atur Modal**: Masukkan modal awal untuk simulasi
        4. **Atur Parameter**: Sesuaikan risk %, stop loss, dan take profit
        5. **Jalankan**: Klik tombol "Jalankan Backtest"
        6. **Analisis**: Review hasil dan statistik performa
        
        ### Interpretasi Metrik:
        
        - **Win Rate**: Persentase trade yang profit (target > 50%)
        - **Avg R-Multiple**: Rata-rata profit/loss dalam kelipatan R (target > 1)
        - **Total PnL**: Total profit/loss dalam Rupiah
        - **Max Drawdown**: Penurunan maksimal dari puncak equity (< 20% ideal)
        - **Profit Factor**: Total profit / Total loss (> 1.5 bagus)
        
        ### Tips:
        
        - Strategi bagus: Win Rate > 50%, Avg R > 1, Profit Factor > 1.5
        - Perhatikan drawdown, jangan terlalu besar
        - Test di berbagai periode untuk validasi
        - Bandingkan dengan buy & hold strategy
        """)

# TAB 2: Parameter Optimization
with tab2:
    st.markdown("## 🔍 Parameter Optimization & Sensitivity Analysis")
    st.info("💡 **Grid Search** untuk menemukan kombinasi parameter yang paling robust")
    
    # Optimization settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Optimization Settings")
    
    opt_symbol = st.sidebar.selectbox(
        "Saham untuk Optimasi",
        watchlist,
        key="opt_symbol",
        help="Pilih saham untuk parameter optimization"
    )
    
    opt_years = st.sidebar.slider(
        "Period Optimasi (Tahun)",
        min_value=1,
        max_value=5,
        value=3,
        key="opt_years",
        help="Durasi data untuk optimization"
    )
    
    opt_capital = st.sidebar.number_input(
        "Modal untuk Optimasi",
        min_value=1_000,
        value=int(Config.DEFAULT_CAPITAL),
        step=1_000,
        key="opt_capital"
    )
    
    st.sidebar.markdown("### 📊 Parameter Ranges")
    
    # Define parameter ranges
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown("**SL % Range:**")
        sl_range = st.multiselect(
            "Stop Loss",
            [1.0, 1.5, 2.0, 2.5, 3.0],
            default=[1.5, 2.0, 2.5],
            key="sl_range"
        )
    
    with col2:
        st.markdown("**TP R Range:**")
        tp_range = st.multiselect(
            "Take Profit",
            [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
            default=[2.0, 2.5, 3.0],
            key="tp_range"
        )
    
    rsi_range = st.sidebar.multiselect(
        "RSI Max Range",
        [60.0, 65.0, 70.0, 75.0, 80.0],
        default=[65.0, 70.0, 75.0],
        key="rsi_range"
    )
    
    # Fundamental Filter for Optimization
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Filter Fundamental")
    
    enable_opt_fundamental = st.sidebar.checkbox(
        "Cek Fundamental Saham",
        value=False,
        key="opt_fundamental",
        help="Tampilkan analisa fundamental sebelum optimization"
    )
    
    # Run optimization button
    if st.button("🚀 Run Parameter Optimization", type="primary", use_container_width=True):
        if not sl_range or not tp_range or not rsi_range:
            st.error("❌ Pilih minimal 1 nilai untuk setiap parameter!")
            st.stop()
        
        # Show fundamental analysis if enabled
        if enable_opt_fundamental:
            st.markdown("### 📊 Analisa Fundamental")
            
            yf_symbol = normalize_symbol(opt_symbol)
            fundamentals = get_fundamental_data(yf_symbol)
            
            if fundamentals:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    quality = get_fundamental_summary(fundamentals)
                    st.info(f"**Kualitas:**\n\n{quality}")
                    
                    df_fund = format_fundamental_display(fundamentals)
                    st.dataframe(df_fund, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("#### 💡 Interpretasi")
                    
                    eps = fundamentals.get('eps')
                    if eps is not None:
                        if eps > 0:
                            st.success(f"✅ EPS Positif: {eps:.2f}")
                        else:
                            st.error(f"❌ EPS Negatif: {eps:.2f}")
                    
                    pe = fundamentals.get('pe_ratio')
                    if pe and pe > 0:
                        if pe < 25:
                            st.success(f"✅ PE {pe:.2f}: Valuasi baik")
                        else:
                            st.warning(f"⚠️ PE {pe:.2f}: Valuasi tinggi")
                    
                    st.info("💡 Fundamental baik meningkatkan confidence hasil backtest!")
            else:
                st.warning("⚠️ Data fundamental tidak tersedia")
            
            st.markdown("---")
        
        total_combinations = len(sl_range) * len(tp_range) * len(rsi_range)
        
        st.info(f"📊 Testing **{total_combinations}** kombinasi parameter...")
        
        with st.spinner("⏳ Running optimization... This may take a while"):
            try:
                # Fetch data
                end = datetime.today()
                start = end - timedelta(days=365 * opt_years)
                yf_symbol = normalize_symbol(opt_symbol)
                
                df = get_history_yf(
                    yf_symbol,
                    start=start.strftime("%Y-%m-%d"),
                    end=end.strftime("%Y-%m-%d")
                )
                
                if df.empty:
                    st.error("❌ Gagal mengambil data")
                    st.stop()
                
                # Prepare data
                df = df.rename_axis("date").reset_index()
                df.set_index("date", inplace=True)
                
                # Grid search
                results_list = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                param_combinations = list(product(sl_range, tp_range, rsi_range))
                
                for idx, (sl, tp, rsi) in enumerate(param_combinations):
                    status_text.text(f"Testing {idx+1}/{total_combinations}: SL={sl}%, TP={tp}R, RSI={rsi}")
                    progress_bar.progress((idx + 1) / total_combinations)
                    
                    try:
                        # Generate signals
                        df_sig = generate_signals(df, rsi_max=rsi)
                        
                        # Run backtest
                        trades = backtest_risk_based(
                            df_sig,
                            capital=opt_capital,
                            risk_pct=Config.DEFAULT_RISK_PER_TRADE,
                            sl_pct=sl/100,
                            tp_r_multiple=tp
                        )
                        
                        if trades.empty:
                            continue
                        
                        # Calculate metrics
                        metrics = calculate_backtest_metrics(trades)
                        
                        # Calculate CAGR
                        days_diff = (trades['exit_time'].max() - trades['entry_time'].min()).days
                        years_traded = days_diff / 365.25
                        final_equity = trades['equity_after'].iloc[-1]
                        cagr = ((final_equity / opt_capital) ** (1 / years_traded) - 1) * 100 if years_traded > 0 else 0
                        
                        results_list.append({
                            'SL (%)': sl,
                            'TP (R)': tp,
                            'RSI Max': rsi,
                            'Total Trades': metrics['total_trades'],
                            'Win Rate (%)': metrics['win_rate'],
                            'Avg R': metrics['avg_r_multiple'],
                            'Profit Factor': metrics['profit_factor'],
                            'CAGR (%)': round(cagr, 2),
                            'Max DD (%)': metrics['max_drawdown'],
                            'Total PnL': metrics['total_pnl'],
                            'Final Equity': final_equity
                        })
                    
                    except Exception as e:
                        continue
                
                progress_bar.empty()
                status_text.empty()
                
                if not results_list:
                    st.error("❌ Tidak ada hasil valid dari optimization")
                    st.stop()
                
                # Convert to DataFrame
                df_results = pd.DataFrame(results_list)
                
                # Store in session state
                st.session_state.optimization_results = df_results
                
                st.success(f"✅ Optimization selesai! {len(df_results)} kombinasi valid")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # Display optimization results
    if st.session_state.optimization_results is not None:
        df_opt = st.session_state.optimization_results
        
        st.markdown("### 📊 Optimization Results")
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Combinations", len(df_opt))
        with col2:
            st.metric("Best CAGR", f"{df_opt['CAGR (%)'].max():.2f}%")
        with col3:
            st.metric("Best Profit Factor", f"{df_opt['Profit Factor'].max():.2f}")
        with col4:
            st.metric("Best Win Rate", f"{df_opt['Win Rate (%)'].max():.1f}%")
        
        # Top 10 Parameter Sets
        st.markdown("### 🏆 Top 10 Parameter Sets")
        
        # Sorting options
        sort_col1, sort_col2 = st.columns([3, 1])
        with sort_col1:
            sort_by = st.selectbox(
                "Sort By",
                ['CAGR (%)', 'Profit Factor', 'Win Rate (%)', 'Avg R', 'Total PnL'],
                index=0
            )
        with sort_col2:
            ascending = st.checkbox("Ascending", value=False)
        
        df_top10 = df_opt.sort_values(by=sort_by, ascending=ascending).head(10).reset_index(drop=True)
        
        # Display as styled table
        def highlight_top3(row):
            if row.name == 0:
                return ['background-color: #FFD700'] * len(row)  # Gold
            elif row.name == 1:
                return ['background-color: #C0C0C0'] * len(row)  # Silver
            elif row.name == 2:
                return ['background-color: #CD7F32'] * len(row)  # Bronze
            else:
                return [''] * len(row)
        
        st.dataframe(
            df_top10.style.apply(highlight_top3, axis=1).format({
                'SL (%)': '{:.1f}',
                'TP (R)': '{:.1f}',
                'RSI Max': '{:.0f}',
                'Win Rate (%)': '{:.1f}',
                'Avg R': '{:.2f}',
                'Profit Factor': '{:.2f}',
                'CAGR (%)': '{:.2f}',
                'Max DD (%)': '{:.2f}',
                'Total PnL': 'Rp {:,.0f}',
                'Final Equity': 'Rp {:,.0f}'
            }),
            use_container_width=True,
            height=400
        )
        
        st.caption("🥇 Gold = #1, 🥈 Silver = #2, 🥉 Bronze = #3")
        
        # Sensitivity Analysis - Heatmaps
        st.markdown("### 🌡️ Sensitivity Analysis - Heatmaps")
        
        tab_heat1, tab_heat2, tab_heat3 = st.tabs(["Profit Factor", "CAGR", "Win Rate"])
        
        with tab_heat1:
            # Profit Factor Heatmap
            pivot_pf = df_opt.pivot_table(
                values='Profit Factor',
                index='SL (%)',
                columns='TP (R)',
                aggfunc='mean'
            )
            
            fig_pf = go.Figure(data=go.Heatmap(
                z=pivot_pf.values,
                x=pivot_pf.columns,
                y=pivot_pf.index,
                colorscale='RdYlGn',
                text=np.round(pivot_pf.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Profit<br>Factor")
            ))
            
            fig_pf.update_layout(
                title="Profit Factor by SL% vs TP(R)",
                xaxis_title="Take Profit (R-Multiple)",
                yaxis_title="Stop Loss (%)",
                height=400
            )
            
            st.plotly_chart(fig_pf, use_container_width=True)
            
            st.info("💡 **Hijau** = lebih baik. Cari area hijau yang luas untuk robustness!")
        
        with tab_heat2:
            # CAGR Heatmap
            pivot_cagr = df_opt.pivot_table(
                values='CAGR (%)',
                index='SL (%)',
                columns='TP (R)',
                aggfunc='mean'
            )
            
            fig_cagr = go.Figure(data=go.Heatmap(
                z=pivot_cagr.values,
                x=pivot_cagr.columns,
                y=pivot_cagr.index,
                colorscale='RdYlGn',
                text=np.round(pivot_cagr.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="CAGR<br>(%)")
            ))
            
            fig_cagr.update_layout(
                title="CAGR (%) by SL% vs TP(R)",
                xaxis_title="Take Profit (R-Multiple)",
                yaxis_title="Stop Loss (%)",
                height=400
            )
            
            st.plotly_chart(fig_cagr, use_container_width=True)
            
            st.info("💡 CAGR = Compound Annual Growth Rate (return tahunan)")
        
        with tab_heat3:
            # Win Rate Heatmap
            pivot_wr = df_opt.pivot_table(
                values='Win Rate (%)',
                index='SL (%)',
                columns='TP (R)',
                aggfunc='mean'
            )
            
            fig_wr = go.Figure(data=go.Heatmap(
                z=pivot_wr.values,
                x=pivot_wr.columns,
                y=pivot_wr.index,
                colorscale='RdYlGn',
                text=np.round(pivot_wr.values, 1),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Win Rate<br>(%)")
            ))
            
            fig_wr.update_layout(
                title="Win Rate (%) by SL% vs TP(R)",
                xaxis_title="Take Profit (R-Multiple)",
                yaxis_title="Stop Loss (%)",
                height=400
            )
            
            st.plotly_chart(fig_wr, use_container_width=True)
            
            st.info("💡 Win Rate tinggi tidak selalu terbaik, perhatikan Profit Factor juga!")
        
        # Parameter Robustness Analysis
        st.markdown("### 🎯 Parameter Robustness Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Stats by SL%
            st.markdown("**Performance by Stop Loss %**")
            stats_sl = df_opt.groupby('SL (%)').agg({
                'CAGR (%)': 'mean',
                'Profit Factor': 'mean',
                'Win Rate (%)': 'mean',
                'Max DD (%)': 'mean'
            }).round(2)
            
            st.dataframe(stats_sl, use_container_width=True)
            
            # Best SL range
            best_sl = stats_sl['Profit Factor'].idxmax()
            st.success(f"📊 Most robust SL: **{best_sl}%**")
        
        with col2:
            # Stats by TP(R)
            st.markdown("**Performance by Take Profit (R)**")
            stats_tp = df_opt.groupby('TP (R)').agg({
                'CAGR (%)': 'mean',
                'Profit Factor': 'mean',
                'Win Rate (%)': 'mean',
                'Max DD (%)': 'mean'
            }).round(2)
            
            st.dataframe(stats_tp, use_container_width=True)
            
            # Best TP range
            best_tp = stats_tp['Profit Factor'].idxmax()
            st.success(f"📊 Most robust TP: **{best_tp}R**")
        
        # Download optimization results
        csv_opt = df_opt.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Optimization Results CSV",
            data=csv_opt,
            file_name=f"optimization_{opt_symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        # Find robust parameters (consistent performance)
        std_metrics = df_opt.groupby(['SL (%)', 'TP (R)']).agg({
            'Profit Factor': ['mean', 'std'],
            'CAGR (%)': ['mean', 'std']
        })
        
        std_metrics.columns = ['_'.join(col) for col in std_metrics.columns]
        std_metrics['Consistency Score'] = (
            std_metrics['Profit Factor_mean'] / (std_metrics['Profit Factor_std'] + 0.01)
        )
        
        best_robust = std_metrics.sort_values('Consistency Score', ascending=False).head(3)
        
        st.info("""
        **🎯 Fokus pada Robustness, bukan hanya best result:**
        
        - Parameter yang baik di banyak kondisi lebih aman
        - Cari area "hijau" yang luas di heatmap (bukan 1 titik)
        - Konsistensi lebih penting dari peak performance
        - Hindari parameter yang sangat sensitif (performa drop drastis saat diubah sedikit)
        """)
        
        st.markdown("**Top 3 Most Robust Parameter Combinations:**")
        st.dataframe(
            best_robust.reset_index()[['SL (%)', 'TP (R)', 'Profit Factor_mean', 'Consistency Score']].round(2),
            use_container_width=True
        )

# Info section
with st.expander("ℹ️ Parameter Optimization Guide"):
    st.markdown("""
    ### 🔍 Cara Menggunakan Parameter Optimization:
    
    **1. Setup:**
    - Pilih saham dan periode (minimal 2-3 tahun recommended)
    - Pilih range parameter yang ingin ditest (SL%, TP R-multiple, RSI max)
    - Semakin banyak kombinasi, semakin lama prosesnya
    
    **2. Interpretasi Hasil:**
    - **Top 10 Table**: Kombinasi parameter terbaik berdasarkan metrik pilihan
    - **Heatmaps**: Visualisasi sensitivity - cari area hijau yang luas!
    - **Robustness Analysis**: Parameter yang konsisten di berbagai kondisi
    
    **3. Memilih Parameter:**
    - ❌ **JANGAN**: Pilih parameter dengan 1 nilai peak tapi sangat sensitif
    - ✅ **LAKUKAN**: Pilih dari area "hijau" yang luas di heatmap
    - ✅ **LAKUKAN**: Cek consistency score tinggi
    - ✅ **LAKUKAN**: Validasi dengan data out-of-sample
    
    **4. Tips Penting:**
    - CAGR tinggi tidak selalu terbaik jika Max DD juga tinggi
    - Profit Factor > 1.5 lebih reliable daripada Win Rate > 70%
    - Parameter yang robust di periode 3-5 tahun lebih dipercaya
    - Selalu test parameter hasil optimization di data baru (forward test)
    
    **5. Menghindari Overfitting:**
    - Jangan terlalu banyak kombinasi (fokus pada range reasonable)
    - Perhatikan trade frequency (minimal 30-50 trades)
    - Parameter yang "terlalu perfect" biasanya overfit
    - Test di multiple stocks untuk validasi
    """)

