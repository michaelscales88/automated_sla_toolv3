import sqlite3 as lite
import pyexcel as pe
import sys
import traceback
from datetime import time, date
from collections import defaultdict
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
            str: 'TEXT',
            time: 'TEXT',
            date: 'INTEGER'
        }
        try:
            self.conn = self.get_conn()
            print('Successful connection to: {0}'.format(self.params.name))
        except Exception:
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error, flush=True)

    def get_conn(self):
        return lite.connect(self.params.get_db_loc())

    def insert(self, table):
        print('inside insert')
        for dtable in self.get_tables():
            try:
                self.drop_table(dtable)
            except Exception as e:
                print(e)
        self.commit_changes()
        print(table)
        print(table.colnames)
        print([table.name] + table.colnames)
        # test_data = [
        #     ['name1', 'val1'],
        #     ['name2', 'val2']
        # ]
        # test_create = '''
        # CREATE TABLE test2
        # (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        # t_name TEXT,
        # val TEXT);
        # '''
        # self.conn.execute(test_create)
        # self.conn.commit()
        # self.refresh_connection()
        # test_insert = '''
        # INSERT INTO
        # test2(t_name, val)
        # VALUES
        # (:t_name, :val)
        # '''
        # test_cur = self.conn.cursor()
        # test_cur.executemany(test_insert, test_data)
        # data = table.query_format()
        # table_name = self.get_table_name(table.name)  # TODO refactor this to get
        # (create_query,
        #  execute_query) = self.make_query(table_name, data)
        # print(create_query)
        # self.conn.execute(create_query)
        # print(execute_query)
        # self.commit_changes()
        # # for row in data:
        # #     insert_row = {
        # #                       'Late': row.get('Late'),
        # #                       'Absent': row.get('Late'),
        # #                       'Inbound_Lost': row.get('Inbound_Lost'),
        # #                       'Employee': row.get('Employee'),
        # #                       'Notes': row.get('Notes'),
        # #                       'Avail': row.get('Avail'),
        # #                       'numDND': row.get('numDND'),
        # #                       'Inbound_Ans': row.get('Inbound_Ans'),
        # #                       'Outbound': row.get('Outbound'),
        # #     }
        # #     print('Starting insert: ' + insert_row['Employee'])
        # #     self.conn.execute(execute_query, insert_row)
        # #     print('Completed insert: ' + insert_row['Employee'])
        # f = lambda: None
        # insert_row = [defaultdict(f,
        #     {
        #         'Late': row.get('Late'),
        #         'Absent': row.get('Absent'),
        #         'Inbound_Lost': row.get('Inbound Lost'),
        #         'Employee': row.get('Employee'),
        #         'Notes': row.get('Notes'),
        #         'Avail': row.get('Avail'),
        #         'numDND': row.get('numDND'),
        #         'Inbound_Ans': row.get('Inbound Ans'),
        #         'Outbound': row.get('Outbound'),
        #     }
        # ) for row in data]
        # self.conn.executemany(execute_query, insert_row)
        # # self.conn.executemany(execute_query, data)
        # self.commit_changes()

        # rtn_data = self.query('mars_report')
        ###################################


        # TODO Below is diff
        # new_sheet = pe.get_sheet(records=)
        # print(new_sheet)


        # make_table = '''
        # CREATE TABLE mars_report
        # (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        # Employee TEXT NOT NULL,
        # Avail REAL);
        # '''
        # self.conn.execute(make_table)
        #
        # insert_data = [
        #     {"Employee": row.get('Employee'),
        #      "Avail": row.get('Avail')} for row in data]
        # insert_cmd = '''
        # INSERT INTO mars_report
        # (Employee, Avail)
        # VALUES
        # (:Employee, :Avail)
        # '''
        # self.conn.executemany(insert_cmd, insert_data)
        # self.commit_changes()
        # self.query('mars_report')

        # for row in data:

        # insert_row = [
        #       data.get('id'),
        #       data.get('title'),
        #       data.get('tags'),
        #       data.get('latitude'),
        #       data.get('longitude'),
        #     ]
        # columns = data[0].keys()
        # data = ', '.join(["'{0}'".format(col_name) for col_name in columns])
        # place_holders = ', '.join([":{0}".format(col_name) for col_name in columns])





        # print(', '.join(columns))
        # print(', '.join([':{0}'.format(col_name) for col_name in columns]))
        # cmd = '''
        # INSERT INTO {0} ({1})
        # VALUES ({2});
        # '''.format(table_name,
        #            data,
        #            place_holders)
        # print(cmd)
        # try:
        #      # TODO this needs to be completed to take a spreadsheet and convert it into a table/make the table etc etc
        # #     cmd = '''
        # #     INSERT INTO {0} VALUES ({1})
        # #     '''.format(table_name, query)
        # #     print(cmd)
        #     self.conn.executemany(cmd, data)
        # # #     print(table)
        # # #     print('Insert successful')
        # # #     # cur.execute(cmd)
        # except lite.OperationalError:
        #     print('Creating a table and INSERTING')
        #     create_table = '''
        #     CREATE TABLE {0}({1})
        #     '''.format(table_name, data)
        #     self.conn.execute(create_table)
        #     for val in data:
        #         self.conn.execute(cmd, val)
        # self.conn.executemany(cmd, values)
        #     cmd = '''
        #                 INSERT INTO {0} VALUES ({1})
        #                 '''.format(table_name, query)
        #     self.conn.executemany(cmd, table.query_format())
        # #     print('Insert successful')
        # #     # self.no_table(table)

    def make_query(self, table_name, data):
        test_row = data[0].items()
        values = ', '.join(['{0}'.format(k.replace(' ', '_')) for k, v in test_row if type(v) is not time])
        values_types = 'ID INTEGER PRIMARY KEY AUTOINCREMENT, ' + ', '.join(['{0} {1}'.format(k.replace(' ', '_'),
                                                                                              self.ci[type(v)]) for k, v
                                                                             in test_row if type(v) is not time])
        # print(values)
        place_holders = ', '.join([':{0}'.format(k.replace(' ', '_')) for k, v in test_row if type(v) is not time])
        # print(place_holders)
        c_query = '''
        CREATE TABLE {0}
        ({1})
        '''.format(table_name, values_types)
        e_query = '''
        INSERT INTO {0}
        ({1})
        VALUES
        ({2});
        '''.format(table_name, values, place_holders)
        return c_query, e_query

    def query(self, table_name):
        cmd = '''
                SELECT * FROM {0}
        '''.format(table_name)
        test_cur = self.conn.cursor()
        test_cur.execute(cmd)
        all_rows = test_cur.fetchall()
        headers = [col_name[0] for col_name in test_cur.description]
        # print(headers)
        # print([[row] for row in all_rows])
        rtn_sheet = pe.Sheet()
        rtn_sheet.row += headers
        rtn_sheet.name_columns_by_row(0)
        for row in all_rows:
            print(row)
            try:
                rtn_sheet.row += list(row)
            except Exception as e:
                print(e.__cause__)
                print(e)
        print(rtn_sheet)

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

    def commit_changes(self):
        self.conn.commit()
        self.refresh_connection()

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
        cur.row_factory = lambda cursor, row: row[0]
        cmd = "SELECT name FROM sqlite_master WHERE type='table'"
        cur.execute(cmd)
        return cur.fetchall()

    def refresh_connection(self):
        self.conn.close()
        self.conn = self.get_conn()
