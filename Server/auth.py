from flask import Blueprint, jsonify, request
from app import db
from models import User, UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user)), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, Config.SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token})
