# Created by Michael Scales
# Version 2.0
# This program will take user modified excel spreadsheets 
# parses the chronicall reports, collates the information and generates a mostly completed Daily SLA Report
# Jan 11 2016

# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import traceback
from datetime import timedelta
from automated_sla_tool.src.SlaReport import SlaReport


def main(report_date_delta):
    print('Running SLAReport...')
    file_queue = []
    try:
        start_date = report_date_delta[0]
        if report_date_delta[1] is not None:
            end_date = report_date_delta[1]
        else:
            end_date = start_date

        while start_date <= end_date:
            try:
                file = SlaReport(report_date=start_date)
                file.compile_call_details()
                file.scrutinize_abandon_group()
                file.extract_report_information()
                file.process_report()
                file.save_report()
                print("Program ran successfully for date: {}".format(start_date.strftime("%m%d%Y")))
            except SystemExit:
                raise SystemExit('SysExiting SLAReport...')
            except (FileNotFoundError, OSError) as e:
                print('Could not open report for date {}'.format(start_date.strftime("%m%d%Y")))
                print(e)
            else:
                pass
                file_queue.append(file.transmit_report())
            finally:
                start_date += timedelta(days=1)
    except SystemExit:
        pass
    except:
        import sys
        error = traceback.format_exc()
        traceback.print_exc(file=sys.stderr)
        raise Exception(error)
    else:
        return file_queue

if __name__ == "__main__":
    import datetime
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    run_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
    main([run_date, None])
else:
    print('entered from else sla_report')
