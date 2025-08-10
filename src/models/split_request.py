from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SplitRequest:
    """Data model for a single PDF split request"""
    start_page: int
    end_page: int
    document_code: str
    output_name: Optional[str] = None
    
    def __post_init__(self):
        """Validate the split request after initialization"""
        if self.start_page < 1:
            raise ValueError("Start page must be >= 1")
        
        if self.end_page < self.start_page:
            raise ValueError("End page must be >= start page")
        
        if not self.document_code or not self.document_code.strip():
            raise ValueError("Document code is required")
        
        # Clean up strings
        self.document_code = self.document_code.strip()
        if self.output_name:
            self.output_name = self.output_name.strip()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for service layer"""
        return {
            'start_page': self.start_page,
            'end_page': self.end_page,
            'document_code': self.document_code,
            'output_name': self.output_name or f"pages_{self.start_page}-{self.end_page}"
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SplitRequest':
        """Create from dictionary"""
        return cls(
            start_page=data['start_page'],
            end_page=data['end_page'],
            document_code=data['document_code'],
            output_name=data.get('output_name')
        )
    
    def get_page_range_str(self) -> str:
        """Get human-readable page range"""
        if self.start_page == self.end_page:
            return f"Page {self.start_page}"
        return f"Pages {self.start_page}-{self.end_page}"


@dataclass
class PDFDocument:
    """Data model for PDF document information"""
    file_path: str
    filename: str
    page_count: int
    file_size_mb: float
    client_name: Optional[str] = None
    case_number: Optional[str] = None
    
    def __post_init__(self):
        """Clean up strings after initialization"""
        if self.client_name:
            self.client_name = self.client_name.strip()
        if self.case_number:
            self.case_number = self.case_number.strip()
    
    def get_unsplit_pages(self, split_requests: List[SplitRequest]) -> int:
        """Calculate number of pages not covered by split requests"""
        covered_pages = set()
        
        for request in split_requests:
            for page in range(request.start_page, request.end_page + 1):
                covered_pages.add(page)
        
        return self.page_count - len(covered_pages)
    
    def get_split_percentage(self, split_requests: List[SplitRequest]) -> float:
        """Calculate percentage of pages covered by splits"""
        if self.page_count == 0:
            return 0.0
        
        covered_pages = set()
        for request in split_requests:
            for page in range(request.start_page, request.end_page + 1):
                covered_pages.add(page)
        
        return round((len(covered_pages) / self.page_count) * 100, 1)
    
    def validate_split_request(self, request: SplitRequest) -> bool:
        """Validate that a split request is valid for this document"""
        return (request.start_page >= 1 and 
                request.end_page <= self.page_count and
                request.start_page <= request.end_page)


@dataclass 
class SplitResult:
    """Data model for split operation result"""
    success: bool
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    request_index: int = 0
    
    @property
    def output_filename(self) -> Optional[str]:
        """Get just the filename from output path"""
        if self.output_path:
            from pathlib import Path
            return Path(self.output_path).name
        return None