import traceback
import pyexcel as pe
from datetime import timedelta
from automated_sla_tool.src.DailyMarsReport import DailyMarsReport
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.TupleKeyDict import TupleKeyDict


class MonthlyMarsReport(AReport):
    def __init__(self, start_date, run_days):
        # TODO improve report_dates to be a month and run for the month
        super().__init__(report_dates=start_date,
                         report_type='monthly_mars_report')
        self.last_date = start_date + timedelta(days=run_days)
        self.file_queue = pe.Book()
        self.final_report_fields = ['Absent', 'Late', 'DND Duration', 'Duration', 'numDND', 'Inbound Ans',
                                    'Inbound Lost', 'Outbound', 'Inbound Duration', 'Outbound Duration']
    '''
    UI Section
    '''

    def run(self):
        # TODO Make this a dispatcher -> threading
        run_date = self.dates
        while run_date <= self.last_date:
            try:
                try:
                    file = DailyMarsReport(month=run_date)
                    file.run()
                    # file.test()
                    # file.read_sql()
                    # file.write_sqlite()
                    file.save()
                except (OSError, FileNotFoundError) as e:
                    print('Could not open report for date {}'.format(run_date))
                    print(e)
                except SystemExit:
                    raise SystemExit('SysExiting MARsReport...')
                except Exception:
                    print('Unexpected Exception encounter: {}'.format(run_date.strftime("%m%d%Y")))
                    import sys
                    error = traceback.format_exc()
                    traceback.print_exc(file=sys.stderr)
                    print(error)
                else:
                    print("Program ran successfully for date: {}".format(run_date.strftime("%m%d%Y")))
                    self.file_queue += file.transmit_report()
            except SystemExit:
                pass
            finally:
                run_date += timedelta(days=1)
        try:
            self.prep_sheets()
        except IndexError:
            pass

    def print_queue(self):
        print(self.file_queue)

    def summarize_queue(self):
        print('starting to summarize queue')
        if self.is_empty_wb(self.file_queue):
            return
        agent_summary = AgentSummary(fields=self.final_report_fields)
        for report in self.file_queue:
            print(report)
            for agent in report.rownames:
                if agent == 'Notes':
                    break
                agent_summary.collect_data(agent, report)
        self.set_final_report(agent_summary)

    '''
    Utilities Section
    '''

    def prep_sheets(self):
        for sheet in self.file_queue:
            sheet.name_rows_by_column(0)
            sheet.name_columns_by_row(0)

    def set_final_report(self, report_summary):
        self.final_report.set_header(report_summary.get_header())
        for (agent, data) in report_summary.items():
            row = [agent] + [data[k] for k in sorted(data.keys())]
            self.final_report.row += row
        self.final_report.make_programatic_column(self.calculate_avail, "Avail")
        self.final_report.format_columns_with(self.convert_time_stamp, "Duration")
        print(self.final_report)

    def create_sheet(self, headers):
        sheet = pe.Sheet()
        sheet.row += headers
        sheet.name_columns_by_row(0)
        return sheet

    def save_report(self):
        self.set_save_path('monthly_mars_report')
        the_file = r'{0}_mars_report'.format(self.dates.strftime('%B'))
        self.final_report.name = self.dates.strftime('%B %Y')
        file_string = r'.\{0}.xlsx'.format(the_file)
        self.final_report.save_as(filename=file_string)

    # def generate_program_columns(self):
    #     # TODO: Add row to count number of times in and out
    #     new_rows = pe.Sheet()
    #     new_rows.row += ["Avail"]
    #     for row in range(self.final_report.number_of_rows()):
    #         try:
    #             p_avail = ((self.final_report[row, "Duration"] - self.final_report[row, "DND Duration"]) /
    #                        self.final_report[row, "Duration"])
    #             new_rows.row += [r'{0:.1%}'.format(p_avail)]
    #         except ZeroDivisionError:
    #             new_rows.row += [0]
    #     self.final_report.column += new_rows

    def calculate_avail(self, row):
        rtn_val = [r'{0:.1%}'.format(0)]
        try:
            print('val: {0} type: {1}'.format(row["Duration"], type(row["Duration"])))
            print('val: {0} type: {1}'.format(row["DND Duration"], type(row["DND Duration"])))
            p_avail = ((row["Duration"] - row["DND Duration"]) /
                       row["Duration"])
            rtn_val = [r'{0:.1%}'.format(p_avail)]
        except (ZeroDivisionError, KeyError) as e:
            print('passing calculate avail bc of {}'.format(e))
        return rtn_val


class AgentSummary(TupleKeyDict):
    def __init__(self, fields=None):
        super().__init__()
        self._fields = fields

    @property
    def fields(self):
        return self._fields

    def get_header(self):
        return ['Employee'] + sorted(self.fields)

    def __setitem__(self, key, value):
        try:
            add_secs = int(timedelta(hours=value.hour, minutes=value.minute, seconds=value.second).total_seconds())
        except AttributeError:
            super().__setitem__(key, value)
        else:
            try:
                comb_secs = self[key] + add_secs
                super().__setitem__(key, comb_secs)
            except KeyError:
                super().__setitem__(key, add_secs)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def collect_data(self, agent, report):
        for column in self.fields:
            try:
                self.__setitem__((agent, column), report[agent, column])
            except ValueError:
                print('Could not retrieve field: <{0}> '
                      'from file: {1}'.format(column, report.name))
