import React, { useEffect, useState } from "react";

const API = "http://localhost:5002";

export default function Feedback() {
  const [feedback, setFeedback] = useState([]);
  const [studentName, setStudentName] = useState("");
  const [message, setMessage] = useState("");

  const fetchFeedback = () => {
    fetch(`${API}/feedback`)
      .then((r) => r.json())
      .then(setFeedback);
  };

  useEffect(() => {
    fetchFeedback();
  }, []);

  const addFeedback = async () => {
    if (!studentName || !message) return;
    const res = await fetch(`${API}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_name: studentName, message }),
    });
    if (res.ok) {
      setStudentName("");
      setMessage("");
      fetchFeedback();
    }
  };

  const deleteFeedback = async (id) => {
    await fetch(`${API}/feedback/${id}`, { method: "DELETE" });
    fetchFeedback();
  };

  return (
    <div>
      <h2>Feedback</h2>

      <div style={{ marginBottom: 16 }}>
        <input
          placeholder="Student Name"
          value={studentName}
          onChange={(e) => setStudentName(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <input
          placeholder="Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <button onClick={addFeedback}>Submit Feedback</button>
      </div>
      <ul>
        {feedback.map((f) => (
          <li key={f.id} style={{ marginBottom: 8 }}>
            <strong>{f.student_name}</strong>: {f.message}
            <button
              onClick={() => deleteFeedback(f.id)}
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