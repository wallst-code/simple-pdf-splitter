"""
Secure file upload service for web application.
Handles PDF file uploads with validation and temporary storage.
"""

import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.config.settings import MAX_CONTENT_LENGTH_MB, VALIDATION
from src.services.pdf_service import PDFService
from src.services.file_validator import FileValidator
from src.services.logging_service import LoggingService


class UploadService:
    """Service for handling secure PDF file uploads."""
    
    def __init__(self, upload_folder: str) -> None:
        """
        Initialize upload service with secure folder.
        
        Args:
            upload_folder: Path to temporary upload directory
        """
        self._upload_folder = Path(upload_folder)
        self._upload_folder.mkdir(exist_ok=True)
    
    def validate_upload(self, file: FileStorage) -> Dict[str, Any]:
        """
        Validate uploaded file for security and format.
        
        Args:
            file: Uploaded file from Flask request
            
        Returns:
            dict: Validation result with success status and details
        """
        logger = LoggingService.get_logger()
        
        # Use enhanced file validator
        is_valid, error_msg = FileValidator.validate_pdf_file(file)
        
        if not is_valid:
            logger.warning(f"File validation failed: {error_msg}")
            LoggingService.log_security_event(
                "INVALID_UPLOAD", 
                f"Rejected file: {file.filename if file else 'None'} - {error_msg}"
            )
            return self._error_result(error_msg)
        
        logger.info(f"File validation passed for: {file.filename}")
        return {"success": True, "message": "File validation passed"}
    
    def save_upload(self, file: FileStorage) -> Dict[str, Any]:
        """
        Securely save uploaded file to temporary storage.
        
        Args:
            file: Validated file from Flask request
            
        Returns:
            dict: Save result with file path and metadata
        """
        validation = self.validate_upload(file)
        if not validation["success"]:
            return validation
        
        secure_name = self._generate_secure_filename(file.filename)
        file_path = self._upload_folder / secure_name
        
        try:
            file.save(str(file_path))
            pdf_info = self._get_pdf_metadata(str(file_path))
            
            return {
                "success": True,
                "file_path": str(file_path),
                "original_name": file.filename,
                "secure_name": secure_name,
                **pdf_info
            }
        except Exception as e:
            return self._error_result(f"Failed to save file: {str(e)}")
    
    def cleanup_file(self, file_path: str) -> bool:
        """
        Remove temporary uploaded file.
        
        Args:
            file_path: Path to file to remove
            
        Returns:
            bool: True if successfully removed
        """
        try:
            Path(file_path).unlink(missing_ok=True)
            return True
        except Exception:
            return False
    
    def _has_valid_file(self, file: FileStorage) -> bool:
        """Check if file object is valid."""
        return file and file.filename and file.filename != ''
    
    def _has_valid_extension(self, filename: Optional[str]) -> bool:
        """Check if filename has PDF extension."""
        if not filename:
            return False
        return filename.lower().endswith('.pdf')
    
    def _has_valid_size(self, file: FileStorage) -> bool:
        """Check if file size is within limits."""
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= (MAX_CONTENT_LENGTH_MB * 1024 * 1024)
    
    def _generate_secure_filename(self, original: Optional[str]) -> str:
        """Generate secure unique filename."""
        if not original:
            original = "upload.pdf"
        
        secure_name = secure_filename(original)
        unique_id = str(uuid.uuid4())[:8]
        name_parts = secure_name.rsplit('.', 1)
        
        if len(name_parts) == 2:
            return f"{name_parts[0]}_{unique_id}.{name_parts[1]}"
        return f"{secure_name}_{unique_id}.pdf"
    
    def _get_pdf_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get PDF file information using existing service."""
        try:
            return PDFService.get_pdf_info(file_path)
        except Exception as e:
            return {"error": f"Could not read PDF: {str(e)}"}
    
    def _error_result(self, message: str) -> Dict[str, Any]:
        """Create standardized error result."""
        return {"success": False, "error": message}