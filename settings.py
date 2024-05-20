from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
import sys


class SettingsUI:
    def __init__(self, app):
        self.players = ["yellow", "blue", "red", "green"]
        self.values = [0, 1, 2, 3]
        self.app = app
        self.ui = uic.loadUi("settings.ui")
        self.ui.setWindowIcon(QtGui.QIcon("images/animations/yellow/yellow-idle-front.png"))
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.show()
        self.ui.players_slider.valueChanged.connect(self.slider_changed)
        self.ui.extra_bomb_checkbox.stateChanged.connect(lambda: self.toggle_spinbox(self.ui.extra_bomb_spinbox))
        self.ui.random_map_rbutton.toggled.connect(lambda: self.toggle_spinbox(self.ui.map_type_spinbox))
        self.ui.player1_left_button.clicked.connect(lambda: self.change_color(self.ui.player1_label, 0, -1))
        self.ui.player1_right_button.clicked.connect(lambda: self.change_color(self.ui.player1_label, 0, 1))
        self.ui.player2_left_button.clicked.connect(lambda: self.change_color(self.ui.player2_label, 1, -1))
        self.ui.player2_right_button.clicked.connect(lambda: self.change_color(self.ui.player2_label, 1, 1))
        self.ui.player3_left_button.clicked.connect(lambda: self.change_color(self.ui.player3_label, 2, -1))
        self.ui.player3_right_button.clicked.connect(lambda: self.change_color(self.ui.player3_label, 2, 1))
        self.ui.player4_left_button.clicked.connect(lambda: self.change_color(self.ui.player4_label, 3, -1))
        self.ui.player4_right_button.clicked.connect(lambda: self.change_color(self.ui.player4_label, 3, 1))
        self.run()

    def run(self):
        self.app.exec_()

    def slider_changed(self, value):
        players_frames = [self.ui.player1_frame, self.ui.player2_frame, self.ui.player3_frame, self.ui.player4_frame]
        line_edits = [self.ui.player1_line_edit, self.ui.player2_line_edit, self.ui.player3_line_edit, self.ui.player4_line_edit]
        keys = [self.ui.wasd_label, self.ui.arrows_label, self.ui.ijkl_label, self.ui.nums_label]
        for i in range(4):
            if i < value:
                players_frames[i].setEnabled(True)
                line_edits[i].setEnabled(True)
                keys[i].setEnabled(True)
            else:
                players_frames[i].setEnabled(False)
                line_edits[i].setEnabled(False)
                keys[i].setEnabled(False)

    @staticmethod
    def toggle_spinbox(spinbox):
        if spinbox.isEnabled():
            spinbox.setEnabled(False)
        else:
            spinbox.setEnabled(True)

    def change_color(self, label, index, value):
        self.values[index] = (self.values[index] + value) % len(self.players)
        png_name = "images/gui/" + self.players[self.values[index]] + "_player.png"
        label.setPixmap(QtGui.QPixmap(png_name))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = SettingsUI(app)
