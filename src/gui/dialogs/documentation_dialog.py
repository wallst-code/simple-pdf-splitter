from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox


class DocumentationDialog(QDialog):
    """Documentation dialog with user guide."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle("Simple PDF Splitter - Documentation")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        doc_text = QTextEdit()
        doc_text.setReadOnly(True)
        doc_text.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                line-height: 1.6;
                padding: 15px;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        doc_text.setHtml(self._get_documentation())
        layout.addWidget(doc_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
    def _get_documentation(self):
        return """
        <h1>Simple PDF Splitter - User Guide</h1>
        
        <h2>🚀 Quick Start</h2>
        <ol>
            <li><b>Load PDF:</b> Click "Select PDF File" or drag & drop your PDF</li>
            <li><b>Enter Info:</b> Add client name and case number (optional)</li>
            <li><b>Configure Splits:</b> Set page ranges and document codes</li>
            <li><b>Process:</b> Click "Run Split" to create your files</li>
        </ol>
        
        <h2>📋 Features</h2>
        <ul>
            <li>✅ <b>Local Processing</b> - No cloud uploads required</li>
            <li>✅ <b>Smart Naming</b> - Automatic file naming with client/case info</li>
            <li>✅ <b>Batch Processing</b> - Split into multiple documents at once</li>
            <li>✅ <b>Page Validation</b> - Automatic checking for gaps and overlaps</li>
            <li>✅ <b>Professional Output</b> - Clean, organized file naming</li>
        </ul>
        
        <h2>🔧 How to Use</h2>
        
        <h3>Step 1: Load Your PDF</h3>
        <p>Choose one of these methods:</p>
        <ul>
            <li>Click the "Browse PDF" button</li>
            <li>Drag and drop your PDF into the marked area</li>
            <li>Use File → Open PDF from the menu</li>
        </ul>
        
        <h3>Step 2: Client Information (Optional)</h3>
        <p>Enter client name and case number for automatic file naming. If left blank, 
        files will use generic names with unique identifiers.</p>
        
        <h3>Step 3: Configure Splits</h3>
        <p>For each document you want to create:</p>
        <ul>
            <li><b>Start/End Page:</b> Select the page range</li>
            <li><b>Doc Code:</b> Enter a document code (e.g., "Ex. A", "Deposition")</li>
            <li><b>Optional Name:</b> Add additional description if needed</li>
            <li>Click "+ Add Split" to add more documents</li>
        </ul>
        
        <h3>Step 4: Process</h3>
        <p>Click "Run Split" to create your documents. Files are saved to your Downloads folder.</p>
        
        <h2>💡 Tips & Best Practices</h2>
        <ul>
            <li>✓ The app automatically calculates page ranges for new splits</li>
            <li>✓ Check the "Range Gaps" indicator to ensure all pages are covered</li>
            <li>✓ Use meaningful document codes for easy identification</li>
            <li>✓ Files include unique IDs to prevent naming conflicts</li>
        </ul>
        
        <h2>⚖️ Privacy & Security</h2>
        <ul>
            <li>🔒 Local processing - more private than web-based tools</li>
            <li>🔒 No requirement for internet transmission</li>
            <li>🔒 Temporary files cleaned after processing</li>
            <li>🔒 Usage not tracked or monitored</li>
        </ul>
        
        <h2>❓ Troubleshooting</h2>
        
        <h3>PDF won't load?</h3>
        <ul>
            <li>Ensure the file is a valid PDF</li>
            <li>Check that the file isn't password protected</li>
            <li>Try copying the file to a local drive if on network storage</li>
        </ul>
        
        <h3>Can't find output files?</h3>
        <p>Files are saved to your Downloads folder. Click "Open Folder" in the success dialog 
        to go directly to the location.</p>
        
        <h2>⌨️ Keyboard Shortcuts</h2>
        <ul>
            <li><b>Ctrl+O:</b> Open PDF</li>
            <li><b>F1:</b> Show this documentation</li>
            <li><b>Ctrl+Q:</b> Exit application</li>
        </ul>
        
        <hr>
        
        <h2 style="color: #dc3545;">⚖️ Legal Disclaimer</h2>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0;">
            <p><b>NO WARRANTY:</b></p>
            <p style="font-size: 12px;">
            THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
            INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
            PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
            FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY.
            </p>
        </div>
        
        <p><b>Important Notices:</b></p>
        <ul>
            <li><b>USE AT YOUR OWN RISK</b> - The authors assume no responsibility for data loss, corruption, or any other consequences</li>
            <li><b>NO LEGAL ADVICE</b> - This software is a tool only and does not constitute legal advice</li>
            <li><b>DATA RESPONSIBILITY</b> - You are solely responsible for the handling and protection of your data</li>
            <li><b>COMPLIANCE</b> - Users must ensure their use complies with all applicable laws and regulations</li>
            <li><b>NO GUARANTEE</b> - No guarantee of fitness for any particular purpose is provided</li>
        </ul>
        
        <p><b>License:</b> MIT License - Copyright © 2025 Legal Tech Solutions</p>
        
        <hr>
        <p><i>Simple PDF Splitter v1.0 - A tool for legal professionals</i></p>
        """