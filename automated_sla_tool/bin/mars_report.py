from os import sys, path
from datetime import timedelta, datetime
from automated_sla_tool.src.MonthlyMarsReport import MonthlyMarsReport


def main(selection=None):
    file = MonthlyMarsReport(month=selection)
    file.run()
    if input('Save? {}'.format({'Yes': 1, 'No': 'Any other key.'})) is 1:
        file.save_report()


if __name__ == "__main__":
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    cal_ui = dict(enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                             'August', 'September', 'October', 'November', 'December'], start=1))
    main(selection=cal_ui[int(input(cal_ui))])

