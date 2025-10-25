import numpy as np
from sklearn.inspection import permutation_importance
from .anomaly_detector import AnomalyDetector


class ExplainabilityService:
    def __init__(self):
        self.detector = AnomalyDetector()
        self.feature_names = [
            'amount',
            'hour_of_day',
            'day_of_week',
            'transaction_frequency',
            'avg_transaction_amount',
            'location_risk_score',
            'merchant_risk_score',
            'time_since_last_transaction',
            'device_trust_score'
        ]
    
    def explain_transaction(self, transaction):
        """Provide explanation for why a transaction was flagged as anomalous"""
        if not self.detector.is_trained:
            return {
                'explanation': 'Model not trained yet',
                'top_features': [],
                'risk_factors': []
            }
        
        # Extract features
        features = self.detector._extract_features(transaction)
        features_scaled = self.detector.scaler.transform(features)
        
        # Get base prediction
        base_score = self.detector.model.decision_function(features_scaled)[0]
        
        # Calculate feature importance by permuting each feature
        feature_importance = []
        
        for i in range(len(self.feature_names)):
            # Create modified feature set with this feature permuted
            modified_features = features_scaled.copy()
            np.random.shuffle(modified_features[0, i:i+1])
            
            # Get score with permuted feature
            modified_score = self.detector.model.decision_function(modified_features)[0]
            
            # Importance is the difference in scores
            importance = abs(base_score - modified_score)
            feature_importance.append({
                'feature': self.feature_names[i],
                'value': features[0, i],
                'importance': importance,
                'contribution': base_score - modified_score
            })
        
        # Sort by importance
        feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        
        # Get top contributing features
        top_features = feature_importance[:5]
        
        # Identify risk factors
        risk_factors = []
        for feature in top_features:
            if feature['contribution'] > 0:  # Positive contribution to anomaly score
                risk_factors.append({
                    'feature': feature['feature'],
                    'value': feature['value'],
                    'reason': self._get_risk_reason(feature['feature'], feature['value'])
                })
        
        return {
            'explanation': f"Transaction scored {base_score:.3f} (lower is more anomalous)",
            'top_features': top_features,
            'risk_factors': risk_factors,
            'is_anomaly': base_score < 0
        }
    
    def _get_risk_reason(self, feature_name, value):
        """Get human-readable reason for why a feature contributes to risk"""
        reasons = {
            'amount': f"Unusually high amount: ${value:.2f}",
            'hour_of_day': f"Transaction at unusual hour: {int(value)}:00",
            'day_of_week': f"Transaction on {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][int(value)]}",
            'transaction_frequency': f"High transaction frequency: {value:.1f}",
            'avg_transaction_amount': f"Above average transaction amount: ${value:.2f}",
            'location_risk_score': f"High location risk: {value:.2f}",
            'merchant_risk_score': f"High merchant risk: {value:.2f}",
            'time_since_last_transaction': f"Short time since last transaction: {value:.1f} minutes",
            'device_trust_score': f"Low device trust score: {value:.2f}"
        }
        return reasons.get(feature_name, f"Unusual {feature_name}: {value}")

