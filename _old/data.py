import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import API_GOAPI_KEY, GOAPI_BASE_URL, DEFAULT_EMA_FAST, DEFAULT_EMA_SLOW, DEFAULT_RSI_PERIOD

def get_history_yf(symbol: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(symbol, start=start, end=end)

    # kalau hasilnya multiindex (Price, Ticker), drop level Ticker
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    })
    data.index = data.index.tz_localize(None)
    return data


def get_realtime_goapi(symbol: str) -> dict:
    """
    Ambil snapshot harga real-time (delay 3–10 menit) dari GOAPI.[web:25][web:40]
    symbol contoh: 'BBCA'
    """
    url = f"{GOAPI_BASE_URL}/stock/idx/prices/{symbol}"
    headers = {"X-API-KEY": API_GOAPI_KEY}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def normalize_symbol(symbol: str) -> str:
    """
    Pastikan symbol cocok untuk yfinance, tambah .JK kalau belum.[web:34]
    """
    if not symbol.endswith(".JK"):
        return symbol + ".JK"
    return symbol

def get_daily_history_for_scan(symbol: str, days: int = 120) -> pd.DataFrame:
    """
    Ambil data harian beberapa bulan terakhir untuk scan sinyal hari ini.
    """
    end = datetime.today()
    start = end - timedelta(days=days)
    yf_symbol = normalize_symbol(symbol)
    data = yf.download(yf_symbol,
                       start=start.strftime("%Y-%m-%d"),
                       end=end.strftime("%Y-%m-%d"))
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    })
    data.index = data.index.tz_localize(None)
    return data