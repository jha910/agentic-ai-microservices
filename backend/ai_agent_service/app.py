from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    req_type = data.get('type')

    if req_type == 'enroll':
        studentName = data.get('studentName')
        courseName = data.get('courseName')
        suggestion = f"Hi {studentName}, based on your interest, we recommend adding 'AI Fundamentals' alongside '{courseName}'."
        return jsonify(status="success", suggestion=suggestion)

    elif req_type == 'leave':
        leaveReason = data.get('leaveReason')
        if 'sick' in leaveReason.lower():
            validation = "Leave approved. Please attach medical certificate if available."
        else:
            validation = "Leave request noted. Hostel warden will review it shortly."
        return jsonify(status="success", validation=validation)

    elif req_type == 'internship':
        role = data.get('role')
        company = data.get('company')
        match = f"The role '{role}' at '{company}' matches your academic profile. Proceed with application."
        return jsonify(status="success", match=match)

    elif req_type == 'feedback':
        message = data.get('message')
        sentiment = "positive" if "thank" in message.lower() else "neutral"
        response = f"Feedback categorized as '{sentiment}'. Thank you for sharing!"
        return jsonify(status="success", analysis=response)

    else:
        return jsonify(status="error", message="Invalid request type"), 400

if __name__ == '__main__':
    app.run(port=5005)
