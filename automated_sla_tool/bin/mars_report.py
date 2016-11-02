from os import sys, path
from datetime import timedelta, datetime
from automated_sla_tool.src.MonthlyMarsReport import MonthlyMarsReport


def main(s_date=None, days=None):
    file = MonthlyMarsReport(start_date=s_date, run_days=days)
    file.run()
    # file.print_queue()
    file.summarize_queue()
    # file.save_report()


if __name__ == "__main__":
    start_date = input(r'What day to start?')
    number_days = input(r'How many days?')
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    run_date = (datetime.today().date() - timedelta(days=1) if start_date is '' else
                datetime.strptime(start_date, '%m%d%Y').date())
    run_days = (0 if number_days is '' else int(number_days))
    main(s_date=run_date, days=run_days)
else:
    print('entered from else mars_report')
