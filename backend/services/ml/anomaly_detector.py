import os
from django.conf import settings

try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML dependencies not available. Anomaly detection will be disabled.")


class AnomalyDetector:
    def __init__(self):
        if not ML_AVAILABLE:
            self.model = None
            self.scaler = None
            self.is_trained = False
            return
            
        self.model = IsolationForest(
            contamination=0.1,  # Expected proportion of anomalies
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = os.path.join(settings.BASE_DIR, 'backend', 'services', 'ml', 'models')
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model if it exists"""
        model_file = os.path.join(self.model_path, 'isolation_forest.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')
        
        if os.path.exists(model_file) and os.path.exists(scaler_file):
            self.model = joblib.load(model_file)
            self.scaler = joblib.load(scaler_file)
            self.is_trained = True
    
    def _save_model(self):
        """Save trained model"""
        os.makedirs(self.model_path, exist_ok=True)
        model_file = os.path.join(self.model_path, 'isolation_forest.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')
        
        joblib.dump(self.model, model_file)
        joblib.dump(self.scaler, scaler_file)
    
    def _extract_features(self, transaction):
        """Extract features from transaction for anomaly detection"""
        features = []
        
        # Basic transaction features
        features.append(float(transaction.amount))
        features.append(transaction.timestamp.hour)  # Hour of day
        features.append(transaction.timestamp.weekday())  # Day of week
        
        # Additional features from transaction.features dict
        if hasattr(transaction, 'features') and transaction.features:
            feature_dict = transaction.features
            features.extend([
                feature_dict.get('transaction_frequency', 0),
                feature_dict.get('avg_transaction_amount', 0),
                feature_dict.get('location_risk_score', 0),
                feature_dict.get('merchant_risk_score', 0),
                feature_dict.get('time_since_last_transaction', 0),
                feature_dict.get('device_trust_score', 0),
            ])
        else:
            # Default values if features not available
            features.extend([0, 0, 0, 0, 0, 0])
        
        return np.array(features).reshape(1, -1)
    
    def train(self, transactions):
        """Train the anomaly detection model"""
        if not transactions:
            return
        
        # Extract features from all transactions
        X = []
        for transaction in transactions:
            features = self._extract_features(transaction)
            X.append(features.flatten())
        
        X = np.array(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(X_scaled)
        self.is_trained = True
        
        # Save the trained model
        self._save_model()
    
    def score_transaction(self, transaction):
        """Score a single transaction for anomaly detection"""
        if not ML_AVAILABLE:
            # Return default scores if ML not available
            return 0.5, False
            
        if not self.is_trained:
            # Return default scores if model not trained
            return 0.5, False
        
        # Extract features
        features = self._extract_features(transaction)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get anomaly score (-1 to 1, where -1 is most anomalous)
        anomaly_score = self.model.decision_function(features_scaled)[0]
        
        # Convert to risk score (0 to 1, where 1 is highest risk)
        risk_score = (1 - anomaly_score) / 2
        risk_score = max(0, min(1, risk_score))  # Clamp to [0, 1]
        
        # Determine if anomaly (score < 0 means anomaly)
        is_anomaly = self.model.predict(features_scaled)[0] == -1
        
        return risk_score, is_anomaly

