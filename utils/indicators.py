"""
Technical indicators utilities
"""
import pandas as pd
import numpy as np
from typing import Union


def ema(series: Union[pd.Series, np.ndarray], period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average
    
    Args:
        series: Price series
        period: EMA period
        
    Returns:
        EMA series
    """
    series = pd.Series(series)
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: Union[pd.Series, np.ndarray], period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index
    
    Args:
        series: Price series
        period: RSI period
        
    Returns:
        RSI series
    """
    series = pd.Series(series)
    
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    gain_series = pd.Series(gain, index=series.index)
    loss_series = pd.Series(loss, index=series.index)
    
    gain_rolling = gain_series.rolling(window=period).mean()
    loss_rolling = loss_series.rolling(window=period).mean()
    
    rs = gain_rolling / loss_rolling.replace(0, 1e-10)
    rsi_values = 100 - (100 / (1 + rs))
    
    return rsi_values
