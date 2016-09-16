import numpy as np
import pyqtgraph.pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from datetime import datetime
from collections import defaultdict
from .DockWidget import DockWidget


class GraphicsDockWidget(DockWidget):
    def __init__(self, parent, window_name=None,
                 widget1=None, widget2=None,
                 button=None, hide_button_name=None):
        super(GraphicsDockWidget, self).__init__(parent, window_name, widget1,
                                                 widget2, button, hide_button_name)

    def make_graph(self, date1, date2):
        graph = GraphData()
        graph.create_graph(date1, date2)
        graph.show()
        self.setWidget(graph)
        self.show()

    def add_curve(self, plot_data):
        self.children()[-1].set_y_axis(plot_data)
        # print(self.children())


class MyStringAxis(pg.AxisItem):
    def __init__(self, xdict, *args, **kwargs):
        super(MyStringAxis, self).__init__(*args, **kwargs)
        self.x_values = np.asarray(xdict.keys())
        self.x_strings = xdict.values()

    def get_x_axis_list(self):
        return list(self.x_values.tolist())

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            # vs is the original tick value
            vs = v * scale
            # if we have vs in our values, show the string
            # otherwise show nothing
            if vs in self.x_values:
                # Find the string with x_values closest to vs
                vstr = self.x_strings[np.abs(self.x_values - vs).argmin()]
            else:
                vstr = ""
            strings.append(vstr)
        return strings


class GraphData(QWidget):
    def __init__(self, title='Default', parent=None):
        super(GraphData, self).__init__(parent)
        self.plot = None
        self.current_x_axis = None
        self.curves = []
        self.win = pg.GraphicsWindow(title)
        layout = QVBoxLayout()
        layout.addWidget(self.win, alignment=Qt.AlignVCenter)
        self.setLayout(layout)

    def make_xdict(self, date1, date2, xlist=None, fmt='%m%d%Y'):
        start_date = datetime.strptime(date1, fmt)
        end_date = datetime.strptime(date2, fmt)
        if xlist is None:
            xlist = []
        while start_date <= end_date:
            xlist.append(start_date.strftime('%A\n%m%d%y'))
            start_date += datetime.timedelta(days=1)
        return dict(enumerate(xlist))

    def create_graph(self, date1, date2):
        self.set_x_axis(date1, date2)
        self.plot = self.win.addPlot(axisItems={'bottom': self.current_x_axis},
                                     name='something', clickable=True)
        self.show()

    def set_x_axis(self, start_date, end_date):
        xdict = self.make_xdict(start_date, end_date)
        string_axis = MyStringAxis(xdict, orientation='bottom')
        string_axis.setTicks([xdict.items()])
        self.current_x_axis = string_axis

    def set_y_axis(self, plot_objects=None):
        list_of_keys = self.current_x_axis.get_x_axis_list()
        for plot_object in plot_objects:
            #     self.plot = self.win.addPlot(axisItems={'bottom': self.current_x_axis},
            #                                  name='something',
            #                                  clickable=True)
            for curve in plot_object.data.items():
                curve_name = str(curve[0])
                data_points = curve[1]
                y_values = []
                for data_pt in data_points:
                    if data_pt is not None:
                        y_values.append(int(data_pt.split('-')[1]))
                new_line = self.plot.plot(list_of_keys, y_values, pen=QColor(28, 78, 99))
                new_line.curve.setClickable(True)
                new_line.sigClicked.connect(self.clicked)
                self.curves.append(new_line)

    def clicked(self):
        print('clicked')


class PlotData:
    def __init__(self, headers):
        self.curves = None
        self.data = defaultdict(list)
        self.name = None
        self.create_curves(headers)

    def create_curves(self, headers):
        self.curves = headers

    def make_data(self, data):
        self.name = data.pop(0)
        init_keys = self.curves
        for key in init_keys:
            self.data[key].append(None)

    def add_data(self, data):
        pass

    def get_name(self):
        return self.name

    def __str__(self):
        # for curve in self.curves.items():
        print(self.name)
        print(self.curves)
        print(self.data)