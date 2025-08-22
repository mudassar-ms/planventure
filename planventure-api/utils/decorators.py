from functools import wraps
from flask import request, jsonify, g
from .jwt_utils import JWTManager

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
            
        token = auth_header.split(' ')[1]
        user_id = JWTManager.verify_access_token(token)
        
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
            
        # Store user_id in Flask's g object for route handlers
        g.user_id = user_id
        return f(*args, **kwargs)
        
    return decorated

from utils.decorators import jwt_required

@app.route('/protected')
@jwt_required
def protected_route():
    user_id = g.user_id  # Access the authenticated user's ID
    return jsonify({"message": f"Hello user {user_id}!"})