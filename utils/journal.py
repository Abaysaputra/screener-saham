"""
Trading journal management
"""
import pandas as pd
import logging
from typing import Dict, Tuple

from core.config import Config

logger = logging.getLogger(__name__)


REQUIRED_TRADE_COLUMNS = [
    "entry_time",
    "exit_time",
    "entry",
    "exit",
    "size",
    "sl",
    "tp",
    "reason",
    "pnl",
    "r_multiple",
    "equity_after",
]

NUMERIC_TRADE_COLUMNS = [
    "entry",
    "exit",
    "size",
    "sl",
    "tp",
    "pnl",
    "r_multiple",
    "equity_after",
]

BASE_DEDUP_TRADE_COLUMNS = [
    "entry_time",
    "exit_time",
    "entry",
    "exit",
]


def _get_dedup_columns(df: pd.DataFrame) -> list:
    """Return dedup keys; add symbol if present to avoid cross-symbol collisions."""
    dedup_cols = BASE_DEDUP_TRADE_COLUMNS.copy()
    if "symbol" in df.columns:
        dedup_cols = ["symbol"] + dedup_cols
    return dedup_cols


def validate_trades_df(trades_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate input DataFrame against journal schema.

    Args:
        trades_df: DataFrame with trade data

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        _normalize_trades_df(trades_df)
        return True, "Valid"
    except ValueError as e:
        return False, str(e)


def _normalize_trades_df(trades_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate trade data before persistence/analytics."""
    if trades_df is None or trades_df.empty:
        raise ValueError("Data trade kosong")

    missing = [col for col in REQUIRED_TRADE_COLUMNS if col not in trades_df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak lengkap: {', '.join(missing)}")

    df = trades_df[REQUIRED_TRADE_COLUMNS].copy()

    # Normalize datetime columns
    for col in ["entry_time", "exit_time"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Normalize numeric columns
    for col in NUMERIC_TRADE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize reason column
    df["reason"] = df["reason"].astype(str).str.strip().str.upper()

    invalid_rows = df[
        df[["entry_time", "exit_time"] + NUMERIC_TRADE_COLUMNS].isna().any(axis=1)
    ]
    if not invalid_rows.empty:
        raise ValueError(
            f"Ditemukan {len(invalid_rows)} baris invalid (tanggal/angka tidak valid)"
        )

    if (df["size"] <= 0).any():
        raise ValueError("Kolom size harus > 0")

    if (df["exit_time"] < df["entry_time"]).any():
        raise ValueError("exit_time tidak boleh lebih awal dari entry_time")

    return df


def _get_existing_journal_normalized() -> pd.DataFrame:
    """Load existing journal as normalized DataFrame for dedup checks."""
    if not Config.JOURNAL_PATH.exists():
        return pd.DataFrame(columns=REQUIRED_TRADE_COLUMNS)

    old = pd.read_csv(Config.JOURNAL_PATH)
    return _normalize_trades_df(old)


def _deduplicate_new_trades(
    new_trades: pd.DataFrame,
    existing_trades: pd.DataFrame,
) -> Tuple[pd.DataFrame, int, int]:
    """
    Deduplicate incoming trades.

    Returns:
        (new_unique, duplicate_in_file, duplicate_in_journal)
    """
    dedup_cols = _get_dedup_columns(new_trades)
    new_local_unique = new_trades.drop_duplicates(subset=dedup_cols, keep="first")
    duplicate_in_file = len(new_trades) - len(new_local_unique)

    if existing_trades.empty:
        return new_local_unique, duplicate_in_file, 0

    existing_keys = existing_trades[dedup_cols].drop_duplicates()
    mark = new_local_unique.merge(
        existing_keys,
        on=dedup_cols,
        how="left",
        indicator=True,
    )["_merge"]
    new_unique = new_local_unique[mark == "left_only"].copy()
    duplicate_in_journal = len(new_local_unique) - len(new_unique)

    return new_unique, duplicate_in_file, duplicate_in_journal


def preview_trade_import(trades_df: pd.DataFrame) -> Tuple[bool, str, Dict[str, int]]:
    """
    Validate and summarize an import before writing to journal.

    Returns:
        (is_valid, message, stats)
    """
    empty_stats = {
        "total_rows": 0,
        "new_rows": 0,
        "duplicate_in_file": 0,
        "duplicate_in_journal": 0,
    }

    try:
        new_trades = _normalize_trades_df(trades_df)
        existing_trades = _get_existing_journal_normalized()
        new_unique, dup_file, dup_journal = _deduplicate_new_trades(new_trades, existing_trades)

        stats = {
            "total_rows": len(new_trades),
            "new_rows": len(new_unique),
            "duplicate_in_file": dup_file,
            "duplicate_in_journal": dup_journal,
        }
        return True, "Valid", stats
    except ValueError as e:
        return False, str(e), empty_stats


def log_trades(trades_df: pd.DataFrame) -> bool:
    """
    Append trades to journal CSV file
    
    Args:
        trades_df: DataFrame with trade data
        
    Returns:
        True if successful, False otherwise
    """
    try:
        new_trades = _normalize_trades_df(trades_df)
        existing_trades = _get_existing_journal_normalized()
        new_unique, dup_file, dup_journal = _deduplicate_new_trades(new_trades, existing_trades)

        if new_unique.empty:
            logger.info(
                "No new trades to log (duplicate_in_file=%s, duplicate_in_journal=%s)",
                dup_file,
                dup_journal,
            )
            return True

        if existing_trades.empty:
            combined = new_unique
        else:
            dedup_cols = _get_dedup_columns(existing_trades)
            combined = pd.concat([existing_trades, new_unique], ignore_index=True)
            combined = combined.drop_duplicates(subset=dedup_cols, keep="first")
        
        combined.to_csv(Config.JOURNAL_PATH, index=False)
        logger.info(
            "Logged %s new trades (duplicate_in_file=%s, duplicate_in_journal=%s)",
            len(new_unique),
            dup_file,
            dup_journal,
        )
        return True
    except ValueError as e:
        logger.error(f"Validation error logging trades: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"Error logging trades: {str(e)}")
        return False


def load_journal() -> pd.DataFrame:
    """
    Load trading journal from CSV
    
    Returns:
        DataFrame with journal data or empty DataFrame
    """
    try:
        if not Config.JOURNAL_PATH.exists():
            logger.info("Journal file not found")
            return pd.DataFrame()
        
        raw_df = pd.read_csv(Config.JOURNAL_PATH)
        df = _normalize_trades_df(raw_df)
        logger.info(f"Loaded {len(df)} trades from journal")
        return df
    except ValueError as e:
        logger.error(f"Invalid journal data: {str(e)}")
        return pd.DataFrame()
        
    except Exception as e:
        logger.error(f"Error loading journal: {str(e)}")
        return pd.DataFrame()


def compute_stats() -> dict:
    """
    Calculate statistics from trading journal
    
    Returns:
        Dictionary with trading statistics
    """
    df = load_journal()
    
    if df.empty:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_r_multiple": 0,
            "total_pnl": 0,
        }
    
    wins = (df["pnl"] > 0).sum()
    losses = (df["pnl"] <= 0).sum()
    win_rate = wins / max(wins + losses, 1)
    
    avg_r = df["r_multiple"].mean()
    total_pnl = df["pnl"].sum()
    
    return {
        "total_trades": len(df),
        "winning_trades": wins,
        "losing_trades": losses,
        "win_rate": round(win_rate * 100, 2),
        "avg_r_multiple": round(avg_r, 2),
        "total_pnl": round(total_pnl, 2),
    }


def clear_journal() -> bool:
    """
    Clear all trades from journal
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if Config.JOURNAL_PATH.exists():
            Config.JOURNAL_PATH.unlink()
            logger.info("Journal cleared")
        return True
        
    except Exception as e:
        logger.error(f"Error clearing journal: {str(e)}")
        return False
