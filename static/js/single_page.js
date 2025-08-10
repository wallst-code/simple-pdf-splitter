// Single page application JavaScript for PDF Splitter
// Handles HTMX integration, drag-and-drop, and UI state management

// Check if HTMX is available and configure UI accordingly
document.addEventListener('DOMContentLoaded', function() {
    if (typeof htmx !== 'undefined') {
        // HTMX is available - enable enhanced features
        document.body.classList.add('htmx-active');
        setupDragAndDrop();
        setupHTMXHandlers();
    } else {
        // HTMX failed - redirect to safe mode with fresh session
        console.log('HTMX not loaded - dynamic features unavailable');
        // Safe-mode removed - just show warning
    }
});

function setupDragAndDrop() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    console.log('Setting up drag and drop...');
    
    // Prevent default drag behaviors on the whole document
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, function(e) {
            e.preventDefault();
        }, false);
    });
    
    // Click to browse
    uploadArea.addEventListener('click', (e) => {
        if (e.target === uploadArea || e.target.parentElement === uploadArea) {
            console.log('Click detected, opening file browser');
            fileInput.click();
        }
    });
    
    // Drag enter
    uploadArea.addEventListener('dragenter', (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('Drag enter');
        uploadArea.classList.add('dragover');
    });
    
    // Drag over
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        // Keep the dragover class
    });
    
    // Drag leave
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        // Only remove if we're leaving the upload area completely
        if (e.target === uploadArea) {
            console.log('Drag leave');
            uploadArea.classList.remove('dragover');
        }
    });
    
    // Drop
    uploadArea.addEventListener('drop', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
        
        console.log('Drop event triggered');
        console.log('DataTransfer items:', e.dataTransfer.items.length);
        console.log('DataTransfer files:', e.dataTransfer.files.length);
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            console.log('File dropped:', file.name, 'Type:', file.type);
            
            // Enhanced PDF validation
            const validation = await PDFValidator.validatePDFFile(file);
            
            if (validation.isValid) {
                console.log('PDF validation passed, uploading...');
                
                // Set the file input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
                
                // Trigger the upload
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            } else {
                console.error('File validation failed:', validation.message);
                PDFValidator.showError(validation.message);
            }
        } else {
            console.log('No files in drop event');
        }
    });
    
    // File input change - trigger upload
    fileInput.addEventListener('change', () => {
        console.log('File input changed, files:', fileInput.files.length);
        
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type);
            
            // Show spinner
            document.getElementById('upload-spinner').classList.add('active');
            
            // Create form data
            const formData = new FormData();
            formData.append('pdf_file', file);
            
            // Upload file
            console.log('Sending POST to /htmx/upload');
            fetch('/htmx/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                console.log('Response received, length:', html.length);
                
                // Hide spinner
                document.getElementById('upload-spinner').classList.remove('active');
                
                // Insert result HTML (success message only)
                document.getElementById('upload-result').innerHTML = html;
                
                // Check if upload was successful by looking for success indicator
                if (html.includes('✅ File uploaded successfully')) {
                    console.log('Upload successful, enabling configure section');
                    
                    // Enable configure section
                    pdfSplitter.enableConfigure();
                    
                    // Load the configure form
                    fetch('/htmx/configure-form')
                        .then(response => response.text())
                        .then(formHtml => {
                            console.log('Configure form loaded');
                            document.getElementById('configure-content').innerHTML = formHtml;
                            // Process the new content with HTMX
                            htmx.process(document.getElementById('configure-content'));
                        })
                        .catch(error => {
                            console.error('Failed to load configure form:', error);
                        });
                }
            })
            .catch(error => {
                console.error('Upload error:', error);
                console.error('Error stack:', error.stack);
                console.error('Error type:', error.name);
                document.getElementById('upload-spinner').classList.remove('active');
                document.getElementById('upload-result').innerHTML = 
                    '<div class="file-info" style="background: #f8d7da; border-color: #f5c6cb; display: block;">' +
                    '<p style="color: #721c24;"><strong>Error:</strong> Upload failed - ' + error + '</p></div>';
            });
        }
    });
}

function setupHTMXHandlers() {
    // Listen for successful upload
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.detail.target.id === 'upload-result') {
            // Check if upload was successful
            if (evt.detail.xhr.status === 200) {
                enableSection('configure-section');
                updateStatus('upload-status', 'complete');
                updateStatus('configure-status', 'active');
            }
        } else if (evt.detail.target.id === 'results-content') {
            // Processing complete
            updateStatus('configure-status', 'complete');
            updateStatus('results-status', 'complete');
        }
    });
    
    // Handle HTMX errors - fall back to basic mode
    document.body.addEventListener('htmx:responseError', function(evt) {
        console.error('HTMX error:', evt.detail);
        fallbackToBasicMode();
    });
    
    document.body.addEventListener('htmx:sendError', function(evt) {
        console.error('HTMX send error:', evt.detail);
        fallbackToBasicMode();
    });
}

function enableSection(sectionId) {
    document.getElementById(sectionId).classList.remove('disabled');
}

function updateStatus(statusId, status) {
    const element = document.getElementById(statusId);
    element.className = 'section-status status-' + status;
    element.textContent = status.charAt(0).toUpperCase() + status.slice(1);
}

function fallbackToBasicMode() {
    // Remove HTMX class to show fallback forms
    document.body.classList.remove('htmx-active');
    document.getElementById('failsafe-notice').classList.add('active');
    
    // Enable all sections for standard form submission
    document.querySelectorAll('.workflow-section').forEach(section => {
        section.classList.remove('disabled');
    });
}

// Public functions for HTMX responses to call
window.pdfSplitter = {
    enableConfigure: function() {
        enableSection('configure-section');
        updateStatus('upload-status', 'complete');
        updateStatus('configure-status', 'active');
    },
    enableResults: function() {
        enableSection('results-section');
        updateStatus('configure-status', 'complete');
        updateStatus('results-status', 'active');
    },
    showResults: function() {
        enableSection('results-section');
        updateStatus('results-status', 'complete');
    }
};