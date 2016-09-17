from PyQt5.QtWidgets import (QWidget, QTextEdit, QHBoxLayout,
                             QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class TextWindowWidget(QWidget):
    status_message = pyqtSignal(str, name='text_status')

    def __init__(self, title="Test Window"):
        super().__init__()
        self.setWindowTitle(title)
        self.te = QTextEdit(self)
        h_box_layout = QHBoxLayout()
        h_box_layout.addWidget(self.te)
        v_box_layout = QVBoxLayout()
        v_box_layout.addLayout(h_box_layout)
        self.setLayout(v_box_layout)
        self.te.setMinimumSize(500, 300)
        self.show()

    def append(self, text_string):
        cursor = self.te.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text_string)
        self.te.ensureCursorVisible()