"""Main Deriv Analyzer - Orchestrates market, digit, and volatility predictions"""

import json
from typing import Dict, List, Any
from datetime import datetime

from src.models.market_analyzer import MarketAnalyzer
from src.models.digit_predictor import DigitPredictor
from src.models.confidence_scorer import ConfidenceScorer
from src.models.volatility_analyzer import VolatilityAnalyzer
from src.utils.data_processor import DataProcessor
from src.config import CONFIDENCE_THRESHOLD


class DerivAnalyzer:
    """Main analyzer class for derivatives market predictions"""

    def __init__(self):
        """Initialize the analyzer with all prediction models"""
        self.market_analyzer = MarketAnalyzer()
        self.digit_predictor = DigitPredictor()
        self.confidence_scorer = ConfidenceScorer()
        self.volatility_analyzer = VolatilityAnalyzer()
        self.data_processor = DataProcessor()
        self.prediction_history = []

    def predict_market(self, data: List[float]) -> Dict[str, Any]:
        """Predict market movements using multiple analysis models
        
        Args:
            data: List of historical price/value data points
            
        Returns:
            Dict containing predictions for:
                - over_under: Next value over/under current
                - matches_differs: Value matches/differs previous
                - even_odd: Digit is even/odd
                - rise_fall: Price rises/falls
                - volatility: Market volatility metrics
        """
        if not self.data_processor.validate_data(data):
            return {"error": "Invalid data provided"}

        # Process data
        processed_data = self.data_processor.process(data)

        # Get predictions from each model
        predictions = {
            "over_under": self.market_analyzer.analyze_over_under(processed_data),
            "matches_differs": self.market_analyzer.analyze_matches_differs(processed_data),
            "even_odd": self.market_analyzer.analyze_even_odd(processed_data),
            "rise_fall": self.market_analyzer.analyze_rise_fall(processed_data)
        }

        # Calculate confidence scores
        for key in predictions:
            confidence = self.confidence_scorer.calculate_confidence(
                predictions[key], processed_data, key
            )
            predictions[key]["confidence"] = confidence

        # Add volatility analysis
        volatility_data = self.volatility_analyzer.analyze_volatility(processed_data)
        predictions["volatility"] = volatility_data

        # Add metadata
        predictions["timestamp"] = datetime.now().isoformat()
        predictions["data_points_analyzed"] = len(data)

        # Store in history
        self.prediction_history.append(predictions)

        return predictions

    def predict_digits(self, data: List[float]) -> Dict[str, Any]:
        """Predict digit outcomes with confidence percentages
        
        Args:
            data: List of historical price/value data points
            
        Returns:
            Dict containing:
                - digit_predictions: Probability for each digit 0-9
                - confidence_percentages: Confidence % for each digit
                - most_likely_digits: Top 3 most likely digits
                - weighted_scores: Weighted confidence scores
                - volatility: Market volatility metrics
        """
        if not self.data_processor.validate_data(data):
            return {"error": "Invalid data provided"}

        # Get digit predictions
        predictions = self.digit_predictor.predict_all_digits(data)
        confidence_scores = self.confidence_scorer.calculate_digit_confidence(data, predictions)

        # Calculate percentages
        total_confidence = sum(confidence_scores.values())
        confidence_percentages = {}
        
        for digit in range(10):
            digit_str = str(digit)
            if total_confidence > 0:
                confidence_percentages[digit_str] = round(
                    (confidence_scores.get(digit_str, 0) / total_confidence) * 100, 2
                )
            else:
                confidence_percentages[digit_str] = 0.0

        # Get top 3 most likely digits
        sorted_digits = sorted(
            confidence_percentages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        most_likely = [int(digit) for digit, _ in sorted_digits]

        # Add volatility analysis
        volatility_data = self.volatility_analyzer.analyze_volatility(data)

        result = {
            "digit_predictions": predictions,
            "confidence_percentages": confidence_percentages,
            "most_likely_digits": most_likely,
            "weighted_scores": confidence_scores,
            "volatility": volatility_data,
            "timestamp": datetime.now().isoformat(),
            "data_points_analyzed": len(data)
        }

        # Store in history
        self.prediction_history.append(result)

        return result

    def get_confidence_scores(self) -> Dict[str, float]:
        """Get current confidence scores for all predictions
        
        Returns:
            Dict with confidence metrics and statistics
        """
        if not self.prediction_history:
            return {"error": "No predictions available yet"}

        latest = self.prediction_history[-1]
        scores = {}

        if "over_under" in latest:
            # Market predictions
            for key in ["over_under", "matches_differs", "even_odd", "rise_fall"]:
                if key in latest and "confidence" in latest[key]:
                    scores[key] = latest[key]["confidence"]
        else:
            # Digit predictions
            scores["average_confidence"] = sum(
                latest["confidence_percentages"].values()
            ) / 10
            scores["max_confidence"] = max(
                latest["confidence_percentages"].values()
            )
            scores["min_confidence"] = min(
                latest["confidence_percentages"].values()
            )

        scores["total_predictions"] = len(self.prediction_history)
        return scores

    def get_volatility_report(self) -> Dict[str, Any]:
        """Get comprehensive volatility report
        
        Returns:
            Dict with volatility analysis and trends
        """
        return self.volatility_analyzer.get_volatility_report()

    def get_volatility_comparison(self, limit: int = 5) -> Dict[str, Any]:
        """Compare volatility across recent periods
        
        Args:
            limit: Number of periods to compare
            
        Returns:
            Dict with volatility comparison data
        """
        return self.volatility_analyzer.compare_volatility_periods(limit)

    def get_prediction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent prediction history
        
        Args:
            limit: Number of recent predictions to return
            
        Returns:
            List of prediction results
        """
        return self.prediction_history[-limit:]

    def export_results(self, filename: str) -> bool:
        """Export prediction history to JSON file
        
        Args:
            filename: Output filename
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.prediction_history, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error exporting results: {e}")
            return False
