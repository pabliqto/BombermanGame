from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from settings import SettingsUI

import sys


class MenuUI:
    def __init__(self, app):
        self.app = app
        self.ui = uic.loadUi("menu.ui")
        self.ui.setWindowIcon(QtGui.QIcon("images/animations/yellow/yellow-idle-front.png"))
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.show()
        self.ui.quit_pushbutton.clicked.connect(self.closing)
        self.ui.play_pushbutton.clicked.connect(self.open_settings)
        self.run()

    def run(self):
        self.app.exec_()

    def closing(self):
        self.ui.close()
        self.app.quit()

    def open_settings(self):
        self.ui.close()
        SettingsUI(self.app)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = MenuUI(app)
