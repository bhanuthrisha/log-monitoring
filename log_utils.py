import re
import json
from datetime import datetime

class LogCollector:
    @staticmethod
    def read_logs(file_path):
        with open(file_path) as f:
            for line in f:
                yield line.strip()

class LogPreprocessor:
    @staticmethod
    def parse(log_entry):
        patterns = {
            'nginx': r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<path>\S+).*?" (?P<status>\d+)',
            'app': r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<message>.+)'
        }
        
        for log_type, pattern in patterns.items():
            match = re.match(pattern, log_entry)
            if match:
                return {**match.groupdict(), 'log_type': log_type}
        return None

    @staticmethod
    def add_features(parsed_log):
        if not parsed_log:
            return None
            
        features = parsed_log.copy()
        
        if 'timestamp' in features:
            try:
                dt = datetime.strptime(features['timestamp'].split()[0], '%d/%b/%Y:%H:%M:%S')
                features['hour'] = dt.hour
                features['is_weekend'] = 1 if dt.weekday() >= 5 else 0
            except:
                pass
            
        if 'message' in features:
            features['error_keyword'] = 1 if any(
                kw in features['message'].lower() 
                for kw in ['fail', 'error', 'timeout']
            ) else 0
            
        return features