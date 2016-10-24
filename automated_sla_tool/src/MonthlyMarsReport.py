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

    def run(self):
        run_date = self.dates
        while run_date <= self.last_date:
            try:
                try:
                    file = DailyMarsReport(month=run_date)
                    file.prep_data()
                    file.process_report()
                    file.save_report()
                    print("Program ran successfully for date: {}".format(run_date.strftime("%m%d%Y")))
                except OSError:
                    print('Could not open report for date {}'.format(run_date))
                except SystemExit:
                    raise SystemExit('SysExiting MARsReport...')
                else:
                    self.file_queue += file.transmit_report()
            except SystemExit:
                pass
            except:
                import sys
                error = traceback.format_exc()
                traceback.print_exc(file=sys.stderr)
                raise Exception(error)
            finally:
                run_date += timedelta(days=1)
        self.prep_sheets()

    def print_queue(self):
        print(self.file_queue)

    def summarize_reports(self):
        agent_summary = TupleKeyDict()
        for report in self.file_queue:
            for row in report.rownames:
                if row == 'Notes':
                    break
                agent_summary[(row, 'Absent')] = report[row, 'Absent']
                agent_summary[(row, 'Late')] = report[row, 'Late']
        print(agent_summary)

    def prep_sheets(self):
        for sheet in self.file_queue:
            sheet.name_rows_by_column(0)
            sheet.name_columns_by_row(0)