from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
# from backend import *
from models import *
from db_config import db

app = Flask(__name__)

# app.run

admin = Admin.Admin(app, name='Admin', template_mode='bootstrap3')

class studentView(ModelView):
    column_list = ['name', 'email']
    can_create = False
    can_edit = False
    can_delete = False

class teacherView(ModelView):
    can_edit = True
    can_delete = False
    can_create = False
    column_searchable_list = ['name', 'grade']

class courseView(ModelView):
    can_edit = False
    can_delete = False
    can_create = False
    


admin.add_view(teacherView(Instructor, db.session))
admin.add_view(courseView(Course,db.session))
admin.add_view(studentView(Student, db.session))

if __name__ == "__main__":
    app.run(debug=True)