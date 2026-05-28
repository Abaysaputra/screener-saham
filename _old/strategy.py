import pandas as pd
from indicators import ema, rsi
from config import DEFAULT_EMA_FAST, DEFAULT_EMA_SLOW, DEFAULT_RSI_PERIOD

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # pastikan 'close' adalah Series 1D
    close = df["close"]
    # kalau hasil rename sebelumnya bikin bentuk (n,1), paksa jadi Series:
    if not isinstance(close, pd.Series):
        close = pd.Series(close.values.flatten(), index=df.index)

    df["ema_fast"] = ema(close, DEFAULT_EMA_FAST)
    df["ema_slow"] = ema(close, DEFAULT_EMA_SLOW)
    df["rsi"] = rsi(close, DEFAULT_RSI_PERIOD)

    return df

def generate_signals(df: pd.DataFrame,
                     rsi_max: float = 70.0) -> pd.DataFrame:
    """
    Logic swing:
    - Buy: ema_fast cross up ema_slow & RSI < rsi_max
    - Sell: ema_fast cross down ema_slow
    """
    print(df.dtypes)
    print(df["close"].shape)

    df = add_indicators(df)
    df["signal"] = "HOLD"

    # Cross up
    cross_up = (df["ema_fast"].shift(1) < df["ema_slow"].shift(1)) & \
               (df["ema_fast"] > df["ema_slow"]) & \
               (df["rsi"] < rsi_max)

    # Cross down
    cross_down = (df["ema_fast"].shift(1) > df["ema_slow"].shift(1)) & \
                 (df["ema_fast"] < df["ema_slow"])

    df.loc[cross_up, "signal"] = "BUY"
    df.loc[cross_down, "signal"] = "SELL"

    return df
