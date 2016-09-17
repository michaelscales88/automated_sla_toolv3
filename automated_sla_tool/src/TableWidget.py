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
        self.sheet = self.open_sheet(file)
        self.clip = QApplication.clipboard()
        self.row_dict = {}
        self.column_dict = {}
        self.setColumnCount(self.sheet.number_of_columns() - 1)
        self.setRowCount(self.sheet.number_of_rows() - 1)
        self.data = self.sheet.to_array()
        self.setWindowTitle(window_title)
        self.set_headers()
        self.set_my_data()
        self.resizeColumnsToContents()
        self.show()

    def open_sheet(self, file):
        return pe.Sheet(file)

    def set_my_data(self):
        for row_index, row in enumerate(self.data):
            for column_index, item in enumerate(row):
                new_item = QTableWidgetItem(str(item))
                self.setItem(row_index, column_index, new_item)

    def set_headers(self):
        self.remove_redundant_date()
        try:
            self.setHorizontalHeaderLabels(self.data[0])
        except TypeError:
            pass
        for index, header in enumerate(self.data[0]):
            self.column_dict[header] = index
        self.data.remove(self.data[0])
        vertical_headers = []
        for index, row in enumerate(self.data):
            vertical_headers.append(row[0])
            self.row_dict[row[0]] = index
            row.remove(row[0])
        try:
            self.setVerticalHeaderLabels(vertical_headers)
        except TypeError:
            pass

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
                print(s)
                print('st: %s' % st)
                print("left header")
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

                # if e.modifiers() & QtCore.Qt.ShiftModifier:
                #     selected = self.selectionModel().selectedIndexes()
                #     if e.key() == QtCore.Qt.Key_Right:
                #         # TODO: this still does not work
                #         print("working")
                #         print(selected.selectedRows())