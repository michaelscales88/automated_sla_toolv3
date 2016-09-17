import os
import pyexcel as pe
from dateutil.parser import parse
from automated_sla_tool.src.AReport import AReport


class SlaSlicer(AReport):
    def __init__(self, report_clients=None, report_dates=None, report_values=None):
        super(SlaSlicer, self).__init__(report_dates=report_dates)
        self.clients = report_clients
        self.report_values = report_values
        self.data = pe.Book()
        self.prepare_final_report()

    def open_reports(self):
        for report_date in self.dates:
            date_string = report_date.strftime('%A %m/%d/%Y')
            the_file = r'{0}\Output\test{1}_Incoming DID Summary.xlsx'.format(os.path.dirname(self.path),
                                                                              report_date.strftime("%m%d%Y"))
            try:
                report_page = pe.get_sheet(file_name=the_file, name_columns_by_row=0)
                client_row_index = report_page.column[date_string]
            except FileNotFoundError:
                print("Couldn't find the file: {}".format(the_file))
            else:
                this_header = self.prepare_sheet_header(self.report_values, date_string)
                page_data = pe.Sheet(this_header)
                page_data.name_columns_by_row(0)
                page_data.name = date_string
                for (client_num, client_name) in self.clients.items():
                    label = '{0} {1}'.format(client_num, client_name)
                    client_index = client_row_index.index(label)
                    client_row = [label]
                    for value in self.report_values:
                        cell_val = report_page[client_index, value]
                        try:
                            cell_val = int(cell_val)
                        except ValueError:
                            cell_val = self.get_sec(cell_val)
                        client_row.append(cell_val)
                    page_data.row += [client_row]
                self.data += page_data

    def compile_report_details(self):
        for sheet in self.data:
            sheet.name_columns_by_row(0)
            for v_index in range(sheet.number_of_rows()):
                for h_index in range(1, len(sheet.row[v_index])):
                    self.final_report[v_index, h_index] += sheet.row[v_index][h_index]
        # print(self.final_report)

    def prepare_final_report(self):
        final_header = self.prepare_sheet_header(self.report_values, 'Compiled')
        self.final_report.row += final_header
        self.final_report.name_columns_by_row(0)
        for (client_num, client_name) in self.clients.items():
            label = '{0} {1}'.format(client_num, client_name)
            temp_row = [0] * (len(self.report_values) + 1)
            temp_row[0] = label
            self.final_report.row += temp_row

    def get_final_report(self):
        return self.final_report.to_array()