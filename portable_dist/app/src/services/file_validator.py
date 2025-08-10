"""Enhanced file validation service for PDF files."""

import os
import io
from pathlib import Path
from typing import Optional, Tuple, BinaryIO
from werkzeug.datastructures import FileStorage

# Try to import magic, but make it optional
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


class FileValidator:
    """Robust file validation for security."""
    
    # PDF file signatures (magic bytes)
    PDF_SIGNATURES = [
        b'%PDF-1.',  # Standard PDF header
        b'%PDF-2.',  # PDF 2.0
        b'\x25\x50\x44\x46',  # %PDF in hex
    ]
    
    # Allowed MIME types
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/x-pdf',
        'application/acrobat',
        'application/vnd.pdf',
        'text/pdf',
        'text/x-pdf',
    }
    
    # Maximum file size (bytes)
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    
    @classmethod
    def validate_pdf_file(cls, file: FileStorage) -> Tuple[bool, str]:
        """Comprehensive PDF file validation.
        
        Args:
            file: File to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file exists
        if not file or not file.filename:
            return False, "No file provided"
        
        # Check file extension
        if not cls._check_extension(file.filename):
            return False, "File must have .pdf extension"
        
        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > cls.MAX_FILE_SIZE:
            return False, f"File too large. Maximum {cls.MAX_FILE_SIZE // (1024*1024)}MB allowed"
        
        if size < 10:  # Minimum viable PDF size
            return False, "File too small to be a valid PDF"
        
        # Check magic bytes (file signature)
        if not cls._check_pdf_signature(file):
            return False, "File is not a valid PDF (invalid signature)"
        
        # Check MIME type if python-magic is available
        if HAS_MAGIC:
            try:
                if not cls._check_mime_type(file):
                    return False, "File MIME type is not PDF"
            except Exception:
                # Skip MIME check if error occurs
                pass
        
        # Additional PDF structure validation
        if not cls._check_pdf_structure(file):
            return False, "File has invalid PDF structure"
        
        return True, "Valid PDF file"
    
    @classmethod
    def _check_extension(cls, filename: str) -> bool:
        """Check if file has PDF extension."""
        if not filename:
            return False
        return filename.lower().endswith('.pdf')
    
    @classmethod
    def _check_pdf_signature(cls, file: FileStorage) -> bool:
        """Check if file starts with PDF signature."""
        file.seek(0)
        header = file.read(8)
        file.seek(0)
        
        for signature in cls.PDF_SIGNATURES:
            if header.startswith(signature):
                return True
        return False
    
    @classmethod
    def _check_mime_type(cls, file: FileStorage) -> bool:
        """Check MIME type using python-magic."""
        try:
            file.seek(0)
            mime = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)
            return mime in cls.ALLOWED_MIME_TYPES
        except Exception:
            # If python-magic fails, return True to not block
            return True
    
    @classmethod
    def _check_pdf_structure(cls, file: FileStorage) -> bool:
        """Basic PDF structure validation."""
        try:
            file.seek(0)
            content = file.read(1024)  # Read first 1KB
            
            # Check for PDF header
            if not content.startswith(b'%PDF-'):
                return False
            
            # Check for basic PDF elements
            # Handle small files properly
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            
            # Read last portion of file (up to 1KB)
            read_size = min(1024, file_size)
            file.seek(-read_size, os.SEEK_END)
            tail = file.read()
            
            # PDF should end with %%EOF
            if b'%%EOF' not in tail:
                return False
            
            file.seek(0)
            return True
            
        except Exception:
            return False
        finally:
            file.seek(0)
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize filename for security.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename safe for filesystem
        """
        if not filename:
            return "document.pdf"
        
        # Remove path components
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', '..', '~', '$', '|', '>', '<', ':', '*', '?', '"', "'"]
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Ensure PDF extension
        if not filename.lower().endswith('.pdf'):
            filename = filename.rsplit('.', 1)[0] + '.pdf'
        
        # Limit length
        if len(filename) > 100:
            name = filename[:-4]  # Remove .pdf
            filename = name[:96] + '.pdf'
        
        return filename