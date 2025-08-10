"""HTMX form fragment helpers."""

from presenters.web_presenter import WebPresenter


def build_configure_form_fragment(presenter: WebPresenter) -> str:
    """Generate configuration form fragment."""
    document = presenter.get_current_document()
    splits = presenter.get_current_splits() or [{}]
    
    splits_html = ''
    for i, split in enumerate(splits):
        splits_html += _build_split_row(i, split, document)
    
    return f'''
    <form id="configure-form">
        <div class="client-info">
            <h3>Client Information (Optional)</h3>
            <div class="form-row">
                <div class="form-group">
                    <label for="client_name">Client Name:</label>
                    <input type="text" id="client_name" name="client_name" 
                           value="{presenter.get_client_name()}" placeholder="Enter client name">
                </div>
                <div class="form-group">
                    <label for="case_number">Case Number:</label>
                    <input type="text" id="case_number" name="case_number" 
                           value="{presenter.get_case_number()}" placeholder="Enter case number">
                </div>
            </div>
        </div>
        
        <h3>Set Up Splits</h3>
        <div class="splits-container" id="splits-container">
            {splits_html}
        </div>
        
        <button type="button" 
                class="btn-add"
                hx-post="/htmx/add-split"
                hx-target="#splits-container"
                hx-swap="beforeend"
                hx-trigger="click"
                hx-include="#configure-form">
            + Add Split
        </button>
        
        <div style="margin-top: 2rem; text-align: center;">
            <button type="button"
                    class="btn-primary"
                    hx-post="/htmx/process"
                    hx-target="#results-content"
                    hx-trigger="click"
                    hx-include="#configure-form"
                    hx-indicator="#process-spinner">
                Process PDF Splits
            </button>
            <span id="process-spinner" class="loading" style="display:none; margin-left: 1rem;"></span>
        </div>
    </form>
    '''


def _build_split_row(index: int, split: dict, document) -> str:
    """Generate a single split row fragment for configure form."""
    start_page = split.get('start_page', 1)
    end_page = split.get('end_page', document.page_count if document else 1)
    doc_code = split.get('document_code', '')
    output_name = split.get('output_name', '')
    
    return f'''
    <div class="split-row">
        <div class="form-group">
            <label>Start Page:</label>
            <input type="number" name="start_page_{index}" value="{start_page}" 
                   min="1" max="{document.page_count if document else 999}" required>
        </div>
        <div class="form-group">
            <label>End Page:</label>
            <input type="number" name="end_page_{index}" value="{end_page}"
                   min="1" max="{document.page_count if document else 999}" required>
        </div>
        <div class="form-group" style="flex: 1;">
            <label>Document Code:</label>
            <input type="text" name="document_code_{index}" value="{doc_code}" 
                   placeholder="Optional">
        </div>
        <div class="form-group" style="flex: 1;">
            <label>Other:</label>
            <input type="text" name="output_name_{index}" value="{output_name}" 
                   placeholder="Optional">
        </div>
        <button type="button" 
                class="btn-remove"
                hx-delete="/htmx/remove-split/{index}"
                hx-target="closest .split-row"
                hx-swap="outerHTML"
                hx-include="#configure-form">
            Remove
        </button>
    </div>
    '''