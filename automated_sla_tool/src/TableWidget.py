import pyexcel as pe
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QApplication,
                             QStyle, QStyleOptionHeader)
from PyQt5.QtCore import Qt, QSize
from datetime import datetime


class TableWidget(QTableWidget):
    def __init__(self,
                 parent=None,
                 window_title='Default Title',
                 file=None):
        super(TableWidget, self).__init__(parent)
        self.data = self.load_data(file)
        self.clip = QApplication.clipboard()
        self.row_dict = {}
        self.column_dict = {}
        self.setColumnCount(self.data.number_of_columns())
        self.setRowCount(self.data.number_of_rows())
        self.setWindowTitle(window_title)
        self.set_headers()
        self.set_my_data()
        self.resizeColumnsToContents()
        self.show()

    def load_data(self, file):
        if type(file) is pe.sheets.sheet.Sheet:
            return_file = file
        else:
            return_file = self.open_pe_file(file)
        return return_file

    def open_pe_file(self, file):
        try:
            return_file = pe.get_sheet(file_name=file)
        except OSError:
            return_file = pe.Sheet(file)
        return return_file

    def set_my_data(self):
        self.data = self.data.to_array()
        self.data.remove(self.data[0])
        for sublist in self.data:
            del sublist[0]
        for row_index, row in enumerate(self.data):
            for column_index, item in enumerate(row):
                new_item = QTableWidgetItem(str(item))
                self.setItem(row_index, column_index, new_item)

    def set_headers(self):
        self.setVerticalHeaderLabels(self.data.rownames)
        self.setHorizontalHeaderLabels(self.data.colnames)

    def remove_redundant_date(self):
        try:
            fmt = "%A %m/%d/%Y"
            date_to_remove = self.data[0][0]
            if not not datetime.strptime(date_to_remove, fmt):
                self.data[0].remove(date_to_remove)
        except (ValueError, TypeError):
            pass

    def sizeHint(self):
        """Reimplemented to define a better size hint for the width of the
        TableEditor."""
        x = self.style().pixelMetric(QStyle.PM_ScrollBarExtent,
                                     QStyleOptionHeader(), self)
        for column in range(self.columnCount() + 1):
            x += self.sizeHintForColumn(column) * 2.5
        y = x * .8
        size_hint = QSize(x, y)
        return size_hint

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            selected = self.selectedRanges()
            if e.key() == Qt.Key_C:  # copy
                # Set column headers
                s = '\t' + "\t".join([str(self.horizontalHeaderItem(i).text()) for i in
                                      range(selected[0].leftColumn(), selected[0].rightColumn() + 1)])
                st = []
                st.append(([str(self.horizontalHeaderItem(i).text()) for i in
                            range(selected[0].leftColumn(), selected[0].rightColumn() + 1)]))

                s = '{0}\n'.format(s)

                for r in range(selected[0].topRow(), selected[0].bottomRow() + 1):
                    # Set row headers
                    s += '{0}\t'.format(str(self.verticalHeaderItem(r).text()))
                    for c in range(selected[0].leftColumn(), selected[0].rightColumn() + 1):
                        try:
                            # Copy cell values
                            s += "{0}\t".format(str(self.item(r, c).text()))
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n"  # eliminate last '\t'
                self.clip.setText(s)

            if e.key() == Qt.Key_X:  # copy w/o labels
                s = ''
                for r in range(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in range(selected[0].leftColumn(), selected[0].rightColumn() + 1):
                        try:
                            # Copy cell values
                            s += "{0}\t".format(str(self.item(r, c).text()))
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n"  # eliminate last '\t'
                self.clip.setText(s)