# Created by Michael Scales
# Version 2.0
# This program will take user modified excel spreadsheets 
# parses the chronicall reports, collates the information and generates a mostly completed Daily SLA Report
# Jan 11 2016

# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import traceback
from datetime import timedelta, datetime, date
from automated_sla_tool.src.SlaReport import SlaReport


def main(report_date_delta):
    print('Running SLAReport...')
    file_queue = []
    try:
        start_date = report_date_delta[0]
        if type(report_date_delta[1]) is date:
            end_date = report_date_delta[1]
        else:
            end_date = start_date

        while start_date <= end_date:
            try:
                file = SlaReport(report_date=start_date)
                print('constructed')
                file.compile_call_details()
                print('compiled')
                file.scrutinize_abandon_group()
                print('scrutinized')
                file.extract_report_information()
                print('extracted')
                file.process_report()
                print('processed')
                file.save_report()
                print('saved')
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
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    start_date = input(r'What day to start?')
    number_days = input(r'How many days?')
    sys.path.append(path.dirname(path.dirname(path.abspath(path.abspath(__file__)))))
    run_date = (datetime.today().date() - timedelta(days=1) if start_date is '' else
                datetime.strptime(start_date, '%m%d%Y').date())
    run_days = (0 if number_days is '' else datetime.today().date() + timedelta(days=number_days))
    main([run_date, run_days])
else:
    print('entered from else sla_report')
