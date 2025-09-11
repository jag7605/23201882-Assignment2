from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import time

# Refer to comments in course-catalogue/app.py for detailed explanations as the structure is very similar.

app = Flask(__name__)
CORS(app)

# Use DATABASE_URL env var (same as student-profile & course-catalogue)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://student:password@student-db:5432/students"
)

# Retry connection until DB is ready
max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB (feedback)!")
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    raise Exception("Could not connect to the database after retries")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Hello from feedback service! CRUD endpoints for feedback are available."

# GET all feedback entries
@app.route("/feedback", methods=["GET"])
def get_feedback():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, student_name, message FROM feedback ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    feedback_list = [{"id": r[0], "student_name": r[1], "message": r[2]} for r in rows]
    return jsonify(feedback_list), 200

# POST new feedback
@app.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json() or {}
    if "student_name" not in data or "message" not in data:
        return jsonify({"error": "student_name and message are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback (student_name, message) VALUES (%s, %s) RETURNING id",
        (data["student_name"], data["message"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "student_name": data["student_name"], "message": data["message"]}), 201

# DELETE feedback
@app.route("/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM feedback WHERE id = %s RETURNING id;", (feedback_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return jsonify({"message": f"Feedback {feedback_id} deleted"}), 200
    else:
        return jsonify({"error": "Feedback not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)