"""Digit prediction model for 0-9 digit forecasting"""

import numpy as np
from typing import Dict, List, Any
from collections import Counter

from src.config import DIGIT_RANGE, MODEL_WEIGHTS
from src.utils.statistics import calculate_volatility


class DigitPredictor:
    """Predicts which digits (0-9) are most likely to occur"""

    def __init__(self):
        """Initialize digit predictor"""
        self.digit_range = DIGIT_RANGE
        self.weights = MODEL_WEIGHTS

    def predict_all_digits(self, data: List[float]) -> Dict[int, float]:
        """Predict probability for all digits 0-9
        
        Args:
            data: Historical price/value data
            
        Returns:
            Dict with digit: probability mapping
        """
        if not data:
            return {i: 1/10 for i in range(10)}

        predictions = {}

        for digit in self.digit_range:
            predictions[digit] = self._predict_single_digit(digit, data)

        # Normalize to ensure sum = 1
        total = sum(predictions.values())
        if total > 0:
            predictions = {k: v/total for k, v in predictions.items()}

        return predictions

    def _predict_single_digit(self, digit: int, data: List[float]) -> float:
        """Predict probability for a single digit
        
        Args:
            digit: Target digit (0-9)
            data: Historical data
            
        Returns:
            Probability score for the digit
        """
        # Extract last digits from data
        last_digits = [int(abs(val)) % 10 for val in data]

        # Count occurrences
        digit_counts = Counter(last_digits)
        frequency = digit_counts.get(digit, 0) / len(data) if data else 0

        # Calculate pattern strength
        pattern_strength = self._calculate_pattern_strength(digit, last_digits)

        # Trend adjustment
        trend_adjustment = self._calculate_trend_adjustment(digit, last_digits)

        # Recent bias
        recent_bias = self._calculate_recent_bias(digit, last_digits)

        # Volatility adjustment
        volatility = calculate_volatility(data)
        volatility_factor = 1 - (volatility * 0.1)

        # Weighted combination
        score = (
            frequency * self.weights["pattern_frequency"] +
            pattern_strength * self.weights["statistical_significance"] +
            trend_adjustment * self.weights["recent_trend"] +
            (recent_bias * volatility_factor) * 0.1
        )

        return max(0.0, score)

    def _calculate_pattern_strength(self, digit: int, last_digits: List[int]) -> float:
        """Calculate how strong the pattern is for a digit
        
        Args:
            digit: Target digit
            last_digits: List of last digits from data
            
        Returns:
            Pattern strength score
        """
        if not last_digits:
            return 0.0

        # Check for consecutive occurrences
        consecutive_count = 0
        max_consecutive = 0

        for d in last_digits:
            if d == digit:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 0

        # Pattern strength based on runs
        pattern_strength = min(max_consecutive / 5, 1.0)
        return pattern_strength

    def _calculate_trend_adjustment(self, digit: int, last_digits: List[int]) -> float:
        """Calculate trend adjustment for digit prediction
        
        Args:
            digit: Target digit
            last_digits: List of last digits
            
        Returns:
            Trend adjustment factor
        """
        if len(last_digits) < 2:
            return 0.0

        # Check if digit appeared more recently
        recent_occurrences = sum(1 for d in last_digits[-5:] if d == digit)
        older_occurrences = sum(1 for d in last_digits[:-5] if d == digit) if len(last_digits) > 5 else 0

        if len(last_digits) > 5:
            recent_rate = recent_occurrences / 5
            older_rate = older_occurrences / (len(last_digits) - 5)
            trend = recent_rate - older_rate
        else:
            trend = recent_occurrences / len(last_digits)

        return min(max(trend, -0.5), 0.5)

    def _calculate_recent_bias(self, digit: int, last_digits: List[int]) -> float:
        """Calculate bias based on recent occurrences
        
        Args:
            digit: Target digit
            last_digits: List of last digits
            
        Returns:
            Recent bias factor
        """
        if not last_digits:
            return 0.0

        # Recent occurrences with decay
        bias = 0.0
        decay = 1.0

        for i in range(len(last_digits) - 1, max(len(last_digits) - 10, -1), -1):
            if last_digits[i] == digit:
                bias += decay
            decay *= 0.8

        return min(bias / 10, 1.0)

    def get_digit_insights(self, data: List[float]) -> Dict[str, Any]:
        """Get detailed insights about digit patterns
        
        Args:
            data: Historical data
            
        Returns:
            Dict with detailed digit analysis
        """
        last_digits = [int(abs(val)) % 10 for val in data]
        digit_counts = Counter(last_digits)
        most_common = digit_counts.most_common(3)

        return {
            "total_values": len(data),
            "unique_digits": len(set(last_digits)),
            "most_common_digits": [digit for digit, _ in most_common],
            "digit_frequencies": dict(digit_counts),
            "entropy": self._calculate_entropy(last_digits)
        }

    def _calculate_entropy(self, digits: List[int]) -> float:
        """Calculate Shannon entropy of digit distribution
        
        Args:
            digits: List of digits
            
        Returns:
            Entropy value
        """
        if not digits:
            return 0.0

        counts = Counter(digits)
        total = len(digits)
        entropy = 0.0

        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)

        return entropy

import numpy as np
