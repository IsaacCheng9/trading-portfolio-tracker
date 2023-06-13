import sys
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow

from src.ui.main_window import Ui_main_window


def main() -> None:
    """
    Open the main menu on program startup.
    """
    # Perform scaling to prevent tiny UI on high resolution screens.
    os.environ["QT_SCALE_FACTOR"] = "1.25"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_menu = MainWindow()
    main_menu.show()
    sys.exit(app.exec())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        table_header = self.ui.portfolio_table_widget.horizontalHeader()
        table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )


if __name__ == "__main__":
    main()
