"""
Risk management utilities
"""
from math import floor
from core.config import Config


def position_size(
    capital: float,
    entry: float,
    stop: float,
    risk_pct: float = None
) -> int:
    """
    Calculate position size based on risk management
    
    Args:
        capital: Total capital available
        entry: Entry price
        stop: Stop loss price
        risk_pct: Risk percentage per trade (default from config)
        
    Returns:
        Number of shares to buy (in lots)
    """
    if risk_pct is None:
        risk_pct = Config.DEFAULT_RISK_PER_TRADE
    
    risk_amount = capital * risk_pct
    risk_per_share = abs(entry - stop)
    
    if risk_per_share == 0:
        return 0
    
    shares = floor(risk_amount / risk_per_share)
    
    # Adjust to BEI lot size
    lots = shares // Config.LOT_SIZE
    return lots * Config.LOT_SIZE


def calc_r_multiple(entry: float, stop: float, exit_price: float) -> float:
    """
    Calculate R-multiple for a trade
    
    Args:
        entry: Entry price
        stop: Stop loss price
        exit_price: Exit price
        
    Returns:
        R-multiple value
    """
    risk_per_share = abs(entry - stop)
    
    if risk_per_share == 0:
        return 0.0
    
    return (exit_price - entry) / risk_per_share


def calculate_stop_loss(entry: float, sl_pct: float = None) -> float:
    """
    Calculate stop loss price
    
    Args:
        entry: Entry price
        sl_pct: Stop loss percentage (default from config)
        
    Returns:
        Stop loss price
    """
    if sl_pct is None:
        sl_pct = Config.DEFAULT_SL_PCT
    
    return entry * (1 - sl_pct)


def calculate_take_profit(
    entry: float,
    stop: float,
    r_multiple: float = None
) -> float:
    """
    Calculate take profit price based on R-multiple
    
    Args:
        entry: Entry price
        stop: Stop loss price
        r_multiple: R-multiple for take profit (default from config)
        
    Returns:
        Take profit price
    """
    if r_multiple is None:
        r_multiple = Config.DEFAULT_TP_R_MULTIPLE
    
    one_r = abs(entry - stop)
    return entry + (one_r * r_multiple)
