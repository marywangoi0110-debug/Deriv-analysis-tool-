"""Volatility analysis module for derivatives predictions"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime

from src.utils.statistics import calculate_volatility


class VolatilityAnalyzer:
    """Analyzes market volatility with multiple metrics"""

    def __init__(self):
        """Initialize volatility analyzer"""
        self.volatility_history = []

    def analyze_volatility(self, data: List[float]) -> Dict[str, Any]:
        """Comprehensive volatility analysis
        
        Args:
            data: Historical price/value data
            
        Returns:
            Dict with multiple volatility metrics
        """
        if len(data) < 2:
            return {"error": "Insufficient data for volatility analysis"}

        arr = np.array(data, dtype=float)
        
        # Calculate various volatility metrics
        metrics = {
            "historical_volatility": self._calculate_historical_volatility(arr),
            "realized_volatility": self._calculate_realized_volatility(arr),
            "parkinson_volatility": self._calculate_parkinson_volatility(arr),
            "garman_klass_volatility": self._calculate_garman_klass_volatility(arr),
            "standard_deviation": float(np.std(arr)),
            "coefficient_of_variation": self._calculate_cv(arr),
            "range_volatility": self._calculate_range_volatility(arr),
            "average_true_range": self._calculate_atr(arr),
        }

        # Volatility classification
        avg_volatility = np.mean(list(metrics.values())[:-1])
        metrics["volatility_level"] = self._classify_volatility(avg_volatility)
        metrics["average_volatility"] = round(avg_volatility, 6)

        # Volatility trend
        metrics["volatility_trend"] = self._calculate_volatility_trend(data)

        # Add timestamp
        metrics["timestamp"] = datetime.now().isoformat()
        metrics["data_points"] = len(data)

        # Store in history
        self.volatility_history.append(metrics)

        return metrics

    def _calculate_historical_volatility(self, arr: np.ndarray, period: int = 20) -> float:
        """Calculate historical volatility using returns standard deviation
        
        Args:
            arr: Price array
            period: Period for calculation
            
        Returns:
            Historical volatility
        """
        if len(arr) < 2:
            return 0.0

        # Use last 'period' or all if less
        data_slice = arr[-period:] if len(arr) >= period else arr

        returns = np.diff(data_slice) / data_slice[:-1]
        volatility = np.std(returns)

        return round(float(volatility), 6)

    def _calculate_realized_volatility(self, arr: np.ndarray) -> float:
        """Calculate realized volatility from intraday data
        
        Args:
            arr: Price array
            
        Returns:
            Realized volatility
        """
        if len(arr) < 2:
            return 0.0

        log_returns = np.diff(np.log(arr))
        realized_vol = np.sqrt(np.sum(log_returns ** 2))

        return round(float(realized_vol), 6)

    def _calculate_parkinson_volatility(self, arr: np.ndarray) -> float:
        """Parkinson's volatility (uses high-low range)
        Assumes arr represents prices with inherent range
        
        Args:
            arr: Price array
            
        Returns:
            Parkinson volatility estimate
        """
        if len(arr) < 2:
            return 0.0

        # Approximate high-low using windowed data
        highs = []
        lows = []
        window = max(2, len(arr) // 10)

        for i in range(0, len(arr) - window + 1, window):
            window_data = arr[i:i+window]
            highs.append(np.max(window_data))
            lows.append(np.min(window_data))

        if len(highs) < 2:
            return self._calculate_historical_volatility(arr)

        hl_ratio = np.array(highs) / np.array(lows)
        parkinson = np.sqrt(np.mean(np.log(hl_ratio) ** 2) / (4 * np.log(2)))

        return round(float(parkinson), 6)

    def _calculate_garman_klass_volatility(self, arr: np.ndarray) -> float:
        """Garman-Klass volatility (more efficient estimator)
        
        Args:
            arr: Price array
            
        Returns:
            Garman-Klass volatility
        """
        if len(arr) < 2:
            return 0.0

        close_prices = arr
        log_returns = np.diff(np.log(close_prices))
        
        # Simplified Garman-Klass
        gk_vol = np.sqrt(np.mean(log_returns ** 2))

        return round(float(gk_vol), 6)

    def _calculate_cv(self, arr: np.ndarray) -> float:
        """Calculate coefficient of variation (CV)
        
        Args:
            arr: Price array
            
        Returns:
            Coefficient of variation
        """
        if len(arr) == 0:
            return 0.0

        mean = np.mean(arr)
        if mean == 0:
            return 0.0

        std = np.std(arr)
        cv = std / mean

        return round(float(cv), 6)

    def _calculate_range_volatility(self, arr: np.ndarray) -> float:
        """Calculate volatility using price range
        
        Args:
            arr: Price array
            
        Returns:
            Range-based volatility
        """
        if len(arr) < 2:
            return 0.0

        price_range = np.max(arr) - np.min(arr)
        avg_price = np.mean(arr)

        if avg_price == 0:
            return 0.0

        range_vol = price_range / avg_price

        return round(float(range_vol), 6)

    def _calculate_atr(self, arr: np.ndarray, period: int = 14) -> float:
        """Calculate Average True Range (ATR)
        
        Args:
            arr: Price array
            period: ATR period
            
        Returns:
            Average True Range
        """
        if len(arr) < period + 1:
            return 0.0

        # Simplified ATR using differences
        tr_values = np.abs(np.diff(arr))
        atr = np.mean(tr_values[-period:])

        return round(float(atr), 6)

    def _calculate_volatility_trend(self, data: List[float]) -> str:
        """Determine if volatility is increasing, decreasing, or stable
        
        Args:
            data: Historical data
            
        Returns:
            Trend classification: "INCREASING", "DECREASING", or "STABLE"
        """
        if len(data) < 10:
            return "INSUFFICIENT_DATA"

        # Split data into two halves
        mid = len(data) // 2
        first_half = data[:mid]
        second_half = data[mid:]

        vol1 = calculate_volatility(first_half)
        vol2 = calculate_volatility(second_half)

        vol_change = (vol2 - vol1) / vol1 if vol1 != 0 else 0

        if vol_change > 0.15:
            return "INCREASING"
        elif vol_change < -0.15:
            return "DECREASING"
        else:
            return "STABLE"

    def _classify_volatility(self, volatility: float) -> str:
        """Classify volatility level
        
        Args:
            volatility: Volatility value
            
        Returns:
            Classification: "VERY_LOW", "LOW", "MODERATE", "HIGH", "VERY_HIGH"
        """
        if volatility < 0.01:
            return "VERY_LOW"
        elif volatility < 0.03:
            return "LOW"
        elif volatility < 0.06:
            return "MODERATE"
        elif volatility < 0.10:
            return "HIGH"
        else:
            return "VERY_HIGH"

    def get_volatility_report(self) -> Dict[str, Any]:
        """Get comprehensive volatility report
        
        Returns:
            Dict with volatility analysis report
        """
        if not self.volatility_history:
            return {"error": "No volatility history available"}

        latest = self.volatility_history[-1]
        
        report = {
            "current_volatility": latest,
            "total_analyses": len(self.volatility_history),
            "timestamp": datetime.now().isoformat()
        }

        # Calculate volatility of volatilities
        if len(self.volatility_history) > 1:
            volatilities = [v["average_volatility"] for v in self.volatility_history]
            report["volatility_of_volatility"] = round(np.std(volatilities), 6)
            report["average_volatility_across_periods"] = round(np.mean(volatilities), 6)

        return report

    def compare_volatility_periods(self, limit: int = 5) -> Dict[str, Any]:
        """Compare volatility across recent periods
        
        Args:
            limit: Number of recent periods to compare
            
        Returns:
            Dict with volatility comparison
        """
        if not self.volatility_history:
            return {"error": "No volatility history available"}

        recent = self.volatility_history[-limit:]

        comparison = {
            "periods_compared": len(recent),
            "trend": "INCREASING" if recent[-1]["average_volatility"] > recent[0]["average_volatility"] else "DECREASING",
            "details": []
        }

        for i, vol_data in enumerate(recent):
            comparison["details"].append({
                "period": i + 1,
                "average_volatility": vol_data["average_volatility"],
                "level": vol_data["volatility_level"]
            })

        return comparison
