from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grades.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Student(db.Model):
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    grade = db.Column(db.Float, primary_key=False, unique=False, nullable=True)

    def to_dict(self):
        return {"username": self.username, "password": self.password, "name": self.name, "grade": self.grade}
    
class Instructor(db.Model):
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, primary_key=False, unique=False, nullable=False)

    def to_dict(self):
        return {"username": self.username, "password": self.password, "name": self.name}

class Course(db.Model):    
    course = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    instructor = db.Column(db.String, unique=False, nullable=False)
    time = db.Column(db.String, unique=False, nullable=False)
    capacity = db.Column(db.Int, unique=False, nullable=False)
    students = db.Column(db.String, unique=False, nullable=False)

    def to_dict(self):
        return {"course": self.course, "instructor": self.instructor, "time": self.time, "capacity": self.capacity, "students": self.students}

def init_db():
    with app.app_context():
        db.create_all()
        if not Student.query.first():
            sample_data = [
                Student(name="John Doe", grade=85.5),
                Student(name="Jane Smith", grade=92.0)
            ]
            db.session.add_all(sample_data)
            db.session.commit()

@app.route('/grades', methods=['GET'])
def get_all_grades():
    students = Student.query.all()
    return jsonify({"grades": [student.to_dict() for student in students]})

@app.route('/grades/<student_name>', methods=['GET'])
def get_grade(student_name):
    student = Student.query.get(student_name)
    if student:
        return jsonify(student.to_dict())
    return jsonify({"error": "Student not found"}), 404

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.get_json()
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        new_student = Student(name=data['name'], grade=float(data['grade']))
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Student already exists"}), 400
    except ValueError:
        return jsonify({"error": "Invalid grade format"}), 400

@app.route('/grades/<student_name>', methods=['PUT'])
def update_grade(student_name):
    student = Student.query.get(student_name)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    if not data or 'grade' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        student.grade = float(data['grade'])
        db.session.commit()
        return jsonify(student.to_dict())
    except ValueError:
        return jsonify({"error": "Invalid grade format"}), 400

@app.route('/grades/<student_name>', methods=['DELETE'])
def delete_grade(student_name):
    student = Student.query.get(student_name)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Deleted grade for {student_name}"})

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)