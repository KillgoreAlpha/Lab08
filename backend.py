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


@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)