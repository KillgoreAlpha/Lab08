from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
# from backend import *
from models import *
from db_config import db

app = Flask(__name__)

# app.run
app.secret_key = "thEZ3cr3tk3y"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

admin = Admin(app, name='Admin', template_mode='bootstrap3')

class studentView(ModelView):
    column_list = ['name', 'grade']
    can_create = True
    can_edit = True
    can_delete = True

class teacherView(ModelView):
    can_edit = True
    can_delete = True
    can_create = True
    column_searchable_list = ['name']

class courseView(ModelView):
    can_edit = True
    can_delete = True
    can_create = True
    


admin.add_view(teacherView(Instructor, db.session))
admin.add_view(courseView(Course,db.session))
admin.add_view(studentView(Student, db.session))

if __name__ == "__main__":
    app.run(debug=True)