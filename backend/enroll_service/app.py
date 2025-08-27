from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "enrollments.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentName TEXT NOT NULL,
            studentID TEXT NOT NULL,
            courseName TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/enroll', methods=['POST'])
def enroll_course():
    data = request.get_json()
    studentName = data.get('studentName')
    studentID = data.get('studentID')
    courseName = data.get('courseName')
    semester = data.get('semester')

    if not studentName or not studentID or not courseName or not semester:
        return jsonify(status="error", message="All fields are required"), 400

    conn = sqlite3.connect(DB)
    conn.execute('''
        INSERT INTO enrollments (studentName, studentID, courseName, semester)
        VALUES (?, ?, ?, ?)
    ''', (studentName, studentID, courseName, semester))
    conn.commit()
    conn.close()

    return jsonify(status="success", message="Enrollment submitted successfully")

if __name__ == '__main__':
    app.run(port=5001)
