"""
Trading strategy implementation
"""
import pandas as pd
import streamlit as st
from typing import Tuple

from utils.indicators import ema, rsi
from core.config import Config


@st.cache_data
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators to dataframe
    
    Args:
        df: OHLCV dataframe
        
    Returns:
        DataFrame with indicators added
    """
    df = df.copy()
    
    # Ensure close is a proper Series
    close = df["close"]
    if not isinstance(close, pd.Series):
        close = pd.Series(close.values.flatten(), index=df.index)
    
    # Add indicators
    df["ema_fast"] = ema(close, Config.DEFAULT_EMA_FAST)
    df["ema_slow"] = ema(close, Config.DEFAULT_EMA_SLOW)
    df["rsi"] = rsi(close, Config.DEFAULT_RSI_PERIOD)
    
    return df


def generate_signals(
    df: pd.DataFrame,
    rsi_max: float = 70.0
) -> pd.DataFrame:
    """
    Generate trading signals based on EMA crossover and RSI
    
    Strategy:
    - BUY: EMA fast crosses above EMA slow AND RSI < rsi_max
    - SELL: EMA fast crosses below EMA slow
    
    Args:
        df: OHLCV dataframe
        rsi_max: Maximum RSI for buy signal
        
    Returns:
        DataFrame with signals added
    """
    df = add_indicators(df)
    df["signal"] = "HOLD"
    
    # EMA cross up (bullish)
    cross_up = (
        (df["ema_fast"].shift(1) < df["ema_slow"].shift(1)) &
        (df["ema_fast"] > df["ema_slow"]) &
        (df["rsi"] < rsi_max)
    )
    
    # EMA cross down (bearish)
    cross_down = (
        (df["ema_fast"].shift(1) > df["ema_slow"].shift(1)) &
        (df["ema_fast"] < df["ema_slow"])
    )
    
    df.loc[cross_up, "signal"] = "BUY"
    df.loc[cross_down, "signal"] = "SELL"
    
    return df


def validate_signal(row: pd.Series) -> Tuple[bool, str]:
    """
    Validate a trading signal
    
    Args:
        row: DataFrame row with signal data
        
    Returns:
        Tuple of (is_valid, reason)
    """
    if pd.isna(row["ema_fast"]) or pd.isna(row["ema_slow"]):
        return False, "Insufficient data for indicators"
    
    if row["signal"] == "BUY":
        if row["rsi"] >= 70:
            return False, "RSI too high (overbought)"
        if row["volume"] == 0:
            return False, "No trading volume"
    
    return True, "Valid signal"
