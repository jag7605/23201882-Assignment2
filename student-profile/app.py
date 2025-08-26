from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import json
import time

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://studentuser:studentpass@student-db:5432/studentsdb")

max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB!")
        break
    except psycopg2.OperationalError as e:
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    raise Exception("Could not connect to the database after 20 retries")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Hello from student-profile service (with Postgres DB)! This is a line of text to let you know that the API service is running smoothly with full CRUD capability"

# GET all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, attendance FROM students ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    students = [{"id": r[0], "name": r[1], "email": r[2], "attendance": r[3] or []} for r in rows]
    return jsonify(students), 200

# GET student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, attendance FROM students WHERE id=%s", (student_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found"}), 404
    student = {"id": row[0], "name": row[1], "email": row[2], "attendance": row[3] or []}
    return jsonify(student), 200

# POST new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json() or {}
    if "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, email, attendance) VALUES (%s, %s, %s) RETURNING id",
        (data["name"], data["email"], json.dumps([]))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data["name"], "email": data["email"], "attendance": []}), 201

# PUT update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json() or {}
    fields = []
    values = []
    if "name" in data:
        fields.append("name=%s")
        values.append(data["name"])
    if "email" in data:
        fields.append("email=%s")
        values.append(data["email"])
    if not fields:
        return jsonify({"error": "No updatable fields provided"}), 400
    values.append(student_id)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE students SET {', '.join(fields)} WHERE id=%s RETURNING id, name, email, attendance", tuple(values))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "email": row[2], "attendance": row[3] or []}), 200

# DELETE student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s RETURNING id", (student_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Deleted"}), 200

# POST attendance record
@app.route("/students/<int:student_id>/attendance", methods=["POST"])
def record_attendance(student_id):
    data = request.get_json() or {}
    if "date" not in data or "status" not in data:
        return jsonify({"error": "date and status are required"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT attendance FROM students WHERE id=%s", (student_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    attendance = row[0] or []
    attendance.append({"date": data["date"], "status": data["status"]})

    cur.execute("UPDATE students SET attendance=%s WHERE id=%s", (json.dumps(attendance), student_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": student_id, "attendance": attendance}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)