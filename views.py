from flask import Blueprint, request, jsonify
from utils import connect, generate_bcrypt_hash, generate_jwt_token, token_required, verify_bcrypt_hash
from datetime import datetime

# Authentication #################################################################
auth_bp = Blueprint("auth_bp", __name__)

def log_user_signin(user_id, user_type, name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (user_id, user_type, name, sign_in_time)
        VALUES (%s, %s, %s, %s)
    """, (user_id, user_type, name, datetime.now()))
    conn.commit()
    conn.close()

@auth_bp.route("/register/<user_type>", methods=["POST"])
def register(user_type):
    if user_type not in ["student", "teacher"]:
        return jsonify({"error": "Invalid user type"}), 400

    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]

    hashed_password = generate_bcrypt_hash(password)

    conn = connect()
    cursor = conn.cursor()

    if user_type == "student":
        cursor.execute("SELECT id FROM students WHERE email = %s", (email,))
    else:
        cursor.execute("SELECT id FROM teachers WHERE email = %s", (email,))
    
    if cursor.fetchone():
        return jsonify({"error": "Email is already registered"}), 400

    if user_type == "student":
        cursor.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s) RETURNING id",
                       (name, email, hashed_password))
    else:
        cursor.execute("INSERT INTO teachers (name, email, password) VALUES (%s, %s, %s) RETURNING id",
                       (name, email, hashed_password))

    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": f"{user_type.capitalize()} registered successfully", "user_id": user_id}), 201

@auth_bp.route("/login/<user_type>", methods=["POST"])
def login(user_type):
    if user_type not in ["student", "teacher"]:
        return jsonify({"error": "Invalid user type"}), 400

    data = request.json
    email = data["email"]
    password = data["password"]

    conn = connect()
    cursor = conn.cursor()

    if user_type == "student":
        cursor.execute("SELECT id, name, password FROM students WHERE email = %s", (email,))
    else:
        cursor.execute("SELECT id, name, password FROM teachers WHERE email = %s", (email,))

    user = cursor.fetchone()
    if user and verify_bcrypt_hash(password, user[2]):
        user_id, name, _ = user
        token = generate_jwt_token(user_id, user_type)

        cursor.execute("""
            INSERT INTO logs (user_id, user_type, name, sign_in_time)
            VALUES (%s, %s, %s, %s)
        """, (user_id, user_type, name, datetime.now()))

        conn.commit()
        conn.close()
        return jsonify({"message": f"{user_type.capitalize()} logged in successfully", "token": token})

    conn.close()
    return jsonify({"error": "Invalid email or password"}), 401


# CRUD operations #################################################################
student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/", methods=["GET"])
@token_required
def view_students():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return jsonify(students)

@student_bp.route("/add", methods=["POST"])
@token_required
def add_student():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = generate_bcrypt_hash(data["password"])

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
                   (name, email, password))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201

@student_bp.route("/update/<int:student_id>", methods=["PUT"])
@token_required
def update_student(student_id):
    data = request.json
    new_name = data["name"]

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name = %s WHERE id = %s", (new_name, student_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated successfully"})

@student_bp.route("/delete/<int:student_id>", methods=["DELETE"])
@token_required
def delete_student(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted successfully"})

@student_bp.route("/<int:student_id>/teachers", methods=["GET"])
@token_required
def get_teachers(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.name FROM teachers t
        JOIN student_teacher st ON t.id = st.teacher_id
        WHERE st.student_id = %s
    """, (student_id,))
    teachers = cursor.fetchall()
    conn.close()
    return jsonify(teachers)

@student_bp.route("/<int:student_id>/teachers", methods=["POST"])
@token_required
def assign_teacher(student_id):
    data = request.json
    teacher_id = data.get("teacher_id")

    if not teacher_id:
        return jsonify({"error": "Teacher ID is required"}), 400

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM teachers WHERE id = %s", (teacher_id,))
    teacher = cursor.fetchone()
    
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404

    cursor.execute("""
        SELECT 1 FROM student_teacher WHERE student_id = %s AND teacher_id = %s
    """, (student_id, teacher_id))
    
    if cursor.fetchone():
        return jsonify({"message": "Teacher is already assigned to this student"}), 400

    cursor.execute("""
        INSERT INTO student_teacher (student_id, teacher_id)
        VALUES (%s, %s)
    """, (student_id, teacher_id))
    
    conn.commit()
    conn.close()

    return jsonify({"message": f"Teacher with ID {teacher_id} assigned to student {student_id} successfully"}), 201
