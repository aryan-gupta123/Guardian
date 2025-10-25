from .anomaly_detector import AnomalyDetector


class ExplainabilityService:
    def __init__(self):
        self.detector = AnomalyDetector()
    
    def explain_transaction(self, transaction):
        """Dummy explanation - simple rule-based"""
        amount = float(transaction.amount) if hasattr(transaction, 'amount') else 100.0
        
        if amount > 1000:
            return {
                'explanation': 'High amount transaction detected',
                'top_features': [
                    {'feature': 'amount', 'value': amount, 'importance': 0.9, 'contribution': 0.8}
                ],
                'risk_factors': [
                    {'feature': 'amount', 'value': amount, 'reason': f'Unusually high amount: ${amount:.2f}'}
                ],
                'is_anomaly': True
            }
        elif amount > 500:
            return {
                'explanation': 'Medium amount transaction',
                'top_features': [
                    {'feature': 'amount', 'value': amount, 'importance': 0.6, 'contribution': 0.4}
                ],
                'risk_factors': [],
                'is_anomaly': False
            }
        else:
            return {
                'explanation': 'Low amount transaction - normal',
                'top_features': [
                    {'feature': 'amount', 'value': amount, 'importance': 0.2, 'contribution': 0.1}
                ],
                'risk_factors': [],
                'is_anomaly': False
            }
    
    def _get_risk_reason(self, feature_name, value):
        """Get human-readable reason for why a feature contributes to risk"""
        return f"Unusual {feature_name}: {value}"

