import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.gui.main_window_clean import MainWindowStyled as MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simple PDF Splitter")
    app.setOrganizationName("Legal Tools")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()