# cli.py
import argparse
from datetime import datetime, timedelta

from data import get_history_yf, normalize_symbol
from strategy import generate_signals
from backtest import backtest_risk_based
from journal import log_trades, compute_stats

from pathlib import Path
from risk import position_size
from config import DEFAULT_RISK_PER_TRADE

from data import get_daily_history_for_scan
from strategy import generate_signals

WATCHLIST_PATH = Path("watchlist.txt")
def load_watchlist():
    if not WATCHLIST_PATH.exists():
        print("watchlist.txt tidak ditemukan.")
        return []
    with WATCHLIST_PATH.open() as f:
        symbols = [line.strip().upper() for line in f if line.strip()]
    return symbols

def scan_today(capital: float = 100_000_000, lookback_signals: int = 3):
    symbols = load_watchlist()
    if not symbols:
        print("Watchlist kosong.")
        return

    results = []

    for sym in symbols:
        df = get_daily_history_for_scan(sym)
        if df.empty or len(df) < lookback_signals + 1:
            continue

        df_sig = generate_signals(df)

        # ambil N candle terakhir
        recent = df_sig.tail(lookback_signals)
        # cek apakah ada BUY di periode ini
        buys = recent[recent["signal"] == "BUY"]

        if buys.empty:
            print(sym, "=> tidak ada BUY di", lookback_signals, "hari terakhir")
            continue

        # pakai sinyal BUY terakhir sebagai referensi
        last_buy = buys.iloc[-1]
        entry_price = float(last_buy["close"])
        sl_price = entry_price * 0.98  # SL 2% di bawah entry (bisa kamu ganti)
        size = position_size(
            capital=capital,
            entry=entry_price,
            stop=sl_price,
            risk_pct=DEFAULT_RISK_PER_TRADE,
        )
        if size == 0:
            continue

        results.append({
            "symbol": sym,
            "entry": entry_price,
            "sl": sl_price,
            "size": size,
            "signal_date": last_buy.name,
        })

    if not results:
        print("Tidak ada sinyal BUY dalam", lookback_signals, "hari terakhir.")
        return

    print(f"Sinyal BUY dalam {lookback_signals} hari terakhir:")
    for r in results:
        print(
            f"{r['symbol']} (tgl {r['signal_date'].date()}): "
            f"entry ~ {r['entry']:.2f}, SL {r['sl']:.2f}, size {r['size']} saham"
        )

    symbols = load_watchlist()
    if not symbols:
        print("Watchlist kosong.")
        return

    results = []

    for sym in symbols:
        df = get_daily_history_for_scan(sym)
        if df.empty:
            continue
        df_sig = generate_signals(df)
        recent = df_sig.tail(3)
        prev_row = df_sig.iloc[-2]

        # kita hanya anggap sinyal valid jika candle terakhir = BUY
        if "BUY" in recent["signal"].values:
            last_row = recent.iloc[-1]
            entry_price = last_row["close"]
            # SL pakai 2% di bawah harga close
            sl_price = entry_price * 0.98
            size = position_size(
                capital=capital,
                entry=entry_price,
                stop=sl_price,
                risk_pct=DEFAULT_RISK_PER_TRADE
            )
            if size == 0:
                continue
            results.append({
                "symbol": sym,
                "entry": entry_price,
                "sl": sl_price,
                "size": size
            })

    if not results:
        print("Tidak ada sinyal BUY pada watchlist hari ini.")
        return

    print("Sinyal BUY hari ini:")
    for r in results:
        print(
            f"{r['symbol']}: entry ~ {r['entry']:.2f}, "
            f"SL {r['sl']:.2f}, size {r['size']} saham"
        )

def run_backtest(symbol: str, years: int = 2):
    end = datetime.today()
    start = end - timedelta(days=365 * years)
    yf_symbol = normalize_symbol(symbol)

    df = get_history_yf(
        yf_symbol,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d")
    )
    df = df.rename_axis("date").reset_index()
    df.set_index("date", inplace=True)

    df_sig = generate_signals(df)
    trades = backtest_risk_based(df_sig)

    if trades.empty:
        print("Tidak ada trade yang terjadi untuk parameter ini.")
        return

    log_trades(trades)

    print(trades.tail())
    stats = compute_stats()
    print("Stats:", stats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", help="Kode saham untuk backtest, misal BBCA")
    parser.add_argument("--years", type=int, default=2)
    parser.add_argument("--mode", choices=["backtest", "scan"], default="backtest")
    parser.add_argument("--capital", type=float, default=100_000_000)

    args = parser.parse_args()

    if args.mode == "backtest":
        if not args.symbol:
            parser.error("--symbol wajib untuk mode backtest")
        run_backtest(args.symbol, args.years)
    else:
        scan_today(capital=args.capital)

