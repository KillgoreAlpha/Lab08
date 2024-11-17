from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_admin import admin
from backend import *
from backend import db

app = Flask(__name__)

app.run

admin = admin.Admin(app, name='Admin', template_mode='bootstrap3')

class studentView(ModelView):
    column_list = ['name', 'email']
    can_create = False
    can_edit = False
    can_delete = False

admin.add_view(studentView(Student, db.session))


# admin = admin.Admin(app, name="Admin", templaye_mode = 'bootstrap3')






class teacherView(ModelView):
    can_edit = True
    can_delete = False
    can_create = False
    column_searchable_list = ['name', 'grade']

class courseView(ModelView):
    can_edit = False
    can_delete = False
    can_delete = False
    


admin.add_view(teacherView(Instructor, db.session))
admin.add_view(courseView(Course,db.session))