"""Dependency injection container for enterprise architecture."""

from typing import Protocol, Optional
from pathlib import Path
from dataclasses import dataclass
from flask import Flask, current_app


class PDFServiceProtocol(Protocol):
    """Protocol for PDF processing service."""
    
    @staticmethod
    def split_pdf(
        input_path: str,
        start_page: int,
        end_page: int,
        output_name: str,
        document_code: str,
        case_number: str,
        optional_other: str,
        output_folder: Optional[str] = None
    ) -> dict: ...
    
    @staticmethod
    def batch_split_pdf(
        input_path: str,
        splits: list[dict]
    ) -> list[dict]: ...


class UploadServiceProtocol(Protocol):
    """Protocol for file upload service."""
    
    def save_upload(self, file) -> dict: ...
    def cleanup_file(self, file_path: str) -> bool: ...
    def get_upload_folder(self) -> str: ...


class PresenterProtocol(Protocol):
    """Protocol for presenters."""
    
    def handle_file_upload(self, file) -> dict: ...
    def get_current_document(self) -> Optional[object]: ...
    def process_split_requests(self, splits: list[dict]) -> dict: ...


@dataclass
class Dependencies:
    """Dependency container for injection."""
    
    pdf_service: PDFServiceProtocol
    upload_service: UploadServiceProtocol
    presenter_factory: type[PresenterProtocol]
    upload_folder: Path
    
    @classmethod
    def from_app(cls, app: Flask) -> 'Dependencies':
        """Create dependencies from Flask app config."""
        from services.pdf_processor import PDFProcessor
        from services.upload_service import UploadService
        from presenters.pdf_presenter import PDFPresenter
        
        upload_folder = Path(app.config['UPLOAD_FOLDER'])
        
        return cls(
            pdf_service=PDFProcessor,
            upload_service=UploadService(str(upload_folder)),
            presenter_factory=PDFPresenter,
            upload_folder=upload_folder
        )


_dependencies: Optional[Dependencies] = None


def init_dependencies(app: Flask) -> None:
    """Initialize dependency container."""
    global _dependencies
    _dependencies = Dependencies.from_app(app)


def get_dependencies() -> Dependencies:
    """Get dependency container."""
    if _dependencies is None:
        init_dependencies(current_app)
    return _dependencies