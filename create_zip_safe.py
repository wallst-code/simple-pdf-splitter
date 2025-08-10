"""
Create a safe ZIP file for distribution without any private data.
"""

import zipfile
import os
from pathlib import Path

def create_safe_zip():
    """Create ZIP archive of portable distribution."""
    
    print("\nCreating Safe Distribution ZIP...")
    print("=" * 50)
    
    source_dir = Path("portable_dist")
    zip_path = Path("SimplePDFSplitter-Portable-v1.0.0.zip")
    
    # Files/folders to exclude (for safety)
    exclude_patterns = [
        '.env',           # Secret keys (but keep .env.example)
        '.git',           # Git data
        '.hypothesis',    # Test data
        '.claude',        # Claude settings
        '*.log',          # Log files
        '__pycache__',    # Python cache
        '*.pyc',          # Compiled Python
        '.DS_Store',      # Mac files
        'Thumbs.db',      # Windows files
    ]
    
    def should_exclude(path):
        """Check if file should be excluded."""
        path_str = str(path)
        # Don't exclude .env.example
        if path_str.endswith('.env.example'):
            return False
        for pattern in exclude_patterns:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False
    
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if should_exclude(file_path):
                    print(f"  Skipping: {file}")
                    continue
                
                # Add file to ZIP with relative path
                arcname = str(file_path.relative_to(source_dir.parent))
                zipf.write(file_path, arcname)
                
    # Report success
    if zip_path.exists():
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"\n[SUCCESS] ZIP created successfully!")
        print(f"  File: {zip_path.name}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"\nSafe for distribution - no private data included!")
        return True
    else:
        print("\n[FAILED] Failed to create ZIP file")
        return False

if __name__ == "__main__":
    success = create_safe_zip()
    if success:
        print("\nYou can now upload this ZIP to GitHub Releases!")
    input("\nPress Enter to exit...")