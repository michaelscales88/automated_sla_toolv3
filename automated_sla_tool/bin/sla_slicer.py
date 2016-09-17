# Created by Michael Scales
# Version 2.0
# This program will take user modified excel spreadsheets
# parses the chronicall reports, collates the information and generates a mostly completed Daily SLA Report
# Jan 11 2016

# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import pickle
import io
from os import path, sys
sys.path.append(r'C:\Users\mscales\Desktop\Development\automated_sla_tool')

from automated_sla_tool.src.SlaSlicer import SlaSlicer


# print("Sla Slicing Program... Created by Michael Scales")


def main(report_date_datetime, report_clients, report_values):
    # sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
    file = SlaSlicer(report_clients=report_clients,
                     report_dates=[report_date_datetime - datetime.timedelta(days=1), report_date_datetime],
                     report_values=report_values)
    file.open_reports()
    file.compile_report_details()
    report = file.get_final_report()
    # print(report)
    # print(type(report))
    d = pickle.dumps(obj=report, protocol=0)
    print(d)
    obj = pickle.loads(data=d, encoding='latin-1')
    print(obj)
    # print("Program ran successfully for date: %r" % report_date_datetime.strftime("%m%d%Y"))

if __name__ == "__main__":
    import datetime
    from os import sys, path

    report_cli = {7506: 'AAP', 7517: 'Humana', 7553: 'Infosys'}
    report_val = ['I/C Presented', 'Average Wait Lost', 'Calls Ans Within 45']
    # print(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    main(datetime.datetime.now() - datetime.timedelta(days=1), report_cli, report_val)
