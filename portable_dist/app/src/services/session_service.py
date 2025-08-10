"""Centralized session management service - SRP compliant."""

from typing import Dict, Any, Optional, List
from flask import session


class SessionService:
    """Handles all session operations - single responsibility."""
    
    # Document keys
    DOCUMENT_KEYS = ['file_path', 'original_name', 'page_count', 'file_size_mb']
    
    # Form keys
    FORM_KEYS = ['client_name', 'case_number', 'splits']
    
    # Result keys
    RESULT_KEYS = ['processing_results']
    
    @classmethod
    def store_document(cls, document_data: Dict[str, Any]) -> None:
        """Store document data in session."""
        session['file_path'] = document_data['file_path']
        session['original_name'] = document_data['original_name']
        session['page_count'] = document_data['page_count']
        session['file_size_mb'] = document_data['file_size_mb']
        session.modified = True
    
    @classmethod
    def get_document(cls) -> Optional[Dict[str, Any]]:
        """Get document data from session."""
        if not cls.has_document():
            return None
        
        return {
            'file_path': session.get('file_path'),
            'original_name': session.get('original_name'),
            'page_count': session.get('page_count'),
            'file_size_mb': session.get('file_size_mb')
        }
    
    @classmethod
    def has_document(cls) -> bool:
        """Check if document exists in session."""
        return all(key in session for key in ['file_path', 'original_name'])
    
    @classmethod
    def clear_document(cls) -> None:
        """Clear document data from session."""
        for key in cls.DOCUMENT_KEYS:
            session.pop(key, None)
        session.modified = True
    
    @classmethod
    def store_form_data(cls, form_data: Dict[str, Any]) -> None:
        """Store form data in session."""
        session['client_name'] = form_data.get('client_name', '')
        session['case_number'] = form_data.get('case_number', '')
        session['splits'] = form_data.get('splits', [])
        session.modified = True
    
    @classmethod
    def get_form_data(cls) -> Dict[str, Any]:
        """Get form data from session."""
        return {
            'client_name': session.get('client_name', ''),
            'case_number': session.get('case_number', ''),
            'splits': session.get('splits', [{}])
        }
    
    @classmethod
    def store_results(cls, results: List[Dict[str, Any]]) -> None:
        """Store processing results in session."""
        session['processing_results'] = results
        session.modified = True
    
    @classmethod
    def get_results(cls) -> List[Dict[str, Any]]:
        """Get processing results from session."""
        return session.get('processing_results', [])
    
    @classmethod
    def clear_all(cls) -> None:
        """Clear entire session."""
        session.clear()
        session.modified = True
    
    @classmethod
    def clear_form_data(cls) -> None:
        """Clear only form data."""
        for key in cls.FORM_KEYS:
            session.pop(key, None)
        session.modified = True