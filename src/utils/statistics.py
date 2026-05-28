"""Statistical utilities for analysis"""

import numpy as np
from typing import List


def calculate_trend(data: List[float]) -> float:
    """Calculate trend direction
    
    Args:
        data: Input data
        
    Returns:
        Trend value (-1 to 1, negative=down, positive=up)
    """
    if len(data) < 2:
        return 0.0

    ups = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
    total = len(data) - 1
    
    if total == 0:
        return 0.0
    
    return (ups / total) - 0.5


def calculate_volatility(data: List[float]) -> float:
    """Calculate volatility (standard deviation of returns)
    
    Args:
        data: Input data
        
    Returns:
        Volatility measure
    """
    if len(data) < 2:
        return 0.0

    arr = np.array(data, dtype=float)
    returns = np.diff(arr) / arr[:-1]
    
    volatility = np.std(returns)
    
    return float(volatility)


def calculate_rsi(data: List[float], period: int = 14) -> float:
    """Calculate Relative Strength Index
    
    Args:
        data: Input data
        period: RSI period
        
    Returns:
        RSI value (0-100)
    """
    if len(data) < period + 1:
        return 50.0

    arr = np.array(data, dtype=float)
    deltas = np.diff(arr)
    
    gains = np.sum(deltas[deltas > 0][-period:]) / period if len(deltas[deltas > 0]) > 0 else 0
    losses = abs(np.sum(deltas[deltas < 0][-period:]) / period) if len(deltas[deltas < 0]) > 0 else 0
    
    if losses == 0:
        return 100.0 if gains > 0 else 50.0
    
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    
    return float(rsi)


def calculate_sma(data: List[float], period: int = 5) -> List[float]:
    """Calculate Simple Moving Average
    
    Args:
        data: Input data
        period: SMA period
        
    Returns:
        List of SMA values
    """
    if len(data) < period:
        return data

    arr = np.array(data, dtype=float)
    sma = np.convolve(arr, np.ones(period)/period, mode='valid')
    
    return sma.tolist()


def calculate_ema(data: List[float], period: int = 5) -> List[float]:
    """Calculate Exponential Moving Average
    
    Args:
        data: Input data
        period: EMA period
        
    Returns:
        List of EMA values
    """
    if len(data) < period:
        return data

    arr = np.array(data, dtype=float)
    multiplier = 2 / (period + 1)
    ema = [np.mean(arr[:period])]
    
    for i in range(period, len(arr)):
        ema.append((arr[i] - ema[-1]) * multiplier + ema[-1])
    
    return ema
