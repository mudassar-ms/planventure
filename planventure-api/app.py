from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables before any other code
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Basic configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

    # Initialize extensions
    CORS(app)
    db.init_app(app)

    # Import models here to avoid circular imports
    from models import User

    # Register routes
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run()
