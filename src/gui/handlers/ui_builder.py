"""UI Builder for creating main window components."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox, QFrame,
    QScrollArea, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt
from pathlib import Path


class UIBuilder:
    """Handles creation of UI components for the main window."""
    
    def __init__(self, main_window):
        """Initialize with reference to main window.
        
        Args:
            main_window: The main window instance
        """
        self.main_window = main_window
    
    def create_header(self, parent_layout):
        """Create the application header with banner."""
        from PyQt6.QtSvgWidgets import QSvgWidget
        
        banner_path = Path("src/assets/SPS_Banner.svg")
        
        if banner_path.exists():
            svg_widget = QSvgWidget(str(banner_path))
            svg_widget.setFixedSize(1160, 80)
            parent_layout.addWidget(svg_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            title = QLabel("Simple PDF Splitter - A Tool for Lawyers")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            parent_layout.addWidget(title)
    
    def create_left_panel(self, parent_layout):
        """Create the left panel with client information."""
        left_group = QGroupBox("Client Information")
        left_layout = QVBoxLayout()
        
        client_label = QLabel("Client Name:")
        self.main_window.client_input = QLineEdit()
        self.main_window.client_input.setPlaceholderText("Enter client name")
        # Add validation styling on text change
        self.main_window.client_input.textChanged.connect(
            lambda text: self.main_window.client_input.setStyleSheet(
                "QLineEdit { border: 2px solid #28a745; }" if text.strip() 
                else "QLineEdit { border: 2px solid #dc3545; }"
            )
        )
        # Start with red border (empty)
        self.main_window.client_input.setStyleSheet("QLineEdit { border: 2px solid #dc3545; }")
        
        case_label = QLabel("Case Number:")
        self.main_window.case_input = QLineEdit()
        self.main_window.case_input.setPlaceholderText("Enter case number")
        # Add validation styling on text change
        self.main_window.case_input.textChanged.connect(
            lambda text: self.main_window.case_input.setStyleSheet(
                "QLineEdit { border: 2px solid #28a745; }" if text.strip() 
                else "QLineEdit { border: 2px solid #dc3545; }"
            )
        )
        # Start with red border (empty)
        self.main_window.case_input.setStyleSheet("QLineEdit { border: 2px solid #dc3545; }")
        
        left_layout.addWidget(client_label)
        left_layout.addWidget(self.main_window.client_input)
        left_layout.addWidget(case_label)
        left_layout.addWidget(self.main_window.case_input)
        left_layout.addStretch()
        
        left_group.setLayout(left_layout)
        left_group.setMaximumWidth(350)
        parent_layout.addWidget(left_group)
    
    def create_right_panel(self, parent_layout):
        """Create the right panel with file selection."""
        from src.gui.handlers.pdf_handler import PDFHandler
        
        right_group = QGroupBox("PDF Information")
        right_layout = QVBoxLayout()
        
        file_label = QLabel("Selected PDF File:")
        self.main_window.file_input = QLineEdit()
        self.main_window.file_input.setReadOnly(True)
        self.main_window.file_input.setPlaceholderText("No file selected")
        
        right_layout.addWidget(file_label)
        right_layout.addWidget(self.main_window.file_input)
        
        # Create drag-drop frame
        from src.gui.main_window_clean import DragDropFrame
        drop_frame = DragDropFrame()
        drop_frame.file_dropped.connect(self.main_window._load_pdf)
        drop_frame.setMinimumHeight(100)
        
        drop_label = QLabel("Or drag and drop PDF here")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout = QVBoxLayout(drop_frame)
        drop_layout.addWidget(drop_label)
        
        right_layout.addWidget(drop_frame)
        
        # Browse button below drag-drop area with blue styling
        browse_btn = QPushButton("Browse PDF")
        browse_btn.clicked.connect(self.main_window._handle_file_select)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        right_layout.addWidget(browse_btn)
        
        self.main_window.status_label = QLabel("No PDF loaded")
        self.main_window.range_label = QLabel("Range Gaps: N/A")
        
        right_layout.addWidget(self.main_window.status_label)
        right_layout.addWidget(self.main_window.range_label)
        right_layout.addStretch()
        
        right_group.setLayout(right_layout)
        parent_layout.addWidget(right_group)
    
    def create_split_section(self, parent_layout):
        """Create the split configuration section."""
        from src.gui.handlers.split_manager import SplitManager
        
        split_group = QGroupBox("Split Instructions with example:")
        split_layout = QVBoxLayout()
        
        self.main_window.splits_container = QWidget()
        self.main_window.splits_layout = QVBoxLayout(self.main_window.splits_container)
        self.main_window.splits_layout.setSpacing(5)
        
        scroll = QScrollArea()
        scroll.setWidget(self.main_window.splits_container)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(300)
        split_layout.addWidget(scroll)
        
        add_btn = QPushButton("+ Add Split")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        add_btn.clicked.connect(self.main_window._add_split_row)
        split_layout.addWidget(add_btn)
        
        split_group.setLayout(split_layout)
        parent_layout.addWidget(split_group)
        
        # Initialize split manager after UI is created
        self.main_window.split_manager = SplitManager(self.main_window.splits_layout)
    
    def create_action_buttons(self, parent_layout):
        """Create the action buttons at the bottom."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.main_window._clear_all)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        button_layout.addWidget(clear_btn)
        
        button_layout.addSpacing(20)
        
        run_btn = QPushButton("Run Split")
        run_btn.setObjectName("runButton")
        run_btn.clicked.connect(self.main_window._handle_process)
        button_layout.addWidget(run_btn)
        
        parent_layout.addLayout(button_layout)