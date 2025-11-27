"""
Configuration file for Ulink Assist Operations Automation Demo
Contains environment variables and security settings
"""

import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ulink-assist-demo-secret-key-2024-change-in-production'
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File paths
    DATABASE_FILE = 'database.json'
    ACTIVITY_LOG = 'activity.log'
    BACKUP_DIR = 'backups'
    
    # Security settings
    PASSWORD_HASH_ALGORITHM = 'pbkdf2:sha256'
    SESSION_TIMEOUT = timedelta(hours=8)
    
    # Automation settings
    AUTO_BACKUP_ENABLED = True
    AUTO_BACKUP_INTERVAL = 3600  # seconds (1 hour)
    EMAIL_NOTIFICATIONS_ENABLED = True
    
    # AI/Automation settings
    AI_TRIAGE_ENABLED = True
    TEXT_SUMMARIZATION_ENABLED = True
    SOP_GENERATION_ENABLED = True
    
    # Supported languages
    LANGUAGES = ['en', 'id']
    DEFAULT_LANGUAGE = 'en'
    
    # Roles
    ROLES = {
        'admin': 'Administrator',
        'staff': 'Staff Member',
        'viewer': 'Viewer'
    }

