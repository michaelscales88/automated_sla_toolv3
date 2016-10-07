from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget)
# from .GraphData import PlotData
from .TableWidget import TableWidget


class ExcelTabContainer(QWidget):
    emit_dict = pyqtSignal(list)
    graph_xaxis = pyqtSignal(list)

    def __init__(self, title='Text Window', parent=None):
        super(ExcelTabContainer, self).__init__(parent)
        self.setWindowTitle(title)
        self.tabs = QTabWidget(self)
        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(self.tabs, alignment=Qt.AlignCenter)
        h_box = QHBoxLayout()
        h_box.addLayout(v_box_layout)
        self.setLayout(h_box)
        self.tabs.currentChanged.connect(self.tab_change_event)
        self.hide()

    def tab_change_event(self):
        index = self.tabs.currentIndex()
        handle = self.tabs.widget(index).children()
        try:
            use_handle = handle[1]
            use_handle.selected_data.connect(self.get_page_data)
        except Exception as e:
            print("passed due to {}".format(e))

    def get_page_data(self, stuff):
        try:
            indexices = self.tabs.count()
            for thing in stuff:
                client = thing.get_name()
                for list_position, curve in enumerate(thing.curves):
                    for index in range(indexices):
                        value = self.tabs.widget(index).children()[1].return_cell_value(client, curve)
                        thing.data[curve].append('%s-%s' % (index, value))
            self.emit_dict.emit(stuff)
        except Exception as e:
            print("passed due to {}".format(e))

    def append_spreadsheet(self, spreadsheet, sheet_title):
        tab = QWidget(self)
        vBoxlayout = QVBoxLayout()
        excel_window = ExcelPageWidget(spreadsheet, sheet_title)
        vBoxlayout.addWidget(excel_window, alignment=Qt.AlignCenter)
        h_box = QHBoxLayout()
        h_box.addLayout(vBoxlayout)
        tab.setLayout(h_box)
        self.tabs.addTab(tab, sheet_title)
        self.show()


class ExcelPageWidget(TableWidget):

    selected_data = pyqtSignal(list, name='selected_data')

    def __init__(self, spreadsheet=None, popup_title='Test', parent=None):
        super(ExcelPageWidget, self).__init__(parent=parent,
                                              window_title=popup_title,
                                              file=spreadsheet)

    def mouseReleaseEvent(self, event):
        # event.accept()
        QTableWidget.mouseReleaseEvent(self, event)
        # if event.button() == Qt.RightButton:  # Release event only if done with left button, you can remove if necessary
        #     selected = self.selectedRanges()
        #
        #     headers = list(([str(self.horizontalHeaderItem(i).text()) for i in
        #                      range(selected[0].leftColumn(), selected[0].rightColumn() + 1)]))
        #     plots = []
        #     for r in range(selected[0].topRow(), selected[0].bottomRow() + 1):
        #         # Set row headers
        #         data = []
        #         client_name = self.verticalHeaderItem(r).text()
        #         data.append(client_name)
        #         for c in range(selected[0].leftColumn(), selected[0].rightColumn() + 1):
        #             # Copy cell values
        #             cell_value = self.item(r, c).text()
        #             data.append(self.remove_cell_format(cell_value))
        #         new_plot = PlotData(headers)
        #         new_plot.make_data(data)
        #         plots.append(new_plot)
        #     self.selected_data.emit(plots)

    def return_cell_value(self, row, column):
        row = self.row_dict[row]
        column = self.column_dict[column]
        cell = self.data[row][column]
        return self.remove_cell_format(cell)

    def remove_cell_format(self, value_to_convert):
        try:
            value_to_convert = value_to_convert.split('%')[0]
        except AttributeError:
            value_to_return = int(value_to_convert)
        else:
            try:
                value_to_return = int(float(value_to_convert))
            except ValueError:
                h, m, s = [int(float(i)) for i in value_to_convert.split(':')]
                value_to_return = (3600 * int(h)) + (60 * int(m)) + int(s)
        return value_to_return
