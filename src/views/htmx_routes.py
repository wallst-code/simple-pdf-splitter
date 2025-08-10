"""
HTMX route handlers for single-page application.
Returns HTML fragments instead of full pages.
"""

from typing import Any
from flask import Flask, render_template_string, request, session, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from flask_limiter import Limiter

from presenters.web_presenter import WebPresenter
from views.htmx_fragments import (
    build_error_fragment,
    build_upload_success_fragment
)
from views.htmx_configure import register_configure_routes
from views.htmx_results import build_results_fragment


def _handle_upload(app: Flask, request) -> str:
    """Handle file upload."""
    try:
        if 'pdf_file' not in request.files:
            return build_error_fragment("No file uploaded")
        
        file = request.files['pdf_file']
        if file.filename == '':
            return build_error_fragment("No file selected")
        
        session.clear()
        app.logger.info(f"Uploading file: {file.filename}")
        
        presenter = WebPresenter()
        result = presenter.handle_file_upload(file)
        app.logger.info(f"Upload result: {result}")
        
        if result.get('success'):
            success_data = {
                'filename': result.get('original_name', file.filename),
                'page_count': result.get('page_count', 0),
                'file_size_mb': result.get('file_size_mb', 0)
            }
            return build_upload_success_fragment(success_data)
        else:
            return build_error_fragment(result.get('error', 'Upload failed'))
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return build_error_fragment(f"Upload failed: {str(e)}")




def _handle_process(request) -> str:
    """Handle process request."""
    presenter = WebPresenter()
    splits_data = presenter.extract_splits_from_form(request.form)
    
    if not splits_data:
        return build_error_fragment("Please configure at least one valid split")
    
    result = presenter.process_split_requests(splits_data)
    
    if result['success']:
        results_data = presenter.get_processing_results()
        return build_results_fragment(results_data)
    else:
        return build_error_fragment(result['error'])


def _handle_reset() -> str:
    """Handle reset request."""
    presenter = WebPresenter()
    presenter.cleanup_session()
    session.clear()
    return _reset_fragment()




def register_htmx_routes(app: Flask, limiter: Limiter = None) -> None:
    """
    Register HTMX-specific routes that return HTML fragments.
    
    Args:
        app: Flask application instance
        limiter: Flask-Limiter instance for rate limiting
    """
    
    # Register configure-related routes
    register_configure_routes(app)
    
    # Create upload route with rate limiting
    if limiter:
        @app.route('/htmx/upload', methods=['POST'])
        @limiter.limit("10 per minute")
        def htmx_upload() -> str:
            """Handle file upload via HTMX, return HTML fragment."""
            return _handle_upload(app, request)
    else:
        @app.route('/htmx/upload', methods=['POST'])
        def htmx_upload() -> str:
            """Handle file upload via HTMX, return HTML fragment."""
            return _handle_upload(app, request)
    
    
    
    @app.route('/htmx/process', methods=['POST'])
    def htmx_process() -> str:
        """Process splits and return results HTML fragment."""
        return _handle_process(request)
    
    @app.route('/htmx/reset', methods=['POST'])
    def htmx_reset() -> str:
        """Reset the application state."""
        return _handle_reset()


def _save_form_state(form_data) -> None:
    """Save current form state to session."""
    session['client_name'] = form_data.get('client_name', '')
    session['case_number'] = form_data.get('case_number', '')
    
    splits = []
    index = 0
    while f'start_page_{index}' in form_data:
        splits.append({
            'start_page': form_data.get(f'start_page_{index}', 1),
            'end_page': form_data.get(f'end_page_{index}', 1),
            'document_code': form_data.get(f'document_code_{index}', ''),
            'output_name': form_data.get(f'output_name_{index}', '')
        })
        index += 1
    
    if splits:
        session['splits'] = splits




def _reset_fragment() -> str:
    """Generate reset fragment - reload the page."""
    return '<script>window.location.reload();</script>'