"""User-facing messages and strings.

Centralizes all user-visible text for consistency and future internationalization.
"""

# Menu Items
MENU_FILE = "File"
MENU_ABOUT = "About"
MENU_SETTINGS = "Settings"
MENU_ABOUT_ACTION = "About PDF Splitter"

# Button Labels
BTN_BROWSE_PDF = "Browse PDF"
BTN_ADD_SPLIT = "+ Add Split"
BTN_RUN_SPLIT = "Run Split"
BTN_CLEAR_ALL = "Clear All"
BTN_SAVE = "Save"
BTN_CANCEL = "Cancel"
BTN_BROWSE = "Browse"

# Field Labels
LABEL_CLIENT_NAME = "Client Name:"
LABEL_CASE_NUMBER = "Case Number:"
LABEL_START_PAGE = "Start Page"
LABEL_END_PAGE = "End Page"
LABEL_DOC_CODE = "Doc Code"
LABEL_OPTIONAL_NAME = "Optional Name"
LABEL_OUTPUT_FOLDER = "Output Folder:"

# Placeholders
PLACEHOLDER_CLIENT_NAME = "Enter client name"
PLACEHOLDER_CASE_NUMBER = "Enter case number"
PLACEHOLDER_OPTIONAL_NAME = "Enter name (optional)"
PLACEHOLDER_PDF_SELECTION = "Select a PDF file..."

# Group Box Titles
GROUP_CLIENT_INFO = "Client Information"
GROUP_DOCUMENT_SELECTION = "Document Selection & Statistics"
GROUP_DOCUMENT_STATS = "Document Stats:"
GROUP_SPLIT_INSTRUCTIONS = "Split Instructions with example:"
GROUP_STATUS = "Status"

# Status Messages
STATUS_READY = "Ready to split PDFs..."
STATUS_NO_PDF = "No PDF loaded"
STATUS_RANGE_GAPS_NA = "Range Gaps: N/A"
STATUS_PROCESSING = "Processing {} split requests..."
STATUS_COMPLETED = "All split operations completed."
STATUS_CLEARED = "All splits cleared."

# Dialog Titles
DIALOG_SETTINGS_TITLE = "Settings"
DIALOG_ABOUT_TITLE = "About Simple PDF Splitter"
DIALOG_SELECT_PDF = "Select PDF File"
DIALOG_SELECT_OUTPUT_FOLDER = "Select Output Folder"
DIALOG_SPLITS_COMPLETE = "Splits Complete"

# Error Messages
ERROR_INVALID_PDF = "Invalid PDF"
ERROR_INVALID_PDF_MESSAGE = "Please select a valid PDF file."
ERROR_NO_PDF_TITLE = "No PDF"
ERROR_NO_PDF_MESSAGE = "Please select a PDF file first."
ERROR_NO_SPLITS_TITLE = "No Splits"
ERROR_NO_SPLITS_MESSAGE = "Please add at least one valid split request."
ERROR_STARTUP = "Startup Error"
ERROR_STARTUP_MESSAGE = "Failed to start PDF Splitter GUI:\\n\\n{}"
ERROR_PDF_LOAD_FAILED = "Failed to load PDF: {}"
ERROR_INVALID_SPLIT_REQUEST = "Invalid split request: {}"

# Success Messages
SUCCESS_SPLIT_RESULT = "✓ {}"
SUCCESS_SPLITS_COMPLETE_MESSAGE = "All PDF splits have been processed. Check the status log for details."

# About Dialog Content
ABOUT_CONTENT = f"""Simple PDF Splitter v1.0

Tools for Lawyers, Built by Lawyers.

Features:
• Split PDFs by page ranges
• Batch processing
• Drag & drop support
• Professional file naming

© 2025 PDF Tools"""

# Drag & Drop Messages
DRAG_DROP_TITLE = "Drag & Drop PDF Here"
DRAG_DROP_SUBTITLE = "Or use Browse PDF button"

# Statistics Display Templates
STATS_TEMPLATE = "Total PDF Pages: {} | Unsplit Remaining: {} | Split Coverage: {}%"
RANGE_GAPS_TEMPLATE = "Range Gaps: {}"
PDF_INFO_TEMPLATE = "{} ({} pages)"

# Log Message Templates
LOG_PDF_LOADED = "Loaded PDF: {} with {} pages"
LOG_ERROR_LOADING = "Error loading PDF: {}"