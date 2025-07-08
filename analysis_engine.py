import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.vectorizer = TfidfVectorizer(max_features=50)
        
    def train(self, normal_logs):
        texts = [log.get('message','') for log in normal_logs]
        self.vectorizer.fit(texts)
        X = self._extract_features(normal_logs)
        self.model.fit(X)
    
    def predict(self, new_logs):
        X = self._extract_features(new_logs)
        return self.model.predict(X)
    
    def _extract_features(self, logs):
        texts = [log.get('message','') for log in logs]
        text_features = self.vectorizer.transform(texts).toarray()
        
        num_features = np.array([
            [
                log.get('hour', 0),
                log.get('is_weekend', 0),
                log.get('error_keyword', 0),
                int(log.get('status', 200)) // 100
            ] for log in logs
        ])
        
        return np.hstack([text_features, num_features])

class IncidentPredictor:
    def __init__(self, window_size=5):
        self.window = []
        self.window_size = window_size
        
    def add_anomalies(self, anomalies):
        self.window.append(sum(anomalies == -1))
        if len(self.window) > self.window_size:
            self.window.pop(0)
    
    def should_alert(self):
        return sum(self.window) >= 3