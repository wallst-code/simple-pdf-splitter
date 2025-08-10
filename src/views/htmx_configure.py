"""HTMX configure form handlers."""

from flask import Flask, request, session
from presenters.web_presenter import WebPresenter
from views.htmx_fragments import build_error_fragment, build_split_row_fragment
from views.htmx_form_helpers import build_configure_form_fragment


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


def register_configure_routes(app: Flask) -> None:
    """Register configuration-related HTMX routes."""
    
    @app.route('/htmx/configure-form', methods=['GET'])
    def htmx_configure_form() -> str:
        """Get the configure form HTML fragment."""
        presenter = WebPresenter()
        document = presenter.get_current_document()
        
        if not document:
            return build_error_fragment("No document uploaded")
        
        return build_configure_form_fragment(presenter)
    
    @app.route('/htmx/add-split', methods=['POST'])
    def htmx_add_split() -> str:
        """Add a new split row."""
        from views.htmx_form_helpers import _build_split_row
        presenter = WebPresenter()
        document = presenter.get_current_document()
        
        if not document:
            return build_error_fragment("No document loaded")
        
        # Save current form state
        _save_form_state(request.form)
        
        # Save form data first to preserve user input
        form_data = dict(request.form)
        
        # Get current splits and find last end page from form data
        splits = []
        index = 0
        last_end_page = 0
        
        # Parse splits from form data to find the actual last end page
        while f'start_page_{index}' in form_data:
            try:
                end_page = int(form_data.get(f'end_page_{index}', 0))
                if end_page > last_end_page:
                    last_end_page = end_page
            except (ValueError, TypeError):
                pass
            index += 1
        
        # Create new split
        # Cap start page at total pages to prevent out of range error
        calculated_start = last_end_page + 1 if last_end_page > 0 else 1
        start_page = min(calculated_start, document.page_count)
        
        new_split = {
            'start_page': start_page,
            'end_page': document.page_count,
            'document_code': '',
            'output_name': ''
        }
        
        presenter.add_split_row_with_data(new_split)
        splits = presenter.get_current_splits()
        
        # Return the properly formatted split row
        return _build_split_row(len(splits) - 1, splits[-1], document)
    
    @app.route('/htmx/remove-split/<int:index>', methods=['DELETE'])
    def htmx_remove_split(index: int) -> str:
        """Remove a split row."""
        splits = session.get('splits', [])
        
        if 0 <= index < len(splits):
            splits.pop(index)
            session['splits'] = splits
        
        return ""  # Return empty to remove the element




def _find_last_end_page(splits: list) -> int:
    """Find the last end page from existing splits."""
    if not splits:
        return 0
    return max(split.get('end', 0) for split in splits)


def _create_new_split(index: int, start_page: int, max_page: int) -> dict:
    """Create a new split configuration."""
    return {
        'start': start_page,
        'end': min(start_page + 9, max_page),  # Default 10 pages or to end
        'description': f'Split {index + 1}'
    }