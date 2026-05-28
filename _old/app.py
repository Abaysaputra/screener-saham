import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from data import (
    get_history_yf,
    get_daily_history_for_scan,
    normalize_symbol,
)
from strategy import generate_signals
from backtest import backtest_risk_based
from journal import compute_stats
from risk import position_size
from config import DEFAULT_RISK_PER_TRADE
from cli import load_watchlist  # fungsi yang sudah ada di cli.py

st.set_page_config(
    page_title="Swing Trader IDX",
    layout="wide",
)

st.title("Swing Trading Assistant - IDX")

# Sidebar
st.sidebar.header("Pengaturan Umum")
capital = st.sidebar.number_input(
    "Modal (Rp)",
    min_value=1_000_000,
    value=100_000_000,
    step=1_000_000,
)
mode = st.sidebar.radio("Mode", ["Scan Harian", "Backtest"])

watchlist = load_watchlist()
if not watchlist:
    st.sidebar.warning("watchlist.txt kosong atau tidak ditemukan.")
else:
    st.sidebar.write("Watchlist:", ", ".join(watchlist))

if mode == "Scan Harian":
    st.header("Scan Sinyal BUY (3 hari terakhir)")
    lookback_signals = st.sidebar.slider(
        "Jumlah hari terakhir untuk mencari sinyal",
        min_value=1,
        max_value=5,
        value=3,
    )

    if st.button("Jalankan Scan"):
        results = []
        for sym in watchlist:
            df = get_daily_history_for_scan(sym)
            if df.empty or len(df) < lookback_signals + 1:
                continue

            df_sig = generate_signals(df)
            recent = df_sig.tail(lookback_signals)
            buys = recent[recent["signal"] == "BUY"]

            if buys.empty:
                continue

            last_buy = buys.iloc[-1]
            entry_price = float(last_buy["close"])
            sl_price = entry_price * 0.98
            size = position_size(
                capital=capital,
                entry=entry_price,
                stop=sl_price,
                risk_pct=DEFAULT_RISK_PER_TRADE,
            )
            if size == 0:
                continue

            results.append({
                "Symbol": sym,
                "Signal Date": last_buy.name.date(),
                "Entry (Close)": round(entry_price, 2),
                "Stop Loss": round(sl_price, 2),
                "Size (shares)": int(size),
            })

        if not results:
            st.info("Tidak ada sinyal BUY dalam periode tersebut di watchlist.")
        else:
            df_res = pd.DataFrame(results)
            st.subheader("Hasil Scan")
            st.dataframe(df_res, use_container_width=True)

else:
    st.header("Backtest EMA Swing")
    symbol = st.selectbox("Pilih saham untuk backtest", watchlist)
    years = st.slider("Tahun historis", min_value=1, max_value=5, value=3)

    if st.button("Jalankan Backtest"):
        end = datetime.today()
        start = end - timedelta(days=365 * years)
        yf_symbol = normalize_symbol(symbol)

        df = get_history_yf(
            yf_symbol,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
        )
        if df.empty:
            st.error("Data historis kosong.")
        else:
            df = df.rename_axis("date").reset_index()
            df.set_index("date", inplace=True)

            df_sig = generate_signals(df)
            trades = backtest_risk_based(df_sig, capital=capital)

            if trades.empty:
                st.info("Tidak ada trade yang terjadi untuk parameter ini.")
            else:
                st.subheader("Daftar Trade")
                st.dataframe(trades, use_container_width=True)

                st.subheader("Statistik")
                stats = compute_stats()
                st.json(stats)
