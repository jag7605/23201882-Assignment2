-- REM: *******************************************************************
-- REM: ***** Assignment 2: INFS605 Microservices Programming Project *****
-- REM: *******************************************************************
-- REM: * Purpose: Creating the PostGres SQL code needed to create the tables for the database *
-- REM: * Stephen Thorpe 9301663 *
-- REM: * Version: 2.0 (Tuesday 26 August 2025) *
-- REM: * Extended to include courses and feedback tables for additional services *

-- ===========================
-- STUDENT PROFILE SERVICE
-- ===========================
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    attendance JSONB DEFAULT '[]'
);

INSERT INTO students (name, email, attendance) VALUES
('Aroha Ngata', 'aroha.ngata@example.com', '[]'),
('Tane Mahuta', 'tane.mahuta@example.com', '[]'),
('Moana Rangi', 'moana.rangi@example.com', '[]'),
('Wiremu Pita', 'wiremu.pita@example.com', '[]'),
('Lani Tui', 'lani.tui@example.com', '[]'),
('Malia Fetu', 'malia.fetu@example.com', '[]'),
('Sione Vaka', 'sione.vaka@example.com', '[]'),
('Tavita Fale', 'tavita.fale@example.com', '[]'),
('Priya Sharma', 'priya.sharma@example.com', '[]'),
('Ravi Patel', 'ravi.patel@example.com', '[]'),
('Anjali Mehta', 'anjali.mehta@example.com', '[]'),
('Arjun Singh', 'arjun.singh@example.com', '[]'),
('Li Wei', 'li.wei@example.com', '[]'),
('Zhang Mei', 'zhang.mei@example.com', '[]'),
('Chen Yong', 'chen.yong@example.com', '[]'),
('Wang Xiu', 'wang.xiu@example.com', '[]'),
('Kim Ji-hoon', 'kim.jihoon@example.com', '[]'),
('Park Soo-jin', 'park.soojin@example.com', '[]'),
('Maria Santos', 'maria.santos@example.com', '[]'),
('Juan Dela Cruz', 'juan.delacruz@example.com', '[]'),
('Ahmad Rahman', 'ahmad.rahman@example.com', '[]'),
('Nur Aisyah', 'nur.aisyah@example.com', '[]'),
('Alice Smith', 'alice.smith@example.com', '[]'),
('Bob Johnson', 'bob.johnson@example.com', '[]'),
('Charlie Brown', 'charlie.brown@example.com', '[]'),
('Diana Prince', 'diana.prince@example.com', '[]'),
('Ethan Hunt', 'ethan.hunt@example.com', '[]'),
('Hannah Lee', 'hannah.lee@example.com', '[]'),
('Michael Scott', 'michael.scott@example.com', '[]'),
('Rachel Green', 'rachel.green@example.com', '[]');

-- ===========================
-- COURSE CATALOGUE SERVICE
-- ===========================
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

INSERT INTO courses (name, description) VALUES
('COMP101', 'Introduction to Computing'),
('COMP202', 'Data Structures and Algorithms'),
('COMP303', 'Databases and Information Systems');

-- ===========================
-- FEEDBACK SERVICE
-- ===========================
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    message TEXT
);

INSERT INTO feedback (student_name, message) VALUES
('Ethan', 'Really enjoyed the course!'),
('Rachel', 'The lectures were too fast.');

-- ===========================
-- NOTIFICATION SERVICE
-- ===========================
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

-- Sample notifications to fill the table
INSERT INTO notifications (student_id, message) VALUES
(1, 'Welcome to the course portal, Aroha!'),
(2, 'Tane, don’t forget to check your attendance records.'),
(3, 'Moana, new feedback is available for your last assignment.');