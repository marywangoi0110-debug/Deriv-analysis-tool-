"""Pattern detection utilities"""

from typing import List, Dict, Any
from collections import Counter


class PatternDetector:
    """Detects patterns in market data"""

    def __init__(self):
        """Initialize pattern detector"""
        pass

    def detect_trends(self, data: List[float]) -> Dict[str, Any]:
        """Detect trend patterns in data
        
        Args:
            data: Input data
            
        Returns:
            Dict with trend information
        """
        if len(data) < 2:
            return {"trend": "INSUFFICIENT_DATA", "strength": 0.0}

        # Calculate trend
        ups = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
        downs = len(data) - 1 - ups
        trend_strength = abs(ups - downs) / (ups + downs) if (ups + downs) > 0 else 0

        trend_type = "UP" if ups > downs else "DOWN" if downs > ups else "SIDEWAYS"

        return {
            "trend": trend_type,
            "strength": trend_strength,
            "ups": ups,
            "downs": downs
        }

    def detect_cycles(self, data: List[float]) -> Dict[str, Any]:
        """Detect cyclical patterns
        
        Args:
            data: Input data
            
        Returns:
            Dict with cycle information
        """
        if len(data) < 4:
            return {"cycle_detected": False, "period": 0}

        # Simple cycle detection
        for period in range(2, min(len(data) // 2, 20)):
            similarity = 0
            for i in range(len(data) - period):
                if abs(data[i] - data[i + period]) < 0.001:
                    similarity += 1

            if similarity / (len(data) - period) > 0.6:
                return {
                    "cycle_detected": True,
                    "period": period,
                    "strength": similarity / (len(data) - period)
                }

        return {"cycle_detected": False, "period": 0}

    def detect_support_resistance(self, data: List[float]) -> Dict[str, List[float]]:
        """Detect support and resistance levels
        
        Args:
            data: Input data
            
        Returns:
            Dict with support and resistance levels
        """
        if len(data) < 5:
            return {"support": [], "resistance": []}

        # Find local minima and maxima
        support_levels = []
        resistance_levels = []

        for i in range(1, len(data) - 1):
            if data[i] < data[i-1] and data[i] < data[i+1]:
                support_levels.append(data[i])
            elif data[i] > data[i-1] and data[i] > data[i+1]:
                resistance_levels.append(data[i])

        return {
            "support": sorted(set(support_levels))[:3],
            "resistance": sorted(set(resistance_levels), reverse=True)[:3]
        }
