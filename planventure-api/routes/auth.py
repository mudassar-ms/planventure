from flask import Blueprint, request, jsonify
from models import User, db
from schemas.user_schema import UserSchema
from utils.jwt_utils import JWTManager
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Get and validate data
        data = request.get_json()
        
        # Validate email format
        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            return jsonify({'error': str(e)}), 400
            
        # Validate data against schema
        errors = user_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        new_user = User(
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        # Set and validate password
        success, error = new_user.set_password(data['password'])
        if not success:
            return jsonify({'error': error}), 400

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        # Generate tokens
        tokens = JWTManager.generate_tokens(new_user.id)

        # Return response
        return jsonify({
            'message': 'Registration successful',
            'user': new_user.to_dict(),
            'tokens': tokens
        }), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate tokens
        tokens = JWTManager.generate_tokens(user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'tokens': tokens
        })

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500