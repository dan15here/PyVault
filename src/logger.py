import logging
import os
from datetime import datetime

class ActivityLogger:
    def __init__(self, log_file='pyvault.log'):
        self.log_file = log_file
        self.logger = logging.getLogger('pyvault')
        self.logger.setLevel(logging.INFO)
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_app_start(self):
        self.logger.info("=" * 50)
        self.logger.info("APPLICATION STARTED")
        self.logger.info("=" * 50)
    
    def log_app_exit(self):
        self.logger.info("APPLICATION EXITED")
        self.logger.info("-" * 50)
    
    def log_first_setup(self, success):
        if success:
            self.logger.info("FIRST TIME SETUP: Master password created successfully")
        else:
            self.logger.warning("FIRST TIME SETUP: Setup cancelled or failed")
    
    def log_login(self, success):
        if success:
            self.logger.info("LOGIN: User logged in successfully")
        else:
            self.logger.warning("LOGIN: Failed login attempt")
    
    def log_add_item(self, site_name):
        self.logger.info(f"ADD ITEM: New account added for '{site_name}'")
    
    def log_view_item(self, site_name):
        self.logger.info(f"VIEW ITEM: Viewed details for '{site_name}'")
    
    def log_edit_item(self, site_name):
        self.logger.info(f"EDIT ITEM: Updated account for '{site_name}'")
    
    def log_delete_item(self, site_name):
        self.logger.warning(f"DELETE ITEM: Deleted account for '{site_name}'")
    
    def log_copy_password(self, site_name):
        self.logger.info(f"COPY PASSWORD: Password copied for '{site_name}'")
    
    def log_menu_action(self, action):
        self.logger.info(f"MENU: User selected '{action}'")
    
    def log_error(self, error_message):
        self.logger.error(f"ERROR: {error_message}")

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = ActivityLogger()
    return _logger
