"""Configuration settings for Deriv Analysis Tool"""

import os

# Analysis Configuration
CONFIDENCE_THRESHOLD = 0.5
MIN_DATA_POINTS = 10
MAX_LOOKBACK_PERIODS = 100

# Digit Configuration
DIGIT_RANGE = list(range(10))  # 0-9
DIGIT_CONFIDENCE_SMOOTHING = 0.1

# Market Analysis Configuration
MARKET_PATTERNS = {
    "over_under": "Predicts if next value is over or under current",
    "matches_differs": "Predicts if value matches or differs from previous",
    "even_odd": "Predicts if digit is even or odd",
    "rise_fall": "Predicts if price rises or falls"
}

# Statistical Configuration
ZSCORE_THRESHOLD = 1.96  # 95% confidence
SMA_PERIOD = 5
EMA_PERIOD = 5

# Data Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")

# Model Weights
MODEL_WEIGHTS = {
    "recent_trend": 0.35,
    "pattern_frequency": 0.30,
    "volatility_adjustment": 0.20,
    "statistical_significance": 0.15
}
