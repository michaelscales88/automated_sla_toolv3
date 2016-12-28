from os import sys, path
from automated_sla_tool.src.MarsReport import MarsReport as MR
from automated_sla_tool.src.GenericUi import GenericUi as ui


def main():
    my_obj = MR(month='December')
    my_ui = ui()
    my_ui.object = my_obj
    my_ui.run()


if __name__ == '__main__':
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    main()
