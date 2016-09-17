from PyQt5.QtWidgets import (QWidget, QDockWidget, QPushButton,
                             QVBoxLayout, QAction, QSplitter)
from PyQt5.QtCore import Qt
from .HorizontalWidget import HorizontalWidget


class DockWidget(QDockWidget):
    def __init__(self, parent=None, window_name=None, widget1=None, widget2=None, button=None, hide_button_name=None):
        super(DockWidget, self).__init__(window_name, parent)
        self.setFeatures(QDockWidget.DockWidgetFloatable |
                         QDockWidget.DockWidgetMovable |
                         QDockWidget.DockWidgetClosable)
        dock_widgets = HorizontalWidget(widget1=widget1, widget2=widget2)
        v_layout = QVBoxLayout()
        v_layout.addWidget(dock_widgets, alignment=Qt.AlignCenter)
        if button:
            self.button = button
            v_layout.addWidget(self.button, alignment=Qt.AlignBottom)
        if hide_button_name:
            self.hide_button = QPushButton(str(hide_button_name))
            self.splitter = QSplitter(Qt.Horizontal)
            button_layout = QVBoxLayout()
            button_layout.addWidget(self.hide_button, alignment=Qt.AlignCenter)
            set_widget = QWidget()
            set_widget.setLayout(button_layout)
            self.splitter.addWidget(set_widget)
            set_widget = QWidget()
            set_widget.setLayout(v_layout)
            self.splitter.addWidget(set_widget)
            self.splitter.setSizes([1, 0])
            self.splitter.show()
            handle = self.splitter.handle(1)
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.switch_frame = QAction(handle)
            self.switch_frame.triggered.connect(self.handle_splitter)
            self.hide_button.clicked.connect(self.switch_frame.trigger)
            self.setWidget(self.splitter)
        else:
            set_widget = QWidget()
            set_widget.setLayout(v_layout)
            self.setWidget(set_widget)
        self.show()

    def handle_splitter(self):
        if self.splitter.sizes()[0] > 0:
            self.splitter.setSizes([0, 1])
        else:
            self.splitter.setSizes([1, 0])

    def closeEvent(self, event):
        event.ignore()
        if self.isFloating():
            self.setFloating(False)
        if self.splitter.sizes()[1] > 0:
            self.splitter.setSizes([1, 0])

