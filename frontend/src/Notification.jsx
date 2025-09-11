import React, { useEffect, useState } from "react";

const API = "http://localhost:5004";

export default function Notification() {
  const [notifications, setNotifications] = useState([]);
  const [studentId, setStudentId] = useState("");
  const [message, setMessage] = useState("");

  const fetchNotifications = () => {
    fetch(`${API}/notifications`)
      .then((r) => r.json())
      .then(setNotifications)
      .catch((err) => console.error("Error fetching notifications:", err));
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const addNotification = async () => {
    if (!studentId || !message) return;
    const res = await fetch(`${API}/notifications`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_id: studentId, message }),
    });
    if (res.ok) {
      setStudentId("");
      setMessage("");
      fetchNotifications();
    }
  };

  const deleteNotification = async (id) => {
    await fetch(`${API}/notifications/${id}`, { method: "DELETE" });
    fetchNotifications();
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
      <h2>Notifications</h2>

      {/* Add notification form */}
      <div
        style={{
          marginBottom: 24,
          padding: 16,
          border: "1px solid #eee",
          borderRadius: 12,
          boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
        }}
      >
        <h3>Add Notification</h3>
        <input
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          style={{ marginRight: 8, padding: 6 }}
        />
        <input
          placeholder="Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ marginRight: 8, padding: 6, width: 300 }}
        />
        <button onClick={addNotification}>Add</button>
      </div>

      {/* List of notifications */}
      {notifications.length === 0 ? (
        <p>No notifications found.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {notifications.map((n) => (
            <li
              key={n.id}
              style={{
                border: "1px solid #eee",
                borderRadius: 8,
                padding: 12,
                marginBottom: 12,
                boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
              }}
            >
              <div>
                <strong>Student {n.student_id}</strong>
              </div>
              <div>{n.message}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>
                {new Date(n.created_at).toLocaleString()}
              </div>
              <button
                onClick={() => deleteNotification(n.id)}
                style={{
                  marginTop: 8,
                  background: "#ffe5e5",
                  border: "1px solid #f5b5b5",
                  padding: "4px 8px",
                  borderRadius: 6,
                }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}