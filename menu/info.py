from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt


class InfoUI(object):
    def __init__(self, controller):
        self.controller = controller
        self.ui = uic.loadUi("menu/info.ui")
        self.ui.setWindowIcon(QtGui.QIcon("images/animations/yellow/yellow-idle-front.png"))
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.back_pushbutton.clicked.connect(self.controller.show_menu)

    def show(self):
        self.ui.show()

    def close(self):
        self.ui.close()
