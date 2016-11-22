import sqlite3 as lite
import psycopg2 as ps2
import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker


class SqliteWriter(object):
    def __init__(self, **parameters):
        super().__init__()
        self.params = QueryParam(**parameters)
        try:
            self.conn = self.get_conn()
            print('connected successfully')
            # local_db = "psycog2"
            # conn_string = ""
            # params = {
            #     'database': 'chronicall',
            #     'user': 'Chronicall',
            #     'password': 'ChR0n1c@ll1337',
            #     'host': '10.1.3.17',
            #     'port': 9086
            # }
            # conn = ps2.connect(**params)
            # self.db_string = local_db
            # self.conn = lite.connect(local_db)
            # print(r'Successful connection to: {}'.format(local_db))
        except Exception:
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error, flush=True)
        # engine = create_engine("sqlite://{0}".format(local_db))
        # self.base = DailyMars()
        # self.session = sessionmaker(bind=engine)


# class DailyMars(declarative_base):
#     __tablename__ = 'daily_mars'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)-
#     weight = Column(Float)
#     birth = Column(Date)

    def get_conn(self):
        if self.params['local_db']:
            conn = lite.connect(self.params.get_db_loc())
        else:
            conn = ps2.connect(self.params.get_dict())
        return conn

    def insert(self, table):
        print('inside insert')
        # print(table)
        cur = self.conn.cursor()
        pass

    def query(self, table):
        cur = self.conn.cursor()
        pass

    def create_table(self, table_name):
        if self.check_exists(table_name) is False:
            cur = self.conn.cursor()
            cmd = 'create table if not exists ' + table_name + ' (id integer)'
            cur.execute(cmd)
            self.conn.commit()

    def drop_table(self, table_name):
        if self.check_exists(table_name):
            cur = self.conn.cursor()
            cmd = "DROP table '{0}'".format(table_name)
            cur.execute(cmd)
            self.conn.commit()
            self.refresh_connection()

    def check_exists(self, table):
        cur = self.conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(table)
        cur.execute(cmd)
        return cur.fetchone() is not None

    def refresh_connection(self):
        self.conn.close()
        self.conn = lite.connect(self.db_string)

    # def __del__(self):
    #     self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)


class QueryParam(object):
    """
    params = {
            'database': None,
            'user': None,
            'password': None,
            'host': None,
            'port': None
        }
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.params = {'database': kwargs.get('database', None),
                       'user': kwargs.get('user', None),
                       'password': kwargs.get('password', None),
                       'host': kwargs.get('host', None),
                       'port': kwargs.get('port', None),
                       'local_db': kwargs.get('local_db', None)}

    def get_port(self):
        return self.params['port']

    def get_host(self):
        return self.params['host']

    def get_user(self):
        return self.params['user']

    def get_pw(self):
        return self.params['password']

    def get_db(self):
        return self.params['database']

    def get_db_loc(self):
        return str(self.params['local_db'])

    def __getitem__(self, item):
        return self.params[item]

    def get_dict(self):
        # TODO in progress
        return ' '.join(['{0}={1}'.format(key, value) for (key, value) in self.params.items() if value is not None])