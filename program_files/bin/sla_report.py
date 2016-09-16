# Created by Michael Scales
# Version 2.0
# This program will take user modified excel spreadsheets 
# parses the chronicall reports, collates the information and generates a mostly completed Daily SLA Report
# Jan 11 2016

# -*- coding: utf-8 -*-
# !/usr/bin/env python3
from program_files.src.SlaReport import SlaReport


print("Daily SLA Program... Created by Michael Scales")


def main(report_date_datetime):
    try:
        file = SlaReport(report_date=report_date_datetime)
        file.download_documents()
        file.load_documents()
        file.compile_call_details()
        file.scrutinize_abandon_group()
        file.extract_report_information()
        file.process_report()
        file.save_report()
        print("Program ran successfully for date: %r" % report_date_datetime.strftime("%m%d%Y"))
    except SystemExit:
        pass
    else:
        return file.transmit_report()

if __name__ == "__main__":
    import datetime
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    main(datetime.datetime.now() - datetime.timedelta(days=3))
else:
    print('inside else')
