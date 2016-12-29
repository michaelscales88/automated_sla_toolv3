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
from collections import defaultdict, OrderedDict


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


class SqlCommand(object):
    def __init__(self):
        super().__init__()
        self._name = None
        self._cmd = None

    def __repr__(self):
        return self._cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, cmd):
        self._cmd = cmd

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


def test():
    sheet = pe.Sheet(colnames=['', 'a', 'b', 'c', 'd'])
    rows = [
        ['{i}'.format(i=chr(i * (x+1) + 97)) for x in reversed(range(5))] for i in range(5)
    ]
    for row in rows:
        sheet.row += row
    sheet.name_rows_by_column(0)
    # print(sheet.rownames)
    # print(sheet.colnames)
    # print(sheet)
    # sheet.colnames += ['e', 'f']
    # print(sheet.colnames)
    # new_rows = [
    #     ['e', 'f'],
    #     ['1', '2'],
    #     ['2', '2'],
    #     ['3', '3'],
    #     ['4', '4'],
    #     ['5', '5']
    #     # ['', 'e', 'f'],
    #     # ['a', '1', '2'],
    #     # ['f', '2', '2'],
    #     # ['k', '3', '3'],
    #     # ['p', '4', '4'],
    #     # ['u', '5', '5']
    # ]
    # new_sheet = pe.Sheet(new_rows)
    # new_sheet.name_rows_by_column(0)
    new_rows = OrderedDict(
        [
            ('e', ['1', '2', '3', '4', '5']),
            ('f', ['1', '2', '3', '4', '5'])
        ]
    )
    print(new_rows)
    # new_sheet.name_rows_by_column(0)
    # sheet.column['e'] += new_sheet.column['e']
    # sheet.column['f'] += new_sheet.column['f']
    sheet.extend_columns(new_rows)
    print(sheet)
    # print(sheet.column['e'])
    # sheet.column += new_sheet
    # print(sheet)
    # conn_string = {
    #     'DATABASE': 'chronicall',
    #     'UID': 'Chronicall',
    #     'PWD': 'ChR0n1c@ll1337',
    #     'SERVER': '10.1.3.17',
    #     'PORT': '9086'
    # }
    # tables = ['c_call', 'c_event', 'c_feature']
    # commands = []
    # raw_commands = {
    #     k: datetime.today().date() for k in tables
    # }
    # for k, v in raw_commands.items():
    #     cmd = SqlCommand()
    #     cmd.name = k
    #     cmd.cmd = (
    #         '''
    #         SELECT *
    #         FROM {t}
    #         WHERE to_char({t}.start_time, 'YYYY-MM-DD') = '{v}'
    #         '''.format(t=cmd.name, v=v.strftime('%Y-%m-%d'))
    #     )
    #     commands.append(cmd)
    # from automated_sla_tool.src.SqlWriter import SqlWriter as ps_write
    # from automated_sla_tool.src.SqliteWriter import SqliteWriter as sq_lite
    # conn = ps_write(**conn_string)
    # conn.replicate_to(dest_conn=sq_lite(), sql_commands=commands)
    # new_conn = sq_lite()
    # print(new_conn.query('c_call'))
    # print(new_conn.query('c_event'))
    # print(new_conn.query('c_feature'))
    # string = 'Call ID - 12312412'
    # import re
    # string = 'Cradle to, Grave - stuff'
    # corner_case = re.split(', | - ', string)
    # print(corner_case)
    # first_split = string.split(' - ')
    # second_split = first_split[0].split(' ')
    # print(second_split)
    # check_one = second_split[0] not in ('Feature', 'Call', 'Event')  # False
    # print(len(first_split))
    # print(True if len(first_split) > 1 else check_one)
    print('Complete')


if __name__ == "__main__":
    test()
