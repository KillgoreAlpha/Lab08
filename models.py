from werkzeug.security import generate_password_hash
from db_config import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    grade = db.Column(db.Float, primary_key=False, unique=False, nullable=True)
    role = db.Column(db.String, unique=False,nullable=False,default="student")

    def to_dict(self):
        return {"id":self.id,
                "username": self.username, 
                #"password": self.password, 
                "name": self.name, 
                "grade": self.grade,
                "role":self.role}
    
class Instructor(db.Model,UserMixin):
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, primary_key=False, unique=False, nullable=False)
    role = db.Column(db.String, unique=False,nullable=False,default="instruct")

    def to_dict(self):
        return {"username": self.username, 
                #"password": self.password, 
                "name": self.name,
                "role":self.role}

class Course(db.Model,UserMixin):   
    id = db.Column(db.Integer, primary_key=True) 
    course = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    instructor = db.Column(db.String, unique=False, nullable=False)
    time = db.Column(db.String, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    students = db.Column(db.String, unique=False, nullable=False)

    def to_dict(self):
        return {"id":self.id,
                "course": self.course, 
                "instructor": self.instructor,
                  "time": self.time, 
                  "capacity": self.capacity, 
                  "students": self.students}
