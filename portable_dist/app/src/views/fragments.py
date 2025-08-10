"""HTML fragment generators for HTMX responses."""

from typing import Optional, Any
from flask import render_template_string


def error_fragment(message: str) -> str:
    """Generate error message fragment."""
    template = '''
    <div class="alert alert-danger" role="alert">
        <strong>Error:</strong> {{ message }}
    </div>
    '''
    return render_template_string(template, message=message)


def success_fragment(message: str) -> str:
    """Generate success message fragment."""
    template = '''
    <div class="alert alert-success" role="alert">
        {{ message }}
    </div>
    '''
    return render_template_string(template, message=message)


def file_info_fragment(result: dict) -> str:
    """Generate file info display fragment."""
    template = '''
    <div class="file-info">
        <h3>📄 File Uploaded Successfully</h3>
        <p><strong>Name:</strong> {{ result.original_name }}</p>
        <p><strong>Pages:</strong> {{ result.page_count }}</p>
        <p><strong>Size:</strong> {{ result.file_size_mb }} MB</p>
    </div>
    '''
    return render_template_string(template, result=result)


def reset_fragment() -> str:
    """Generate reset/clear form fragment."""
    return '''
    <div class="upload-area" 
         onclick="document.getElementById('pdf_file').click()">
        <div class="upload-icon">📁</div>
        <h3>Click to Select PDF</h3>
        <p>or drag and drop your file here</p>
        <input type="file" id="pdf_file" name="pdf_file" 
               accept=".pdf" style="display: none;"
               hx-post="/htmx/upload"
               hx-target="#upload-content"
               hx-trigger="change"
               hx-encoding="multipart/form-data">
    </div>
    '''