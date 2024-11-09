##### student-management
# Student Management System API

This project is a RESTful API for managing student and teacher data, user authentication, and CRUD operations using Flask and PostgreSQL. The system allows user registration, login, and tracks sign-in activity in the `logs` table.

## Features

- User authentication with JWT (JSON Web Tokens)
- User registration (Student and Teacher)
- Login functionality (Student and Teacher)
- CRUD operations for students (Create, Read, Update, Delete)
- Assigning teachers to students
- Log tracking for user sign-ins

## Technologies

- **Flask**: Python web framework for building the API
- **PostgreSQL**: Database for storing user and student data
- **JWT**: For authentication and token management
- **Bcrypt**: For password hashing and verification
- **Psycopg2**: PostgreSQL database adapter for Python

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/varshamohan08/student-management.git
   ```
2. Navigate to the project folder:
   ```
   cd student-management
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Configure your PostgreSQL database:
   Set the following environment variables or modify the Config.py file to reflect your PostgreSQL database credentials:
   ```
   DB_NAME = "student_management"
   DB_USER = "your_db_user"
   DB_PASSWORD = "your_db_password"
   DB_HOST = "localhost"
   DB_PORT = 5432
   ```
6. Create the required database tables using SQL script: [database.sql](https://github.com/varshamohan08/student-management/blob/main/database.sql).

## Endpoints
### Authentication Routes
#### 1. Register User
   Endpoint: `auth/register/<user_type>`<br>
   Method: POST<br>
   Body:
   ```
   {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
   }
   ```
   User Types: student, teacher
#### 2. Login User
   Endpoint: `auth/login/<user_type>`<br>
   Method: POST<br>
   Body:
   ```
   {
    "email": "john.doe@example.com",
    "password": "password123"
   }
   ```
### Student Routes
#### 3. View Students
   Endpoint: `students/`<br>
   Method: GET<br>
   Authorization: Bearer token required
#### 4. Add Student
   Endpoint: `students/add`<br>
   Method: POST<br>
   Body:
   ```
   {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "password": "password123"
   }
   ```
   Authorization: Bearer token required
#### 5. Update Student
   Endpoint: `students/update/<student_id>`<br>
   Method: PUT<br>
   Body:
   ```
   {
    "name": "Updated Name"
   }
   ```
   Authorization: Bearer token required
#### 6. Delete Student
   Endpoint: `students/delete/<student_id>`<br>
   Method: DELETE<br>
   Authorization: Bearer token required
#### 7. Assign Teacher to Student
   Endpoint: `students/<student_id>/teachers`<br>
   Method: POST<br>
   Body:
   ```
   {
    "teacher_id": 1
   }
   ```
   Authorization: Bearer token required
### JWT Authentication
   Use the Authorization header with the Bearer token in the request to authenticate protected routes:
   ```
   Authorization: Bearer <your_jwt_token>
   ```
### Logging
   Every sign-in event is logged in the logs table with the following details: user ID, user type, name, and sign-in time.
