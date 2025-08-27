from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "internship.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS internship (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentName TEXT NOT NULL,
            studentID TEXT NOT NULL,
            role TEXT NOT NULL,
            company TEXT NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/internship', methods=['POST'])
def internship_application():
    data = request.get_json()
    studentName = data.get('studentName')
    studentID = data.get('studentID')
    role = data.get('role')
    company = data.get('company')
    duration = data.get('duration')

    if not studentName or not studentID or not role or not company or not duration:
        return jsonify(status="error", message="All fields are required"), 400

    conn = sqlite3.connect(DB)
    conn.execute('''
        INSERT INTO internship (studentName, studentID, role, company, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (studentName, studentID, role, company, duration))
    conn.commit()
    conn.close()

    return jsonify(status="success", message="Internship application submitted successfully")

if __name__ == '__main__':
    app.run(port=5003)
