# Student Admin Portal (Microservices with Docker Compose)

## Jagrith Narayan - 23201882

## Overview

This project expands on the microservices-based student administration portal given to us with the existing student-profile service. It consists of four backend services and a React-based frontend. 

(Please note, I did not use a virtual machine like ubuntu as I did this locally on my Macbook with docker installed on it) 

Link to repo: https://github.com/jag7605/23201882-Assignment2 

### Services:

-   **Student Profile Service** (port 5001)
    
    -   Manages student details and attendance.
        
-   **Course Catalogue Service** (port 5003)
    
    -   Stores and manages available courses.
        
-   **Feedback Service** (port 5002)
    
    -   Handles feedback from students about courses.
        
-   **Notification Service** (port 5004)
    
    -   Manages system notifications for students.
        
-   **Frontend (Admin Portal)** (port 3000)
    
    -   React UI for managing students, courses, feedback, and notifications.
        
-   **Database (PostgreSQL)** (port 5432)
    
    -   Shared by all services. Initialized via `init.sql`.
        
## Project Structure

```
23201882-Assignment2/
├── course-catalogue/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait-for-it.sh
├── feedback/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait-for-it.sh
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── node_modules/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── CourseCatalogue.jsx
│       ├── Feedback.jsx
│       ├── main.jsx
│       ├── Notification.jsx
│       ├── StudentProfile.jsx
│       └── vite.config.js
├── notification/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait-for-it.sh
├── postgres/
│   └── init.sql
├── student-profile/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wait-for-it.sh
├── .gitattributes
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.MD
```

##  Setup & Running

1.  **Clone the Repository**
    
    ```
    git clone https://github.com/jag7605/23201882-Assignment2 
    cd 23201882-Assignment2
    ```
    
2.  **Build and Start Containers (ensure docker is opened and running on your machine)**
    
    ```
    docker compose up --build
    ```
    
    This will start:
    
    -   `student-db` (Postgres)
        
    -   `student-profile` (Flask service)
        
    -   `course-catalogue` (Flask service)
        
    -   `feedback` (Flask service)
        
    -   `notification` (Flask service)
        
    -   `frontend` (React app)
        
3.  **Access Services**
    
    -   **Frontend (Admin Portal):**  `http://localhost:3000`
        
    -   **Student Profile API:**  `http://localhost:5001`
        
    -   **Course Catalogue API:**  `http://localhost:5003`
        
    -   **Feedback API:**  `http://localhost:5002`
        
    -   **Notification API:**  `http://localhost:5004`
        

##  Database Initialisation

The Postgres container runs `postgres/init.sql` on first build. This script:

-   Creates tables for students, courses, feedback, and notifications.
    
-   Inserts some sample data for testing.
    

##  Testing the Services

### Using curl commands

**Examples:**

-   **Get all students**
    
    ```
    curl http://localhost:5001/students
    ```
    
-   **Add a new course:**
    
    ```
    curl -X POST http://localhost:5003/courses \
    -H "Content-Type: application/json" \
    -d '{"name":"COMP999","description":"Special Topics in Software"}'
    ```
    
-   **Submit feedback:**
    
    ```
    curl -X POST http://localhost:5002/feedback \
    -H "Content-Type: application/json" \
    -d '{"student_name":"Alice","message":"Loving this course!"}'
    ```
    
-   **Create a notification:**
    
    ```
    curl -X POST http://localhost:5004/notifications \
    -H "Content-Type: application/json" \
    -d '{"student_id":1,"message":"Your COMP999 course has been added!"}'
    ```
    

### Using the Frontend

Go to `http://localhost:3000`. Use the buttons to switch between:

-   Students
    
-   Courses
    
-   Feedback
    
-   Notifications
    

Perform add/delete actions and verify updates live.

## API Documentation

Each backend service exposes a REST API with JSON responses.  

---

### Course Catalogue Service (port 5003)

- **GET /courses** → Returns all courses.  
- **POST /courses**  
  - Request:  
    ```json
    { "name": "COMP999", "description": "Special Topics in Software" }
    ```
  - Response:  
    ```json
    { "id": 4, "name": "COMP999", "description": "Special Topics in Software" }
    ```
- **DELETE /courses/{id}** → Deletes a course by ID.  
  - Response:  
    ```json
    { "message": "Course 4 deleted" }
    ```

---

### Feedback Service (port 5002)

- **GET /feedback** → Returns all feedback entries.  
- **POST /feedback**  
  - Request:  
    ```json
    { "student_name": "Alice", "message": "Loving this course!" }
    ```
  - Response:  
    ```json
    { "id": 3, "student_name": "Alice", "message": "Loving this course!" }
    ```
- **DELETE /feedback/{id}** → Deletes a feedback entry by ID.  
  - Response:  
    ```json
    { "message": "Feedback 3 deleted" }
    ```

---

### Notification Service (port 5004)

- **GET /notifications** → Returns all notifications.  
- **POST /notifications**  
  - Request:  
    ```json
    { "student_id": 1, "message": "Your COMP999 course has been added!" }
    ```
  - Response:  
    ```json
    { "id": 4, "student_id": 1, "message": "Your COMP999 course has been added!" }
    ```
- **DELETE /notifications/{id}** → Deletes a notification by ID.  
  - Response:  
    ```json
    { "message": "Notification 4 deleted" }
    ```

##  Verification

-   Services were tested with `curl` and through the frontend.
    
-   Adding and deleting data was confirmed across both interfaces.
    
-   CORS enabled for frontend → backend communication.