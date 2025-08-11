"""Split row management logic separated from main window."""

from typing import List, Set, Tuple, Optional
from PyQt6.QtWidgets import QVBoxLayout


class SplitManager:
    """Manages split row operations and calculations."""
    
    def __init__(self, splits_layout: QVBoxLayout):
        """Initialize split manager with the layout container.
        
        Args:
            splits_layout: The QVBoxLayout where split rows are added
        """
        self.splits_layout = splits_layout
        self.split_rows: List = []
    
    def add_split_row(self, total_pages: int) -> Optional[object]:
        """Add a new split row with smart page range calculation.
        
        Args:
            total_pages: Total pages in the PDF
            
        Returns:
            The created split row widget or None
        """
        from src.gui.widgets.split_row_styled import SplitRowStyled
        
        row_number = len(self.split_rows) + 1
        start = 1
        end = total_pages
        
        # Calculate smart ranges based on last row
        if self.split_rows:
            last_row = self.split_rows[-1]
            last_end = last_row.end_spin.value()
            if last_end < total_pages:
                start = last_end + 1
                end = total_pages
            else:
                start = total_pages
                end = total_pages
        
        row = SplitRowStyled(row_number, start, end, total_pages)
        self.splits_layout.addWidget(row)
        self.split_rows.append(row)
        
        return row
    
    def remove_split(self, row) -> None:
        """Remove a split row and renumber remaining rows.
        
        Args:
            row: The split row widget to remove
        """
        if row in self.split_rows:
            self.split_rows.remove(row)
            row.deleteLater()
            self._renumber_rows()
    
    def _renumber_rows(self) -> None:
        """Renumber all rows after removal."""
        for i, row in enumerate(self.split_rows):
            row.set_row_number(i + 1)
    
    def calculate_range_gaps(self, total_pages: int) -> Tuple[bool, List[int]]:
        """Calculate missing page ranges.
        
        Args:
            total_pages: Total pages in PDF
            
        Returns:
            Tuple of (has_gaps, list_of_missing_pages)
        """
        if not self.split_rows:
            return False, []
        
        covered = set()
        for row in self.split_rows:
            start = row.start_spin.value()
            end = row.end_spin.value()
            for page in range(start, end + 1):
                covered.add(page)
        
        all_pages = set(range(1, total_pages + 1))
        missing = sorted(all_pages - covered)
        
        return bool(missing), missing
    
    def clear_all_splits(self) -> None:
        """Remove all split rows."""
        for row in self.split_rows:
            row.deleteLater()
        self.split_rows.clear()
    
    def get_split_data(self) -> List[dict]:
        """Extract data from all split rows.
        
        Returns:
            List of dictionaries containing split data
        """
        splits = []
        for row in self.split_rows:
            splits.append({
                'start_page': row.start_spin.value(),
                'end_page': row.end_spin.value(),
                'document_code': row.code_input.text().strip(),
                'optional_other': row.other_input.text().strip()
            })
        return splits
    
    def has_splits(self) -> bool:
        """Check if there are any split rows."""
        return bool(self.split_rows)
    
    def count(self) -> int:
        """Get the number of split rows."""
        return len(self.split_rows)