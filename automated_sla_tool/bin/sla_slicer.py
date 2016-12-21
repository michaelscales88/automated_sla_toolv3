# Created by Michael Scales
# Version 2.0
# This program will take user modified excel spreadsheets
# parses the chronicall reports, collates the information and generates a mostly completed Daily SLA Report
# Jan 11 2016

# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import traceback
from automated_sla_tool.src.SlaSlicer import SlaSlicer


def main(report_date_delta, report_clients=None, report_values=('I/C Answered', 'Voice Mails')):
    print('inside main')
    if report_clients is None:
        report_clients = {7506: 'AAP', 7507: 'Ameren'}
    try:
        file = SlaSlicer(report_clients=report_clients,
                         report_delta=report_date_delta,
                         report_values=report_values)
        file.prepare_final_report()
        file.open_reports()
        file.compile_report_details()
    except:
        import sys
        error = traceback.format_exc()
        traceback.print_exc(file=sys.stderr)
        raise Exception(error)
    else:
        return [file.get_final_report()]


if __name__ == "__main__":
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))

    try:
        report_dates = sys.argv[1]
        report_cli = sys.argv[2]
        report_val = sys.argv[3]
    except:
        raise ImportError('__name__Main... sla_slicer.py ->'
                          'No file data provided...')
    else:
        main(report_dates, report_cli, report_val)
