from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton,
                             QCheckBox, QComboBox, QLabel,
                             QFontDialog, QColorDialog, QStyleFactory,
                             QApplication)
from PyQt5.QtCore import pyqtSignal, Qt


class SettingsWidget(QWidget):
    selected_color = pyqtSignal(str, name='selected color')
    selected_font = pyqtSignal(QFont, name='selected color')
    selected_style = pyqtSignal(str, name='style choice')

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        grid_input = QGridLayout()
        fontChoice = QPushButton('Font', self)
        fontChoice.clicked.connect(self.font_choice)
        fontColor = QPushButton('Font bg Color', self)
        fontColor.clicked.connect(self.color_picker)
        checkBox = QCheckBox('Enlarge Window', self)
        checkBox.stateChanged.connect(self.enlarge_window)
        self.styleChoice = QLabel("Windows Vista", self)

        comboBox = QComboBox(self)
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks")
        comboBox.addItem("windowsvista")

        comboBox.activated[str].connect(self.style_choice)
        grid_input.addWidget(fontChoice, 0, 0)
        grid_input.addWidget(fontColor, 0, 1)
        grid_input.addWidget(checkBox, 1, 0)
        grid_input.addWidget(self.styleChoice, 1, 1)
        grid_input.addWidget(comboBox, 1, 2)
        self.setLayout(grid_input)

    def font_choice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.selected_font.emit(font)

    def color_picker(self):
        color = QColorDialog.getColor(initial=Qt.darkBlue)
        self.selected_color.emit("QMainWindow { background-color: %s}" % color.name())

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QApplication.setStyle(QStyleFactory.create(text))
        self.selected_style.emit(text)

    def enlarge_window(self, state):
        # TODO: This needs to modify the QMainWindows
        if state == Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)