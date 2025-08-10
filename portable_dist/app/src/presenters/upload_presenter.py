"""Upload presenter - handles only upload concerns (SRP)."""

from typing import Dict, Any
from werkzeug.datastructures import FileStorage
from services.upload_service import UploadService
from services.session_service import SessionService


class UploadPresenter:
    """Handles file upload operations only."""
    
    def __init__(self, upload_service: UploadService):
        """Initialize with injected service."""
        self._upload_service = upload_service
        self._session = SessionService
    
    def handle_upload(self, file: FileStorage) -> Dict[str, Any]:
        """Handle file upload process."""
        result = self._upload_service.save_upload(file)
        
        if result['success']:
            self._session.store_document(result)
        
        return result
    
    def cleanup_upload(self) -> bool:
        """Clean up uploaded file."""
        document = self._session.get_document()
        if not document:
            return True
        
        success = self._upload_service.cleanup_file(
            document['file_path']
        )
        
        if success:
            self._session.clear_document()
        
        return success