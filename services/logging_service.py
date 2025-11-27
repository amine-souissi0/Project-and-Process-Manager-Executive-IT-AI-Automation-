"""
Logging Service Module
Handles activity logging with security considerations
"""

import os
from datetime import datetime
from config import Config

class LoggingService:
    """Service for activity logging"""
    
    def __init__(self):
        self.log_file = Config.ACTIVITY_LOG
    
    def log_activity(self, message, user='System', action_type='info'):
        """
        Log activity to the activity log file
        
        Args:
            message: The log message
            user: User who performed the action (default: 'System')
            action_type: Type of action (info, warning, error, security)
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] [{action_type.upper()}] [{user}] {message}\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log: {e}")
    
    def log_security_event(self, message, user='System'):
        """Log security-related events"""
        self.log_activity(message, user, 'security')
    
    def log_error(self, message, user='System'):
        """Log error events"""
        self.log_activity(message, user, 'error')
    
    def get_recent_logs(self, lines=50):
        """Get recent log entries"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []

