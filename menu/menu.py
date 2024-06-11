from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt


class MenuUI(object):
    def __init__(self, controller):
        self.controller = controller
        self.ui = uic.loadUi("Menu/menu.ui")
        self.ui.setWindowIcon(QtGui.QIcon("images/animations/yellow/yellow-idle-front.png"))
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.play_pushbutton.clicked.connect(self.controller.show_settings)
        self.ui.quit_pushbutton.clicked.connect(self.controller.app.quit)
        self.ui.info_pushbutton.clicked.connect(self.controller.show_info)

    def show(self):
        self.ui.show()

    def close(self):
        self.ui.close()
