"""Adapter for backward compatibility with WebPresenter."""

from presenters.pdf_presenter import PDFPresenter


class WebPresenter(PDFPresenter):
    """Backward compatibility wrapper for WebPresenter."""
    
    def __init__(self):
        """Initialize without dependency injection for compatibility."""
        super().__init__(upload_service=None)