"""
Authentication Routes Module
Handles user login, logout, and session management
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from security.auth_service import AuthService
from services.logging_service import LoggingService
from translations import get_all_translations

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
logger = LoggingService()

def get_language():
    """Get current language from session"""
    return session.get('language', 'en')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    lang = get_language()
    t = get_all_translations(lang)
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = auth_service.authenticate_user(username, password)
        
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            
            logger.log_security_event(f"User logged in: {username} (role: {user['role']})", username)
            
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            logger.log_security_event(f"Failed login attempt: {username}", 'System')
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', translations=t, lang=lang)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'Unknown')
    logger.log_security_event(f"User logged out: {username}", username)
    
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

