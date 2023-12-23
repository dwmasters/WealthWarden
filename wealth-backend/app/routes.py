from flask import Blueprint, request, jsonify, current_app
from app.models import db, User, Account
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'error': 'Email already in use'}), 409

    try:
        user = User(email=data['email'], username=data.get('username'))
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except SQLAlchemyError as e:
        current_app.logger.error(f'Registration Error: {str(e)}')
        return jsonify({'error': 'Database error occurred'}), 500

@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@routes_bp.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or not data.get('account_type'):
        return jsonify({'error': 'Missing account type'}), 400

    try:
        account = Account(account_type=data['account_type'], user_id=user_id)
        db.session.add(account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully', 'account_id': account.id}), 201
    except SQLAlchemyError as e:
        current_app.logger.error(f'Account Creation Error: {str(e)}')
        return jsonify({'error': 'Database error occurred'}), 500

# Additional routes can be added here

# Example of an error handling route
@routes_bp.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500
