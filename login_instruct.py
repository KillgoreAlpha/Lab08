from flask import Blueprint,request, jsonify
from flask_login import  login_user, logout_user, current_user,login_required
from werkzeug.security import check_password_hash
from db_config import db
from models import Instructor, Course, Student

instruct_login_bp = Blueprint('instruct_login',__name__)

@instruct_login_bp.route('/login',methods=['POST','GET'])

def instruct_login():
    # data = request.get_json()
    data = request.json
    if not data:
      return jsonify({"error": "Invalid JSON body"}), 400

    username = data.get('username')
    password = data.get('password')

    instruct = Instructor.query.filter_by(username=username,role='instruct').first()
    if instruct and check_password_hash(instruct.password,password):
        login_user(instruct)
        return jsonify({"message":"Instructor login sucessful"})
    return jsonify({"error":"Username/Password not found or Not Instructor"}), 401

@instruct_login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if current_user.role == 'instruct':
        logout_user()
        return jsonify({"message":"Instructor Logged Out"})
    return jsonify({"error":"Only Instructor can log out here"}), 403

@instruct_login_bp.route('/my-classes',methods=['GET'])
@login_required
def view_courses():
    if current_user.role != 'instruct':
        return jsonify({"error":"Unauthorized"}),403
    classes = Course.query.filter_by(instructor=current_user.name).all()
    return jsonify({"classes": [course.to_dict() for course in classes]})

@instruct_login_bp.route('/class/<int:class_id>/students',methods=['GET'])
@login_required
def view_students_in_class(class_id):
    if current_user.role != 'instruct':
        return jsonify({"error":"Unauthorized"}),403
    
    course = Course.query.get(class_id)
    if not course or course.instructor != current_user.name:
        return jsonify({"error":"Class not found or authourized to view"}),404

    return jsonify({
        "courses":course.name,
        "students":[student.to_dict() for student in course.students]
    })

#Edit Grade
@instruct_login_bp.route('/class/<int:class_id>/student/<int:student_id>/grade', methods=['PUT'])
@login_required

def edit_grade(class_id,student_id):
    if current_user.role != 'instruct':
        return jsonify({"error":"Unauthorized"}),403
    
    course = course.query.get(class_id)
    if not course or course.instructor != current_user.name:
        return jsonify({"error":"Class not found or not authorized to view"}), 404
    
    student = Student.query.get(class_id)
    if not student or student != course.students:
        return jsonify({"error":"Student not found or not authorized to view"}), 404

    data = request.get_json()
    new_grade = data.get('grade')

    if not new_grade:
        return jsonify({"error": "Invalid data"}), 4004
    try:
        student.grade = float(new_grade)
        db.session.commit()
        return jsonify({"message":f"Grade updated for {student.name} in {course.name}"})
    except ValueError:
        return jsonify({"error": "Invalid grade format"}), 400
    