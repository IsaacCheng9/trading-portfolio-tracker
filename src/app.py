import sys
import os
from PySide6 import QtWidgets
from src.portfolio import MainWindow


def main() -> None:
    """
    Open the main menu on program startup.
    """
    # No scaling is required - increase font sizes instead if necessary.
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_menu = MainWindow()
    main_menu.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
