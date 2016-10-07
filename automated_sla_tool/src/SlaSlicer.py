import os
import pyexcel as pe
from datetime import timedelta
from automated_sla_tool.src.AReport import AReport


class SlaSlicer(AReport):
    def __init__(self, report_clients=None, report_delta=None, report_values=None):
        super(SlaSlicer, self).__init__(report_dates=report_delta)
        self.clients = report_clients
        self.report_values = report_values
        self.data = pe.Book()

    def prepare_final_report(self):
        final_header = self.prepare_sheet_header(self.report_values, 'Compiled')
        self.final_report.row += final_header
        self.final_report.name_columns_by_row(0)
        for (client_num, client_name) in self.clients.items():
            label = '{0} {1}'.format(client_num, client_name)
            temp_row = [0] * (len(self.report_values) + 1)
            temp_row[0] = label
            self.final_report.row += temp_row

    def open_reports(self):
        if len(self.dates) != 2:
            raise ValueError('SlaSlicer.open_reports'
                             '-> bad dates. Check format'
                             'list[start_date, end_date]')
        else:
            start_date = self.dates[0]
            end_date = self.dates[1]
            while start_date <= end_date:
                first_col_name = start_date.strftime('%A %m/%d/%Y')
                the_file = r'{0}\Output\{1}_Incoming DID Summary.xlsx'.format(os.path.dirname(self.path),
                                                                              start_date.strftime("%m%d%Y"))
                try:
                    report_page = pe.get_sheet(file_name=the_file, name_columns_by_row=0)
                    client_row_index = report_page.column[first_col_name]
                except FileNotFoundError:
                    print("Couldn't find the file: {}".format(the_file))
                else:
                    this_header = self.prepare_sheet_header(self.report_values, first_col_name)
                    page_data = pe.Sheet(this_header)
                    page_data.name_columns_by_row(0)
                    page_data.name = first_col_name
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
                finally:
                    start_date += timedelta(days=1)

    def compile_report_details(self):
        for sheet in self.data:
            sheet.name_columns_by_row(0)
            for v_index in range(sheet.number_of_rows()):
                for h_index in range(1, len(sheet.row[v_index])):
                    self.final_report[v_index, h_index] += sheet.row[v_index][h_index]

    def get_final_report(self):
        return self.final_report
