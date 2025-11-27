"""
Authentication Service Module
Handles user authentication and authorization with security best practices
"""

import hashlib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

class AuthService:
    """Service for authentication and authorization"""
    
    # Demo users (in production, this would be in a database)
    DEMO_USERS = {
        'admin': {
            'password_hash': generate_password_hash('admin123'),  # Demo password
            'role': 'admin',
            'name': 'Administrator'
        },
        'staff': {
            'password_hash': generate_password_hash('staff123'),  # Demo password
            'role': 'staff',
            'name': 'Staff Member'
        },
        'viewer': {
            'password_hash': generate_password_hash('viewer123'),  # Demo password
            'role': 'viewer',
            'name': 'Viewer'
        }
    }
    
    @staticmethod
    def hash_password(password):
        """Hash a password using secure hashing algorithm"""
        return generate_password_hash(password)
    
    @staticmethod
    def verify_password(password_hash, password):
        """Verify a password against its hash"""
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user
        
        Returns:
            dict with user info if successful, None otherwise
        """
        user = AuthService.DEMO_USERS.get(username)
        if user and AuthService.verify_password(user['password_hash'], password):
            return {
                'username': username,
                'role': user['role'],
                'name': user['name']
            }
        return None
    
    @staticmethod
    def has_permission(user_role, required_permission):
        """
        Check if user role has required permission
        
        Permissions:
        - admin: Full access
        - staff: Can create, view, update requests
        - viewer: Can only view requests
        """
        role_permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'manage_users'],
            'staff': ['create', 'read', 'update'],
            'viewer': ['read']
        }
        
        user_perms = role_permissions.get(user_role, [])
        return required_permission in user_perms
    
    @staticmethod
    def generate_session_token():
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_user_role(username):
        """Get user role"""
        user = AuthService.DEMO_USERS.get(username)
        return user['role'] if user else None

