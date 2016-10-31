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
                    # file.save_report()
                except OSError:
                    print('Could not open report for date {}'.format(run_date))
                except SystemExit:
                    raise SystemExit('SysExiting MARsReport...')
                except Exception as e:
                    print('Unexpected Exception encounter')
                    print(e)
                else:
                    print("Program ran successfully for date: {}".format(run_date.strftime("%m%d%Y")))
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

    def summarize_queue(self):
        print(self.file_queue)
        if self.is_empty_wb(self.file_queue):
            print('empty wb')
            return
        agent_summary = AgentSummary()
        for report in self.file_queue:
            for agent in report.rownames:
                if agent == 'Notes':
                    break
                agent_summary[(agent, 'Absent')] = report[agent, 'Absent']
                agent_summary[(agent, 'Late')] = report[agent, 'Late']
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
        print(display_report)

    def create_sheet(self, headers):
        sheet = pe.Sheet()
        sheet.row += headers
        sheet.name_columns_by_row(0)
        return sheet


class AgentSummary(TupleKeyDict):
    def __init__(self):
        super().__init__()

    def get_header(self):
        adict = self.get_dict()
        return ['Employee'] + sorted(next(iter(adict.values())).keys())
