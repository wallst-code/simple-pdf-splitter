"""Path management utilities.

Standardizes path handling across the application using pathlib.
"""

import os
from pathlib import Path
from typing import Optional

class AppPaths:
    """Centralized path management for the application."""
    
    def __init__(self):
        """Initialize path manager with application root detection."""
        # Detect if running from PyInstaller bundle
        if hasattr(os.sys, '_MEIPASS'):
            # Running from PyInstaller bundle
            self._app_root = Path(os.sys._MEIPASS)
            self._is_bundled = True
        else:
            # Running from source
            # Navigate from src/config/paths.py to project root
            self._app_root = Path(__file__).parent.parent.parent
            self._is_bundled = False
    
    @property
    def app_root(self) -> Path:
        """Get the application root directory."""
        return self._app_root
    
    @property
    def src_root(self) -> Path:
        """Get the src directory."""
        if self._is_bundled:
            return self._app_root / "src"
        return self._app_root / "src"
    
    @property
    def assets_dir(self) -> Path:
        """Get the assets directory."""
        return self.src_root / "assets"
    
    @property
    def banner_path(self) -> Path:
        """Get the banner SVG file path."""
        return self.assets_dir / "banner.svg"
    
    @property
    def user_home(self) -> Path:
        """Get the user's home directory."""
        return Path.home()
    
    @property
    def default_output_dir(self) -> Path:
        """Get the default output directory."""
        return self.user_home / "Downloads"
    
    @property
    def settings_file(self) -> Path:
        """Get the user settings file path."""
        return self.user_home / ".pdf_splitter_settings.json"
    
    def ensure_directory_exists(self, path: Path) -> Path:
        """Ensure a directory exists, creating it if necessary.
        
        Args:
            path: The directory path to ensure exists
            
        Returns:
            The path object (for chaining)
            
        Raises:
            OSError: If directory creation fails
        """
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def get_relative_to_src(self, path: str) -> Path:
        """Get a path relative to the src directory.
        
        Args:
            path: Relative path string from src directory
            
        Returns:
            Absolute path object
        """
        return self.src_root / path
    
    def is_valid_pdf_path(self, path: Optional[str]) -> bool:
        """Check if a path is a valid PDF file.
        
        Args:
            path: Path to check
            
        Returns:
            True if path exists and has .pdf extension
        """
        if not path:
            return False
        
        try:
            pdf_path = Path(path)
            return (
                pdf_path.exists() and 
                pdf_path.is_file() and 
                pdf_path.suffix.lower() == '.pdf'
            )
        except (OSError, ValueError):
            return False

# Global instance for easy access
app_paths = AppPaths()