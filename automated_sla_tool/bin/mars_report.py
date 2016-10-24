from os import sys, path
from datetime import timedelta, datetime
from automated_sla_tool.src.MonthlyMarsReport import MonthlyMarsReport


def main(s_date=None, days=None):
    file = MonthlyMarsReport(start_date=s_date, run_days=days)
    file.run()
    # file.print_queue()
    file.summarize_reports()


if __name__ == "__main__":
    start_date = input(r'What day to start?')
    number_days = input(r'How many days?')
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    run_date = (datetime.strptime(start_date, '%m%d%Y').date() if start_date is not None else
                datetime.today().date() - timedelta(days=1))
    run_days = (int(number_days) if number_days is not None else 0)
    main(s_date=run_date, days=run_days)
else:
    print('entered from else mars_report')
