MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QGroupBox {
    font-size: 14px;
    font-weight: bold;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton#removeButton {
    background-color: #dc3545;
    padding: 6px 12px;
}

QPushButton#removeButton:hover {
    background-color: #c82333;
}

QPushButton#addSplitButton {
    background-color: transparent;
    color: #333;
    text-align: left;
    padding: 8px;
    font-weight: normal;
}

QPushButton#addSplitButton:hover {
    background-color: #f0f0f0;
}

QPushButton#browseButton {
    background-color: #007bff;
}

QPushButton#browseButton:hover {
    background-color: #0056b3;
}

QPushButton#clearAllButton {
    background-color: #6c757d;
}

QPushButton#clearAllButton:hover {
    background-color: #545b62;
}

QLineEdit {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #4CAF50;
    outline: none;
}

QSpinBox {
    padding: 6px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 13px;
}

QSpinBox:focus {
    border-color: #4CAF50;
}

QLabel {
    color: #333;
    font-size: 13px;
}

QLabel#headerLabel {
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

QLabel#subheaderLabel {
    font-size: 14px;
    color: #666;
}

QLabel#dropZoneLabel {
    color: #999;
    font-size: 16px;
    padding: 40px;
}

QStatusBar {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
}

QListWidget {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
    background-color: white;
}

QFrame#dropZone {
    border: 2px dashed #ccc;
    border-radius: 8px;
    background-color: #fafafa;
    min-height: 150px;
}

QFrame#dropZone:hover {
    border-color: #4CAF50;
    background-color: #f0f8f0;
}

QMenuBar {
    background-color: white;
    border-bottom: 1px solid #ddd;
}

QMenuBar::item {
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #f0f0f0;
}

QMenu {
    background-color: white;
    border: 1px solid #ddd;
}

QMenu::item {
    padding: 5px 20px;
}

QMenu::item:selected {
    background-color: #f0f0f0;
}
"""