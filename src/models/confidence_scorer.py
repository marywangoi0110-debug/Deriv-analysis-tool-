"""Confidence scoring for predictions"""

import numpy as np
from typing import Dict, List, Any

from src.utils.statistics import calculate_volatility
from src.config import CONFIDENCE_THRESHOLD


class ConfidenceScorer:
    """Calculates confidence scores for predictions"""

    def __init__(self):
        """Initialize confidence scorer"""
        self.min_confidence = 0.0
        self.max_confidence = 1.0

    def calculate_confidence(self, prediction: Dict[str, Any], data: List[float], 
                            prediction_type: str) -> float:
        """Calculate confidence for a market prediction
        
        Args:
            prediction: Prediction dict with probabilities
            data: Historical data used for prediction
            prediction_type: Type of prediction (over_under, etc.)
            
        Returns:
            Confidence score between 0 and 1
        """
        if not data or len(data) < 2:
            return CONFIDENCE_THRESHOLD

        # Get probability difference from 0.5 (50%)
        if prediction_type == "over_under":
            max_prob = max(prediction["probability_over"], prediction["probability_under"])
        elif prediction_type == "matches_differs":
            max_prob = max(prediction["probability_match"], prediction["probability_differ"])
        elif prediction_type == "even_odd":
            max_prob = max(prediction["probability_even"], prediction["probability_odd"])
        elif prediction_type == "rise_fall":
            max_prob = max(prediction["probability_rise"], prediction["probability_fall"])
        else:
            max_prob = 0.5

        # Base confidence on probability deviation from 50%
        prob_confidence = (max_prob - 0.5) * 2  # Scale to 0-1

        # Data quality factor
        data_quality = self._calculate_data_quality(data)

        # Consistency factor
        consistency = self._calculate_consistency(data, prediction_type)

        # Volatility adjustment
        volatility = calculate_volatility(data)
        volatility_factor = max(0.5, 1 - (volatility * 0.5))

        # Combine factors
        confidence = (
            prob_confidence * 0.40 +
            data_quality * 0.25 +
            consistency * 0.20 +
            volatility_factor * 0.15
        )

        return round(max(0.0, min(1.0, confidence)), 4)

    def calculate_digit_confidence(self, data: List[float], 
                                  predictions: Dict[int, float]) -> Dict[str, float]:
        """Calculate confidence scores for digit predictions
        
        Args:
            data: Historical data
            predictions: Digit predictions (0-9)
            
        Returns:
            Dict with digit: confidence mapping
        """
        if not data:
            return {str(i): 0.1 for i in range(10)}

        # Extract last digits
        last_digits = [int(abs(val)) % 10 for val in data]

        # Calculate base confidence factors
        data_quality = self._calculate_data_quality(data)
        volatility = calculate_volatility(data)
        volatility_factor = max(0.5, 1 - (volatility * 0.3))

        confidence_scores = {}

        for digit in range(10):
            digit_str = str(digit)

            # Prediction strength
            prediction_strength = predictions.get(digit, 0.1)

            # Frequency in data
            frequency = last_digits.count(digit) / len(last_digits) if last_digits else 0.1

            # Recent occurrence boost
            recent_boost = 1.0 if last_digits[-1] == digit else 0.9

            # Combined confidence
            confidence = (
                prediction_strength * 0.35 +
                frequency * 0.25 +
                data_quality * 0.20 +
                (volatility_factor * recent_boost) * 0.20
            )

            confidence_scores[digit_str] = round(max(0.0, min(1.0, confidence)), 4)

        return confidence_scores

    def _calculate_data_quality(self, data: List[float]) -> float:
        """Calculate quality score of input data
        
        Args:
            data: Input data
            
        Returns:
            Quality score 0-1
        """
        if not data:
            return 0.0

        quality = 0.5  # Base quality

        # More data points = better
        if len(data) >= 50:
            quality += 0.3
        elif len(data) >= 20:
            quality += 0.2
        elif len(data) >= 10:
            quality += 0.1

        # Check for NaN/Inf
        has_invalid = any(not np.isfinite(x) for x in data)
        if not has_invalid:
            quality += 0.2

        return min(quality, 1.0)

    def _calculate_consistency(self, data: List[float], prediction_type: str) -> float:
        """Calculate consistency of patterns in data
        
        Args:
            data: Historical data
            prediction_type: Type of prediction
            
        Returns:
            Consistency score 0-1
        """
        if len(data) < 3:
            return 0.5

        consistency = 0.5

        if prediction_type == "over_under":
            # Check consistency of over/under pattern
            pattern = [data[i] > data[i-1] for i in range(1, len(data))]
            transitions = sum(1 for i in range(1, len(pattern)) if pattern[i] != pattern[i-1])
            consistency = 1 - (transitions / len(pattern)) if len(pattern) > 1 else 0.5

        elif prediction_type == "rise_fall":
            # Similar to over_under
            changes = [data[i] != data[i-1] for i in range(1, len(data))]
            consistency = sum(changes) / len(changes) if changes else 0.5

        return min(max(consistency, 0.0), 1.0)


import numpy as np
