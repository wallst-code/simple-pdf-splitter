from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox


class AboutDialog(QDialog):
    """About dialog with application information."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle("About Simple PDF Splitter")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        about_text = QTextBrowser()
        about_text.setOpenExternalLinks(True)
        about_text.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                line-height: 1.6;
                padding: 10px;
                background-color: white;
                border: none;
            }
        """)
        
        about_text.setHtml(self._get_about_content())
        layout.addWidget(about_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
    def _get_about_content(self):
        return """
        <center>
            <h2>Simple PDF Splitter</h2>
            <p><b>Version 1.0.0</b></p>
            <p><i>A Professional PDF Splitting Tool for Legal Teams</i></p>
        </center>
        
        <hr>
        
        <p><b>Features:</b></p>
        <ul>
            <li>Privacy-focused local processing</li>
            <li>Smart file naming with case management</li>
            <li>Batch processing capabilities</li>
            <li>Enterprise-grade code quality</li>
        </ul>
        
        <p><b>Privacy-Focused Design:</b><br>
        Processing happens locally on your computer, making it more private than 
        web-based alternatives. No requirement for internet transmission or cloud uploads. 
        Designed to minimize data exposure risks.</p>
        
        <hr>
        
        <h3 style="color: #dc3545;">⚖️ LICENSE & LEGAL DISCLAIMER</h3>
        
        <p><b>License:</b> MIT License<br>
        Copyright © 2025 Legal Tech Solutions</p>
        
        <p style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
        <b>NO WARRANTY:</b><br>
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
        INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
        PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
        FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
        OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
        DEALINGS IN THE SOFTWARE.
        </p>
        
        <p><b>Important Legal Notices:</b></p>
        <ul style="font-size: 12px;">
            <li><b>USE AT YOUR OWN RISK</b> - No responsibility for data loss or corruption</li>
            <li><b>NO LEGAL ADVICE</b> - This software is a tool only</li>
            <li><b>DATA RESPONSIBILITY</b> - You are responsible for your data</li>
            <li><b>COMPLIANCE</b> - Ensure your use complies with applicable laws</li>
        </ul>
        
        <hr>
        
        <p><b>Repository:</b> <a href="https://github.com/wallst-code/simple-pdf-splitter">GitHub</a></p>
        
        <center>
            <p style="color: #666;">© 2025 Legal Tech Solutions - MIT License</p>
        </center>
        """