import sqlite3 as lite
import sys
import traceback
from automated_sla_tool.src.QueryWriter import QueryWriter
from automated_sla_tool.src.QueryParam import QueryParam


class SqliteWriter(QueryWriter):
    """
        params = {
                'database': None,
                'user': None,
                'password': None,
                'host': None,
                'port': None
            }
    """

    def __init__(self, **parameters):
        super().__init__()
        self.params = QueryParam(**parameters)
        # Command Interpreter Python/SQLite
        self.ci = {
            None: 'NULL',
            int: 'INTEGER',
            float: 'REAL',
            str: 'TEXT'
        }
        try:
            self.conn = self.get_conn()
            print('Successful connection to: {0}'.format(self.params.name))
        except Exception:
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error, flush=True)

    def get_conn(self):
        conn = lite.connect(self.params.get_db_loc())
        conn.row_factory = lambda cursor, row: row[0]
        return conn

    def insert(self, table):
        print('inside insert')
        # print(table.name)
        # print(table.rownames)
        # print(table.colnames)
        # cur = self.conn.cursor()
        (table_name,
         query) = self.write_query(table)
        try:
            # # TODO this needs to be completed to take a spreadsheet and convert it into a table/make the table etc etc
            cmd = '''
            INSERT INTO {0} VALUES ({1})
            '''.format(table_name, query)
            print(cmd)
            self.conn.executemany(cmd, [table.to_array()])
            print(table)
            print('Insert successful')
            # cur.execute(cmd)
        except lite.OperationalError:
            print('Creating a table and INSERTING')
            cmd = '''
            CREATE TABLE {0}({1})
            '''.format(table_name, query)
            print(cmd)
            self.conn.execute(cmd)
            cmd = '''
                        INSERT INTO {0} VALUES ({1})
                        '''.format(table_name, query)
            self.conn.executemany(cmd, table)
            print('Insert successful')
            # self.no_table(table)
        cmd = '''
        SELECT * FROM mars_report
        '''
        for row in self.conn.execute(cmd):
            print(row)

    def query(self, table):
        cur = self.conn.cursor()
        pass

    def write_query(self, table):
        table_name = self.get_table_name(table.name)
        query = "".join(["'{}', ".format(i) for i in table.colnames])
        return table_name, query.rstrip(', ')

    def no_table(self, table):
        print('Could not identify table for {}'.format(table.name))
        rec_tables = dict(enumerate(self.get_tables()))
        selection = input('Did you mean? ...'
                          '{0}\n'
                          'OR enter a new table name.'.format(rec_tables))
        if selection.isdigit():
            selection = rec_tables[int(selection)]
            print('Using table {}'.format(selection))
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
