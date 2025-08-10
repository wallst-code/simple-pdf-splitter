"""Adapter to maintain backward compatibility with PDFService."""

from typing import Dict, Any, List, Optional
from services.pdf_processor import PDFProcessor


class PDFService:
    """Backward compatibility adapter for PDFService."""
    
    @staticmethod
    def split_pdf(
        input_path: str,
        start_page: int,
        end_page: int,
        output_name: str = "",
        document_code: str = "",
        case_number: str = "",
        optional_other: str = "",
        output_folder: Optional[str] = None
    ) -> Dict[str, Any]:
        """Legacy split_pdf interface."""
        from pathlib import Path
        
        if not output_folder:
            output_folder = str(Path(input_path).parent)
        
        config = {
            'input_path': input_path,
            'start_page': start_page,
            'end_page': end_page,
            'output_name': output_name,
            'document_code': document_code,
            'case_number': case_number,
            'optional_other': optional_other,
            'output_folder': output_folder,
            'client_name': ''  # Not in original interface
        }
        
        processor = PDFProcessor()
        return processor.split_single(config)
    
    @staticmethod
    def batch_split_pdf(
        input_path: str,
        splits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Legacy batch_split_pdf interface."""
        processor = PDFProcessor()
        return processor.batch_split(input_path, splits)