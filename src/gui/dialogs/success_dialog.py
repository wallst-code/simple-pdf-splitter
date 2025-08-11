from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QDialogButtonBox, QPushButton, QWidget
)
from PyQt6.QtCore import Qt
import os
import sys
import subprocess


class SuccessDialog(QDialog):
    """Professional success dialog for PDF split completion."""
    
    def __init__(self, parent, results, output_folder):
        super().__init__(parent)
        self.results = results
        self.output_folder = output_folder
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle("✓ PDF Split Complete")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self._add_header(layout)
        self._add_location_info(layout)
        self._add_files_list(layout)
        self._add_buttons(layout)
        
    def _add_header(self, layout):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        success_icon = QLabel("✓")
        success_icon.setStyleSheet("""
            QLabel {
                background-color: #4CAF50;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                border-radius: 25px;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
            }
        """)
        success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_text = QLabel(f"Successfully Created {len(self.results)} PDF Files")
        header_text.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2e7d32;
        """)
        
        header_layout.addWidget(success_icon)
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addWidget(header_widget)
        
    def _add_location_info(self, layout):
        location_widget = QWidget()
        location_widget.setStyleSheet("""
            QWidget {
                background-color: #e8f5e9;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        location_layout = QVBoxLayout(location_widget)
        
        location_label = QLabel("📁 Files saved to:")
        location_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        location_layout.addWidget(location_label)
        
        path_label = QLabel(self.output_folder)
        path_label.setStyleSheet("""
            font-family: monospace;
            font-size: 13px;
            color: #1976d2;
            padding: 5px;
        """)
        path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        location_layout.addWidget(path_label)
        
        layout.addWidget(location_widget)
        
    def _add_files_list(self, layout):
        files_label = QLabel("Created Files:")
        files_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(files_label)
        
        files_text = QTextEdit()
        files_text.setReadOnly(True)
        files_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-family: monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
        
        files_content = ""
        for i, result in enumerate(self.results, 1):
            files_content += f"{i}. {result['filename']}\n"
        files_text.setPlainText(files_content)
        files_text.setMaximumHeight(150)
        layout.addWidget(files_text)
        
    def _add_buttons(self, layout):
        button_box = QDialogButtonBox()
        
        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        open_folder_btn.clicked.connect(self._open_folder)
        
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        button_box.addButton(open_folder_btn, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.addButton(ok_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        
        layout.addWidget(button_box)
        
    def _open_folder(self):
        """Open the output folder in the system file explorer."""
        try:
            if os.name == 'nt':  # Windows
                # Use explorer.exe to open the folder
                subprocess.Popen(['explorer', self.output_folder])
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.call(['open', self.output_folder])
                else:  # Linux
                    subprocess.call(['xdg-open', self.output_folder])
        except Exception as e:
            print(f"Failed to open folder: {e}")