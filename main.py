#!/usr/bin/env python3
"""Main entry point for Deriv Analysis Tool"""

import json
from src.analyzer import DerivAnalyzer


def main():
    """Main function with example usage"""
    
    print("="*60)
    print("DERIV ANALYSIS TOOL - Market & Digit Predictions")
    print("="*60)
    
    # Initialize analyzer
    analyzer = DerivAnalyzer()
    
    # Example market data
    market_data = [
        1.2050, 1.2055, 1.2045, 1.2060, 1.2070,
        1.2065, 1.2075, 1.2080, 1.2070, 1.2085,
        1.2090, 1.2085, 1.2095, 1.2100, 1.2105,
        1.2110, 1.2115, 1.2120, 1.2115, 1.2125
    ]
    
    print("\n" + "-"*60)
    print("MARKET ANALYSIS PREDICTIONS")
    print("-"*60)
    
    # Get market predictions
    market_predictions = analyzer.predict_market(market_data)
    
    print("\n1. OVER/UNDER ANALYSIS:")
    ou = market_predictions["over_under"]
    print(f"   Prediction: {ou['prediction']}")
    print(f"   Probability Over: {ou['probability_over']*100:.2f}%")
    print(f"   Probability Under: {ou['probability_under']*100:.2f}%")
    print(f"   Confidence: {ou['confidence']*100:.2f}%")
    
    print("\n2. MATCHES/DIFFERS ANALYSIS:")
    md = market_predictions["matches_differs"]
    print(f"   Prediction: {md['prediction']}")
    print(f"   Probability Match: {md['probability_match']*100:.2f}%")
    print(f"   Probability Differ: {md['probability_differ']*100:.2f}%")
    print(f"   Confidence: {md['confidence']*100:.2f}%")
    
    print("\n3. EVEN/ODD ANALYSIS:")
    eo = market_predictions["even_odd"]
    print(f"   Prediction: {eo['prediction']}")
    print(f"   Probability Even: {eo['probability_even']*100:.2f}%")
    print(f"   Probability Odd: {eo['probability_odd']*100:.2f}%")
    print(f"   Confidence: {eo['confidence']*100:.2f}%")
    print(f"   Last Digit: {eo['last_digit']}")
    
    print("\n4. RISE/FALL ANALYSIS:")
    rf = market_predictions["rise_fall"]
    print(f"   Prediction: {rf['prediction']}")
    print(f"   Probability Rise: {rf['probability_rise']*100:.2f}%")
    print(f"   Probability Fall: {rf['probability_fall']*100:.2f}%")
    print(f"   Confidence: {rf['confidence']*100:.2f}%")
    
    print("\n" + "-"*60)
    print("DIGIT PREDICTIONS (0-9)")
    print("-"*60)
    
    # Get digit predictions
    digit_predictions = analyzer.predict_digits(market_data)
    
    print("\nDigit Confidence Percentages:")
    conf = digit_predictions["confidence_percentages"]
    for digit in sorted(conf.keys(), key=lambda x: conf[x], reverse=True):
        print(f"   Digit {digit}: {conf[digit]:.2f}%")
    
    print(f"\nMost Likely Digits: {digit_predictions['most_likely_digits']}")
    
    print("\n" + "-"*60)
    print("CONFIDENCE SCORES")
    print("-"*60)
    scores = analyzer.get_confidence_scores()
    for key, value in scores.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)
    
    # Export results
    analyzer.export_results("predictions_results.json")
    print("\nResults exported to: predictions_results.json")


if __name__ == "__main__":
    main()
