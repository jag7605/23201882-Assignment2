from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

# Refer to comments in course-catalogue/app.py for detailed explanations as the structure is very similar.

app = Flask(__name__)
CORS(app)

# Use DATABASE_URL (same as other services)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://student:password@student-db:5432/students"
)

# Retry until DB is ready
max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB (notification)!")
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    raise Exception("Could not connect to DB after retries")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Hello from notification service! CRUD endpoints for notifications are available."

# GET all notifications
@app.route("/notifications", methods=["GET"])
def get_notifications():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notifications ORDER BY created_at DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200

# GET a single notification
@app.route("/notifications/<int:notification_id>", methods=["GET"])
def get_notification(notification_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notifications WHERE id = %s;", (notification_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return jsonify(row), 200
    else:
        return jsonify({"error": "Notification not found"}), 404

# POST new notification
@app.route("/notifications", methods=["POST"])
def create_notification():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    message = data.get("message")

    if not student_id or not message:
        return jsonify({"error": "student_id and message are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notifications (student_id, message) VALUES (%s, %s) RETURNING id;",
        (student_id, message)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "student_id": student_id, "message": message}), 201

# DELETE a notification
@app.route("/notifications/<int:notification_id>", methods=["DELETE"])
def delete_notification(notification_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE id = %s RETURNING id;", (notification_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return jsonify({"message": f"Notification {notification_id} deleted"}), 200
    else:
        return jsonify({"error": "Notification not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)