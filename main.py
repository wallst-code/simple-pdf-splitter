#!/usr/bin/env python3
"""
Flask web application entry point for Simple PDF Splitter.
Localhost deployment for desktop browsers.
"""

import sys
import os
import webbrowser
import threading
import time
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.settings import (
    FLASK_SECRET_KEY, FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
    MAX_CONTENT_LENGTH_MB, SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE,
    WTF_CSRF_ENABLED, WTF_CSRF_TIME_LIMIT
)

def create_app() -> Flask:
    """
    Create and configure Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Security Configuration
    app.secret_key = FLASK_SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH_MB * 1024 * 1024
    
    # Secure Session Configuration
    app.config['SESSION_COOKIE_SECURE'] = SESSION_COOKIE_SECURE
    app.config['SESSION_COOKIE_HTTPONLY'] = SESSION_COOKIE_HTTPONLY
    app.config['SESSION_COOKIE_SAMESITE'] = SESSION_COOKIE_SAMESITE
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    app.config['SESSION_PERMANENT'] = False  # Session clears on browser close
    
    # CSRF Protection (disabled for now in .env during development)
    app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
    app.config['WTF_CSRF_TIME_LIMIT'] = WTF_CSRF_TIME_LIMIT
    if WTF_CSRF_ENABLED:
        csrf = CSRFProtect(app)
    
    # Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
        headers_enabled=True  # Enable rate limit headers including Retry-After
    )
    
    # Security Headers
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https://unpkg.com; img-src 'self' data:; style-src 'self' 'unsafe-inline';"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response
    
    _register_routes(app, limiter)
    _configure_upload_folder(app)
    
    return app

def _register_routes(app: Flask, limiter: Limiter) -> None:
    """Register all application routes with rate limiting."""
    from views.web_routes import register_web_routes
    register_web_routes(app, limiter)

def _configure_upload_folder(app: Flask) -> None:
    """Configure secure upload folder for temporary files."""
    upload_dir = Path.cwd() / 'temp_uploads'
    upload_dir.mkdir(exist_ok=True)
    app.config['UPLOAD_FOLDER'] = str(upload_dir)

def open_browser(url: str, delay: float = 1.5) -> None:
    """
    Open browser after a short delay to ensure server is running.
    
    Args:
        url: URL to open
        delay: Seconds to wait before opening browser
    """
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    
    thread = threading.Thread(target=_open)
    thread.daemon = True
    thread.start()

def cleanup_temp_files() -> None:
    """Clean up temporary files on shutdown."""
    temp_dir = Path.cwd() / 'temp_uploads'
    if temp_dir.exists():
        try:
            count = 0
            for file in temp_dir.glob('*.pdf'):
                try:
                    file.unlink()
                    count += 1
                except:
                    pass  # Ignore files in use
            if count > 0:
                print(f"Cleaned up {count} temporary file(s)")
        except:
            pass

def main() -> int:
    """
    Main entry point for localhost web application.
    
    Returns:
        int: Exit code
    """
    import atexit
    
    # Register cleanup on exit
    atexit.register(cleanup_temp_files)
    
    try:
        app = create_app()
        url = f"http://{FLASK_HOST}:{FLASK_PORT}"
        print(f"Starting Simple PDF Splitter at {url}")
        print("DEBUG: Print statements are working in terminal!")
        
        # Open browser automatically if not in debug reload mode
        if not os.environ.get('WERKZEUG_RUN_MAIN'):
            print("Opening browser...")
            open_browser(url)
        
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
        return 0
    except Exception as e:
        print(f"Failed to start application: {e}")
        return 1
    finally:
        cleanup_temp_files()

if __name__ == "__main__":
    sys.exit(main())