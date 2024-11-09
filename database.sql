CREATE DATABASE student_management;
-- CREATE DATABASE teacher_management;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE student_teacher (
    student_id INT REFERENCES students(id),
    teacher_id INT REFERENCES teachers(id),
    PRIMARY KEY (student_id, teacher_id)
);

CREATE TABLE logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT,
    user_type VARCHAR(10), -- 'student' or 'teacher'
    name VARCHAR(50),
    sign_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE teachers ALTER COLUMN password TYPE character varying(255);


GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT USAGE ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
