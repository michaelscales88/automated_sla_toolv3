import traceback
import pyexcel as pe
from datetime import timedelta
from automated_sla_tool.src.DailyMarsReport import DailyMarsReport
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.TupleKeyDict import TupleKeyDict
from automated_sla_tool.src.UtilityObject import UtilityObject


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
                    file.save_report()
                except OSError:
                    print('Could not open report for date {}'.format(run_date))
                except SystemExit:
                    raise SystemExit('SysExiting MARsReport...')
                except Exception as e:
                    print('Unexpected Exception encounter: {}'.format(run_date.strftime("%m%d%Y")))
                    import sys
                    error = traceback.format_exc()
                    traceback.print_exc(file=sys.stderr)
                    print(e)
                    print(error)
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
        if self.is_empty_wb(self.file_queue):
            return
        agent_summary = AgentSummary()
        for report in self.file_queue:
            for agent in report.rownames:
                if agent == 'Notes':
                    break
                # TODO: make this += for clarity
                agent_summary[(agent, 'Absent')] = report[agent, 'Absent']
                agent_summary[(agent, 'Late')] = report[agent, 'Late']
                agent_summary[(agent, 'DND')] = report[agent, 'DND']
                agent_summary[(agent, 'Duration')] = report[agent, 'Duration']
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


class AgentSummary(TupleKeyDict):
    def __init__(self):
        super().__init__()
        self.__util = UtilityObject()

    def get_header(self):
        adict = self.get_dict()
        return ['Employee'] + sorted(next(iter(adict.values())).keys())

    def __setitem__(self, key, value):
        try:
            super().__setitem__(key, value)
        except TypeError:
            try:
                # TODO modify this... current timedelta rolls over at 24hours
                value = timedelta(hours=value.hour, minutes=value.minute, seconds=value.second)
            except AttributeError:
                # TODO this handles type int, but should only work for 0
                pass
            else:
                try:
                    curr_val = self[key[0]][key[1]]
                    curr_val = timedelta(hours=curr_val.hour, minutes=curr_val.minute, seconds=curr_val.second)
                except AttributeError:
                    pass
                else:
                    new_val = value + curr_val
                    super().set_item(key, new_val)
