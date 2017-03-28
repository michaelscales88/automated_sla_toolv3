from automated_sla_tool.src.GenericUi import GenericUi as Ui
from automated_sla_tool.src.SlaReport import SlaReport

from sys import argv
from datetime import datetime


def main(report_date=None):
    my_ui = Ui()
    if report_date:
        my_obj = SlaReport(report_date=report_date)
    else:
        my_obj = SlaReport()
    my_ui.object = my_obj
    my_ui.run()


if __name__ == '__main__':
    # main(datetime.today().date().replace(year=int(input('Year?')), month=int(input('Month?')), day=int(input('Day?'))))
    main()
else:
    main(argv[1:])
    # main(datetime.date().replace(year=int(input('Year?')), month=int(input('Month?')), day=int(input('Day?'))))
