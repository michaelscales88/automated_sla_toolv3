from datetime import datetime, date, time, timedelta
from dateutil.parser import parse
from automated_sla_tool.src.BucketDict import BucketDict
from automated_sla_tool.src.UtilityObject import UtilityObject
import pyexcel as pe
from automated_sla_tool.src.FinalReport import FinalReport
from automated_sla_tool.src.TupleKeyDict import TupleKeyDict
import os
import re
from glob import glob as glob
from socket import *
import multiprocessing
from dateutil.parser import parse
import time
import sys
from queue import Queue
import sqlite3
import logging
import logging.config
from automated_sla_tool.src.SysLog import SysLog
from time import sleep
from collections import defaultdict

def get_config(config_path, name):
    logging.config.dictConfig(config_path)
    return logging.getLogger(name)

class Test:

    def __init__(self):
        self._finished = False

    @property
    def finished(self):
        return self._finished

    def set_finished(self):
        self._finished = True

    def run(self):
        print('running..')


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%f;%f" % (self.x, self.y)


def worker():
    p = multiprocessing.current_process()
    print('worker {0} {1}'.format(p.name, datetime.now().time()))
    sys.stdout.flush()
    time.sleep(2)
    print('worker {0} {1}'.format(p.name, datetime.now().time()))
    sys.stdout.flush()


def main():
    #TODO build dictionary builder
    from os import path
    log_file_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), r'settings\logging2.conf')
    d = SysLog(__name__, file_path=log_file_path)
    print(type(d))
    print('Complete')
        # ev, ei, tb =
        # print('{e}\n{tb}'.format(e=e, tb=tb))
    # d = {}
    # with open(log_file_path, 'r') as log_file:
    #     d = dict(x.rstrip().split(None, 1) for x in log_file)
    # logging.config.fileConfig(log_file_path)
    # logger = logging.getLogger(__name__)
    # create logger
    # print(__name__)
    # logger = logging.getLogger('simpleExample')
    # logger = get_config(log_file_path, __name__)
    # 'application' code
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    # list = []
    # for i in range(3):
    #     t = multiprocessing.Process(name='cool{}'.format(i), target=worker)
    #     t.daemon = True
    #     list.append(t)
    #     t.start()
    #
    # for t in list:
    #     t.join()
    # print((True, False)[any([False, False, None])])
    # tuple_obj = (1, 2)
    # date_obj = datetime.today().date()
    # string_obj = str("Stuff Bitches")
    # print([type(date_obj), type(string_obj)])
    # print([date, str])
    # print(all(x in [type(tuple_obj), type(date_obj), type(string_obj)] for x in [tuple, date, str]))
    # month = input('Enter month')
    # print(month)
    # dt = datetime.strptime(month, '%B').date().replace(year=2016)
    # print(dt)









    #####################################
    # import win32api
    # import win32net
    # ip = '192.168.1.18'
    # username = 'ram'
    # password = 'ram@123'
    #
    # use_dict = {}
    # use_dict['remote'] = unicode('\\\\192.168.1.18\C$')
    # use_dict['password'] = unicode(password)
    # use_dict['username'] = unicode(username)
    # win32net.NetUseAdd(None, 2, use_dict)
    # import os
    # filelist = [f for f in os.listdir(r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203') if f.endswith((".xlsx", ".xls"))]
    # spc_ch = ['-', '_']
    # del_ch = ['(', ')', '%' r'\d+']
    # for f in filelist:
    #     f_name, ext = os.path.splitext(f)
    #     f_name = re.sub('[{0}]'.format(''.join(spc_ch)), ' ', f_name)
    #     f_name = re.sub('[{0}]'.format(''.join(del_ch)), '', f_name)
    #     f_name = f_name.strip()
    #     # print(f_name)
    #     full_f = r'{0}{1}'.format(f_name, ext)
    #     print(f)
    #     print(full_f)
    #     os.rename(f, full_f)
    # file_string = r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203\Call Details*.xlsx'
    # file_list = os.listdir(r'C:\Users\mscales\Desktop\Development\automated_sla_tool\Attachment Archive\1203')
    # print(file_list)
    # print(glob(file_string))
    # print('Call Details*.xlsx' in file_list)
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