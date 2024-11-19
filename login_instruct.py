from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from db_config import db
from models import Instructor, Course, Student

instruct_login_bp = Blueprint('instruct_login', __name__)

@instruct_login_bp.route('/login', methods=['POST', 'GET'])
def instruct_login():
    if request.method == 'GET':
        return send_from_directory('static', 'instruct.html')
        
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
        
    instructor = Instructor.query.filter_by(username=username, role='instruct').first()
    
    if instructor and check_password_hash(instructor.password, password):
        login_user(instructor)
        return jsonify({"message": "Instructor login successful"})
        
    return jsonify({"error": "Username/Password not found or Not Instructor"}), 401

@instruct_login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if current_user.role != 'instruct':
        return jsonify({"error": "Only Instructors can log out here"}), 403
    logout_user()
    return jsonify({"message": "Instructor Logged Out"})

@instruct_login_bp.route('/my-classes', methods=['GET'])
@login_required
def view_courses():
    if current_user.role != 'instruct':
        return jsonify({"error": "Unauthorized - Instructor access only"}), 403
        
    classes = Course.query.filter_by(instructor=current_user.name).all()
    if not classes:
        return jsonify({"message": "No classes found", "classes": []}), 200
        
    return jsonify({"classes": [course.to_dict() for course in classes]})

@instruct_login_bp.route('/class/<int:class_id>/students', methods=['GET'])
@login_required
def view_students_in_class(class_id):
    if current_user.role != 'instruct':
        return jsonify({"error": "Unauthorized - Instructor access only"}), 403
    
    course = Course.query.get(class_id)
    if not course:
        return jsonify({"error": "Class not found"}), 404
        
    if course.instructor != current_user.name:
        return jsonify({"error": "Unauthorized to view this class"}), 403

    return jsonify({
        "course": course.name,
        "students": [student.to_dict() for student in course.students]
    })

@instruct_login_bp.route('/class/<int:class_id>/student/<int:student_id>/grade', methods=['PUT'])
@login_required
def edit_grade(class_id, student_id):
    if current_user.role != 'instruct':
        return jsonify({"error": "Unauthorized - Instructor access only"}), 403
    
    if not request.is_json:
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "Request must be JSON with Content-Type: application/json"
        }), 415
    
    course = Course.query.get(class_id)
    if not course:
        return jsonify({"error": "Class not found"}), 404
        
    if course.instructor != current_user.name:
        return jsonify({"error": "Unauthorized to modify grades for this class"}), 403
    
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    if student not in course.students:
        return jsonify({"error": "Student not enrolled in this class"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400
        
    new_grade = data.get('grade')
    if new_grade is None:
        return jsonify({"error": "Grade is required"}), 400
        
    try:
        new_grade = float(new_grade)
        if not (0 <= new_grade <= 100):  # Assuming grades are on a 0-100 scale
            return jsonify({"error": "Grade must be between 0 and 100"}), 400
            
        student.grade = new_grade
        db.session.commit()
        return jsonify({
            "message": f"Grade updated for {student.name} in {course.name}",
            "new_grade": new_grade
        })
    except ValueError:
        return jsonify({"error": "Invalid grade format - must be a number"}), 400