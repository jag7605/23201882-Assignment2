from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

# Use DATABASE_URL env var (same style as student-profile)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://student:password@student-db:5432/students"
)

# Retry connection (to avoid crash if DB not ready yet)
max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB (course-catalogue)!")
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
    return "Hello from course-catalogue service! CRUD endpoints for courses are available."

# GET all courses
@app.route("/courses", methods=["GET"])
def get_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM courses ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    courses = [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]
    return jsonify(courses), 200

# POST new course
@app.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json() or {}
    if "name" not in data or "description" not in data:
        return jsonify({"error": "name and description are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO courses (name, description) VALUES (%s, %s) RETURNING id",
        (data["name"], data["description"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data["name"], "description": data["description"]}), 201

# DELETE a course
@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id = %s RETURNING id;", (course_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return jsonify({"message": f"Course {course_id} deleted"}), 200
    else:
        return jsonify({"error": "Course not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)