"""Tests for main analyzer module"""

import pytest
from src.analyzer import DerivAnalyzer


class TestDerivAnalyzer:
    """Test suite for DerivAnalyzer"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return DerivAnalyzer()

    @pytest.fixture
    def sample_data(self):
        """Sample market data"""
        return [1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27, 1.28, 1.29]

    def test_market_prediction_structure(self, analyzer, sample_data):
        """Test market prediction returns proper structure"""
        result = analyzer.predict_market(sample_data)
        
        assert "over_under" in result
        assert "matches_differs" in result
        assert "even_odd" in result
        assert "rise_fall" in result
        assert "timestamp" in result

    def test_digit_prediction_structure(self, analyzer, sample_data):
        """Test digit prediction returns proper structure"""
        result = analyzer.predict_digits(sample_data)
        
        assert "digit_predictions" in result
        assert "confidence_percentages" in result
        assert "most_likely_digits" in result
        assert len(result["confidence_percentages"]) == 10

    def test_confidence_scores(self, analyzer, sample_data):
        """Test confidence score calculation"""
        analyzer.predict_market(sample_data)
        scores = analyzer.get_confidence_scores()
        
        assert "over_under" in scores or "average_confidence" in scores

    def test_invalid_data_handling(self, analyzer):
        """Test handling of invalid data"""
        result = analyzer.predict_market([])
        assert "error" in result or len(result) == 0

    def test_prediction_history(self, analyzer, sample_data):
        """Test prediction history tracking"""
        analyzer.predict_market(sample_data)
        analyzer.predict_digits(sample_data)
        
        history = analyzer.get_prediction_history(limit=10)
        assert len(history) >= 2
