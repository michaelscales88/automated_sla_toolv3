import traceback
from os import sys, path
from datetime import timedelta, datetime
from automated_sla_tool.src.DailyMarsReport import DailyMarsReport


def main(start_date):
    print('Running MARsReport...')
    file_queue = []
    try:
        try:
            file = DailyMarsReport(month=start_date)
            file.prep_data()
            file.process_report()
            print("Program ran successfully for date: {}".format(start_date.strftime("%m%d%Y")))
        except SystemExit:
            raise SystemExit('SysExiting MARsReport...')
        else:
            pass
            # file_queue.append(file.transmit_report())
    except SystemExit:
        pass
    except:
        import sys
        error = traceback.format_exc()
        traceback.print_exc(file=sys.stderr)
        raise Exception(error)
    else:
        return file_queue

if __name__ == "__main__":
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    run_date = datetime.today().date() - timedelta(days=3)
    main(run_date)
else:
    print('entered from else mars_report')
