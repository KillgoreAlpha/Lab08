import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from db_config import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from login_instruct import instruct_login_bp
from login_student import student_login_bp
from flask_login import LoginManager
from models import *

app = Flask(__name__, static_folder='static')

app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grades.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = '/student/login'

# @login_manager.user_loader
# def load_user(user_id):
#     user = Student.query.get(int(user_id)) or Instructor.query.get(int(user_id))
#     return user

#register blueprints
app.register_blueprint(student_login_bp,url_prefix='/student')
app.register_blueprint(instruct_login_bp,url_prefix='/instruct')

@login_manager.user_loader
def load_user(user_id):
    user = Student.query.get(int(user_id)) or Instructor.query.get(int(user_id))
    return user

# class Student(db.Model):
#     username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
#     password = db.Column(db.String, unique=False, nullable=False)
#     name = db.Column(db.String, unique=False, nullable=False)
#     grade = db.Column(db.Float, primary_key=False, unique=False, nullable=True)
#     role = db.Column(db.String, unique=False,nullable=False,default="student")

#     def to_dict(self):
#         return {"username": self.username, 
#                 #"password": self.password, 
#                 "name": self.name, 
#                 "grade": self.grade,
#                 "role":self.role}
    
# class Instructor(db.Model):
#     username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
#     password = db.Column(db.String, unique=False, nullable=False)
#     name = db.Column(db.String, primary_key=False, unique=False, nullable=False)
#     role = db.Column(db.String, unique=False,nullable=False,default="instruct")

#     def to_dict(self):
#         return {"username": self.username, 
#                 #"password": self.password, 
#                 "name": self.name,
#                 "role":self.role}

# class Course(db.Model):    
#     course = db.Column(db.String, primary_key=True, unique=True, nullable=False)
#     instructor = db.Column(db.String, unique=False, nullable=False)
#     time = db.Column(db.String, unique=False, nullable=False)
#     capacity = db.Column(db.Integer, unique=False, nullable=False)
#     students = db.Column(db.String, unique=False, nullable=False)

#     def to_dict(self):
#         return {"course": self.course, "instructor": self.instructor, "time": self.time, "capacity": self.capacity, "students": self.students}

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        if not Student.query.first():
            sample_data = [
                Student(
                        id = 1,
                        name="John Doe", 
                        grade=85.5, 
                        username="JDoe1",
                        password = generate_password_hash("samplepassword1"),
                        role="student"),
                Student(
                        id = 2,
                        name="Jane Smith", 
                        grade=92.0, 
                        username ="JaneSmith43",
                        password = generate_password_hash("samplepassword2"), 
                        role="student")
            ]
            # db.session.add_all(sample_data)

        if not Instructor.query.first():
            sample_instructors = [
                Instructor(
                    id=1,
                    name="Dr. Alice",
                    username="Alice",
                    password=generate_password_hash("securepassword1"),
                    role="instruct"
                ),
                Instructor(
                    id=2,
                    name="Prof. Bob",
                    username="Bob",
                    password=generate_password_hash("securepassword2"),
                    role="instruct"
                )
            ]
            db.session.add_all(sample_data + sample_instructors)
            db.session.commit()
        # Sample courses
        if not Course.query.first():
            sample_courses = [
                Course(
                    id=1,
                    course="Math 101",
                    instructor="Dr. Alice",
                    time="Mon/Wed 10:00-11:30",
                    capacity=30,
                    students=[]
                ),
                Course(
                    id=2,
                    course="Physics 201",
                    instructor="Prof. Bob",
                    time="Tue/Thu 1:00-2:30",
                    capacity=25,
                    students=[]
                )
            ]

            sample_courses[0].students.append(sample_data[0])
            sample_courses[1].students.append(sample_data[1])
            db.session.add_all(sample_courses)
            db.session.commit()

# @app.route('/grades', methods=['GET'])
# def get_all_grades():
#     students = Student.query.all()
#     return jsonify({"grades": [student.to_dict() for student in students]})

# @app.route('/grades/<student_name>', methods=['GET'])
# def get_grade(student_name):
#     student = Student.query.get(student_name)
#     if student:
#         return jsonify(student.to_dict())
#     return jsonify({"error": "Student not found"}), 404

# @app.route('/grades', methods=['POST'])
# def add_grade():
#     data = request.get_json()
#     if not data or 'name' not in data or 'grade' not in data:
#         return jsonify({"error": "Invalid data"}), 400
    
#     try:
#         new_student = Student(name=data['name'], grade=float(data['grade']))
#         db.session.add(new_student)
#         db.session.commit()
#         return jsonify(new_student.to_dict())
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Student already exists"}), 400
#     except ValueError:
#         return jsonify({"error": "Invalid grade format"}), 400

# @app.route('/grades/<student_name>', methods=['PUT'])
# def update_grade(student_name):
#     student = Student.query.get(student_name)
#     if not student:
#         return jsonify({"error": "Student not found"}), 404
    
#     data = request.get_json()
#     if not data or 'grade' not in data:
#         return jsonify({"error": "Invalid data"}), 400
    
#     try:
#         student.grade = float(data['grade'])
#         db.session.commit()
#         return jsonify(student.to_dict())
#     except ValueError:
#         return jsonify({"error": "Invalid grade format"}), 400

# @app.route('/grades/<student_name>', methods=['DELETE'])
# def delete_grade(student_name):
#     student = Student.query.get(student_name)
#     if not student:
#         return jsonify({"error": "Student not found"}), 404
    
#     db.session.delete(student)
#     db.session.commit()
#     return jsonify({"message": f"Deleted grade for {student_name}"})

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)