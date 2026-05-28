"""Market analysis models for derivatives predictions"""

import numpy as np
from typing import Dict, List, Any

from src.utils.pattern_detector import PatternDetector
from src.utils.statistics import calculate_volatility, calculate_trend


class MarketAnalyzer:
    """Analyzes market patterns for derivatives trading"""

    def __init__(self):
        """Initialize market analyzer"""
        self.pattern_detector = PatternDetector()

    def analyze_over_under(self, data: List[float]) -> Dict[str, Any]:
        """Analyze if next value will be over or under current
        
        Args:
            data: Processed price data
            
        Returns:
            Dict with prediction and supporting data
        """
        if len(data) < 2:
            return {"prediction": None, "probability_over": 0.5, "probability_under": 0.5}

        current = data[-1]
        previous = data[-2]
        trend = calculate_trend(data)

        # Calculate historical ratio of over/under moves
        over_count = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
        under_count = len(data) - 1 - over_count

        # Apply trend adjustment
        if trend > 0:
            prob_over = min((over_count / len(data)) + 0.15, 1.0)
        else:
            prob_over = max((over_count / len(data)) - 0.15, 0.0)

        prob_under = 1.0 - prob_over

        prediction = "OVER" if prob_over > 0.5 else "UNDER"

        return {
            "prediction": prediction,
            "probability_over": round(prob_over, 4),
            "probability_under": round(prob_under, 4),
            "trend": round(trend, 4),
            "current_value": current
        }

    def analyze_matches_differs(self, data: List[float]) -> Dict[str, Any]:
        """Analyze if next value will match or differ from previous
        
        Args:
            data: Processed price data
            
        Returns:
            Dict with prediction and supporting data
        """
        if len(data) < 3:
            return {"prediction": None, "probability_match": 0.5, "probability_differ": 0.5}

        # Count matching vs differing patterns
        matches = 0
        differs = 0

        for i in range(1, len(data)):
            if abs(data[i] - data[i-1]) < 0.001:
                matches += 1
            else:
                differs += 1

        total = matches + differs
        prob_match = matches / total if total > 0 else 0.5
        prob_differ = 1.0 - prob_match

        prediction = "MATCH" if prob_match > 0.5 else "DIFFER"

        return {
            "prediction": prediction,
            "probability_match": round(prob_match, 4),
            "probability_differ": round(prob_differ, 4),
            "matches_count": matches,
            "differs_count": differs
        }

    def analyze_even_odd(self, data: List[float]) -> Dict[str, Any]:
        """Analyze if next digit will be even or odd
        
        Args:
            data: Processed price data
            
        Returns:
            Dict with prediction and supporting data
        """
        if len(data) == 0:
            return {"prediction": None, "probability_even": 0.5, "probability_odd": 0.5}

        # Convert last value to digit
        last_digit = int(abs(data[-1])) % 10

        # Count even/odd patterns from last digits
        even_count = 0
        odd_count = 0

        for value in data:
            digit = int(abs(value)) % 10
            if digit % 2 == 0:
                even_count += 1
            else:
                odd_count += 1

        total = even_count + odd_count
        prob_even = even_count / total if total > 0 else 0.5
        prob_odd = 1.0 - prob_even

        prediction = "EVEN" if prob_even > 0.5 else "ODD"

        return {
            "prediction": prediction,
            "probability_even": round(prob_even, 4),
            "probability_odd": round(prob_odd, 4),
            "last_digit": last_digit,
            "even_count": even_count,
            "odd_count": odd_count
        }

    def analyze_rise_fall(self, data: List[float]) -> Dict[str, Any]:
        """Analyze if price will rise or fall
        
        Args:
            data: Processed price data
            
        Returns:
            Dict with prediction and supporting data
        """
        if len(data) < 2:
            return {"prediction": None, "probability_rise": 0.5, "probability_fall": 0.5}

        current = data[-1]
        previous = data[-2]
        trend = calculate_trend(data)
        volatility = calculate_volatility(data)

        # Calculate rise/fall ratio
        rises = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
        falls = len(data) - 1 - rises

        # Base probability from historical data
        prob_rise = rises / len(data) if len(data) > 0 else 0.5

        # Adjust based on trend
        prob_rise += (trend * 0.1)
        prob_rise = max(0.0, min(1.0, prob_rise))
        prob_fall = 1.0 - prob_rise

        prediction = "RISE" if prob_rise > 0.5 else "FALL"

        return {
            "prediction": prediction,
            "probability_rise": round(prob_rise, 4),
            "probability_fall": round(prob_fall, 4),
            "trend": round(trend, 4),
            "volatility": round(volatility, 4),
            "recent_movement": round(current - previous, 4)
        }
