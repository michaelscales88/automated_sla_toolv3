from automated_sla_tool.src.GenericUi import GenericUi as ui
from automated_sla_tool.src.SlaReport import SlaReport
from datetime import datetime


def main():
    my_ui = ui()
    my_obj = SlaReport(report_date=datetime.today().date().replace(year=2017, month=1, day=10))
    # my_obj = SlaReport()
    my_ui.object = my_obj
    my_ui.run()


if __name__ == '__main__':
    main()
