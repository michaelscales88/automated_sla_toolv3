import sqlite3 as lite
import psycopg2 as ps2
import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker


class SqliteWriter(object):
    """
        params = {
                'database': None,
                'user': None,
                'password': None,
                'host': None,
                'port': None
            }
    """

    def __init__(self, pg_db=False, **parameters):
        super().__init__()
        self.params = QueryParam(**parameters,
                                 spc_case=pg_db)
        try:
            self.conn = self.get_conn()
            print('Successful connection to: {0}'.format(self.params.name))
        except Exception:
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error, flush=True)

    def get_conn(self):
        if self.params['local_db']:
            conn = lite.connect(self.params.get_db_loc())
            conn.row_factory = lambda cursor, row: row[0]
        else:
            conn = ps2.connect(self.params.connection_string())
        return conn

    def insert(self, table):
        print('inside insert')
        # print(table.name)
        # print(table.rownames)
        # print(table.colnames)
        cur = self.conn.cursor()
        try:
            table_name = self.get_table_name(table.name)
            # TODO this needs to be completed to take a spreadsheet and convert it into a table/make the table etc etc
            cur.execute("INSERT INTO table_name(server) VALUES (?)",(0,))
        except lite.OperationalError:
            self.no_table(table)

    def query(self, table):
        cur = self.conn.cursor()
        pass

    def no_table(self, table):
        print('Could not identify table for {}'.format(table.name))
        rec_tables = dict(enumerate(self.get_tables()))
        selection = input('Did you mean? ...'
                          '{0}\n'
                          'OR enter a new table name.'.format(rec_tables))
        if selection.isdigit():
            print('Using table {}'.format(rec_tables[int(selection)]))
        else:
            print('Creating a table named {}'.format(selection))
            self.make_table(selection)

    def get_table_name(self, sheet_name):
        # TODO this needs logic... this is cheap
        file_names = sheet_name.split('_')
        return "{0}_{1}".format(file_names[1], file_names[2])

    def make_table(self, table_name):
        cur = self.conn.cursor()
        cmd = 'CREATE table if not exists ' + table_name + ' (id integer)'
        cur.execute(cmd)
        self.conn.commit()

    def drop_table(self, table_name):
        if self.check_exists(table_name):
            cur = self.conn.cursor()
            cmd = "DROP table '{0}'".format(table_name)
            cur.execute(cmd)
            self.conn.commit()
            self.refresh_connection()

    def check_exists(self, table_name):
        cur = self.conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(table_name)
        return len(cur.execute(cmd).fetchall()) > 0

    def get_tables(self):
        cur = self.conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table'"
        cur.execute(cmd)
        return cur.fetchall()

    def refresh_connection(self):
        self.conn.close()
        self.conn = self.get_conn()

    def __del__(self):
        try:
            self.conn.close()
            print(r'Connection successfully closed.')
        except AttributeError:
            print(r'No connection to close.')


class QueryParam(object):
    def __init__(self, spc_case=False, **kwargs):
        super().__init__()
        self._params = {'dbname' if spc_case is True else 'database': kwargs.get('database', None),
                        'user': kwargs.get('user', None),
                        'password': kwargs.get('password', None),
                        'host': kwargs.get('host', None),
                        'port': kwargs.get('port', None),
                        'local_db': kwargs.get('local_db', None)}

    @property
    def name(self):
        return self.get_ext_db() or self._params['local_db']

    def get_port(self):
        return self._params['port']

    def get_host(self):
        return self._params['host']

    def get_user(self):
        return self._params['user']

    def get_pw(self):
        return self._params['password']

    def get_ext_db(self):
        return self._params.get('dbname', None) or self._params.get('database', None)

    def get_db_loc(self):
        return str(self._params['local_db'])

    def __getitem__(self, item):
        return self._params.get(item, None)

    def connection_string(self):
        return " ".join(["{0}='{1}'".format(key, value) for (key, value) in self._params.items() if value is not None])
