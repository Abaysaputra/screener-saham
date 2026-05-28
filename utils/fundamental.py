"""
Fundamental Analysis Module
Provides functions to fetch and filter stocks based on fundamental criteria
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Optional
import streamlit as st
from core.config import Config


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_fundamental_data(symbol: str) -> Optional[Dict]:
    """
    Fetch fundamental data for a stock from Yahoo Finance
    
    Args:
        symbol: Stock symbol (already normalized with .JK)
    
    Returns:
        Dictionary with fundamental metrics or None if error
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Extract key fundamental metrics
        fundamentals = {
            'symbol': symbol,
            'name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', None),
            'forward_pe': info.get('forwardPE', None),
            'pb_ratio': info.get('priceToBook', None),
            'eps': info.get('trailingEps', None),
            'profit_margin': info.get('profitMargins', None),
            'roe': info.get('returnOnEquity', None),
            'debt_to_equity': info.get('debtToEquity', None),
            'current_ratio': info.get('currentRatio', None),
            'dividend_yield': info.get('dividendYield', None),
            'peg_ratio': info.get('pegRatio', None),
        }
        
        return fundamentals
        
    except Exception as e:
        return None


def check_fundamental_criteria(fundamentals: Dict, criteria: Dict) -> bool:
    """
    Check if a stock meets fundamental criteria
    
    Args:
        fundamentals: Dict with fundamental data
        criteria: Dict with filtering criteria
    
    Returns:
        True if stock passes all criteria
    """
    if not fundamentals:
        return False
    
    try:
        # Check EPS positive
        if criteria.get('eps_positive', False):
            eps = fundamentals.get('eps')
            if eps is None or eps <= 0:
                return False
        
        # Check PE Ratio
        if criteria.get('max_pe') is not None:
            pe = fundamentals.get('pe_ratio')
            if pe is None or pe > criteria['max_pe'] or pe < 0:
                return False
        
        # Check PB Ratio
        if criteria.get('max_pb') is not None:
            pb = fundamentals.get('pb_ratio')
            if pb is None or pb > criteria['max_pb'] or pb < 0:
                return False
        
        # Check Profit Margin
        if criteria.get('min_profit_margin') is not None:
            margin = fundamentals.get('profit_margin')
            if margin is None or margin < criteria['min_profit_margin']:
                return False
        
        # Check ROE
        if criteria.get('min_roe') is not None:
            roe = fundamentals.get('roe')
            if roe is None or roe < criteria['min_roe']:
                return False
        
        # Check Debt to Equity
        if criteria.get('max_debt_to_equity') is not None:
            de = fundamentals.get('debt_to_equity')
            if de is not None and de > criteria['max_debt_to_equity']:
                return False
        
        # Check Market Cap minimum
        if criteria.get('min_market_cap') is not None:
            mc = fundamentals.get('market_cap', 0)
            if mc < criteria['min_market_cap']:
                return False
        
        return True
        
    except Exception as e:
        return False


def format_fundamental_display(fundamentals: Dict) -> pd.DataFrame:
    """
    Format fundamental data for display in Streamlit
    
    Args:
        fundamentals: Dict with fundamental data
    
    Returns:
        DataFrame formatted for display
    """
    if not fundamentals:
        return pd.DataFrame()
    
    # Format display
    display_data = {
        'Metric': [],
        'Value': []
    }
    
    # Name and Sector
    display_data['Metric'].append('Company')
    display_data['Value'].append(fundamentals.get('name', 'N/A'))
    
    display_data['Metric'].append('Sector')
    display_data['Value'].append(fundamentals.get('sector', 'N/A'))
    
    # Market Cap
    mc = fundamentals.get('market_cap', 0)
    if mc > 0:
        mc_str = f"Rp {mc/1e12:.2f}T" if mc >= 1e12 else f"Rp {mc/1e9:.2f}B"
    else:
        mc_str = "N/A"
    display_data['Metric'].append('Market Cap')
    display_data['Value'].append(mc_str)
    
    # PE Ratio
    pe = fundamentals.get('pe_ratio')
    display_data['Metric'].append('PE Ratio')
    display_data['Value'].append(f"{pe:.2f}" if pe else "N/A")
    
    # PB Ratio
    pb = fundamentals.get('pb_ratio')
    display_data['Metric'].append('PB Ratio')
    display_data['Value'].append(f"{pb:.2f}" if pb else "N/A")
    
    # EPS
    eps = fundamentals.get('eps')
    display_data['Metric'].append('EPS')
    display_data['Value'].append(f"{eps:.2f}" if eps else "N/A")
    
    # Profit Margin
    margin = fundamentals.get('profit_margin')
    display_data['Metric'].append('Profit Margin')
    display_data['Value'].append(f"{margin*100:.2f}%" if margin else "N/A")
    
    # ROE
    roe = fundamentals.get('roe')
    display_data['Metric'].append('ROE')
    display_data['Value'].append(f"{roe*100:.2f}%" if roe else "N/A")
    
    # Debt to Equity
    de = fundamentals.get('debt_to_equity')
    display_data['Metric'].append('Debt/Equity')
    display_data['Value'].append(f"{de:.2f}" if de else "N/A")
    
    return pd.DataFrame(display_data)


def get_fundamental_summary(fundamentals: Dict) -> str:
    """
    Get a text summary of fundamental quality
    
    Args:
        fundamentals: Dict with fundamental data
    
    Returns:
        Quality rating string
    """
    if not fundamentals:
        return "❓ Data tidak tersedia"
    
    score = 0
    max_score = 0
    
    # Check EPS
    eps = fundamentals.get('eps')
    if eps is not None:
        max_score += 1
        if eps > 0:
            score += 1
    
    # Check PE
    pe = fundamentals.get('pe_ratio')
    if pe is not None and pe > 0:
        max_score += 1
        if 5 < pe < 25:  # Reasonable range
            score += 1
    
    # Check PB
    pb = fundamentals.get('pb_ratio')
    if pb is not None and pb > 0:
        max_score += 1
        if pb < 3:  # Not overvalued
            score += 1
    
    # Check Profit Margin
    margin = fundamentals.get('profit_margin')
    if margin is not None:
        max_score += 1
        if margin > 0.05:  # At least 5%
            score += 1
    
    # Check ROE
    roe = fundamentals.get('roe')
    if roe is not None:
        max_score += 1
        if roe > 0.10:  # At least 10%
            score += 1
    
    if max_score == 0:
        return "❓ Data tidak lengkap"
    
    quality_pct = (score / max_score) * 100
    
    if quality_pct >= 80:
        return "🟢 Berkualitas Baik"
    elif quality_pct >= 60:
        return "🟡 Kualitas Sedang"
    elif quality_pct >= 40:
        return "🟠 Kualitas Rendah"
    else:
        return "🔴 Kualitas Sangat Rendah"


def filter_watchlist_by_fundamentals(watchlist: list, criteria: Dict, progress_callback=None) -> list:
    """
    Filter watchlist based on fundamental criteria
    
    Args:
        watchlist: List of stock symbols
        criteria: Dict with filtering criteria
        progress_callback: Optional callback for progress updates
    
    Returns:
        List of stocks that pass fundamental filters
    """
    from core.data import normalize_symbol
    
    passed_stocks = []
    
    for idx, symbol in enumerate(watchlist):
        if progress_callback:
            progress_callback(idx + 1, len(watchlist), symbol)
        
        yf_symbol = normalize_symbol(symbol)
        fundamentals = get_fundamental_data(yf_symbol)
        
        if check_fundamental_criteria(fundamentals, criteria):
            passed_stocks.append(symbol)
    
    return passed_stocks
