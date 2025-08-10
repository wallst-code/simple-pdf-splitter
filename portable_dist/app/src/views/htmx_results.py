"""HTMX result fragments and helpers."""

from typing import Dict, Any
from views.htmx_fragments import (
    build_error_fragment,
    build_success_result,
    build_error_result,
    build_download_all_button,
    build_new_pdf_button,
    build_status_update_script
)


def build_results_fragment(results_data: Dict[str, Any]) -> str:
    """Generate complete results fragment."""
    if not results_data:
        return build_error_fragment("No results found")
    
    success_summary = _build_success_summary(results_data)
    document_info = _build_document_info(results_data)
    results_list = _build_results_list(results_data['results'])
    download_options = _build_download_options()
    new_pdf_button = build_new_pdf_button()
    status_script = build_status_update_script()
    
    return f'''
    <div>
        {success_summary}
        {document_info}
        <div class="results-list">
            <h4 style="color: #495057; margin-bottom: 1rem;">Created Files:</h4>
            {results_list}
        </div>
        {download_options}
        {new_pdf_button}
    </div>
    {status_script}
    '''




def _build_success_summary(results_data: Dict[str, Any]) -> str:
    """Build success summary HTML."""
    return f'''
    <div class="alert alert-success">
        <h3>✅ Processing Complete!</h3>
        <p>Successfully created {results_data['success_count']} of {results_data['total_count']} PDF files</p>
        <p><strong>📁 All files have been saved to your Downloads folder</strong></p>
    </div>
    '''


def _build_document_info(results_data: Dict[str, Any]) -> str:
    """Build document info HTML."""
    original_doc = results_data.get('original_document')
    if original_doc:
        original_name = original_doc.filename
        page_count = original_doc.page_count
    else:
        original_name = 'Unknown'
        page_count = 'Unknown'
    
    return f'''
    <div style="background: #e9ecef; border: 1px solid #dee2e6; border-radius: 6px; padding: 1rem; margin-bottom: 1.5rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #495057;">Original Document: {original_name}</h4>
        <p style="margin: 0; color: #6c757d;">Total Pages: {page_count} | Split into {results_data['success_count']} files</p>
    </div>
    '''


def _build_results_list(results: list) -> str:
    """Build results list HTML."""
    html = ''
    for result in results:
        if result['success']:
            html += build_success_result(result)
        else:
            html += build_error_result(result)
    return html


def _build_download_options() -> str:
    """Build download options HTML."""
    return '''
    <div style="margin-top: 2rem; padding: 1.5rem; background: #e9ecef; border-radius: 6px;">
        <h4 style="margin: 0 0 1rem 0; color: #495057;">Download Options:</h4>
        <div style="display: flex; gap: 1rem; justify-content: center; align-items: center; flex-wrap: wrap;">
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">📁 Download individual files using the buttons above</p>
            <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">- OR -</p>
            <a href="/download-all" class="btn-secondary" style="position: relative; top: -7px;">📦 ZIP All</a>
        </div>
    </div>
    '''