import pyexcel as pe
from PyQt5.QtWidgets import (QApplication,
                             QStyle, QStyleOptionHeader, QTableView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class TableWidget(QTableView):
    def __init__(self,
                 parent=None,
                 window_title=None,
                 file=None):
        super().__init__(parent)
        self.data = self.load_data(file)
        self.prepare_table()
        self.clip = QApplication.clipboard()
        self.row_dict = {}
        self.column_dict = {}
        self.resizeColumnsToContents()
        self.show()

    def load_data(self, file):
        from automated_sla_tool.src.FinalReport import FinalReport
        return file if type(file) in (pe.sheets.sheet.Sheet, FinalReport) else self.open_pe_file(file)

    def open_pe_file(self, file):
        try:
            return_file = pe.get_sheet(file_name=file)
        except OSError:
            return_file = pe.Sheet(file)
        return return_file

    def set_my_data(self, model):
        for c_index, column in enumerate(self.data.colnames):
            for r_index, row in enumerate(self.data.rownames):
                item = QStandardItem(str(self.data[row, column]))
                model.setItem(r_index, c_index, item)
        return model

    def prepare_table(self):
        model = QStandardItemModel()
        col_headers = self.data.rownames if len(self.data.rownames) is not 0 else self.make_row_names()
        row_names = self.data.colnames if len(self.data.colnames) is not 0 else self.make_col_names()
        model.setVerticalHeaderLabels(col_headers)
        model.setHorizontalHeaderLabels(row_names)
        model.setColumnCount(self.data.number_of_columns())
        model.setRowCount(self.data.number_of_rows())
        model = self.set_my_data(model)
        self.setModel(model)

    def make_row_names(self):
        self.data.name_rows_by_column(0)
        return [i for i in self.data.rownames if i]

    def make_col_names(self):
        self.data.name_columns_by_row(0)
        return [i for i in self.data.colnames if i]

    def sizeHint(self):
        """Reimplemented to define a better size hint for the width of the
        TableEditor."""
        x = self.style().pixelMetric(QStyle.PM_ScrollBarExtent,
                                     QStyleOptionHeader(), self)
        for column in range(self.data.number_of_columns() + 1):
            x += self.sizeHintForColumn(column) * 2.5
        y = x * .8
        size_hint = QSize(x, y)
        return size_hint

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            selected = self.selectionModel().selectedIndexes()
            if len(selected) > 0:
                if e.key() == Qt.Key_X:
                    previous = selected[0]
                    columns = []
                    rows = []
                    for index in selected:
                        if previous.column() != index.column():
                            columns.append(rows)
                            rows = []
                        rows.append(index.data())
                        previous = index
                    columns.append(rows)
                    # print(columns)
                    # print()
                    # print()
                    # # add rows and columns to clipboard
                    clipboard = ""
                    nrows = len(columns[0])
                    ncols = len(columns)
                    for r in range(nrows):
                        for c in range(ncols):
                            clipboard += columns[c][r]
                            if c != (ncols - 1):
                                clipboard += '\t'
                        clipboard += '\n'
                    # print(clipboard)
                    self.clip.setText(clipboard)
