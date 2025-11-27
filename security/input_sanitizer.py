"""
Input Sanitization Module
Security best practice: Sanitize all user inputs to prevent injection attacks
"""

import re
import html
from urllib.parse import quote, unquote

class InputSanitizer:
    """Service for sanitizing user inputs"""
    
    @staticmethod
    def sanitize_string(input_str, max_length=1000):
        """
        Sanitize a string input
        
        Args:
            input_str: The input string
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Convert to string and strip whitespace
        sanitized = str(input_str).strip()
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Escape HTML entities
        sanitized = html.escape(sanitized)
        
        return sanitized
    
    @staticmethod
    def sanitize_email(email):
        """Sanitize and validate email format"""
        if not email:
            return ""
        
        email = str(email).strip().lower()
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, email):
            return html.escape(email)
        return ""
    
    @staticmethod
    def sanitize_phone(phone):
        """Sanitize phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters except +, -, spaces
        phone = re.sub(r'[^\d+\-\s]', '', str(phone))
        return phone.strip()[:20]  # Limit to 20 characters
    
    @staticmethod
    def sanitize_request_id(request_id):
        """Sanitize request ID (alphanumeric and hyphens only)"""
        if not request_id:
            return ""
        
        # Only allow alphanumeric, hyphens, and underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '', str(request_id))
        return sanitized
    
    @staticmethod
    def sanitize_text_area(text, max_length=5000):
        """Sanitize text area input (allows more characters)"""
        if not text:
            return ""
        
        text = str(text).strip()
        
        # Limit length
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Escape HTML but preserve line breaks
        text = html.escape(text)
        text = text.replace('\n', '<br>')
        
        return text
    
    @staticmethod
    def validate_request_type(request_type):
        """Validate request type against allowed values"""
        allowed_types = [
            'Teleconsultation',
            'Hospital Booking',
            'Medical Evacuation',
            'Case Inquiry',
            'Claim',
            'Repatriation of Mortal Remains (RMR)',
            'Travel & Security Risk Evacuation',
            'Other'
        ]
        return request_type if request_type in allowed_types else 'Other'
    
    @staticmethod
    def validate_status(status):
        """Validate status against allowed values"""
        allowed_statuses = [
            'New',
            'In Progress',
            'Pending Info',
            'Completed',
            'Closed'
        ]
        return status if status in allowed_statuses else 'New'
    
    @staticmethod
    def validate_priority(priority):
        """Validate priority level"""
        allowed_priorities = ['Low', 'Medium', 'High', 'Urgent']
        return priority if priority in allowed_priorities else 'Medium'

