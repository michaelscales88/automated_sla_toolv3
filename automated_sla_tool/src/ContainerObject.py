import pyexcel as pe


class ContainerObject:
    def __init__(self):
        pass

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
            print('entered OSerror')
            return_file = pe.Sheet(file)
        return return_file