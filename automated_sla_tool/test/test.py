from datetime import datetime, date, time, timedelta
from dateutil.parser import parse
from automated_sla_tool.src.BucketDict import BucketDict
from automated_sla_tool.src.UtilityObject import UtilityObject
import pyexcel as pe
from automated_sla_tool.src.FinalReport import FinalReport
import os
import re
from glob import glob as glob

import sqlite3


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%f;%f" % (self.x, self.y)


def main():
    import os
    filelist = [f for f in os.listdir(r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203') if f.endswith((".xlsx", ".xls"))]
    spc_ch = ['-', '_']
    del_ch = ['(', ')', '%' r'\d+']
    for f in filelist:
        f_name, ext = os.path.splitext(f)
        f_name = re.sub('[{0}]'.format(''.join(spc_ch)), ' ', f_name)
        f_name = re.sub('[{0}]'.format(''.join(del_ch)), '', f_name)
        f_name = f_name.strip()
        # print(f_name)
        full_f = r'{0}{1}'.format(f_name, ext)
        print(f)
        print(full_f)
        os.rename(f, full_f)
    file_string = r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203\Call Details*.xlsx'
    file_list = os.listdir(r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203')
    print(file_list)
    print(glob(file_string))
    print('Call Details*.xlsx' in file_list)
    # con = sqlite3.connect(":memory:")
    # cur = con.cursor()
    #
    # p = Point(4.0, -3.2)
    # cur.execute("SELECT ?", (p,))
    # print(cur.fetchone()[0])
    # report = FinalReport()
    # print(report)
    # report.open_report(r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Output\mars_report\11032016_mars_report.xlsx')

    # time1 = timedelta(minutes=10, seconds=12)
    # time2 = timedelta(hours=24)
    # print(time1)
    # sheet = pe.Sheet()
    # sheet.row += ['test', 'test1']
    # print(sheet)
    # sheet.row += [time1, time1]
    # print(sheet)
    # dt_date = '07:56:45'
    # print(parse(dt_date))
    # default_date = datetime.now() - timedelta(days=3)
    # print(parse(dt_date, default=default_date))
    # bool_str = 'False'
    # dt = datetime.now()
    # print(dt)
    # obj = UtilityObject(dt)
    # print(obj.str_to_bool(bool_str))
    # parse(date, default=(default if default is not None else self.util_datetime))
    # list_of_seconds = [15, 16, 5, 60, 65, 44, 32, 32, 90, 2, 15, 17]
    # # call_details_ticker = BetweenDict({(0, 16): 'found 0-16', (15, 31): 'found 15-31', (30, 46): 'found 30-46', (45, 61): 'found 45-61', (60, 1000): 'found 60-1000', (999, 999999): 'found 0-16'})
    # call_details_ticker = BucketDict(
    #     {(0, 15): 0, (15, 30): 0, (30, 45): 0, (45, 60): 0, (60, 999): 0, (999, 999999): 0}
    # )
    # for seconds in list_of_seconds:
    #     call_details_ticker.add_range_item(seconds)
    # call_details_ticker.add_range_item(999999909)
    # print(call_details_ticker)
    # print(call_details_ticker)
    # time_string = 'Mon, Aug 22, 2016 08:00 AM'
    # date_time = parse(time_string)
    # time_date = date_time.time()
    # print(60 * (time_date.hour * 60) + time_date.minute * 60 + time_date.second)
    # print(date_time.time().total_seconds())
    # date_time = date_time - date_time.date()
    # print(date_time)
    # date_time = datetime.strptime(str(date_time.time()), '%H:%M:%S')
    # date_time = time(date_time.hour, date_time.minute, date_time.second)
    # midnight = time()
    # print(date_time)
    # some_time = date_time - midnight
    # seconds = time.mktime(date_time.timetuple()) + date_time.microsecond / 1000000.0
    # print(some_time)
    # print(type(some_time))
    # print(seconds)
    # print(date_time.hours())
    # time_time = date_time.time()
    # print(time_time)
    # print(type(time_time))
    # today = date.today()
    # midnight = time(0, 0, 0)
    # midnight_today = datetime.combine(today, midnight)
    # print(midnight_today)
    # difference = abs(date_time - midnight_today)
    # print(difference)
    # print(type(difference))
    # print(difference.total_seconds())
    # time_example = datetime.time(0, 0, 0, 0)
    # print(time_example)
    # print(type(time_example))
    # time_difference = abs(time - time_example)
    # print(time_difference)
    # print(type(time_difference))

if __name__ == "__main__":
    main()
