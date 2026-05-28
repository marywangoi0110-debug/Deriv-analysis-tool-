# Deriv Analysis Tool - Quick Access Guide

## 🚀 **Quick Start - How to Access During Trading**

### **Option 1: Web API (Recommended for Live Trading)**

#### Start the API Server:
```bash
python api_server.py
```

Server runs on: `http://localhost:5000`

#### Example API Calls:

**1. Market Predictions:**
```bash
curl -X POST http://localhost:5000/api/market-predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.20, 1.21, 1.22, 1.23, 1.24]}'
```

**2. Digit Predictions:**
```bash
curl -X POST http://localhost:5000/api/digit-predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.20, 1.21, 1.22, 1.23, 1.24]}'
```

**3. Get Confidence Scores:**
```bash
curl http://localhost:5000/api/confidence-scores
```

**4. Get Volatility Report:**
```bash
curl http://localhost:5000/api/volatility-report
```

---

### **Option 2: Interactive Trading CLI**

#### Start CLI Interface:
```bash
python trading_cli.py
```

#### Features:
- ✅ Enter live market data
- ✅ Get instant predictions
- ✅ View confidence scores
- ✅ Check volatility metrics
- ✅ Export results

---

### **Option 3: Python Script Integration**

Use directly in your trading bot:

```python
from src.analyzer import DerivAnalyzer

# Initialize
analyzer = DerivAnalyzer()

# Get live market data (example)
market_data = [1.20, 1.21, 1.22, 1.23, 1.24]

# Market predictions
market_pred = analyzer.predict_market(market_data)
print(f"Over/Under: {market_pred['over_under']['prediction']}")
print(f"Confidence: {market_pred['over_under']['confidence']}")

# Digit predictions
digit_pred = analyzer.predict_digits(market_data)
print(f"Top Digits: {digit_pred['most_likely_digits']}")
print(f"Digit 5 Confidence: {digit_pred['confidence_percentages']['5']:.2f}%")

# Volatility
vol = market_pred['volatility']
print(f"Volatility Level: {vol['volatility_level']}")
```

---

### **Option 4: Docker Container**

#### Build Docker Image:
```bash
docker build -t deriv-analysis .
```

#### Run Container:
```bash
docker run -p 5000:5000 deriv-analysis
```

---

## 📋 **Installation**

### Update requirements.txt:
```bash
pip install -r requirements.txt
```

Add Flask for API:
```bash
pip install Flask flask-cors
```

---

## 🔌 **Integration with Trading Platforms**

### **For Deriv Binary Options:**

```python
# Example integration
from src.analyzer import DerivAnalyzer
import requests
import json

analyzer = DerivAnalyzer()

def make_trade(symbol, amount, market_data):
    # Get predictions
    predictions = analyzer.predict_market(market_data)
    
    # Make decision based on confidence
    if predictions['rise_fall']['prediction'] == 'RISE':
        # Place CALL trade
        if predictions['rise_fall']['confidence'] > 0.7:
            print(f"✓ CALL Trade: High confidence ({predictions['rise_fall']['confidence']*100:.1f}%)")
            # Make API call to your trading platform
        else:
            print(f"⚠ CALL Trade: Medium confidence")
    else:
        # Place PUT trade
        if predictions['rise_fall']['prediction'] == 'FALL':
            print(f"✓ PUT Trade")
```

---

## 📊 **Output Example**

### API Response:
```json
{
  "status": "success",
  "timestamp": "2026-05-28T02:50:30.123456",
  "predictions": {
    "over_under": {
      "prediction": "OVER",
      "probability_over": 0.65,
      "probability_under": 0.35,
      "confidence": 0.62
    },
    "rise_fall": {
      "prediction": "RISE",
      "probability_rise": 0.68,
      "probability_fall": 0.32,
      "confidence": 0.65,
      "trend": 0.15,
      "volatility": 0.012345
    },
    "volatility": {
      "historical_volatility": 0.012345,
      "realized_volatility": 0.011234,
      "volatility_level": "LOW",
      "volatility_trend": "STABLE"
    }
  }
}
```

---

## ⚙️ **Configuration**

Edit `src/config.py` to customize:
- Confidence thresholds
- Data processing parameters
- Model weights
- Volatility calculations

---

## 🎯 **Trading Strategy Example**

```python
from src.analyzer import DerivAnalyzer

class TradingStrategy:
    def __init__(self):
        self.analyzer = DerivAnalyzer()
    
    def execute(self, market_data, amount):
        # Get predictions
        pred = self.analyzer.predict_market(market_data)
        
        # Decision logic
        risk_level = pred['volatility']['volatility_level']
        
        if risk_level in ['LOW', 'MODERATE']:
            confidence = pred['rise_fall']['confidence']
            
            if confidence > 0.75:
                direction = pred['rise_fall']['prediction']
                print(f"🎯 {direction} with {confidence*100:.1f}% confidence")
                # Execute trade
            elif confidence > 0.60:
                print(f"⚠️  Wait for better signal")
        else:
            print(f"🛑 High volatility - Skip this trade")

# Use it
strategy = TradingStrategy()
strategy.execute([1.20, 1.21, 1.22], 100)
```

---

## 🔐 **Best Practices**

1. **Always check volatility** before trading
2. **Require minimum confidence** (e.g., > 65%)
3. **Use proper position sizing**
4. **Monitor prediction history** for accuracy
5. **Update data frequently** for fresh predictions
6. **Export results** for audit trail

---

## 📞 **API Endpoints Summary**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API Documentation |
| `/api/market-predict` | POST | Market predictions |
| `/api/digit-predict` | POST | Digit predictions |
| `/api/volatility-report` | GET | Volatility metrics |
| `/api/confidence-scores` | GET | Confidence scores |
| `/api/prediction-history` | GET | Recent history |
| `/api/export` | POST | Export results |
| `/health` | GET | Health check |

---

## 💡 **Tips for Best Results**

- Use at least 20+ historical data points
- Update predictions every 5-10 seconds for live trading
- Combine with your own risk management
- Don't rely on predictions alone - use with technical analysis
- Backtest your strategy first

---

Happy Trading! 🚀
