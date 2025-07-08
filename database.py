import sqlite3
from datetime import datetime
from contextlib import contextmanager

class IncidentDB:
    def __init__(self, db_path='incidents.db'):
        self.db_path = db_path
        self._init_db()
        
    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()
            
    def _init_db(self):
        with self._get_cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    log_text TEXT,
                    prediction_score REAL,
                    resolved BOOLEAN DEFAULT 0,
                    alert_sent BOOLEAN DEFAULT 0
                )
            ''')
            
    def log_incident(self, log_data, score):
        with self._get_cursor() as c:
            c.execute('''
                INSERT INTO incidents (log_text, prediction_score)
                VALUES (?, ?)
            ''', (str(log_data), float(score)))
            
    def get_recent_incidents(self, limit=50):
        with self._get_cursor() as c:
            return c.execute('''
                SELECT * FROM incidents 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,)).fetchall()