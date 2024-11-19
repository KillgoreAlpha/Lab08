from flask import Blueprint,request, jsonify, send_from_directory
from flask_login import  login_user, logout_user, current_user,login_required
from werkzeug.security import check_password_hash
from db_config import db
from models import Student, Course

student_login_bp = Blueprint('student_login',__name__)

@student_login_bp.route('/login',methods=['POST','GET'])

def student_login():
    # data = request.get_json()
    if request.method == 'GET':
        return send_from_directory('static', 'student.html')

    if not request.is_json:
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "Request must be JSON with Content-Type: application/json"
        }), 415
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    student = Student.query.filter_by(username=username, role='student').first()
    
    if student and check_password_hash(student.password, password):
        login_user(student)
        return jsonify({"message": "Student login successful"})
        
    return jsonify({"error": "Username/Password not found or Not Student"}), 401

@student_login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if current_user.role == 'student':
        logout_user()
        return jsonify({"message":"Student Logged Out"})
    return jsonify({"error":"Only students can log out here"}), 403

@student_login_bp.route('enroll',methods=['POST'])
@login_required
def enroll_course():
    data = request.get_json()
    course_id = data.get('course_id')

    student = current_user
    course = Course.query.get(course_id)

    if not course:
        return jsonify({"error":"Course not found"}, 404)
    if student in course.students:
        return jsonify({"message":"Already enrolled"}, 400)
    if len(course.students) >= course.capacity:
        return jsonify({"message":"Course is full"}, 404)
    course.students.append(student)
    db.session.commit()
    return jsonify({"message":f"{student.name} enrolled in {course.course}"})

#view enrolled courses
@student_login_bp.route('/my-courses',methods=['GET'])
@login_required
def get_courses():
    student = current_user
    return jsonify({"courses":[course.to_dict() for course in student.courses]})


 
