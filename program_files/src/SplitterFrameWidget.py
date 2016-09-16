from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QHBoxLayout,
                             QVBoxLayout, QToolButton, QSplitter)
from PyQt5.QtCore import pyqtSignal, Qt


class SplitterFrameWidget(QWidget):
    status_message = pyqtSignal(str, name='status_message')

    def __init__(self, parent, widget1, widget2, orientation='horizontal', arrow_direction='right'):
        super(SplitterFrameWidget, self).__init__(parent)
        if orientation == 'horizontal':
            orientation = Qt.Horizontal
        else:
            orientation = Qt.Vertical
        if arrow_direction == 'right':
            arrow = Qt.RightArrow
        else:
            arrow = Qt.LeftArrow

        self.splitter = QSplitter(orientation)
        self.splitter.addWidget(self.center_widget(widget1))
        self.splitter.addWidget(widget2)
        self.splitter.setSizes([1, 0])

        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter, alignment=Qt.AlignBottom)
        handle = self.splitter.handle(1)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        button = QToolButton(handle)
        button.setText("Save")
        button.setCheckable(True)
        button.setArrowType(arrow)
        button.clicked.connect(self.handle_splitter_button)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        handle.setLayout(layout)
        self.center_frame()
        self.show()

    def handle_splitter_button(self):
        if not all(self.splitter.sizes()):
            self.splitter.setSizes([1, 1])
        else:
            self.splitter.setSizes([1, 0])

    def center_widget(self, widget):
        centered_widget = QWidget()
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(widget, alignment=Qt.AlignCenter)
        centered_widget.setLayout(temp_layout)
        return centered_widget

    def center_frame(self):
        screen_dimensions = self.geometry()
        center_dimensions = QDesktopWidget().availableGeometry().topLeft()
        screen_dimensions.moveCenter(center_dimensions)
        self.move(screen_dimensions.center())