from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import time

# All of the app.py files for the services are very similar, so I'll add detailed comments to this file and skip them in others.

app = Flask(__name__) # Initialize Flask app
CORS(app) # Enable CORS for all routes

# Use DATABASE_URL env var (same style as student-profile)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://student:password@student-db:5432/students" 
)

# Retry connection (to avoid crash if DB not ready yet)
max_retries = 20
for i in range(max_retries): # Try to connect to DB with retries
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB (course-catalogue)!") # Success message if connected
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...") # Retry message if connection fails for some reason
        time.sleep(2)
else:
    raise Exception("Could not connect to the database after retries") # Raise exception if all retries fail

def get_connection(): # Helper function to get a new DB connection
    return psycopg2.connect(DATABASE_URL) # Return a new connection to the database

@app.route("/")
def home(): # Simple home route to check if service is running
    return "Hello from course-catalogue service! CRUD endpoints for courses are available." # Simple message for home route (follows the same style given in student-profile)

# GET all courses
@app.route("/courses", methods=["GET"]) 
def get_courses(): # Retrieve all courses from the database
    conn = get_connection() # Get a new DB connection
    cur = conn.cursor() # Create a new cursor
    cur.execute("SELECT id, name, description FROM courses ORDER BY id ASC;") # Execute SQL query to fetch all courses
    rows = cur.fetchall() # Fetch all results
    cur.close() # Close the cursor
    conn.close() # Close the connection
    courses = [{"id": r[0], "name": r[1], "description": r[2]} for r in rows] # Convert rows to list of dictionaries
    return jsonify(courses), 200 # Return the list of courses as JSON with 200 status code

# POST new course
@app.route("/courses", methods=["POST"])
def add_course(): # Add a new course to the database
    data = request.get_json() or {} # Get JSON data from request body
    if "name" not in data or "description" not in data: # Validate required fields
        return jsonify({"error": "name and description are required"}), 400 # Return 400 if validation fails
    # Insert new course into the database
    conn = get_connection() # Get a new DB connection
    cur = conn.cursor() # Create a new cursor
    cur.execute( # Execute SQL query to insert new course
        "INSERT INTO courses (name, description) VALUES (%s, %s) RETURNING id", 
        (data["name"], data["description"]) 
    )
    new_id = cur.fetchone()[0] # Get the ID of the newly inserted course
    conn.commit() # Commit the transaction
    cur.close() # Close the cursor
    conn.close() # Close the connection
    return jsonify({"id": new_id, "name": data["name"], "description": data["description"]}), 201 # Return the new course with 201 status code

# DELETE a course
@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id): # Delete a course by ID
    conn = get_connection() # Get a new DB connection
    cur = conn.cursor() # Create a new cursor
    cur.execute("DELETE FROM courses WHERE id = %s RETURNING id;", (course_id,)) # Execute SQL query to delete the course
    deleted = cur.fetchone() # Check if a row was deleted
    conn.commit() # Commit the transaction
    cur.close() # Close the cursor
    conn.close() # Close the connection
    if deleted: # If a course was deleted,
        return jsonify({"message": f"Course {course_id} deleted"}), 200 # Return success message with 200 status code
    else: # If no course was found with the given ID,
        return jsonify({"error": "Course not found"}), 404 # Return 404 if course not found

if __name__ == "__main__": # Run the app if this file is executed directly
    app.run(host="0.0.0.0", port=5003, debug=True) # Run the app on all interfaces at port 5003 with debug mode enabled

    # Like I mentioned earlier, the other app.py files are very similar, so I won't add comments to them.