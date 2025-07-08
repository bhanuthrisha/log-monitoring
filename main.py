from log_utils import LogCollector, LogPreprocessor
from analysis_engine import AnomalyDetector, IncidentPredictor
import json

def main():
    # Initialize components
    collector = LogCollector()
    preprocessor = LogPreprocessor()
    detector = AnomalyDetector()
    predictor = IncidentPredictor()
    
    # Simulate training phase
    print("Training on normal logs...")
    normal_logs = []
    for log in collector.read_logs('sample_logs_normal.txt'):
        parsed = preprocessor.parse(log)
        if parsed:
            normal_logs.append(preprocessor.add_features(parsed))
    detector.train(normal_logs[:100])  # Use first 100 logs for training
    
    # Real-time monitoring
    print("\nStarting monitoring...")
    for log in collector.read_logs('sample_logs_live.txt'):
        parsed = preprocessor.parse(log)
        if not parsed:
            continue
            
        features = preprocessor.add_features(parsed)
        anomalies = detector.predict([features])
        predictor.add_anomalies(anomalies)
        
        if predictor.should_alert():
            print(f"\n🚨 INCIDENT PREDICTED! Pattern detected in logs:")
            print(json.dumps(features, indent=2))
            predictor.window = []  # Reset after alert

if __name__ == "__main__":
    main()