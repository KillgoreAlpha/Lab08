from flask import Blueprint,request, jsonify
from flask_login import  login_user, logout_user, current_user,login_required
from werkzeug.security import check_password_hash
from db_config import db
from models import Student

student_login_bp = Blueprint('student_login',__name__)

@student_login_bp.route('/',methods=['POST'])

def student_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    student = Student.query.filter_by(username=username,role='student').first()
    if student and check_password_hash(student.password,password):
        login_user(student)
        return jsonify({"message":"Student login sucessful"})
    return jsonify({"error":"Username/Password not found or Not Student"}), 401

@student_login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if current_user.role == 'student':
        logout_user()
        return jsonify({"message":"Student Logged Out"})
    return jsonify({"error":"Only students can log out here"}), 403