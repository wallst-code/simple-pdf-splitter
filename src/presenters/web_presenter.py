"""
Web presenter for PDF splitter application.
Implements MVP pattern for web interface coordination.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from flask import session, current_app
from werkzeug.datastructures import FileStorage

from services.upload_service import UploadService
from services.pdf_service import PDFService
from models.split_request import SplitRequest, PDFDocument
from presenters.upload_presenter import UploadPresenter
from presenters.process_presenter import ProcessPresenter
from services.session_service import SessionService
from presenters.helpers import SplitManager


class WebPresenter:
    """Coordinator presenter - delegates to specialized presenters (SRP)."""
    
    def __init__(self) -> None:
        """Initialize with composed presenters for separation of concerns."""
        self._upload_presenter: Optional[UploadPresenter] = None
        self._process_presenter: Optional[ProcessPresenter] = None
        self._session_service = SessionService
    
    def handle_file_upload(self, file: FileStorage) -> Dict[str, Any]:
        """
        Delegate file upload to specialized presenter.
        
        Args:
            file: Uploaded file from web form
            
        Returns:
            dict: Upload result with success status and metadata
        """
        presenter = self._get_upload_presenter()
        return presenter.handle_upload(file)
    
    def get_current_document(self) -> Optional[PDFDocument]:
        """
        Get currently uploaded document from session.
        
        Returns:
            PDFDocument or None if no document uploaded
        """
        document_data = self._session_service.get_document()
        if not document_data:
            return None
        
        return PDFDocument(
            file_path=document_data["file_path"],
            filename=document_data["original_name"],
            page_count=document_data["page_count"],
            file_size_mb=document_data["file_size_mb"]
        )
    
    def process_split_requests(self, split_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Delegate split processing to specialized presenter.
        
        Args:
            split_data: List of split request dictionaries
            
        Returns:
            dict: Processing results with success status and file paths
        """
        # Parse and format the split data
        formatted_splits = self._parse_split_requests(split_data)
        
        # Delegate to process presenter
        presenter = self._get_process_presenter()
        return presenter.process_splits(formatted_splits)
    
    def _get_possible_download_dirs(self) -> List[Path]:
        """Get list of possible directories for downloads. Max 20 lines."""
        from pathlib import Path
        return [
            Path.home() / "Downloads",  # Default Windows/Mac Downloads
            Path.cwd(),  # Current working directory
            Path.cwd() / "temp_uploads",  # Our upload directory
        ]
    
    def _find_file_in_directory(self, directory: Path, filename: str) -> Optional[str]:
        """Search for file in a specific directory. Max 20 lines."""
        if not directory.exists():
            return None
            
        # Direct file check
        file_path = directory / filename
        if file_path.exists() and file_path.suffix.lower() == '.pdf':
            return str(file_path)
        
        # Check for Windows duplicate naming like "file (2).pdf"
        try:
            base_name = filename.rsplit('.', 1)[0]
            for existing_file in directory.glob("*.pdf"):
                existing_base = existing_file.stem
                if (existing_base == base_name or 
                    existing_base.startswith(f"{base_name} (") and 
                    existing_base.endswith(")")):
                    return str(existing_file)
        except (OSError, PermissionError):
            pass
        return None
    
    def get_download_path(self, filename: str) -> Optional[str]:
        """Get secure download path for processed PDF file. Max 20 lines."""
        if not filename or '..' in filename:
            return None
        
        from pathlib import Path
        possible_dirs = self._get_possible_download_dirs()
        
        for directory in possible_dirs:
            result = self._find_file_in_directory(directory, filename)
            if result:
                return result
        
        return None
    
    def cleanup_session(self) -> bool:
        """
        Clean up temporary files and session data.
        
        Returns:
            bool: True if cleanup successful
        """
        success = True
        
        # Delegate file cleanup to upload presenter
        if self._session_service.has_document():
            presenter = self._get_upload_presenter()
            success = presenter.cleanup_upload()
        
        # Clear all session data
        self._session_service.clear_all()
        
        return success
    
    def get_current_splits(self) -> List[Dict[str, Any]]:
        """Get current split configuration from session."""
        return SplitManager.get_current_splits()
    
    def add_split_row(self) -> None:
        """Add a new split row to session."""
        SplitManager.add_split_row()
    
    def add_split_row_with_data(self, split_data: Dict[str, Any]) -> None:
        """Add a new split row with specific data to session."""
        SplitManager.add_split_row_with_data(split_data)
    
    def remove_split_row(self, index: int) -> None:
        """Remove split row at given index."""
        SplitManager.remove_split_row(index)
    
    def get_client_name(self) -> str:
        """Get client name from session."""
        return SplitManager.get_client_name()
    
    def get_case_number(self) -> str:
        """Get case number from session."""
        return SplitManager.get_case_number()
    
    def extract_splits_from_form(self, form_data) -> List[Dict[str, Any]]:
        """Extract split data from form submission."""
        return SplitManager.extract_splits_from_form(form_data)
    
    def get_processing_results(self) -> Optional[Dict[str, Any]]:
        """
        Get processing results from session.
        
        Returns:
            Dictionary with results data or None
        """
        results = self._session_service.get_results()
        if not results:
            return None
        
        # Count successes
        success_count = sum(1 for r in results if r.get("success"))
        
        return {
            "results": results,
            "success_count": success_count,
            "total_count": len(results),
            "original_document": self.get_current_document()
        }
    
    def _get_upload_presenter(self) -> UploadPresenter:
        """Get or create upload presenter instance."""
        if not self._upload_presenter:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            upload_service = UploadService(upload_folder)
            self._upload_presenter = UploadPresenter(upload_service)
        return self._upload_presenter
    
    def _get_process_presenter(self) -> ProcessPresenter:
        """Get or create process presenter instance."""
        if not self._process_presenter:
            from services.pdf_processor import PDFProcessor
            processor = PDFProcessor()
            self._process_presenter = ProcessPresenter(processor)
        return self._process_presenter
    
    def _store_session_data(self, upload_result: Dict[str, Any]) -> None:
        """Store upload result in session for later use."""
        self._session_service.store_document(upload_result)
    
    def _has_session_document(self) -> bool:
        """Check if session contains uploaded document data."""
        return self._session_service.has_document()
    
    def _extract_split_fields(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract and clean split form fields. Max 20 lines."""
        return {
            'client_name': (data.get("client_name") or "").strip(),
            'case_number': (data.get("case_number") or "").strip(),
            'output_name': (data.get("output_name") or "").strip(),
            'doc_code': (data.get("document_code") or "").strip()
        }
    
    def _build_split_request(self, data: Dict[str, Any], index: int, 
                           session_timestamp: str) -> Dict[str, Any]:
        """Build a single split request dictionary. Max 20 lines."""
        fields = self._extract_split_fields(data)
        
        # Ensure unique document code
        doc_code = fields['doc_code'] or f"Split_{index}"
        
        # Ensure valid base name
        base_name = fields['client_name'] or f"PDF_{session_timestamp}"
        
        return {
            'start_page': int(data["start_page"]),
            'end_page': int(data["end_page"]),
            'document_code': doc_code,
            'client_name': base_name,
            'case_number': fields['case_number'],
            'output_name': fields['output_name'],
            'output_folder': ""
        }
    
    def _parse_split_requests(self, split_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse web form data into dictionaries for PDFService. Max 20 lines."""
        from datetime import datetime
        
        session_timestamp = datetime.now().strftime("%H%M%S")
        requests = []
        
        for i, data in enumerate(split_data, 1):
            request_dict = self._build_split_request(data, i, session_timestamp)
            requests.append(request_dict)
            
        return requests