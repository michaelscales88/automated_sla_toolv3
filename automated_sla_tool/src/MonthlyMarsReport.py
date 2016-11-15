import traceback
import pyexcel as pe
from datetime import timedelta
from automated_sla_tool.src.DailyMarsReport import DailyMarsReport
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.TupleKeyDict import TupleKeyDict


class MonthlyMarsReport(AReport):
    def __init__(self, start_date, run_days):
        super().__init__(report_dates=start_date)
        self.last_date = start_date + timedelta(days=run_days)
        self.file_queue = pe.Book()
        self.final_report_fields = ['Absent', 'Late', 'DND', 'Duration', 'numDND', 'Inbound Ans', 'Inbound Lost',
                                    'Outbound', 'Inbound Duration', 'Outbound Duration']
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
                    # file.run()
                    try:
                        file.query_sql_server()
                    except Exception as e:
                        print("**SQL Query Exception raised**")
                        print(e)
                    # file.save_report()
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
        # self.prep_sheets()

    def print_queue(self):
        print(self.file_queue)

    def summarize_queue(self):
        if self.is_empty_wb(self.file_queue):
            return
        agent_summary = AgentSummary(fields=self.final_report_fields)
        for report in self.file_queue:
            for agent in report.rownames:
                if agent == 'Notes':
                    break
                agent_summary.collect_data(agent, report)
                # agent_summary[(agent, 'Absent'] = report[agent, 'Absent']
                # agent_summary[(agent, 'Late'] = report[agent, 'Late']
                # agent_summary[(agent, 'DND'] = report[agent, 'DND']
                # agent_summary[(agent, 'Duration')] = report[agent, 'Duration']
                # agent_summary[(agent, 'numDND')] = report[agent, 'numDND']
        self.create_final_report(agent_summary)

    '''
    Utilities Section
    '''

    def prep_sheets(self):
        for sheet in self.file_queue:
            sheet.name_rows_by_column(0)
            sheet.name_columns_by_row(0)

    def create_final_report(self, report_summary):
        report_header = report_summary.get_header()
        display_report = self.create_sheet(report_header)
        for (agent, data) in report_summary.items():
            row = [agent] + [data[k] for k in sorted(data.keys())]
            display_report.row += row
        display_report.name_rows_by_column(0)
        self.final_report = display_report
        self.generate_program_columns()
        self.time_stamp_format_col("DND", "Duration")

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

    def generate_program_columns(self):
        # TODO: Add row to count number of times in and out
        new_rows = pe.Sheet()
        new_rows.row += ["Avail"]
        for row in range(self.final_report.number_of_rows()):
            try:
                p_avail = ((self.final_report[row, "Duration"] - self.final_report[row, "DND"]) /
                           self.final_report[row, "Duration"])
                new_rows.row += [r'{0:.1%}'.format(p_avail)]
            except ZeroDivisionError:
                new_rows.row += [0]
        self.final_report.column += new_rows


class AgentSummary(TupleKeyDict):
    def __init__(self, fields=None):
        super().__init__()
        self.fields = fields

    def get_header(self):
        return ['Employee'] + sorted(self.fields)

    def __setitem__(self, key, value):
        try:
            add_secs = int(timedelta(hours=value.hour, minutes=value.minute, seconds=value.second).total_seconds())
        except AttributeError:
            super().__setitem__(key, value)
        else:
            super().__setitem__(key, add_secs)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def collect_data(self, agent, report):
        for column in self.fields:
            try:
                self[agent, column] += report[agent, column]
            except KeyError:
                self[agent, column] = report[agent, column]
