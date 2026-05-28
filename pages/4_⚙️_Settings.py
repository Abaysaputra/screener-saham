"""
Settings Page
"""
import streamlit as st
from pathlib import Path

from core.config import Config
from core.data import load_watchlist
from utils.theme import apply_app_theme

st.set_page_config(
    page_title="Settings - Swing Trader",
    page_icon="⚙️",
    layout="wide"
)

apply_app_theme()

st.title("⚙️ Settings & Configuration")

# Tabs for different settings
tab1, tab2, tab3, tab4 = st.tabs(["📋 Watchlist", "🎯 Trading Parameters", "🔑 API Keys", "ℹ️ About"])

# Tab 1: Watchlist Management
with tab1:
    st.header("📋 Watchlist Management")
    
    # Load current watchlist
    watchlist = load_watchlist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Current Watchlist")
        
        if watchlist:
            st.success(f"✅ {len(watchlist)} saham di watchlist")
            
            # Display as editable text area
            watchlist_text = "\n".join(watchlist)
            edited_watchlist = st.text_area(
                "Edit Watchlist (satu simbol per baris)",
                value=watchlist_text,
                height=300,
                help="Masukkan kode saham IDX tanpa .JK (contoh: BBCA, BBRI, TLKM)"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("💾 Simpan Watchlist", type="primary", use_container_width=True):
                    try:
                        # Parse and validate
                        new_symbols = [s.strip().upper() for s in edited_watchlist.split("\n") if s.strip()]
                        
                        # Save to file
                        with Config.WATCHLIST_PATH.open("w") as f:
                            f.write("\n".join(new_symbols))
                        
                        st.success(f"✅ Watchlist berhasil disimpan! ({len(new_symbols)} saham)")
                        st.cache_data.clear()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with col_btn2:
                if st.button("🔄 Reset", use_container_width=True):
                    st.rerun()
        else:
            st.warning("⚠️ Watchlist kosong")
            st.info("Tambahkan kode saham di kolom sebelah kanan →")
    
    with col2:
        st.markdown("### Quick Add")
        
        # Popular stocks
        st.markdown("**Popular IDX Stocks:**")
        popular_stocks = [
            "BBCA", "BBRI", "BMRI", "TLKM", "ASII",
            "UNVR", "ICBP", "INDF", "KLBF", "ACES",
            "GOTO", "BUKA", "EMTK", "ANTM", "ADRO"
        ]
        
        selected_stocks = []
        for stock in popular_stocks:
            if st.checkbox(stock, value=(stock in watchlist), key=f"pop_{stock}"):
                selected_stocks.append(stock)
        
        if st.button("➕ Add Selected to Watchlist", use_container_width=True):
            try:
                current = set(watchlist)
                current.update(selected_stocks)
                
                with Config.WATCHLIST_PATH.open("w") as f:
                    f.write("\n".join(sorted(current)))
                
                st.success(f"✅ Added {len(selected_stocks)} stocks!")
                st.cache_data.clear()
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        
        # Manual add
        st.markdown("**Manual Add:**")
        new_symbol = st.text_input("Kode Saham", placeholder="BBCA", key="manual_add").upper()
        
        if st.button("➕ Add to Watchlist", use_container_width=True):
            if new_symbol:
                try:
                    current = set(watchlist)
                    current.add(new_symbol)
                    
                    with Config.WATCHLIST_PATH.open("w") as f:
                        f.write("\n".join(sorted(current)))
                    
                    st.success(f"✅ {new_symbol} added!")
                    st.cache_data.clear()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Masukkan kode saham!")

# Tab 2: Trading Parameters
with tab2:
    st.header("🎯 Trading Parameters")
    
    st.info("⚠️ Parameter ini adalah default untuk aplikasi. Anda bisa override saat menjalankan scan atau backtest.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Risk Management")
        
        st.markdown(f"**Current Settings:**")
        st.write(f"- Default Risk per Trade: **{Config.DEFAULT_RISK_PER_TRADE * 100}%**")
        st.write(f"- Default Stop Loss: **{Config.DEFAULT_SL_PCT * 100}%**")
        st.write(f"- Default Take Profit: **{Config.DEFAULT_TP_R_MULTIPLE}R**")
        st.write(f"- Lot Size: **{Config.LOT_SIZE}** shares")
        
        st.markdown("---")
        
        new_risk = st.slider(
            "Risk per Trade (%)",
            min_value=0.5,
            max_value=5.0,
            value=Config.DEFAULT_RISK_PER_TRADE * 100,
            step=0.5,
            help="Persentase modal yang dirisiko per trade"
        )
        
        new_sl = st.slider(
            "Stop Loss (%)",
            min_value=1.0,
            max_value=5.0,
            value=Config.DEFAULT_SL_PCT * 100,
            step=0.5,
            help="Stop loss dari entry price"
        )
        
        new_tp = st.slider(
            "Take Profit (R-Multiple)",
            min_value=1.0,
            max_value=5.0,
            value=Config.DEFAULT_TP_R_MULTIPLE,
            step=0.5,
            help="Target profit dalam kelipatan R"
        )
        
        st.info("💡 Untuk mengubah parameter default, edit file `.env` atau `core/config.py`")
    
    with col2:
        st.markdown("### Technical Indicators")
        
        st.markdown(f"**Current Settings:**")
        st.write(f"- EMA Fast: **{Config.DEFAULT_EMA_FAST}** periods")
        st.write(f"- EMA Slow: **{Config.DEFAULT_EMA_SLOW}** periods")
        st.write(f"- RSI Period: **{Config.DEFAULT_RSI_PERIOD}** periods")
        
        st.markdown("---")
        
        new_ema_fast = st.number_input(
            "EMA Fast Period",
            min_value=5,
            max_value=50,
            value=Config.DEFAULT_EMA_FAST,
            step=1
        )
        
        new_ema_slow = st.number_input(
            "EMA Slow Period",
            min_value=20,
            max_value=200,
            value=Config.DEFAULT_EMA_SLOW,
            step=10
        )
        
        new_rsi = st.number_input(
            "RSI Period",
            min_value=7,
            max_value=28,
            value=Config.DEFAULT_RSI_PERIOD,
            step=1
        )
        
        st.info("💡 Untuk mengubah parameter default, edit file `.env` atau `core/config.py`")
    
    st.markdown("---")
    
    st.markdown("### Capital Settings")
    
    st.write(f"**Default Capital:** Rp {Config.DEFAULT_CAPITAL:,.0f}")
    
    new_capital = st.number_input(
        "Default Capital (Rp)",
        min_value=1_000_000,
        value=int(Config.DEFAULT_CAPITAL),
        step=1_000_000,
        help="Modal default untuk scan dan backtest"
    )
    
    st.info("💡 Untuk mengubah modal default, edit file `.env` atau `core/config.py`")

# Tab 3: Data Source Configuration
with tab3:
    st.header("📊 Data Source Configuration")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📡 Status Koneksi")
        
        st.info(f"**Data Source**: {Config.DATA_SOURCE}")
        st.info(f"**IDX Suffix**: {Config.YF_SUFFIX}")
        
        st.markdown("---")
        
        st.markdown("### 🧪 Test Koneksi Data")
        
        st.markdown("""
        Klik tombol di bawah untuk test koneksi ke Yahoo Finance:
        """)
        
        # Test data connection
        test_symbol = st.text_input("Test Symbol", value="BBCA", help="Masukkan kode saham untuk test")
        
        if st.button("🧪 Test Data Connection", type="primary"):
            with st.spinner(f"Testing connection for {test_symbol}..."):
                try:
                    from core.data import get_realtime_price
                    result = get_realtime_price(test_symbol)
                    if result:
                        st.success(f"✅ Yahoo Finance connection successful for {test_symbol}!")
                        
                        # Display data in nice format
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Price", f"Rp {result['price']:,.2f}")
                        with col_b:
                            st.metric("Change", f"Rp {result['change']:,.2f}")
                        with col_c:
                            st.metric("Change %", f"{result['change_percent']:.2f}%")
                        
                        with st.expander("📊 Full Data"):
                            st.json(result)
                    else:
                        st.error("❌ Connection failed - Check internet connection or symbol")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("""💡 Pastikan:
- Internet connection aktif
- Symbol benar (contoh: BBCA, TLKM)
- Library yfinance ter-install""")
    
    with col2:
        st.markdown("### 📚 Resources")
        
        st.markdown("""
        **yfinance Documentation:**
        - [GitHub Repository](https://github.com/ranaroussi/yfinance)
        - [PyPI Page](https://pypi.org/project/yfinance/)
        - [Yahoo Finance](https://finance.yahoo.com)
        
        **IDX Stocks:**
        - [IDX Website](https://www.idx.co.id)
        - Format: SYMBOL.JK (e.g., BBCA.JK)
        """)
        
        st.markdown("---")
        
        st.markdown("### 📁 File Locations")
        st.markdown(f"""
        - **Watchlist**: `{Config.WATCHLIST_PATH}`
        - **Journal**: `{Config.JOURNAL_PATH}`
        - **Config**: `core/config.py`
        
        **Note**: File `.env` opsional untuk custom config
        """)

# Tab 4: About
with tab4:
    st.header("ℹ️ About Swing Trader IDX")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Swing Trading Assistant for Indonesia Stock Exchange
        
        Aplikasi ini dirancang untuk membantu trader Indonesia dalam melakukan analisis teknikal
        dan manajemen risiko untuk swing trading di Bursa Efek Indonesia (IDX).
        
        #### 🎯 Fitur Utama:
        
        - **Scan Harian**: Deteksi sinyal BUY otomatis dari watchlist
        - **Backtest**: Uji strategi pada data historis
        - **Trading Journal**: Tracking dan analisis performa
        - **Risk Management**: Kalkulasi position size berbasis risiko
        - **Technical Analysis**: EMA crossover dan RSI
        
        #### 📊 Strategi Trading:
        
        **Entry Signal:**
        - EMA Fast (20) cross above EMA Slow (50)
        - RSI < 70 (tidak overbought)
        
        **Exit Signal:**
        - Stop Loss: 2% di bawah entry (risk management)
        - Take Profit: 2R (2x risiko untuk reward)
        - Sell Signal: EMA Fast cross below EMA Slow
        
        #### ⚠️ Disclaimer:
        
        Aplikasi ini untuk tujuan **edukasi dan research** saja.
        Trading saham mengandung risiko. Selalu lakukan riset sendiri dan
        gunakan modal yang siap Anda rugikan.
        
        **Tidak ada jaminan profit!**
        
        ---
        
        #### 🛠️ Tech Stack:
        
        - **Framework**: Streamlit
        - **Data Source**: Yahoo Finance (yfinance) - 100% Gratis!
        - **Libraries**: pandas, plotly, yfinance, ta
        - **Language**: Python 3.8+
        
        ---
        
        #### 📝 Version:
        
        - **Version**: 2.0.0 (100% yfinance)
        - **Last Update**: 17 January 2026
        - **Data Source**: Yahoo Finance - Free & No API Key!
        - **Author**: Swing Trader Team
        """)
    
    with col2:
        st.markdown("### 📚 Resources")
        
        st.info("""
        **Documentation**
        - User Guide
        - API Reference
        - Strategy Guide
        """)
        
        st.success("""
        **Support**
        - GitHub Issues
        - Email Support
        - Community Forum
        """)
        
        st.warning("""
        **Legal**
        - Terms of Service
        - Privacy Policy
        - Risk Disclaimer
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔗 Links")
        st.markdown("""
        - [GitHub](https://github.com)
        - [Documentation](https://docs.example.com)
        - [Report Bug](https://github.com/issues)
        """)
        
        st.markdown("---")
        
        st.markdown("### 💖 Support")
        st.markdown("""
        Jika aplikasi ini bermanfaat, consider:
        - ⭐ Star di GitHub
        - 🐛 Report bugs
        - 💡 Suggest features
        - 📣 Share dengan trader lain
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>© 2026 Swing Trader IDX | Made with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)
