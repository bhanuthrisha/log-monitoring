from flask import Flask, render_template
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

# Get absolute path to the database
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / '..' / 'incidents.db'

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return dictionaries instead of tuples
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    incidents = conn.execute('''
        SELECT * FROM incidents 
        ORDER BY timestamp DESC 
        LIMIT 50
    ''').fetchall()
    conn.close()
    return render_template('dashboard.html', incidents=incidents)

if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    (BASE_DIR / 'templates').mkdir(exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)