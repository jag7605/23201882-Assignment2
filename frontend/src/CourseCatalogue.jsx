import React, { useEffect, useState } from "react";

const API = "http://localhost:5003";

export default function CourseCatalogue() {
  const [courses, setCourses] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const fetchCourses = () => {
    fetch(`${API}/courses`)
      .then((r) => r.json())
      .then(setCourses);
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const addCourse = async () => {
    if (!name || !description) return;
    const res = await fetch(`${API}/courses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    });
    if (res.ok) {
      setName("");
      setDescription("");
      fetchCourses();
    }
  };

  const deleteCourse = async (id) => {
    await fetch(`${API}/courses/${id}`, { method: "DELETE" });
    fetchCourses();
  };

  return (
    <div>
      <h2>Course Catalogue</h2>

      <div style={{ marginBottom: 16 }}>
        <input
          placeholder="Course Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <button onClick={addCourse}>Add Course</button>
      </div>

      <ul>
        {courses.map((c) => (
          <li key={c.id} style={{ marginBottom: 8 }}>
            <strong>{c.name}</strong>: {c.description}
            <button
              onClick={() => deleteCourse(c.id)}
              style={{ marginLeft: 12, background: "#ffe5e5" }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}