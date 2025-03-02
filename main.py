import sys

from PyQt6.QtWidgets import QApplication

from app import PasswordGenerator


def main() -> None:
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
