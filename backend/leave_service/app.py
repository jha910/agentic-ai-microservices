from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "hostel_leave.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS hostel_leave (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentName TEXT NOT NULL,
            studentID TEXT NOT NULL,
            leaveReason TEXT NOT NULL,
            leaveFrom TEXT NOT NULL,
            leaveTo TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/hostel_leave', methods=['POST'])
def hostel_leave_request():
    data = request.get_json()
    studentName = data.get('studentName')
    studentID = data.get('studentID')
    leaveReason = data.get('leaveReason')
    leaveFrom = data.get('leaveFrom')
    leaveTo = data.get('leaveTo')

    if not studentName or not studentID or not leaveReason or not leaveFrom or not leaveTo:
        return jsonify(status="error", message="All fields are required"), 400

    conn = sqlite3.connect(DB)
    conn.execute('''
        INSERT INTO hostel_leave (studentName, studentID, leaveReason, leaveFrom, leaveTo)
        VALUES (?, ?, ?, ?, ?)
    ''', (studentName, studentID, leaveReason, leaveFrom, leaveTo))
    conn.commit()
    conn.close()

    return jsonify(status="success", message="Hostel leave request submitted successfully")

if __name__ == '__main__':
    app.run(port=5002)
