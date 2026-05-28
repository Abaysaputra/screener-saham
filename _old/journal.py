import pandas as pd
from pathlib import Path

JOURNAL_PATH = Path("trades_journal.csv")

def log_trades(trades_df: pd.DataFrame):
    if JOURNAL_PATH.exists():
        old = pd.read_csv(JOURNAL_PATH)
        combined = pd.concat([old, trades_df], ignore_index=True)
    else:
        combined = trades_df
    combined.to_csv(JOURNAL_PATH, index=False)

def compute_stats() -> dict:
    if not JOURNAL_PATH.exists():
        return {}
    df = pd.read_csv(JOURNAL_PATH)
    win = (df["pnl"] > 0).sum()
    loss = (df["pnl"] <= 0).sum()
    win_rate = win / max(win + loss, 1)

    avg_r = df["r_multiple"].mean()
    total_pnl = df["pnl"].sum()

    return {
        "trades": len(df),
        "win_rate": win_rate,
        "avg_r": avg_r,
        "total_pnl": total_pnl,
    }
