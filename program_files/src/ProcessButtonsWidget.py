from PyQt5.QtWidgets import QListWidget, QAbstractItemView


class ProcessButtonsWidget(QListWidget):
    def __init__(self, args=None):
        super().__init__()
        self.lngst_opt = ''
        if args:
            for arg in args:
                self.add_list_item(arg)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.change_transmit_arguments)
        self.argument_list = []
        self.show()

    def change_transmit_arguments(self, argument):
        list_argument = argument.text()
        if list_argument in self.argument_list:
            argument.setSelected(False)
            self.argument_list.remove(list_argument)
        else:
            self.argument_list.append(list_argument)

    def get_arguments(self):
        return self.argument_list

    def add_list_item(self, item):
        self.lngst_opt = max([self.lngst_opt, item], key=len)
        self.addItem(item)

    def remove_list_item(self, item):
        return

    def get_longest_arg(self):
        return self.lngst_opt
