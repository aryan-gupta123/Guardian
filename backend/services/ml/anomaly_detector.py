import os
from django.conf import settings
import random


class AnomalyDetector:
    def __init__(self):
        # Simple dummy detector - no ML dependencies
        self.is_trained = True
    
    def train(self, transactions):
        """Dummy training - no actual ML"""
        pass
    
    def score_transaction(self, transaction):
        """Dummy scoring - returns random risk scores"""
        # Simple dummy scoring based on amount
        amount = float(transaction.amount) if hasattr(transaction, 'amount') else 100.0
        
        # Higher amounts = higher risk (simple rule)
        if amount > 1000:
            risk_score = 0.8
            is_anomaly = True
        elif amount > 500:
            risk_score = 0.6
            is_anomaly = False
        else:
            risk_score = 0.2
            is_anomaly = False
            
        return risk_score, is_anomaly

