"""Enterprise-compliant PDF presenter."""

from typing import Dict, Any, Optional, List
from pathlib import Path
from flask import session
from werkzeug.datastructures import FileStorage

from services.upload_service import UploadService
from services.pdf_processor import PDFProcessor
from models.split_request import PDFDocument


class PDFPresenter:
    """Coordinates PDF operations following MVP pattern."""
    
    def __init__(self, upload_service: Optional[UploadService] = None):
        """Initialize with optional service injection."""
        self._upload_service = upload_service
        self._processor = PDFProcessor()
    
    def handle_file_upload(self, file: FileStorage) -> Dict[str, Any]:
        """Process file upload."""
        service = self._get_upload_service()
        result = service.save_upload(file)
        
        if result["success"]:
            self._store_session_data(result)
        
        return result
    
    def get_current_document(self) -> Optional[PDFDocument]:
        """Get current document from session."""
        if not self._has_document_in_session():
            return None
        
        return PDFDocument(
            file_path=session["file_path"],
            filename=session["original_name"],
            page_count=session["page_count"],
            file_size_mb=session["file_size_mb"]
        )
    
    def process_split_requests(
        self, 
        splits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process multiple split requests."""
        document = self.get_current_document()
        if not document:
            return {"success": False, "error": "No document uploaded"}
        
        formatted_splits = self._format_splits(splits)
        results = self._processor.batch_split(
            document.file_path, 
            formatted_splits
        )
        
        processed = self._process_results(results, splits)
        session["processing_results"] = processed
        
        return {"success": True, "results": processed}
    
    def cleanup_session(self) -> bool:
        """Clean up session and files."""
        success = True
        
        if self._has_document_in_session():
            service = self._get_upload_service()
            file_path = session.get("file_path")
            if file_path:
                success = service.cleanup_file(file_path)
        
        self._clear_session_data()
        return success
    
    def get_download_path(self, filename: str) -> Optional[str]:
        """Get download path for file."""
        results = session.get('processing_results', [])
        
        for result in results:
            if result.get('filename') == filename:
                return self._build_download_path(filename)
        
        return None
    
    def extract_splits_from_form(
        self, 
        form_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract split data from form."""
        splits = []
        index = 0
        
        while f'start_page_{index}' in form_data:
            split = self._extract_single_split(form_data, index)
            if self._is_valid_split(split):
                splits.append(split)
            index += 1
        
        return splits
    
    # Session management helpers
    def get_client_name(self) -> str:
        """Get client name from session."""
        return session.get('client_name', '')
    
    def get_case_number(self) -> str:
        """Get case number from session."""
        return session.get('case_number', '')
    
    def get_current_splits(self) -> List[Dict[str, Any]]:
        """Get current splits from session."""
        return session.get('splits', [{}])
    
    def add_split_row(self) -> None:
        """Add new split row to session."""
        splits = self.get_current_splits()
        splits.append({})
        session['splits'] = splits
        session.modified = True
    
    def remove_split_row(self, index: int) -> None:
        """Remove split row from session."""
        splits = self.get_current_splits()
        if 0 <= index < len(splits):
            splits.pop(index)
            session['splits'] = splits
            session.modified = True
    
    # Private helper methods
    def _get_upload_service(self) -> UploadService:
        """Get upload service instance."""
        if not self._upload_service:
            from flask import current_app
            folder = current_app.config['UPLOAD_FOLDER']
            self._upload_service = UploadService(folder)
        return self._upload_service
    
    def _has_document_in_session(self) -> bool:
        """Check if document exists in session."""
        return all(key in session for key in ["file_path", "original_name"])
    
    def _store_session_data(self, result: Dict[str, Any]) -> None:
        """Store upload result in session."""
        session["file_path"] = result["file_path"]
        session["original_name"] = result["original_name"]
        session["page_count"] = result["page_count"]
        session["file_size_mb"] = result["file_size_mb"]
        session.modified = True
    
    def _clear_session_data(self) -> None:
        """Clear all session data."""
        keys = [
            "file_path", "original_name", "page_count", 
            "file_size_mb", "splits", "client_name", 
            "case_number", "processing_results"
        ]
        for key in keys:
            session.pop(key, None)
        session.modified = True
    
    def _format_splits(
        self, 
        splits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Format splits for processor."""
        formatted = []
        
        for split in splits:
            formatted.append({
                'start_page': int(split.get('start_page', 1)),
                'end_page': int(split.get('end_page', 1)),
                'client_name': split.get('client_name', ''),
                'case_number': split.get('case_number', ''),
                'document_code': split.get('document_code', ''),
                'output_name': split.get('output_name', ''),
                'optional_other': split.get('output_name', '')
            })
        
        return formatted
    
    def _process_results(
        self, 
        results: List[Dict[str, Any]], 
        splits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process split results."""
        processed = []
        
        for i, result in enumerate(results):
            if i < len(splits):
                processed.append({
                    "success": result.get("success", False),
                    "filename": result.get("filename", f"Split_{i+1}.pdf"),
                    "start_page": splits[i].get("start_page", 1),
                    "end_page": splits[i].get("end_page", 1),
                    "document_code": splits[i].get("document_code", ""),
                    "error": result.get("error", "")
                })
        
        return processed
    
    def _build_download_path(self, filename: str) -> str:
        """Build download file path."""
        document = self.get_current_document()
        if document:
            folder = Path(document.file_path).parent
            return str(folder / filename)
        return ""
    
    def _extract_single_split(
        self, 
        form_data: Dict[str, Any], 
        index: int
    ) -> Dict[str, Any]:
        """Extract single split from form data."""
        return {
            'start_page': form_data.get(f'start_page_{index}', ''),
            'end_page': form_data.get(f'end_page_{index}', ''),
            'client_name': form_data.get('client_name', ''),
            'case_number': form_data.get('case_number', ''),
            'document_code': form_data.get(f'document_code_{index}', ''),
            'output_name': form_data.get(f'output_name_{index}', '')
        }
    
    def _is_valid_split(self, split: Dict[str, Any]) -> bool:
        """Check if split data is valid."""
        try:
            start = int(split.get('start_page', 0))
            end = int(split.get('end_page', 0))
            return start > 0 and end > 0 and start <= end
        except (ValueError, TypeError):
            return False