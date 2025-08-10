"""Application settings and configuration constants.

This module centralizes all application constants, defaults, and configuration
values to eliminate magic numbers and strings throughout the codebase.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Application Information
APP_NAME = "Simple PDF Splitter"
APP_VERSION = "1.0"
APP_ORGANIZATION = "PDF Tools"
APP_DESCRIPTION = "Tools for Lawyers, Built by Lawyers."

# Window Configuration
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_GEOMETRY = (100, 100, 1200, 800)  # x, y, width, height
WINDOW_MIN_SIZE = (1000, 600)  # width, height

# Header Configuration
HEADER_HEIGHT = 60
HEADER_MARGINS = (10, 5, 10, 5)  # left, top, right, bottom
BANNER_HEIGHT = 50

# UI Layout
LEFT_PANEL_WIDTH = 300
SPLIT_AREA_MIN_HEIGHT = 200
STATUS_TEXT_MAX_HEIGHT = 100

# File Paths
SETTINGS_FILENAME = ".pdf_splitter_settings.json"
BANNER_FILENAME = "banner.svg"

# Default Values
DEFAULT_OUTPUT_FOLDER = str(Path.home() / "Downloads")
DEFAULT_DOC_CODE = "DOC001"

# Colors and Styling
COLORS = {
    'background': '#f5f5f5',
    'header_background': '#f0f0f0',
    'header_border': '#ccc',
    'success_button': '#4CAF50',
    'button_hover': '#e6e6e6',
    'white': 'white',
    'border': '#ddd',
    'text_background': 'white'
}

# File Types
SUPPORTED_FILE_TYPES = "PDF Files (*.pdf)"

# Build Configuration
PYINSTALLER_HIDDEN_IMPORTS = [
    'src.services.pdf_service',
    'src.models.split_request', 
    'src.ui.gui.widgets.split_row_widget',
    'src.ui.gui.widgets.drag_drop_handler',
    'PyQt6.QtSvgWidgets'
]

# Feature Flags
FEATURES = {
    'drag_drop_enabled': True,
    'svg_banner_enabled': True,
    'auto_save_settings': True,
    'progress_reporting': True
}

# Validation Rules
VALIDATION = {
    'max_client_name_length': 100,
    'max_case_number_length': 50,
    'max_doc_code_length': 20,
    'max_optional_name_length': 100,
    'min_page_number': 1,
    'max_page_number': 10000
}

# Flask Web Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# SECURITY: Secret key from environment variable
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
if not FLASK_SECRET_KEY:
    # For local/desktop use, auto-generate a key
    import secrets
    FLASK_SECRET_KEY = secrets.token_hex(32)
    print("📝 Note: Auto-generated session key for local use. Run setup_simple.py to save configuration.")

MAX_CONTENT_LENGTH_MB = int(os.getenv('MAX_CONTENT_LENGTH_MB', '100'))

# Session Security Configuration
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')

# Security Settings
WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED', 'True').lower() == 'true'
WTF_CSRF_TIME_LIMIT = int(os.getenv('WTF_CSRF_TIME_LIMIT', '3600'))

def get_default_settings() -> Dict[str, Any]:
    """Get default application settings.
    
    Returns:
        Dict containing default settings for the application
    """
    return {
        'output_folder': DEFAULT_OUTPUT_FOLDER,
        'window_geometry': WINDOW_GEOMETRY,
        'auto_save': FEATURES['auto_save_settings'],
        'theme': 'default'
    }