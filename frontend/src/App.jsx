import React, { useState } from "react";
import StudentProfile from "./StudentProfile";
import CourseCatalogue from "./CourseCatalogue";
import Feedback from "./Feedback";
import Notification from "./Notification";

export default function App() {
  const [page, setPage] = useState("students");

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Admin Portal</h1>
      <nav style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        <button onClick={() => setPage("students")}>Students</button>
        <button onClick={() => setPage("courses")}>Courses</button>
        <button onClick={() => setPage("feedback")}>Feedback</button>
        <button onClick={() => setPage("notifications")}>Notifications</button>
      </nav>

      {page === "students" && <StudentProfile />}
      {page === "courses" && <CourseCatalogue />}
      {page === "feedback" && <Feedback />}
      {page === "notifications" && <Notification />}
    </div>
  );
}