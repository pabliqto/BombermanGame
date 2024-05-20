import sys
from PyQt5 import QtWidgets
from menu import MenuUI
from settings import SettingsUI
from info import InfoUI
from game import main


class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.menu_ui = MenuUI(self)
        self.settings_ui = None
        self.info_ui = None

    def show_menu(self):
        if self.settings_ui is not None:
            self.settings_ui.close()
        if self.info_ui is not None:
            self.info_ui.close()
        self.menu_ui.show()

    def show_settings(self):
        self.menu_ui.close()
        if self.settings_ui is None:
            self.settings_ui = SettingsUI(self)
        self.settings_ui.show()

    def show_info(self):
        self.menu_ui.close()

        if self.info_ui is None:
            self.info_ui = InfoUI(self)
        self.info_ui.show()

    def run(self):
        self.show_menu()
        sys.exit(self.app.exec_())

    def close_all(self):
        self.menu_ui.close()
        if self.settings_ui is not None:
            self.settings_ui.close()
        if self.info_ui is not None:
            self.info_ui.close()

    def play_game(self):
        self.close_all()
        main()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
