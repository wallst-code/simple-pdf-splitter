"""HTMX request handlers - enterprise compliant."""

from typing import Dict, Any, List
from flask import request, render_template, session
from core.dependencies import get_dependencies
from views.fragments import (
    error_fragment, 
    success_fragment, 
    file_info_fragment,
    reset_fragment
)


class HTMXHandlers:
    """Handles HTMX requests with dependency injection."""
    
    def __init__(self):
        """Initialize with injected dependencies."""
        deps = get_dependencies()
        self.presenter = deps.presenter_factory()
        self.pdf_service = deps.pdf_service
    
    def handle_upload(self) -> str:
        """Handle file upload via HTMX."""
        if 'pdf_file' not in request.files:
            return error_fragment("No file selected")
        
        file = request.files['pdf_file']
        if not file or not file.filename:
            return error_fragment("No file selected")
        
        result = self.presenter.handle_file_upload(file)
        
        if not result['success']:
            return error_fragment(result.get('error', 'Upload failed'))
        
        return self._upload_success_response(result)
    
    def handle_reset(self) -> str:
        """Reset upload form."""
        self.presenter.cleanup_session()
        return reset_fragment()
    
    def handle_configure(self) -> str:
        """Get configuration form."""
        document = self.presenter.get_current_document()
        if not document:
            return error_fragment("No document uploaded")
        
        splits = self.presenter.get_current_splits() or [{}]
        
        return render_template(
            'fragments/configure_form.html',
            document=document,
            splits=splits,
            client_name=self.presenter.get_client_name(),
            case_number=self.presenter.get_case_number()
        )
    
    def handle_add_split(self) -> str:
        """Add new split row."""
        self._save_form_state(request.form)
        self.presenter.add_split_row()
        
        document = self.presenter.get_current_document()
        splits = self.presenter.get_current_splits()
        new_index = len(splits) - 1
        
        return render_template(
            'fragments/split_row.html',
            split=splits[new_index],
            document=document,
            loop={'index0': new_index}
        )
    
    def handle_remove_split(self, index: int) -> str:
        """Remove split row."""
        self._save_form_state(request.form)
        self.presenter.remove_split_row(index)
        return ""
    
    def handle_process(self) -> str:
        """Process PDF splits."""
        splits_data = self.presenter.extract_splits_from_form(request.form)
        
        if not splits_data:
            return error_fragment("Please configure at least one valid split")
        
        result = self.presenter.process_split_requests(splits_data)
        
        if not result['success']:
            return error_fragment(result.get('error', 'Processing failed'))
        
        return self._process_success_response(result['results'])
    
    def _upload_success_response(self, result: Dict[str, Any]) -> str:
        """Generate upload success response."""
        html = file_info_fragment(result)
        html += '''
        <script>
            document.getElementById('configure-section').classList.remove('disabled');
            document.getElementById('configure-status').textContent = 'Active';
            document.getElementById('configure-status').className = 'section-status status-active';
            htmx.ajax('GET', '/htmx/configure', {target: '#configure-content', swap: 'innerHTML'});
        </script>
        '''
        return html
    
    def _process_success_response(self, results: List[Dict[str, Any]]) -> str:
        """Generate process success response."""
        return render_template(
            'fragments/results.html',
            results=results
        )
    
    def _save_form_state(self, form_data: Dict[str, Any]) -> None:
        """Save form state to session."""
        session['client_name'] = form_data.get('client_name', '')
        session['case_number'] = form_data.get('case_number', '')
        
        splits = []
        index = 0
        while f'start_page_{index}' in form_data:
            split = {
                'start_page': form_data.get(f'start_page_{index}', 1),
                'end_page': form_data.get(f'end_page_{index}', 1),
                'document_code': form_data.get(f'document_code_{index}', ''),
                'output_name': form_data.get(f'output_name_{index}', '')
            }
            splits.append(split)
            index += 1
        
        session['splits'] = splits
        session.modified = True