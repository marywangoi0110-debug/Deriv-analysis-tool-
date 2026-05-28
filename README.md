# Deriv Analysis Tool

A comprehensive derivatives market analysis tool that provides predictive analytics for binary options and digital markets. This tool analyzes market trends using multiple prediction models including over/under, matches/differs, even/odd, and rise/fall patterns.

## Features

### Market Analysis
- **Over/Under Analysis**: Predicts whether next value will be over or under current level
- **Matches/Differs Analysis**: Predicts whether value will match or differ from previous values
- **Even/Odd Analysis**: Predicts whether the digit will be even or odd
- **Rise/Fall Analysis**: Predicts whether price will rise or fall

### Digit Predictions
- Analyzes individual digits (0-9)
- Provides confidence percentages for each digit
- Weighted prediction models based on historical patterns
- Real-time confidence calculations

### Analysis Features
- Pattern recognition and trend analysis
- Statistical confidence scoring
- Multi-factor prediction weighting
- Historical data processing
- Market volatility assessment

## Installation

```bash
git clone https://github.com/marywangoi0110-debug/Deriv-analysis-tool-.git
cd Deriv-analysis-tool-
pip install -r requirements.txt
```

## Quick Start

```python
from src.analyzer import DerivAnalyzer

# Initialize the analyzer
analyzer = DerivAnalyzer()

# Get market predictions
market_pred = analyzer.predict_market([1, 2, 3, 4, 5])
print(market_pred)

# Get digit predictions with confidence
digit_pred = analyzer.predict_digits([1, 2, 3, 4, 5])
print(digit_pred)
```

## Project Structure

```
Deriv-analysis-tool-/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── market_analyzer.py
│   │   ├── digit_predictor.py
│   │   └── confidence_scorer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   ├── pattern_detector.py
│   │   └── statistics.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py
└── data/
    └── sample_data.json
```

## API Reference

### DerivAnalyzer

#### predict_market(data)
Predicts market movements using multiple analysis models.
- **Returns**: Dict with over/under, matches/differs, even/odd, and rise/fall predictions

#### predict_digits(data)
Predicts digit outcomes with confidence scores.
- **Returns**: Dict with digit probabilities and confidence percentages

#### get_confidence_scores()
Returns current confidence scores for all predictions.
- **Returns**: Dict with confidence metrics

## Author

marywangoi0110-debug

## License

MIT License
