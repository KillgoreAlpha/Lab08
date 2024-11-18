from flask import Blueprint,request, jsonify
from flask_login import  login_user, logout_user, current_user,login_required
from werkzeug.security import check_password_hash
from db_config import db
from models import Instructor

instruct_login_bp = Blueprint('instruct_login',__name__)

@instruct_login_bp.route('/',methods=['POST'])

def instruct_login():
    data = request.get_json()
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