from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentName TEXT NOT NULL,
            studentID TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    studentName = data.get('studentName')
    studentID = data.get('studentID')
    category = data.get('category')
    message = data.get('message')

    if not studentName or not studentID or not category or not message:
        return jsonify(status="error", message="All fields are required"), 400

    conn = sqlite3.connect(DB)
    conn.execute('''
        INSERT INTO feedback (studentName, studentID, category, message)
        VALUES (?, ?, ?, ?)
    ''', (studentName, studentID, category, message))
    conn.commit()
    conn.close()

    return jsonify(status="success", message="Feedback submitted successfully")

if __name__ == '__main__':
    app.run(port=5004)
