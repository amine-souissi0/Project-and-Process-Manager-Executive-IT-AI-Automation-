"""
Ulink Assist Operations Automation Demo
A comprehensive Flask web application demonstrating IT, AI, and automation capabilities.
Built for Project and Process Manager Executive (IT, AI & Automation) role demonstration.
"""

from flask import Flask, session
from config import Config
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("ℹ️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually.")
except Exception as e:
    print(f"ℹ️  Could not load .env file: {e}")

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

# Initialize directories
def init_directories():
    """Initialize required directories"""
    directories = [
        'backups',
        'static/images',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

@app.before_request
def before_request():
    """Set default language if not set"""
    if 'language' not in session:
        session['language'] = Config.DEFAULT_LANGUAGE

@app.context_processor
def inject_config():
    """Make config available to all templates"""
    return dict(config=Config)

# Initialize directories on import (for Gunicorn)
init_directories()

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or use default
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 70)
    print("Ulink Assist Operations Automation Demo")
    print("=" * 70)
    print(f"Server starting on http://{host}:{port}")
    print("=" * 70)
    print("\nDemo Login Credentials:")
    print("  Admin:  username=admin, password=admin123")
    print("  Staff:  username=staff, password=staff123")
    print("  Viewer: username=viewer, password=viewer123")
    print("=" * 70)
    
    app.run(debug=debug, host=host, port=port)
