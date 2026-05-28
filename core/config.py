"""
Configuration management with environment variables support
Optimized for yfinance (Yahoo Finance) data source
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Data Source Configuration
    DATA_SOURCE = "yfinance"  # Primary data source: Yahoo Finance
    YF_SUFFIX = ".JK"  # Yahoo Finance suffix for IDX stocks
    
    # Trading Parameters
    DEFAULT_EMA_FAST = int(os.getenv("DEFAULT_EMA_FAST", "20"))
    DEFAULT_EMA_SLOW = int(os.getenv("DEFAULT_EMA_SLOW", "50"))
    DEFAULT_RSI_PERIOD = int(os.getenv("DEFAULT_RSI_PERIOD", "14"))
    DEFAULT_RISK_PER_TRADE = float(os.getenv("DEFAULT_RISK_PER_TRADE", "0.015"))
    LOT_SIZE = int(os.getenv("LOT_SIZE", "100"))
    
    # App Configuration
    DEFAULT_CAPITAL = float(os.getenv("DEFAULT_CAPITAL", "100000000"))
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    WATCHLIST_PATH = BASE_DIR / "watchlist.txt"
    JOURNAL_PATH = BASE_DIR / "trades_journal.csv"
    
    # Backtest Parameters
    DEFAULT_SL_PCT = 0.02  # 2% stop loss
    DEFAULT_TP_R_MULTIPLE = 2.0  # 2R take profit
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.WATCHLIST_PATH.exists():
            cls.WATCHLIST_PATH.touch()
            import warnings
            warnings.warn(f"Created empty watchlist at {cls.WATCHLIST_PATH}")

# Initialize and validate config on import
Config.validate()
