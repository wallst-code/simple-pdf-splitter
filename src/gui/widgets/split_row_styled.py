from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QSpinBox, 
    QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon


class SplitRowStyled(QWidget):
    remove_clicked = pyqtSignal()
    values_changed = pyqtSignal()
    
    def __init__(self, row_number, start_page, end_page, max_pages):
        super().__init__()
        self.row_number = row_number
        self.max_pages = max_pages
        self._init_ui(start_page, end_page)
        
    def _init_ui(self, start, end):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        self.row_label = QLabel(str(self.row_number))
        self.row_label.setStyleSheet("""
            background-color: #f8f9fa;
            padding: 8px 12px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-weight: bold;
        """)
        layout.addWidget(self.row_label)
        
        layout.addWidget(QLabel("Start Page"))
        
        self.start_spin = QSpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(self.max_pages)
        self.start_spin.setValue(start)
        self.start_spin.valueChanged.connect(self._on_values_changed)
        self.start_spin.setMinimumWidth(80)
        layout.addWidget(self.start_spin)
        
        self.start_check = QLabel("✓")
        self.start_check.setStyleSheet("color: green; font-size: 16px;")
        layout.addWidget(self.start_check)
        
        layout.addWidget(QLabel("End Page"))
        
        self.end_spin = QSpinBox()
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(self.max_pages)
        self.end_spin.setValue(end)
        self.end_spin.valueChanged.connect(self._on_values_changed)
        self.end_spin.setMinimumWidth(80)
        layout.addWidget(self.end_spin)
        
        self.end_check = QLabel("✓")
        self.end_check.setStyleSheet("color: green; font-size: 16px;")
        layout.addWidget(self.end_check)
        
        layout.addWidget(QLabel("Doc Code"))
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("DOC001")
        self.code_input.setMaximumWidth(120)
        self.code_input.textChanged.connect(self._on_values_changed)
        # Add validation styling - green when filled, red when empty
        self.code_input.textChanged.connect(
            lambda text: self.code_input.setStyleSheet(
                "QLineEdit { border: 2px solid #28a745; }" if text.strip() 
                else "QLineEdit { border: 2px solid #dc3545; }"
            )
        )
        # Start with red border (empty)
        self.code_input.setStyleSheet("QLineEdit { border: 2px solid #dc3545; }")
        layout.addWidget(self.code_input)
        
        layout.addWidget(QLabel("Optional Name"))
        
        self.other_input = QLineEdit()
        self.other_input.setPlaceholderText("Enter name (optional)")
        self.other_input.textChanged.connect(self._on_values_changed)
        # Optional field - use softer colors (grey when empty, green when filled)
        self.other_input.textChanged.connect(
            lambda text: self.other_input.setStyleSheet(
                "QLineEdit { border: 2px solid #28a745; }" if text.strip() 
                else "QLineEdit { border: 1px solid #ccc; }"
            )
        )
        layout.addWidget(self.other_input, 1)
        
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setObjectName("removeButton")
        self.remove_btn.clicked.connect(self.remove_clicked.emit)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        layout.addWidget(self.remove_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            SplitRowStyled {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        
    def _on_values_changed(self):
        if self.end_spin.value() < self.start_spin.value():
            self.end_spin.setValue(self.start_spin.value())
        
        self._update_validation()
        self.values_changed.emit()
        
    def _update_validation(self):
        start_valid = 1 <= self.start_spin.value() <= self.max_pages
        end_valid = self.start_spin.value() <= self.end_spin.value() <= self.max_pages
        
        self.start_check.setText("✓" if start_valid else "✗")
        self.start_check.setStyleSheet(
            "color: green; font-size: 16px;" if start_valid else "color: red; font-size: 16px;"
        )
        
        self.end_check.setText("✓" if end_valid else "✗")
        self.end_check.setStyleSheet(
            "color: green; font-size: 16px;" if end_valid else "color: red; font-size: 16px;"
        )
        
    def get_values(self):
        return {
            'start_page': self.start_spin.value(),
            'end_page': self.end_spin.value(),
            'doc_code': self.code_input.text(),
            'other': self.other_input.text()
        }
        
    def set_row_number(self, number):
        self.row_number = number
        self.row_label.setText(str(number))
        
    def validate(self):
        return self.start_spin.value() <= self.end_spin.value()