import pandas as pd
import numpy as np

def ema(series: pd.Series, period: int) -> pd.Series:
    series = pd.Series(series)          # pastikan 1D
    return series.ewm(span=period, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    series = pd.Series(series)          # pastikan 1D

    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain_series = pd.Series(gain, index=series.index)
    loss_series = pd.Series(loss, index=series.index)

    gain_rolling = gain_series.rolling(window=period).mean()
    loss_rolling = loss_series.rolling(window=period).mean()

    rs = gain_rolling / loss_rolling.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi
