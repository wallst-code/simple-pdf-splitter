"""HTML fragment builders for HTMX responses."""

from typing import Dict, Any, List, Optional


def build_error_fragment(message: str) -> str:
    """Build error message HTML fragment."""
    return f'''
    <div class="file-info" style="background: #f8d7da; border-color: #f5c6cb;">
        <p style="color: #721c24;"><strong>Error:</strong> {message}</p>
    </div>
    '''


def build_upload_success_fragment(data: Dict[str, Any]) -> str:
    """Build upload success HTML fragment."""
    return f'''
    <div class="file-info active">
        <p><strong>✅ File uploaded successfully!</strong></p>
        <p><strong>File:</strong> {data.get('filename', 'Unknown')}</p>
        <p><strong>Pages:</strong> {data.get('page_count', 0)}</p>
        <p><strong>Size:</strong> {data.get('file_size_mb', 0):.2f} MB</p>
    </div>
    '''


def build_split_row_fragment(index: int, page_count: int, 
                            start: int = None, end: int = None,
                            description: str = "") -> str:
    """Build split row HTML fragment."""
    start_val = start if start else (1 if index == 0 else "")
    end_val = end if end else (page_count if index == 0 else "")
    desc_val = description or f"Split {index + 1}"
    
    return f'''
    <div class="split-row" id="split-{index}">
        <div class="split-fields">
            <div class="form-group">
                <label>Start Page</label>
                <input type="number" 
                       name="split_{index}_start" 
                       min="1" 
                       max="{page_count}" 
                       value="{start_val}"
                       required>
            </div>
            <div class="form-group">
                <label>End Page</label>
                <input type="number" 
                       name="split_{index}_end" 
                       min="1" 
                       max="{page_count}" 
                       value="{end_val}"
                       required>
            </div>
            <div class="form-group" style="flex: 2;">
                <label>Description</label>
                <input type="text" 
                       name="split_{index}_description" 
                       value="{desc_val}"
                       placeholder="e.g., Pages 1-10">
            </div>
        </div>
        <button type="button" 
                class="btn-remove"
                hx-delete="/htmx/remove-split/{index}"
                hx-target="#split-{index}"
                hx-swap="outerHTML">
            Remove
        </button>
    </div>
    '''


def build_success_summary(total: int, successful: int) -> str:
    """Build success summary HTML."""
    return f'''
    <div class="results-summary">
        <h3>✅ PDF Split Complete!</h3>
        <p>{successful} of {total} splits completed successfully.</p>
    </div>
    '''


def build_document_info(filename: str, page_count: int) -> str:
    """Build document info HTML."""
    return f'''
    <div class="document-info">
        <p><strong>Original File:</strong> {filename}</p>
        <p><strong>Total Pages:</strong> {page_count}</p>
    </div>
    '''


def build_success_result(result: Dict[str, Any]) -> str:
    """Build successful result item HTML."""
    return f'''
    <div class="result-item success">
        <div class="result-info">
            <h4>{result.get('filename', 'Unknown')}</h4>
            <p>Pages {result.get('start_page', '?')}-{result.get('end_page', '?')}</p>
            <p class="description">{result.get('description', '')}</p>
        </div>
        <a href="/download/{result.get('filename', '')}" 
           class="btn-download">
            Download
        </a>
    </div>
    '''


def build_error_result(result: Dict[str, Any]) -> str:
    """Build error result item HTML."""
    error_msg = result.get('error', 'Unknown error')
    description = result.get('description', '')
    
    return f'''
    <div class="result-item error">
        <div class="result-info">
            <h4>❌ Split Failed</h4>
            <p class="description">{description}</p>
            <p class="error-message">{error_msg}</p>
        </div>
    </div>
    '''


def build_download_all_button() -> str:
    """Build download all button HTML."""
    return '''
    <div style="margin-top: 2rem; text-align: center;">
        <a href="/download-all" class="btn-secondary">
            📦 ZIP All
        </a>
    </div>
    '''


def build_new_pdf_button() -> str:
    """Build new PDF button HTML."""
    return '''
    <div style="margin-top: 2rem; text-align: center;">
        <button type="button" 
                class="btn-primary"
                onclick="window.location.href='/'">
            📄 Add New PDF
        </button>
    </div>
    '''


def build_status_update_script() -> str:
    """Build status update JavaScript."""
    return '''
    <script>
        // Update status to show results
        if (window.pdfSplitter) {
            window.pdfSplitter.showResults();
        }
    </script>
    '''