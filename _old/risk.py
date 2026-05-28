from math import floor
from config import DEFAULT_RISK_PER_TRADE, LOT_SIZE

def position_size(capital: float,
                  entry: float,
                  stop: float,
                  risk_pct: float = DEFAULT_RISK_PER_TRADE) -> int:
    """
    Hitung jumlah saham yang boleh dibeli berdasarkan risiko.
    """
    risk_amount = capital * risk_pct
    risk_per_share = abs(entry - stop)
    if risk_per_share == 0:
        return 0
    shares = floor(risk_amount / risk_per_share)
    # Sesuaikan ke kelipatan lot BEI
    lots = shares // LOT_SIZE
    return lots * LOT_SIZE

def calc_r_multiple(entry: float, stop: float, exit_price: float) -> float:
    risk_per_share = abs(entry - stop)
    if risk_per_share == 0:
        return 0.0
    return (exit_price - entry) / risk_per_share
