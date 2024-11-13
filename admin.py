from flask import Flask
from flask_admin import admin
from flask_admin.contrib.sqla import ModelView
from backend import db
from backend import *

app = Flask(__name__)

app.run

admin = admin.Admin(app, name='Admin', template_mode='bootstrap3')

class studentView(ModelView):
    column_list = ['name', 'email']
    can_create = False
    can_edit = False
    can_delete = False

admin.add_view(studentView(Student, db.session))

