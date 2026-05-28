"""Data processing utilities"""

import numpy as np
from typing import List, Any

from src.config import MIN_DATA_POINTS, MAX_LOOKBACK_PERIODS


class DataProcessor:
    """Handles data validation and processing"""

    def __init__(self):
        """Initialize data processor"""
        self.min_points = MIN_DATA_POINTS
        self.max_lookback = MAX_LOOKBACK_PERIODS

    def validate_data(self, data: List[float]) -> bool:
        """Validate input data
        
        Args:
            data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not data:
            return False

        if len(data) < 2:
            return False

        # Check for invalid values
        try:
            for val in data:
                if not np.isfinite(val):
                    return False
        except (TypeError, ValueError):
            return False

        return True

    def process(self, data: List[float]) -> List[float]:
        """Process and normalize data
        
        Args:
            data: Raw input data
            
        Returns:
            Processed data
        """
        if not self.validate_data(data):
            return []

        # Convert to numpy array
        arr = np.array(data, dtype=float)

        # Handle outliers using z-score
        arr = self._remove_outliers(arr)

        # Limit lookback period
        if len(arr) > self.max_lookback:
            arr = arr[-self.max_lookback:]

        return arr.tolist()

    def _remove_outliers(self, data: np.ndarray) -> np.ndarray:
        """Remove outliers from data using z-score
        
        Args:
            data: Input array
            
        Returns:
            Data with outliers removed
        """
        if len(data) < 3:
            return data

        # Calculate z-scores
        mean = np.mean(data)
        std = np.std(data)

        if std == 0:
            return data

        z_scores = np.abs((data - mean) / std)

        # Keep values with z-score < 3
        return data[z_scores < 3]

    def normalize(self, data: List[float]) -> List[float]:
        """Normalize data to 0-1 range
        
        Args:
            data: Input data
            
        Returns:
            Normalized data
        """
        if not data:
            return []

        arr = np.array(data, dtype=float)
        min_val = np.min(arr)
        max_val = np.max(arr)

        if max_val - min_val == 0:
            return [0.5] * len(data)

        normalized = (arr - min_val) / (max_val - min_val)
        return normalized.tolist()

    def standardize(self, data: List[float]) -> List[float]:
        """Standardize data (z-score normalization)
        
        Args:
            data: Input data
            
        Returns:
            Standardized data
        """
        if len(data) < 2:
            return data

        arr = np.array(data, dtype=float)
        mean = np.mean(arr)
        std = np.std(arr)

        if std == 0:
            return data

        standardized = (arr - mean) / std
        return standardized.tolist()
