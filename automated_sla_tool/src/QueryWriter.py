import pyexcel as pe
from sys import stdin
from datetime import datetime
from collections import OrderedDict
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
        return ';'.join(['{k}={v}'.format(k=key, v=val) for key, val in self._settings['Connection Info'].items()])

    @staticmethod
    def transform(ptr):
        headers = [column[0] for column in ptr.description]
        rtn_sheet = pe.Sheet()
        rtn_sheet.row += headers
        rtn_sheet.name_columns_by_row(0)
        for rows in ptr.fetchall():
            rtn_sheet.row += list(rows)
        return rtn_sheet

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
    @staticmethod
    def multi_line_cmd():
        buffer = ''
        while True:
            line = stdin.readline()
            if line.strip() == 'quit':
                break
            else:
                buffer += line
        return buffer

    def get_data(self, sql_command):
        cur = self.exc_cmd(sql_command)
        return OrderedDict([(column[0], column[1]) for column in cur.description]), QueryWriter.transform(cur)

    def exc_cmd(self, sql_command):
        print(sql_command, flush=True)
        return self._conn.cursor().execute(sql_command)

    def replicate_to(self, dest_conn=None, sql_commands=()):
        if dest_conn:
            for sql_command in sql_commands:
                print('Starting replicate {name} {time}'.format(name=sql_command.name, time=datetime.now().time()), flush=True)
                columns, data = self.get_data(sql_command.cmd)
                data.name = sql_command.name
                dest_conn.copy_tables(columns, data)
                print('returning get_data {name} {time}'.format(name=data.name, time=datetime.now().time()), flush=True)
        else:
            print('No connection to transfer to.')

    def copy_table(self):
        print('No copy_table function provided.', flush=True)


