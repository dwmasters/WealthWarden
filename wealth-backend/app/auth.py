from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, db
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    email = data.get('email')
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({'message': 'User already exists'}), 409)

    # Create new user
    new_user = User(
        email=email,
        password_hash=generate_password_hash(data.get('password'))
    )
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'message': 'User registered successfully'}), 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=1))
        return jsonify(access_token=access_token), 200

    return make_response(jsonify({'message': 'Invalid credentials'}), 401)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        user_data = {
            "email": user.email,
            "created_at": user.created_at
        }
        return jsonify(user_data), 200

    return make_response(jsonify({'message': 'User not found'}), 404)

# Additional routes and functionalities can be added here
