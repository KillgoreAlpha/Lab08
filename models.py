from werkzeug.security import generate_password_hash
from db_config import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    __tablename__='student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    grade = db.Column(db.Float ,unique=False, nullable=True)
    role = db.Column(db.String, unique=False,nullable=False,default="student")
    courses = db.relationship('Course', secondary='course_student', lazy='subquery', backref=db.backref('enrolled_students', lazy=True))
    def to_dict(self):
        return {"id":self.id,
                "username": self.username, 
                #"password": self.password, 
                "name": self.name, 
                "grade": self.grade,
                "role":self.role}
    
class Instructor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.String, unique=False,nullable=False,default="instruct")

    def to_dict(self):
        return {"id":self.id,
                "username": self.username, 
                #"password": self.password, 
                "name": self.name,
                "role":self.role}
course_student = db.Table(
    'course_student',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)

class Course(db.Model,UserMixin): 
    __tablename__ = 'course'  
    id = db.Column(db.Integer, primary_key=False) 
    course = db.Column(db.String, primary_key=True,unique=True, nullable=False)
    instructor = db.Column(db.String, unique=False, nullable=False)
    time = db.Column(db.String, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    students = db.relationship('Student', secondary=course_student,lazy='subquery')

    def to_dict(self):
        return {"id":self.id,
                "course": self.course, 
                "instructor": self.instructor,
                  "time": self.time, 
                  "capacity": self.capacity, 
                  "students": [student.to_dict() for student in self.students],}
