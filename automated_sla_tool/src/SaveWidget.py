import ctypes.wintypes
import pyexcel as pe
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QFileDialog, QStyle, QStyleOptionHeader)
from PyQt5.QtGui import QFontMetrics as fm
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from .ProcessButtonsWidget import ProcessButtonsWidget as PbWidget


class SaveWidget(QWidget):
    save_request_list = pyqtSignal(list, name='save_request_list')
    status_message = pyqtSignal(str, name='save_status')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('MiStRP Explorer')
        self.list_items = PbWidget()
        v_box = QVBoxLayout()
        v_box.addWidget(self.list_items, alignment=Qt.AlignCenter)
        self.setLayout(v_box)

    def save_event(self):
        try:
            process_menu = self.parent().children()[1].children()[1]
        except AttributeError:
            print("wrong parent")
        else:
            file_list = process_menu.get_save_info()

            items_to_save = []
            for item in self.list_items.selectedItems():
                default_file_name = file_list[str(item.text())]
                items_to_save.append(default_file_name)

            num_items = len(self.list_items.selectedIndexes())
            if num_items > 0:
                if num_items is 1:
                    file_name = items_to_save[0]
                    filename = self.save_file(file_name)
                else:
                    filename = self.save_multiple_files(items_to_save)
                self.status_message.emit("Saved '{}".format(filename))

    def add_event(self, item):
        self.list_items.add_list_item(item)

    def get_save_dir(self):
        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return buf.value

    def save_file(self, file_name):
        dialog = QFileDialog()
        download_directory = self.get_save_dir()
        default_file = file_name.split('\\')[-1]
        default_directory = r'{0}\{1}'.format(download_directory, default_file)
        filename, extension = dialog.getSaveFileName(self,
                                                     caption='Select save location',  # directory=items_to_save[0],
                                                     directory=default_directory,
                                                     filter="Text files (*.txt);;Excel (*.xlsx *.xls);;All Files (*.*)",
                                                     initialFilter="Excel (*.xlsx *.xls)")
        if not filename:
            return

        self.file_saver(file_name, filename)
        return filename

    def save_multiple_files(self, items_to_save):
        dialog = QFileDialog()
        filename = dialog.getExistingDirectory(self,
                                               caption='Select folder',
                                               directory=self.get_save_dir())
        if not filename:
            return
        for file in items_to_save:
            self.file_saver(file, filename)
        return filename

    def file_saver(self, original_file, destination):
        # TODO: implement implicit file conversion based on filter type
        unsaved_file = pe.get_sheet(file_name=original_file)
        try:
            unsaved_file.save_as(filename=destination)
        except OSError:
            unsaved_file.save_as(filename=destination[0])