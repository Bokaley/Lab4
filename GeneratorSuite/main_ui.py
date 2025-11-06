import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main_ui():
    """
    Главная функция для запуска UI версии.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main_ui()
