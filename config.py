# Application Configuration
class Config:
    # Log Processing
    LOG_PATTERNS = {
        'nginx': r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<path>\S+).*?" (?P<status>\d+)',
        'app': r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<message>.+)'
    }
    
    # Alert Thresholds
    ANOMALY_THRESHOLD = 0.9
    CONSECUTIVE_ERRORS_FOR_ALERT = 3
    
    # Email Settings
    SMTP_SERVER = "smtp.yourmailserver.com"
    SMTP_PORT = 587
    EMAIL_FROM = "alerts@yourdomain.com"
    
    # Slack Webhook
    SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK"
    
    
    # ... (existing config)
    
    # Email Authentication
    EMAIL_USER = "your_username@yourdomain.com"
    EMAIL_PASSWORD = "your_email_password"
    
    # Timeout Settings
    SLACK_TIMEOUT = 5  # seconds