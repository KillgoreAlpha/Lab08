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
    
    classes_with_students = []
    for course in classes:
            if course.enrolled_students:  
                classes_with_students.append({
                    "course": course.course,
                    "capacity": course.capacity,
                    "students": [
                        {
                            "name": student.name,
                            "grade": student.grade
                        } for student in course.enrolled_students
                    ]
                })

    if not classes_with_students:
        return jsonify({"message": "No classes with enrolled students found", "classes": []}), 200

    return jsonify({"classes": classes_with_students})

@instruct_login_bp.route('/class/<string:course>/students', methods=['GET'])
@login_required
def view_students_in_class(course):
    if current_user.role != 'instruct':
        return jsonify({"error": "Unauthorized - Instructor access only"}), 403
    
    course = Course.query.filter_by(course=course, instructor=current_user.name).first()
    if not course:
        return jsonify({"error": "Class not found"}), 404

    students = course.enrolled_students  
    if not students:
        return jsonify({"error": "Unauthorized to view this class"}), 403

    return jsonify({
        "course": course.name,
        "students": [{
            "name":student.name,
            "grade":student.grade
    } for student in students]
    })

@instruct_login_bp.route('/class/<string:course>/student/<string:student_username>/grade', methods=['PUT'])
@login_required
def edit_grade(course, student_username):
    if current_user.role != 'instruct':
        return jsonify({"error": "Unauthorized - Instructor access only"}), 403
    
    if not request.is_json:
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "Request must be JSON with Content-Type: application/json"
        }), 415
    

    course_instance = Course.query.filter_by(course=course, instructor=current_user.name).first()
    if not course_instance:
        return jsonify({"error": f"Course '{course}' not found or you are not authorized to modify it"}), 404
    
    
    student = Student.query.filter_by(username=student_username).first()
    if not student:
        return jsonify({"error": f"Student '{student.name}' not found"}), 404
    
   
    if student not in course_instance.students:
        return jsonify({"error": f"Student '{student.name}' is not enrolled in the course '{course}'"}), 404

    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400
        
    new_grade = data.get('grade')
    if new_grade is None:
        return jsonify({"error": "Grade is required"}), 400
        
    try:
        new_grade = float(new_grade)
        if not (0 <= new_grade <= 100):  
            return jsonify({"error": "Grade must be between 0 and 100"}), 400
            
       
        student.grade = new_grade
        db.session.commit()
        return jsonify({
            "message": f"Grade updated for {student.name} in {course_instance.course}",
            "new_grade": new_grade
        })
    except ValueError:
        return jsonify({"error": "Invalid grade format - must be a number"}), 400
