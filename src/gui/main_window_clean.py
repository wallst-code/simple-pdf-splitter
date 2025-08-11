from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox, QFrame,
    QMessageBox, QFileDialog, QScrollArea,
    QStatusBar, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent
from src.gui.styles import MAIN_STYLE
from src.gui.handlers.pdf_handler import PDFHandler
from src.gui.handlers.split_manager import SplitManager
from src.gui.handlers.ui_builder import UIBuilder
import os


class DragDropFrame(QFrame):
    file_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("dropZone")
        self.default_style = """
            QFrame {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        """
        self.hover_style = """
            QFrame {
                border: 2px dashed #4CAF50;
                border-radius: 5px;
                background-color: #f0f8f0;
            }
        """
        self.success_style = """
            QFrame {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background-color: #e8f5e9;
            }
        """
        self.setStyleSheet(self.default_style)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet(self.hover_style)
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)
            
    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            if file.lower().endswith('.pdf'):
                # Show success style briefly
                self.setStyleSheet(self.success_style)
                self.file_dropped.emit(file)
                # Reset style after a delay
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(1500, lambda: self.setStyleSheet(self.default_style))
                break
        else:
            # No PDF found, reset to default
            self.setStyleSheet(self.default_style)


class MainWindowStyled(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_handler = PDFHandler()
        self.split_manager = None  # Will be initialized after UI creation
        self.ui_builder = UIBuilder(self)
        
        self._init_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self.setStyleSheet(MAIN_STYLE)
        
    def _init_ui(self):
        self.setWindowTitle("Simple PDF Splitter v1.0")
        self.setMinimumSize(1200, 900)
        self.resize(1200, 950)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.ui_builder.create_header(main_layout)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        self.ui_builder.create_left_panel(content_layout)
        self.ui_builder.create_right_panel(content_layout)
        
        main_layout.addLayout(content_layout)
        
        self.ui_builder.create_split_section(main_layout)
        self.ui_builder.create_action_buttons(main_layout)
        
    def _setup_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open PDF", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._handle_file_select)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menubar.addMenu("Help")
        
        doc_action = QAction("Documentation", self)
        doc_action.setShortcut("F1")
        doc_action.triggered.connect(self._show_documentation)
        help_menu.addAction(doc_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About Simple PDF Splitter", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("[-1] Ready to split PDFs...")
        
    def _handle_file_select(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        
        if file_path:
            self._load_pdf(file_path)
            
    def _load_pdf(self, file_path):
        success, message = self.pdf_handler.load_pdf(file_path)
        
        if success:
            filename = os.path.basename(file_path)
            self.file_input.setText(file_path)
            # Green text with checkmark for loaded status
            self.status_label.setText(f"✓ Loaded: {filename} ({self.pdf_handler.total_pages} pages)")
            self.status_label.setStyleSheet("QLabel { color: #28a745; font-weight: bold; }")
            # Start with green "no gaps" status
            self.range_label.setText("Range Gaps: None")
            self.range_label.setStyleSheet("QLabel { color: #28a745; font-weight: bold; }")
            
            self._clear_splits()
            self._add_split_row()
            
            self.status_bar.showMessage(f"[0] PDF loaded: {filename}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to load PDF: {message}")
            
    def _add_split_row(self):
        if not self.pdf_handler.is_loaded():
            QMessageBox.warning(self, "Warning", "Please select a PDF first")
            return
        
        row = self.split_manager.add_split_row(self.pdf_handler.total_pages)
        if row:
            row.remove_clicked.connect(lambda: self._remove_split(row))
            row.values_changed.connect(self._update_range_gaps)
        self._update_range_gaps()
        
    def _remove_split(self, row):
        self.split_manager.remove_split(row)
        self._update_range_gaps()
            
    def _update_range_gaps(self):
        if not self.pdf_handler.is_loaded():
            return
        
        has_gaps, missing = self.split_manager.calculate_range_gaps(self.pdf_handler.total_pages)
        
        if has_gaps:
            # Red text for gaps with warning symbol
            self.range_label.setText(f"⚠ Range Gaps: {missing}")
            self.range_label.setStyleSheet("QLabel { color: #dc3545; font-weight: bold; }")
        else:
            # Green text for no gaps with checkmark
            self.range_label.setText("✓ Range Gaps: None")
            self.range_label.setStyleSheet("QLabel { color: #28a745; font-weight: bold; }")
            
    def _clear_splits(self):
        self.split_manager.clear_all_splits()
        
    def _clear_all(self):
        self._clear_splits()
        self.client_input.clear()
        self.client_input.setStyleSheet("QLineEdit { border: 2px solid #dc3545; }")  # Reset to red
        self.case_input.clear()
        self.case_input.setStyleSheet("QLineEdit { border: 2px solid #dc3545; }")  # Reset to red
        self.file_input.clear()
        self.status_label.setText("No PDF loaded")
        self.status_label.setStyleSheet("")  # Reset to default style
        self.range_label.setText("Range Gaps: N/A")
        self.range_label.setStyleSheet("")  # Reset to default style
        self.pdf_handler.clear()
        self.status_bar.showMessage("[-1] Ready to split PDFs...")
        
    def _handle_process(self):
        if not self.pdf_handler.is_loaded():
            QMessageBox.warning(self, "Warning", "Please select a PDF first")
            return
            
        if not self.split_manager.has_splits():
            QMessageBox.warning(self, "Warning", "Please add at least one split")
            return
            
        self.status_bar.showMessage("[1] Processing PDF...")
        self._process_pdf()
        
    def _process_pdf(self):
        from src.services.pdf_service import PDFService
        from src.gui.dialogs.success_dialog import SuccessDialog
        from pathlib import Path
        import uuid
        from datetime import datetime
        
        try:
            service = PDFService()
            results = []
            output_folder = str(Path.home() / "Downloads")
            
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            splits = self.split_manager.get_split_data()
            for i, split_data in enumerate(splits):
                unique_id = str(uuid.uuid4())[:8]
                
                client_name = self.client_input.text().strip()
                case_number = self.case_input.text().strip()
                doc_code = split_data['document_code']
                other = split_data['optional_other']
                
                if not client_name and not case_number and not doc_code and not other:
                    client_name = f"Split_{session_id}"
                    doc_code = f"Part{i+1:02d}"
                elif not doc_code:
                    doc_code = f"DOC{i+1:03d}"
                
                # Add unique ID to the optional_other field (at the end)
                if other:
                    other = f"{other}_{unique_id}"
                else:
                    other = unique_id
                
                output_path = service.split_pdf(
                    input_path=self.pdf_handler.pdf_path,
                    start_page=split_data['start_page'],
                    end_page=split_data['end_page'],
                    output_name=client_name or "Document",
                    document_code=doc_code,
                    case_number=case_number,
                    optional_other=other,
                    output_folder=output_folder
                )
                
                results.append({
                    'filename': os.path.basename(output_path),
                    'path': output_path
                })
            
            dialog = SuccessDialog(self, results, output_folder)
            dialog.exec()
            self.status_bar.showMessage(f"✓ Complete! Created {len(results)} files", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Processing failed: {str(e)}")
            self.status_bar.showMessage("[E] Processing failed")
    
    def _show_documentation(self):
        from src.gui.dialogs.documentation_dialog import DocumentationDialog
        dialog = DocumentationDialog(self)
        dialog.exec()
    
    def _show_about(self):
        from src.gui.dialogs.about_dialog import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec()