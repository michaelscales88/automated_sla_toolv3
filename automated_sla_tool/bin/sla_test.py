from automated_sla_tool.src.GenericUi import GenericUi as ui
from automated_sla_tool.src.SlaReport import SlaReport
from datetime import datetime


def main():
    my_obj = SlaReport()  # report_date=datetime().date().replace(year=2016, month=12, day=22)
    my_ui = ui()
    my_ui.object = my_obj
    my_ui.run()

if __name__ == '__main__':
    main()
