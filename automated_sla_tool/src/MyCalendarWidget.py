from datetime import date
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QVBoxLayout,
                             QHBoxLayout, QLabel)
from PyQt5.QtCore import QDate, pyqtSignal


class MyCalendarWidget(QWidget):
    updated_date = pyqtSignal(date, name='updated_date')

    def __init__(self, name=None, parent=None):
        super().__init__(parent)
        self.name = name
        self.cal = QCalendarWidget(self)
        initial_date = QDate.currentDate().addDays(-1)
        self.cal.setSelectedDate(initial_date)
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.show_date)
        self.text_area = QLabel(self)
        date = self.cal.selectedDate()
        self.text_area.setText(date.toString())

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.cal)
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.addWidget(self.text_area)
        self.setLayout(vbox_layout)

    def show_date(self, date):
        self.updated_date.emit(date.toPyDate())
        self.text_area.setText(date.toString())
