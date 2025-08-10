"""Enterprise-compliant PDF processing service."""

from typing import Dict, Any, Optional, List
from pathlib import Path
import fitz  # PyMuPDF
from datetime import datetime


class PDFProcessor:
    """Handles PDF splitting operations with clean separation."""
    
    @staticmethod
    def split_single(
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Split a single PDF section.
        
        Args:
            config: Split configuration
            
        Returns:
            Result dictionary with success status
        """
        validator = PDFValidator()
        generator = OutputNameGenerator()
        
        # Validate input
        validation = validator.validate_split_config(config)
        if not validation['valid']:
            return {'success': False, 'error': validation['error']}
        
        # Generate output name
        output_name = generator.generate_name(config)
        output_path = Path(config['output_folder']) / output_name
        
        # Execute split
        try:
            _execute_split(
                config['input_path'],
                config['start_page'],
                config['end_page'],
                str(output_path)
            )
            return {
                'success': True,
                'output_path': str(output_path),
                'filename': output_name
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def batch_split(
        input_path: str,
        splits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple PDF splits.
        
        Args:
            input_path: Source PDF path
            splits: List of split configurations
            
        Returns:
            List of results for each split
        """
        results = []
        output_folder = str(Path(input_path).parent)
        
        for split in splits:
            config = {
                'input_path': input_path,
                'output_folder': output_folder,
                **split
            }
            result = PDFProcessor.split_single(config)
            results.append(result)
        
        return results


class PDFValidator:
    """Validates PDF operations."""
    
    def validate_split_config(
        self, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate split configuration."""
        if not Path(config['input_path']).exists():
            return {'valid': False, 'error': 'Input file not found'}
        
        start = config.get('start_page', 1)
        end = config.get('end_page', 1)
        
        if start < 1 or end < 1:
            return {'valid': False, 'error': 'Invalid page range'}
        
        if start > end:
            return {'valid': False, 'error': 'Start page after end page'}
        
        return {'valid': True}
    
    def validate_page_range(
        self,
        start: int,
        end: int,
        total_pages: int
    ) -> bool:
        """Validate page range against document."""
        return (1 <= start <= total_pages and 
                1 <= end <= total_pages and 
                start <= end)


class OutputNameGenerator:
    """Generates output filenames."""
    
    def generate_name(self, config: Dict[str, Any]) -> str:
        """Generate output filename."""
        if config.get('output_name'):
            return self._ensure_pdf_extension(config['output_name'])
        
        parts = self._build_name_parts(config)
        return self._join_parts(parts) + '.pdf'
    
    def _build_name_parts(self, config: Dict[str, Any]) -> List[str]:
        """Build filename parts."""
        parts = []
        
        if config.get('client_name'):
            parts.append(self._sanitize(config['client_name']))
        
        if config.get('case_number'):
            parts.append(self._sanitize(config['case_number']))
        
        if config.get('document_code'):
            parts.append(self._sanitize(config['document_code']))
        
        if not parts:
            parts.append(self._default_name(config))
        
        return parts
    
    def _default_name(self, config: Dict[str, Any]) -> str:
        """Generate default name."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pages = f"pages_{config.get('start_page', 1)}-{config.get('end_page', 1)}"
        return f"split_{timestamp}_{pages}"
    
    def _sanitize(self, text: str) -> str:
        """Sanitize filename component."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text.strip()
    
    def _join_parts(self, parts: List[str]) -> str:
        """Join filename parts."""
        return '_'.join(filter(None, parts))
    
    def _ensure_pdf_extension(self, name: str) -> str:
        """Ensure .pdf extension."""
        if not name.lower().endswith('.pdf'):
            return name + '.pdf'
        return name


def _execute_split(
    input_path: str,
    start_page: int,
    end_page: int,
    output_path: str
) -> None:
    """
    Execute the actual PDF split operation.
    
    Args:
        input_path: Source PDF
        start_page: First page (1-indexed)
        end_page: Last page (1-indexed)
        output_path: Destination path
    """
    with fitz.open(input_path) as pdf_input:
        pdf_output = fitz.open()
        
        # Convert to 0-indexed for PyMuPDF
        for page_num in range(start_page - 1, end_page):
            if page_num < len(pdf_input):
                pdf_output.insert_pdf(
                    pdf_input,
                    from_page=page_num,
                    to_page=page_num
                )
        
        pdf_output.save(output_path)
        pdf_output.close()