import pandas as pd
from risk import position_size, calc_r_multiple

def backtest_risk_based(
    df: pd.DataFrame,
    capital: float = 100_000_000,
    risk_pct: float = 0.015,   # 1.5% modal per trade
    sl_pct: float = 0.02,      # stop loss 2% di bawah entry
    tp_r_multiple: float = 2.0 # take profit 2R
) -> pd.DataFrame:
    """
    Backtest berbasis R:
    - Entry ketika sinyal BUY
    - Stop loss = entry * (1 - sl_pct)
    - Take profit = entry + (entry - SL) * tp_r_multiple
    - Position size ditentukan oleh risk_pct
    - Exit saat SL/TP tersentuh (cek high/low bar berikutnya)
    """

    trades = []
    in_position = False
    equity = capital

    df_bt = df.copy()

    for i in range(len(df_bt) - 1):
        row = df_bt.iloc[i]
        next_row = df_bt.iloc[i + 1]

        # Entry
        if (not in_position) and (row["signal"] == "BUY"):
            entry_price = row["close"]
            sl_price = entry_price * (1 - sl_pct)
            # 1R jaraknya:
            one_r = entry_price - sl_price
            tp_price = entry_price + one_r * tp_r_multiple

            size = position_size(
                capital=equity,
                entry=entry_price,
                stop=sl_price,
                risk_pct=risk_pct
            )
            if size == 0:
                continue

            in_position = True
            entry_index = row.name

        elif in_position:
            # cek apakah di candle berikutnya SL/TP kena
            low_next = next_row["low"]
            high_next = next_row["high"]

            exit_price = None
            exit_reason = None

            # asumsikan kalau 1 candle kena SL & TP sekaligus, SL dulu.[web:51]
            if low_next <= sl_price:
                exit_price = sl_price
                exit_reason = "SL"
            elif high_next >= tp_price:
                exit_price = tp_price
                exit_reason = "TP"

            if exit_price is not None:
                pnl = (exit_price - entry_price) * size
                r_mult = calc_r_multiple(entry_price, sl_price, exit_price)
                equity += pnl

                trades.append({
                    "entry_time": entry_index,
                    "exit_time": next_row.name,
                    "entry": entry_price,
                    "exit": exit_price,
                    "size": size,
                    "sl": sl_price,
                    "tp": tp_price,
                    "reason": exit_reason,
                    "pnl": pnl,
                    "r_multiple": r_mult,
                    "equity_after": equity,
                })

                in_position = False

    trades_df = pd.DataFrame(trades)
    return trades_df
