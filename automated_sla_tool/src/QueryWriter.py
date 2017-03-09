import pyexcel as pe
from sys import stdin
from datetime import datetime
from collections import OrderedDict
from numbers import Integral
from automated_sla_tool.src.AppSettings import AppSettings


class QueryWriter(object):
    # TODO Settings needed to be configured for multiple connections
    def __init__(self):
        self._settings = AppSettings(app=self)
        self._conn = None
        self.connect()

    @property
    def name(self):
        return self._settings.get('DATABASE', 'Generic Name')

    @property
    def conn_settings(self):
        return [
            '{k}={v}'.format(k=key, v=val) for key, val in self._settings['Connection Info'].items()
            ]

    @property
    def conn_string(self):
        return ';'.join(self.conn_settings)

    @staticmethod
    def transform_ptr(ptr):
        # print(len(QueryWriter.header(ptr)))
        return pe.get_sheet(
            colnames=QueryWriter.header(ptr),
            array=QueryWriter.data(ptr),
        )

    @staticmethod
    def header(ptr):
        return [column[0] for column in ptr.description]

    @staticmethod
    def header_w_metadata(ptr):
        return [(column[0], column[1]) for column in ptr.description]

    @staticmethod
    def row(seq):
        for x in seq:
            if isinstance(x, datetime):
                yield x
            elif isinstance(x, Integral):
                yield int(x)
            else:
                yield str(x)

    @staticmethod
    def data(ptr):
        return [list(QueryWriter.row(row)) for row in ptr.fetchall()]

    @staticmethod
    def multi_line_cmd():
        buffer = ''
        while True:
            line = stdin.readline()
            # TODO change the execute to f5 from keyboard AND something else typed 'f5'
            if line.strip() == 'quit':
                break
            else:
                buffer += line
        return buffer

    def __repr__(self):
        return self._settings.__str__()

    def __del__(self):
        self.close_conn()

    '''
    dB Connection Methods
    '''

    def connect(self):
        self._conn = self.get_conn()
        print('Successful connection to:\n{0}'.format(self))

    def get_conn(self):
        pass

    def refresh_connection(self):
        self.close_conn()
        self.connect()

    def close_conn(self):
        try:
            self._conn.close()
            print(r'Connection to {conn} successfully closed.'.format(conn=self.name))
        except AttributeError:
            print(r'No connection to close.')

    '''
    Query Methods
    '''

    def simple_query(self):
        table = QueryWriter.transform_ptr(
            self.exc_cmd(
                self.multi_line_cmd()
            )
        )
        # print(table)
        return table

    def get_data(self, sql_command):
        ptr = self.exc_cmd(sql_command)
        return OrderedDict(
            QueryWriter.header_w_metadata(ptr),
            QueryWriter.transform_ptr(ptr)
        )

    def exc_cmd(self, sql_command):
        return self._conn.cursor().execute(sql_command)

    def replicate_to(self, dest_conn=None, sql_commands=()):
        if dest_conn:
            for sql_command in sql_commands:
                print('Starting replicate {name} {time}'.format(name=sql_command.name, time=datetime.now().time()),
                      flush=True)
                columns, data = self.get_data(sql_command.cmd)
                data.name = sql_command.name
                dest_conn.copy_tables(columns, data)
                print('returning get_data {name} {time}'.format(name=data.name, time=datetime.now().time()), flush=True)
        else:
            print('No connection to transfer to.')

    def copy_table(self):
        print('No copy_table function provided.', flush=True)
