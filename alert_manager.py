import smtplib
from email.mime.text import MIMEText
from config import Config
import logging

class AlertManager:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
    def send_email(self, subject, body, recipients=None):
        if recipients is None:
            recipients = ["admin@yourdomain.com"]
            
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.config.EMAIL_FROM
        msg['To'] = ", ".join(recipients)
        
        try:
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.EMAIL_USER, self.config.EMAIL_PASSWORD)
                server.send_message(msg)
            self.logger.info("Email alert sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Email alert failed: {str(e)}")
            return False
            
    def send_slack(self, message):
        try:
            import requests
            response = requests.post(
                self.config.SLACK_WEBHOOK,
                json={"text": message},
                timeout=5  # 5-second timeout
            )
            if response.status_code == 200:
                self.logger.info("Slack alert sent successfully")
                return True
            else:
                self.logger.error(f"Slack returned status code {response.status_code}")
                return False
        except ImportError:
            self.logger.error("Requests library not installed. Run: pip install requests")
            return False
        except Exception as e:
            self.logger.error(f"Slack alert failed: {str(e)}")
            return False
            
    def trigger_alert(self, incident_data):
        message = f"🚨 Incident Detected\n{incident_data}"
        success = self.send_slack(message)
        success &= self.send_email("Incident Alert", message)
        return success