"""
Backtesting engine
"""
import pandas as pd
import streamlit as st
from typing import Optional
import logging

from utils.risk import position_size, calc_r_multiple, calculate_stop_loss, calculate_take_profit
from core.config import Config

logger = logging.getLogger(__name__)


@st.cache_data
def backtest_risk_based(
    df: pd.DataFrame,
    capital: float = None,
    risk_pct: float = None,
    sl_pct: float = None,
    tp_r_multiple: float = None
) -> pd.DataFrame:
    """
    Run backtest with risk-based position sizing
    
    Strategy:
    - Entry on BUY signal
    - Stop loss at entry * (1 - sl_pct)
    - Take profit at entry + (1R * tp_r_multiple)
    - Position size based on risk_pct of capital
    
    Args:
        df: DataFrame with signals
        capital: Starting capital (default from config)
        risk_pct: Risk per trade (default from config)
        sl_pct: Stop loss percentage (default from config)
        tp_r_multiple: Take profit R-multiple (default from config)
        
    Returns:
        DataFrame with trade results
    """
    # Set defaults from config
    if capital is None:
        capital = Config.DEFAULT_CAPITAL
    if risk_pct is None:
        risk_pct = Config.DEFAULT_RISK_PER_TRADE
    if sl_pct is None:
        sl_pct = Config.DEFAULT_SL_PCT
    if tp_r_multiple is None:
        tp_r_multiple = Config.DEFAULT_TP_R_MULTIPLE
    
    trades = []
    in_position = False
    equity = capital
    
    df_bt = df.copy()
    
    for i in range(len(df_bt) - 1):
        row = df_bt.iloc[i]
        next_row = df_bt.iloc[i + 1]
        
        # Entry logic
        if not in_position and row["signal"] == "BUY":
            entry_price = float(row["close"])
            sl_price = calculate_stop_loss(entry_price, sl_pct)
            tp_price = calculate_take_profit(entry_price, sl_price, tp_r_multiple)
            
            size = position_size(
                capital=equity,
                entry=entry_price,
                stop=sl_price,
                risk_pct=risk_pct
            )
            
            if size == 0:
                logger.warning(f"Position size is 0 at {row.name}")
                continue
            
            in_position = True
            entry_index = row.name
            
        # Exit logic
        elif in_position:
            low_next = float(next_row["low"])
            high_next = float(next_row["high"])
            
            exit_price = None
            exit_reason = None
            
            # Check stop loss first (risk management priority)
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
                    "entry": round(entry_price, 2),
                    "exit": round(exit_price, 2),
                    "size": int(size),
                    "sl": round(sl_price, 2),
                    "tp": round(tp_price, 2),
                    "reason": exit_reason,
                    "pnl": round(pnl, 2),
                    "r_multiple": round(r_mult, 2),
                    "equity_after": round(equity, 2),
                })
                
                in_position = False
    
    trades_df = pd.DataFrame(trades)
    logger.info(f"Backtest completed: {len(trades_df)} trades")
    
    return trades_df


def calculate_backtest_metrics(trades_df: pd.DataFrame) -> dict:
    """
    Calculate performance metrics from backtest results
    
    Args:
        trades_df: DataFrame with trade results
        
    Returns:
        Dictionary with performance metrics
    """
    if trades_df.empty:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_r_multiple": 0,
            "total_pnl": 0,
            "max_drawdown": 0,
            "profit_factor": 0,
        }
    
    wins = trades_df[trades_df["pnl"] > 0]
    losses = trades_df[trades_df["pnl"] <= 0]
    
    win_rate = len(wins) / len(trades_df) if len(trades_df) > 0 else 0
    avg_r = trades_df["r_multiple"].mean()
    total_pnl = trades_df["pnl"].sum()
    
    # Calculate max drawdown
    equity_curve = trades_df["equity_after"].values
    peak = equity_curve[0]
    max_dd = 0
    
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak
        if dd > max_dd:
            max_dd = dd
    
    # Calculate profit factor
    total_profit = wins["pnl"].sum() if not wins.empty else 0
    total_loss = abs(losses["pnl"].sum()) if not losses.empty else 1
    profit_factor = total_profit / total_loss if total_loss > 0 else 0
    
    return {
        "total_trades": len(trades_df),
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "win_rate": round(win_rate * 100, 2),
        "avg_r_multiple": round(avg_r, 2),
        "total_pnl": round(total_pnl, 2),
        "max_drawdown": round(max_dd * 100, 2),
        "profit_factor": round(profit_factor, 2),
        "avg_win": round(wins["pnl"].mean(), 2) if not wins.empty else 0,
        "avg_loss": round(losses["pnl"].mean(), 2) if not losses.empty else 0,
    }
