"""
Flask web routes for PDF splitter application.
Implements desktop-focused web interface for localhost deployment.
"""

from typing import Any, Dict
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session
from werkzeug.exceptions import RequestEntityTooLarge
from flask_limiter import Limiter

from src.presenters.web_presenter import WebPresenter
from src.views.htmx_routes import register_htmx_routes
from src.models.split_request import PDFDocument

def register_web_routes(app: Flask, limiter: Limiter = None) -> None:
    """
    Register all web routes with Flask application.
    
    Args:
        app: Flask application instance
        limiter: Flask-Limiter instance for rate limiting
    """
    _register_main_routes(app)
    _register_api_routes(app, limiter)
    _register_error_handlers(app)
    register_htmx_routes(app, limiter)  # Register HTMX routes with limiter

def _register_index_route(app: Flask) -> None:
    """Register index route."""
    @app.route('/')
    def index() -> str:
        """Single-page HTMX application with failsafe."""
        # Clean up orphaned files if session exists but file is missing
        if 'file_path' in session:
            import os
            if not os.path.exists(session.get('file_path', '')):
                # File doesn't exist, clear the session
                session.clear()
                session.modified = True
        return render_template('single_page.html')

def _register_session_routes(app: Flask) -> None:
    """Register session management routes."""
    @app.route('/clear-session', methods=['GET', 'POST'])
    def clear_session() -> str:
        """Clear session and redirect to index."""
        print(f"CLEAR-SESSION: Before clear, session keys={list(session.keys())}")
        from flask import redirect, url_for
        # Clean up any temp files first
        if 'file_path' in session:
            presenter = WebPresenter()
            presenter.cleanup_session()
        
        # Clear everything
        session.clear()
        session.modified = True
        print(f"CLEAR-SESSION: After clear, session keys={list(session.keys())}")
        print(f"CLEAR-SESSION: Redirecting to index")
        return redirect(url_for('index'))

def _register_about_route(app: Flask) -> None:
    """Register about page route."""
    @app.route('/about')
    def about() -> str:
        """Display about page with application information."""
        return render_template('about.html')
    
    @app.route('/documentation')
    def documentation() -> str:
        """Display documentation from README.md."""
        import os
        import markdown
        # Try multiple possible locations for README.md
        possible_paths = [
            os.path.join(os.path.dirname(app.root_path), 'README.md'),  # One level up from app
            os.path.join(app.root_path, 'README.md'),  # Same level as app
            'README.md'  # Current directory
        ]
        
        readme_content = None
        for readme_path in possible_paths:
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        readme_content = f.read()
                    break
                except Exception:
                    continue
        
        if readme_content:
            # Convert markdown to HTML
            html_content = markdown.markdown(
                readme_content, 
                extensions=['fenced_code', 'tables', 'toc']
            )
            return render_template('documentation.html', content=html_content)
        else:
            return render_template('documentation.html', 
                                 content="<p>Documentation not found.</p>")

def _register_main_routes(app: Flask) -> None:
    """Register all main page routes."""
    _register_index_route(app)
    _register_session_routes(app)
    _register_about_route(app)
    # Safe-mode removed - focusing on main functionality only
    _register_configure_route(app)
    _register_results_route(app)
    _register_download_routes(app)
    
def _register_configure_route(app: Flask) -> None:
    """Register configure route."""
    def _handle_configure_get(presenter: WebPresenter, document: PDFDocument) -> str:
        """Handle GET request for configure page. Max 20 lines."""
        splits = presenter.get_current_splits() or [{}]
        return render_template('configure.html', 
                             document=document, 
                             splits=splits,
                             client_name=presenter.get_client_name(),
                             case_number=presenter.get_case_number())
    
    @app.route('/configure', methods=['GET', 'POST'])
    def configure() -> str:
        """Configuration page - GET shows form, POST processes form. Max 20 lines."""
        presenter = WebPresenter()
        document = presenter.get_current_document()
        
        if not document:
            return redirect(url_for('index'))
        
        if request.method == 'GET':
            return _handle_configure_get(presenter, document)
        
        # Handle POST actions
        if 'add_split' in request.form:
            return _handle_configure_add_split(presenter, document)
        elif 'remove_split' in request.form:
            return _handle_configure_remove_split(presenter, document)
        elif 'process' in request.form:
            return _handle_configure_process(presenter, document)
    
def _register_results_route(app: Flask) -> None:
    """Register results route."""
    @app.route('/results')
    def results() -> str:
        """Results page showing processed files."""
        presenter = WebPresenter()
        results_data = presenter.get_processing_results()
        
        if not results_data:
            return render_template('results.html', error='No results found. Please process a PDF first.')
        
        return render_template('results.html',
                             results=results_data['results'],
                             success_count=results_data['success_count'],
                             total_count=results_data['total_count'],
                             original_document=results_data['original_document'])
    
def _create_results_zip(presenter: WebPresenter, results: Dict[str, Any]) -> Any:
    """Create zip file with all processed PDFs. Max 20 lines."""
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for result in results['results']:
            if result.get('success') and result.get('filename'):
                file_path = presenter.get_download_path(result['filename'])
                if file_path:
                    zip_file.write(file_path, result['filename'])
    
    zip_buffer.seek(0)
    return zip_buffer

def _register_download_routes(app: Flask) -> None:
    """Register download routes."""
    @app.route('/download/<filename>')
    def download_file(filename: str) -> Any:
        """Download processed PDF file securely."""
        presenter = WebPresenter()
        download_path = presenter.get_download_path(filename)
        
        if not download_path:
            return f'File {filename} not found', 404
        
        return send_file(download_path, as_attachment=True, download_name=filename)
    
    @app.route('/download-all')
    def download_all() -> Any:
        """Download all processed files as a zip. Max 20 lines."""
        presenter = WebPresenter()
        results = presenter.get_processing_results()
        
        if not results:
            return redirect(url_for('index'))
        
        zip_buffer = _create_results_zip(presenter, results)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='pdf_splits.zip'
        )

def _register_api_routes(app: Flask, limiter: Limiter = None) -> None:
    """Register minimal API endpoints if needed."""
    pass  # No API routes needed for pure form-based approach

def _register_error_handlers(app: Flask) -> None:
    """Register error handlers for common web errors."""
    
    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(error: RequestEntityTooLarge) -> Any:
        """Handle file size exceeded error."""
        return jsonify({
            'success': False, 
            'error': 'File too large. Maximum 100MB allowed.'
        }), 413