"""
ML-based Anomaly Detection with BrightData Merchant Intelligence
"""
import numpy as np
from typing import Tuple
from ..data.brightdata import merchant_intel


class AnomalyDetector:
    """
    Fraud detection using ML + merchant sentiment analysis
    """
    
    def __init__(self):
        # Base thresholds
        self.amount_threshold = 1000
        self.risk_threshold = 0.7
    
    def score_transaction(self, transaction) -> Tuple[float, bool]:
        """
        Score transaction combining ML features + BrightData intelligence
        """
        risk_score = 0.0
        
        # Feature 1: Amount-based risk
        amount = float(transaction.amount)
        if amount > self.amount_threshold:
            risk_score += 0.3
        elif amount > 500:
            risk_score += 0.2
        elif amount > 100:
            risk_score += 0.1
        
        # Feature 2: Merchant Intelligence (BrightData)
        merchant_risk = 0.0
        if transaction.merchant:
            merchant_data = merchant_intel(transaction.merchant.name)
            
            if merchant_data:
                # Sentiment analysis impact
                sentiment = merchant_data.get("sentiment_analysis", {})
                sentiment_score = sentiment.get("sentiment_score", 0)
                
                if sentiment_score < -0.3:
                    merchant_risk += 0.25
                elif sentiment_score < 0:
                    merchant_risk += 0.15
                
                # Fraud keywords impact
                fraud_keywords = len(sentiment.get("fraud_keywords_found", []))
                merchant_risk += min(fraud_keywords * 0.1, 0.3)
                
                # Overall risk category
                overall_risk = merchant_data.get("overall_risk", "LOW")
                risk_multipliers = {
                    "CRITICAL": 0.35,
                    "HIGH": 0.25,
                    "MEDIUM": 0.15,
                    "LOW": 0.0
                }
                merchant_risk += risk_multipliers.get(overall_risk, 0)
                
                # Trust score impact (inverted)
                trust_score = merchant_data.get("financial_intelligence", {}).get("trust_score", 50)
                if trust_score < 30:
                    merchant_risk += 0.2
                elif trust_score < 50:
                    merchant_risk += 0.1
        
        risk_score += merchant_risk
        
        # Feature 3: Time-based risk
        if transaction.timestamp:
            hour = transaction.timestamp.hour
            # 11 PM - 6 AM is high risk
            if hour >= 23 or hour <= 6:
                risk_score += 0.15
        
        # Feature 4: Existing risk score (if calculated before)
        if hasattr(transaction, 'risk_score') and transaction.risk_score:
            risk_score += float(transaction.risk_score) * 0.2
        
        # Cap at 1.0
        risk_score = min(risk_score, 1.0)
        
        # Determine if anomaly
        is_anomaly = risk_score > self.risk_threshold
        
        return round(risk_score, 3), is_anomaly
    
    def explain_risk_factors(self, transaction) -> dict:
        """
        Explain which factors contributed to risk score
        """
        factors = []
        
        amount = float(transaction.amount)
        if amount > self.amount_threshold:
            factors.append(f"Large transaction amount (${amount})")
        
        if transaction.merchant:
            merchant_data = merchant_intel(transaction.merchant.name)
            if merchant_data:
                overall_risk = merchant_data.get("overall_risk")
                if overall_risk in ["HIGH", "CRITICAL"]:
                    factors.append(f"Merchant risk level: {overall_risk}")
                
                sentiment = merchant_data.get("sentiment_analysis", {})
                fraud_keywords = sentiment.get("fraud_keywords_found", [])
                if fraud_keywords:
                    factors.append(f"Fraud indicators found: {', '.join(fraud_keywords)}")
                
                sentiment_score = sentiment.get("sentiment_score", 0)
                if sentiment_score < -0.3:
                    factors.append(f"Negative merchant sentiment ({sentiment_score})")
        
        if transaction.timestamp:
            hour = transaction.timestamp.hour
            if hour >= 23 or hour <= 6:
                factors.append(f"Unusual transaction time ({hour}:00)")
        
        return {
            "risk_factors": factors,
            "merchant_intelligence": merchant_data if transaction.merchant else None
        }
