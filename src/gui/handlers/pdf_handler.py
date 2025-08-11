"""PDF file handling logic separated from main window."""

import fitz
from typing import Optional, Tuple


class PDFHandler:
    """Handles PDF file operations and state management."""
    
    def __init__(self):
        """Initialize PDF handler with empty state."""
        self.pdf_path: Optional[str] = None
        self.pdf_doc: Optional[fitz.Document] = None
        self.total_pages: int = 0
    
    def load_pdf(self, file_path: str) -> Tuple[bool, str]:
        """Load a PDF file and extract metadata.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Close existing document if any
            if self.pdf_doc:
                self.pdf_doc.close()
            
            # Load new document
            self.pdf_doc = fitz.open(file_path)
            self.pdf_path = file_path
            self.total_pages = len(self.pdf_doc)
            
            return True, f"Loaded: {file_path.split('/')[-1]} ({self.total_pages} pages)"
            
        except Exception as e:
            self.pdf_path = None
            self.pdf_doc = None
            self.total_pages = 0
            return False, f"Error loading PDF: {str(e)}"
    
    def clear(self):
        """Clear the current PDF state."""
        if self.pdf_doc:
            self.pdf_doc.close()
        self.pdf_path = None
        self.pdf_doc = None
        self.total_pages = 0
    
    def is_loaded(self) -> bool:
        """Check if a PDF is currently loaded."""
        return self.pdf_doc is not None
    
    def get_filename(self) -> str:
        """Get the filename of the loaded PDF."""
        if self.pdf_path:
            return self.pdf_path.split('/')[-1]
        return ""