"""Split configuration management helper."""

from typing import Dict, Any, List
from services.session_service import SessionService


class SplitManager:
    """Manages split configurations in session."""
    
    @staticmethod
    def get_current_splits() -> List[Dict[str, Any]]:
        """Get current split configurations from session."""
        form_data = SessionService.get_form_data()
        return form_data.get("splits", [{}])
    
    @staticmethod
    def add_split_row() -> None:
        """Add empty split row to session."""
        form_data = SessionService.get_form_data()
        splits = form_data.get("splits", [])
        splits.append({})
        form_data["splits"] = splits
        SessionService.store_form_data(form_data)
    
    @staticmethod
    def add_split_row_with_data(split_data: Dict[str, Any]) -> None:
        """Add split row with specific data."""
        form_data = SessionService.get_form_data()
        splits = form_data.get("splits", [])
        splits.append(split_data)
        form_data["splits"] = splits
        SessionService.store_form_data(form_data)
    
    @staticmethod
    def remove_split_row(index: int) -> None:
        """Remove split row at index."""
        form_data = SessionService.get_form_data()
        splits = form_data.get("splits", [])
        if 0 <= index < len(splits) and len(splits) > 1:
            splits.pop(index)
            form_data["splits"] = splits
            SessionService.store_form_data(form_data)
    
    @staticmethod
    def extract_splits_from_form(form_data) -> List[Dict[str, Any]]:
        """Extract split configurations from form data."""
        client_name = form_data.get("client_name", "").strip()
        case_number = form_data.get("case_number", "").strip()
        
        splits = []
        index = 0
        
        while f"start_page_{index}" in form_data:
            try:
                start_page = int(form_data[f"start_page_{index}"])
                end_page = int(form_data[f"end_page_{index}"])
                document_code = form_data.get(f"document_code_{index}", "").strip()
                output_name = form_data.get(f"output_name_{index}", "").strip()
                
                splits.append({
                    "start_page": start_page,
                    "end_page": end_page,
                    "document_code": document_code,
                    "output_name": output_name,
                    "client_name": client_name,
                    "case_number": case_number
                })
                
                index += 1
            except (ValueError, KeyError):
                index += 1
                continue
        
        # Store in session
        if splits:
            stored_data = {
                "splits": splits,
                "client_name": client_name,
                "case_number": case_number
            }
            SessionService.store_form_data(stored_data)
        
        return splits
    
    @staticmethod
    def get_client_name() -> str:
        """Get client name from session."""
        form_data = SessionService.get_form_data()
        return form_data.get("client_name", "")
    
    @staticmethod
    def get_case_number() -> str:
        """Get case number from session."""
        form_data = SessionService.get_form_data()
        return form_data.get("case_number", "")