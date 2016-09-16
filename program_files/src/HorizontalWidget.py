from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt


class HorizontalWidget(QWidget):
    def __init__(self, parent=None, widget1=None, widget2=None):
        super(HorizontalWidget, self).__init__(parent)
        if widget1 and widget2:
            layout = QHBoxLayout()
            layout.addWidget(widget1, alignment=Qt.AlignCenter)
            layout.addWidget(widget2, alignment=Qt.AlignCenter)
            exp_layout = QVBoxLayout()
            exp_layout.addLayout(layout)
        else:
            layout = QHBoxLayout()
            if widget1:
                layout.addWidget(widget1, alignment=Qt.AlignCenter)
            if widget2:
                layout.addWidget(widget2, alignment=Qt.AlignCenter)
            exp_layout = QVBoxLayout()
            exp_layout.addLayout(layout)
        self.setLayout(exp_layout)

    def show_widgets(self, show_widget='Both'):
        if show_widget == 'Both':
            self.children()[1].show()
            self.children()[2].show()
        elif show_widget == 'left':
            self.children()[1].show()
        else:
            self.children()[2].show()
