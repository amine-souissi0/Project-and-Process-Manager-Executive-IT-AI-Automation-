"""
Database Service Module
Handles all database operations with security best practices
"""

import json
import os
import shutil
from datetime import datetime
from config import Config

class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        self.database_file = Config.DATABASE_FILE
        self.backup_dir = Config.BACKUP_DIR
        self._ensure_backup_dir()
        self._init_database()
    
    def _ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def _init_database(self):
        """Initialize the database file if it doesn't exist"""
        if not os.path.exists(self.database_file):
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
    
    def load_requests(self):
        """Load all requests from the database with error handling"""
        self._init_database()
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Error loading database: {e}")
            return []
    
    def save_requests(self, requests):
        """Save requests to the database with atomic write"""
        try:
            # Create backup before saving
            if Config.AUTO_BACKUP_ENABLED:
                self._create_backup()
            
            # Atomic write: write to temp file first, then rename
            temp_file = self.database_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(requests, f, indent=2, ensure_ascii=False)
            
            # Replace original file
            if os.path.exists(temp_file):
                if os.path.exists(self.database_file):
                    os.replace(temp_file, self.database_file)
                else:
                    os.rename(temp_file, self.database_file)
            
            return True
        except (IOError, OSError) as e:
            print(f"Error saving database: {e}")
            return False
    
    def _create_backup(self):
        """Create a backup of the database file"""
        try:
            if os.path.exists(self.database_file):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = os.path.join(self.backup_dir, f'database_backup_{timestamp}.json')
                shutil.copy2(self.database_file, backup_file)
                
                # Keep only last 10 backups
                self._cleanup_old_backups()
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self):
        """Keep only the most recent 10 backup files"""
        try:
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('database_backup_') and filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    backups.append((os.path.getmtime(filepath), filepath))
            
            # Sort by modification time (newest first)
            backups.sort(reverse=True)
            
            # Remove backups beyond the 10 most recent
            for _, filepath in backups[10:]:
                try:
                    os.remove(filepath)
                except Exception:
                    pass
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
    
    def get_request_by_id(self, request_id):
        """Get a specific request by ID"""
        requests = self.load_requests()
        return next((r for r in requests if r.get('request_id') == request_id), None)
    
    def update_request(self, request_id, updates):
        """Update a specific request"""
        requests = self.load_requests()
        for i, req in enumerate(requests):
            if req.get('request_id') == request_id:
                requests[i].update(updates)
                return self.save_requests(requests)
        return False

