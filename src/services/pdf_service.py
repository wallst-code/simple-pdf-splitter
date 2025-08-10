import fitz  # PyMuPDF
import os
from pathlib import Path
from typing import List, Dict, Any


class PDFService:
    """Service class for PDF operations - separates logic from UI"""
    
    @staticmethod
    def _check_pdf_readable(path_obj: Path) -> bool:
        """Check if PDF file can be opened and has pages. Max 20 lines."""
        try:
            doc = fitz.open(str(path_obj))
            page_count = len(doc)
            doc.close()
            return page_count > 0
        except Exception:
            return False
    
    @staticmethod
    def validate_pdf_path(file_path: str) -> bool:
        """Validate that the provided path is a valid PDF file. Max 20 lines."""
        # Strip quotes if present
        file_path = file_path.strip().strip('"').strip("'")
        
        # Convert to Path object for better handling
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            return False
        
        if not path_obj.suffix.lower() == '.pdf':
            return False
        
        return PDFService._check_pdf_readable(path_obj)
    
    @staticmethod
    def _get_pdf_page_count(path_obj: Path) -> int:
        """Get page count from PDF file. Max 20 lines."""
        try:
            doc = fitz.open(str(path_obj))
            page_count = len(doc)
            doc.close()
            return page_count
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
    
    @staticmethod
    def get_pdf_info(file_path: str) -> Dict[str, Any]:
        """Get information about a PDF file. Max 20 lines."""
        file_path = file_path.strip().strip('"').strip("'")
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        page_count = PDFService._get_pdf_page_count(path_obj)
        file_size = path_obj.stat().st_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        return {
            'page_count': page_count,
            'file_size_bytes': file_size,
            'file_size_mb': file_size_mb,
            'filename': path_obj.name,
            'file_path': str(path_obj)
        }
    
    @staticmethod
    def _validate_page_range(doc: fitz.Document, start_page: int, end_page: int) -> None:
        """Validate page range for PDF. Max 20 lines."""
        total_pages = len(doc)
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            doc.close()
            raise ValueError(f"Invalid page range. PDF has {total_pages} pages.")
    
    @staticmethod
    def _build_output_filename(output_name: str, document_code: str, 
                             case_number: str, optional_other: str) -> str:
        """Build output filename from components. Max 20 lines."""
        filename_parts = [output_name]
        if case_number:
            filename_parts.append(case_number)
        filename_parts.append(document_code)
        if optional_other:
            filename_parts.append(optional_other)
        return "_".join(filename_parts) + ".pdf"
    
    @staticmethod
    def _get_unique_output_path(output_dir: Path, filename: str) -> Path:
        """Get unique output path, adding counter if needed. Max 20 lines."""
        output_path = output_dir / filename
        
        if not output_path.exists():
            return output_path
            
        # Handle duplicates
        counter = 1
        original_path = output_path
        while output_path.exists():
            name_without_ext = original_path.stem
            extension = original_path.suffix
            output_path = output_dir / f"{name_without_ext} ({counter}){extension}"
            counter += 1
        return output_path
    
    @staticmethod
    def _extract_page_range(doc: fitz.Document, start_page: int, end_page: int) -> fitz.Document:
        """Extract page range from PDF document. Max 20 lines."""
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page-1, to_page=end_page-1)
        return new_doc
    
    @staticmethod
    def _prepare_output_directory(output_folder: str) -> Path:
        """Prepare output directory for PDF. Max 20 lines."""
        if output_folder:
            return Path(output_folder)
        return Path.home() / "Downloads"
    
    @staticmethod
    def _save_pdf_document(new_doc: fitz.Document, output_path: Path) -> str:
        """Save PDF document to file. Max 20 lines."""
        new_doc.save(output_path)
        return str(output_path)
    
    @staticmethod
    def split_pdf(input_path: str, start_page: int, end_page: int, 
                  output_name: str, document_code: str, case_number: str = "", optional_other: str = "", output_folder: str = "") -> str:
        """
        Split a PDF file by extracting specified page range.
        
        Args:
            input_path (str): Path to the input PDF file
            start_page (int): Starting page number (1-indexed)
            end_page (int): Ending page number (1-indexed)
            output_name (str): Name for the output file
            document_code (str): Document code to append to filename
        
        Returns:
            str: Path to the created output file
        """
        # Clean up the input path
        input_path = input_path.strip().strip('"').strip("'")
        
        # Open the PDF
        doc = fitz.open(input_path)
        
        # Validate page range
        PDFService._validate_page_range(doc, start_page, end_page)
        
        # Create new PDF with selected pages
        new_doc = PDFService._extract_page_range(doc, start_page, end_page)
        
        # Prepare output path
        output_dir = PDFService._prepare_output_directory(output_folder)
        filename = PDFService._build_output_filename(
            output_name, document_code, case_number, optional_other
        )
        output_path = PDFService._get_unique_output_path(output_dir, filename)
        
        # Save the new PDF
        result = PDFService._save_pdf_document(new_doc, output_path)
        
        # Close documents
        doc.close()
        new_doc.close()
        
        return result
    
    @staticmethod
    def _process_single_split(input_path: str, request: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Process a single split request. Max 20 lines."""
        try:
            output_path = PDFService.split_pdf(
                input_path=input_path,
                start_page=request['start_page'],
                end_page=request['end_page'],
                output_name=request.get('client_name', ''),
                document_code=request['document_code'],
                case_number=request.get('case_number', ''),
                optional_other=request.get('output_name', ''),
                output_folder=request.get('output_folder', '')
            )
            
            return {
                'success': True,
                'output_path': output_path,
                'request_index': index,
                'message': f"Successfully created {Path(output_path).name}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'request_index': index,
                'message': f"Failed to create split {index+1}: {e}"
            }
    
    @staticmethod
    def batch_split_pdf(input_path: str, split_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple split requests for the same PDF.
        
        Args:
            input_path (str): Path to the input PDF file
            split_requests (list): List of split request dictionaries
        
        Returns:
            list: Results of each split operation
        """
        results = []
        
        for i, request in enumerate(split_requests):
            result = PDFService._process_single_split(input_path, request, i)
            results.append(result)
        
        return results