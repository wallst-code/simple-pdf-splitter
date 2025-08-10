"""Process presenter - handles only PDF processing concerns (SRP)."""

from typing import Dict, Any, List
from pathlib import Path


class ProcessPresenter:
    """Handles PDF processing operations only."""
    
    def __init__(self, pdf_processor):
        """Initialize with injected service."""
        self._processor = pdf_processor
        from src.services.session_service import SessionService
        self._session = SessionService
    
    def process_splits(
        self, 
        splits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process PDF split requests."""
        document_data = self._session.get_document()
        if not document_data:
            return {
                'success': False, 
                'error': 'No document uploaded'
            }
        
        formatted = self._format_splits(splits)
        
        # Use PDFService for batch splitting
        from src.services.pdf_service import PDFService
        results = PDFService.batch_split_pdf(
            document_data['file_path'],
            formatted
        )
        
        processed = self._process_results(results, splits)
        self._session.store_results(processed)
        
        return {'success': True, 'results': processed}
    
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
                'optional_other': split.get('output_name', ''),
                'output_folder': ''  # Use default
            })
        
        return formatted
    
    def _process_results(
        self,
        results: List[Dict[str, Any]],
        splits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process and format results."""
        processed = []
        
        for i, result in enumerate(results):
            if i < len(splits):
                processed.append({
                    'success': result.get('success', False),
                    'filename': self._extract_filename(result, i),
                    'start_page': splits[i].get('start_page', 1),
                    'end_page': splits[i].get('end_page', 1),
                    'document_code': splits[i].get('document_code', ''),
                    'error': result.get('error', '')
                })
        
        return processed
    
    def _extract_filename(self, result: Dict[str, Any], index: int) -> str:
        """Extract filename from result."""
        default = f'Split_{index+1}.pdf'
        if result.get('success') and result.get('output_path'):
            return Path(result['output_path']).name
        return default