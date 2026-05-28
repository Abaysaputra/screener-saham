"""
Data fetching module with caching and error handling
Optimized for yfinance (Yahoo Finance) as primary data source
"""
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging

from core.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_history_yf(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch historical data from Yahoo Finance with caching
    
    Args:
        symbol: Stock symbol (e.g., 'BBCA.JK')
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        
    Returns:
        DataFrame with OHLCV data
    """
    try:
        data = yf.download(symbol, start=start, end=end, progress=False)
        
        if data.empty:
            logger.warning(f"No data found for {symbol}")
            return pd.DataFrame()
        
        # Handle multiindex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Standardize column names
        data = data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        })
        
        # Remove timezone info
        data.index = data.index.tz_localize(None)
        
        logger.info(f"Successfully fetched {len(data)} rows for {symbol}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=60)  # Cache for 1 minute (real-time data)
def get_realtime_price(symbol: str) -> Optional[dict]:
    """
    Fetch real-time price from Yahoo Finance with caching
    
    Args:
        symbol: Stock symbol (e.g., 'BBCA' or 'BBCA.JK')
        
    Returns:
        Dictionary with price data or None if error
    """
    try:
        yf_symbol = normalize_symbol(symbol)
        ticker = yf.Ticker(yf_symbol)
        
        # Get current data
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty:
            logger.warning(f"No real-time data found for {symbol}")
            return None
        
        current = hist.iloc[-1]
        
        data = {
            "symbol": symbol,
            "price": float(current['Close']),
            "open": float(current['Open']),
            "high": float(current['High']),
            "low": float(current['Low']),
            "volume": int(current['Volume']),
            "previous_close": float(info.get('previousClose', current['Close'])),
            "change": float(current['Close'] - info.get('previousClose', current['Open'])),
            "change_percent": float((current['Close'] - info.get('previousClose', current['Open'])) / info.get('previousClose', current['Open']) * 100) if info.get('previousClose', current['Open']) > 0 else 0
        }
        
        logger.info(f"Successfully fetched real-time data for {symbol}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching real-time data for {symbol}: {str(e)}")
        return None


# Alias for backward compatibility
def get_realtime_goapi(symbol: str) -> Optional[dict]:
    """
    Alias for get_realtime_price for backward compatibility
    Now uses Yahoo Finance instead of GOAPI
    """
    return get_realtime_price(symbol)


def normalize_symbol(symbol: str) -> str:
    """
    Ensure symbol is formatted for Yahoo Finance
    
    Args:
        symbol: Stock symbol (e.g., 'BBCA' or 'BBCA.JK')
        
    Returns:
        Symbol with .JK suffix if not present
    """
    symbol = symbol.strip().upper()
    if not symbol.endswith(".JK"):
        return f"{symbol}.JK"
    return symbol


@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_daily_history_for_scan(symbol: str, days: int = 120) -> pd.DataFrame:
    """
    Fetch recent daily data for signal scanning
    
    Args:
        symbol: Stock symbol
        days: Number of days to fetch
        
    Returns:
        DataFrame with OHLCV data
    """
    try:
        end = datetime.today()
        start = end - timedelta(days=days)
        yf_symbol = normalize_symbol(symbol)
        
        data = yf.download(
            yf_symbol,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            progress=False
        )
        
        if data.empty:
            logger.warning(f"No data found for {symbol}")
            return pd.DataFrame()
        
        # Handle multiindex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Standardize column names
        data = data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        })
        
        # Remove timezone info
        data.index = data.index.tz_localize(None)
        
        logger.info(f"Successfully fetched {len(data)} rows for {symbol}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_intraday_data(symbol: str, interval: str = "1m", days: int = 7) -> pd.DataFrame:
    """
    Fetch intraday data from Yahoo Finance (1m, 5m, 15m, 30m, 1h)
    
    Args:
        symbol: Stock symbol
        interval: Data interval ('1m', '5m', '15m', '30m', '1h')
        days: Number of days to fetch (max 7 for 1m, 60 for others)
        
    Returns:
        DataFrame with OHLCV data
    """
    try:
        yf_symbol = normalize_symbol(symbol)
        
        # Adjust period based on interval
        if interval == "1m":
            period = f"{min(days, 7)}d"
        else:
            period = f"{min(days, 60)}d"
        
        data = yf.download(
            yf_symbol,
            period=period,
            interval=interval,
            progress=False
        )
        
        if data.empty:
            logger.warning(f"No intraday data found for {symbol}")
            return pd.DataFrame()
        
        # Handle multiindex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Standardize column names
        data = data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        })
        
        # Remove timezone info
        data.index = data.index.tz_localize(None)
        
        logger.info(f"Successfully fetched {len(data)} {interval} candles for {symbol}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching intraday data for {symbol}: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_watchlist() -> list:
    """
    Load watchlist from file with caching
    
    Returns:
        List of stock symbols
    """
    try:
        if not Config.WATCHLIST_PATH.exists():
            logger.warning(f"Watchlist file not found: {Config.WATCHLIST_PATH}")
            return []
        
        with Config.WATCHLIST_PATH.open() as f:
            symbols = [line.strip().upper() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(symbols)} symbols from watchlist")
        return symbols
        
    except Exception as e:
        logger.error(f"Error loading watchlist: {str(e)}")
        return []


def get_stock_info(symbol: str) -> dict:
    """
    Get stock information from Yahoo Finance
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Dictionary with stock info
    """
    try:
        yf_symbol = normalize_symbol(symbol)
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info
        
        logger.info(f"Successfully fetched info for {symbol}")
        return info
        
    except Exception as e:
        logger.error(f"Error fetching info for {symbol}: {str(e)}")
        return {}


@st.cache_data
def load_idx_universe() -> pd.DataFrame:
    """
    Load IDX universe from CSV file
    
    Returns:
        DataFrame with all IDX stocks
    """
    try:
        from pathlib import Path
        csv_path = Path(__file__).parent.parent / "idx_universe.csv"
        
        if not csv_path.exists():
            logger.warning(f"Universe file not found: {csv_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} stocks from IDX universe")
        return df
        
    except Exception as e:
        logger.error(f"Error loading universe: {str(e)}")
        return pd.DataFrame()


def get_universe_symbols(filtered_df: Optional[pd.DataFrame] = None) -> list:
    """
    Get list of symbols from filtered universe or full universe
    
    Args:
        filtered_df: Filtered universe DataFrame (optional)
        
    Returns:
        List of stock symbols
    """
    try:
        if filtered_df is not None and not filtered_df.empty:
            symbols = filtered_df['Symbol'].tolist()
            logger.info(f"Using {len(symbols)} symbols from filtered universe")
            return symbols
        else:
            df = load_idx_universe()
            if not df.empty:
                symbols = df['Symbol'].tolist()
                logger.info(f"Using {len(symbols)} symbols from full universe")
                return symbols
            else:
                return []
    except Exception as e:
        logger.error(f"Error getting universe symbols: {str(e)}")
        return []


def merge_watchlist_and_universe(use_universe: bool = False, 
                                  filtered_universe: Optional[pd.DataFrame] = None) -> list:
    """
    Merge watchlist with filtered universe based on settings
    
    Args:
        use_universe: Whether to use universe instead of watchlist
        filtered_universe: Filtered universe DataFrame from session state
        
    Returns:
        List of symbols to scan
    """
    try:
        if use_universe:
            # Use filtered universe if available
            if filtered_universe is not None and not filtered_universe.empty:
                symbols = filtered_universe['Symbol'].tolist()
                logger.info(f"Using {len(symbols)} symbols from filtered universe")
                return symbols
            else:
                # Fallback to watchlist if universe not available
                logger.warning("Filtered universe not available, falling back to watchlist")
                return load_watchlist()
        else:
            # Use watchlist
            return load_watchlist()
            
    except Exception as e:
        logger.error(f"Error merging watchlist and universe: {str(e)}")
        return load_watchlist()  # Fallback to watchlist
