import pypyodbc as ps
import pyexcel as pe
from automated_sla_tool.src.QueryWriter import QueryWriter


class SqlWriter(QueryWriter):
    def __init__(self, **parameters):
        super().__init__()
        self._params = {}
        self.init_params(**parameters)
        self.conn = self.get_conn()
        print('Successful connection to:\n{0}'.format(self))

    def get_conn(self):
        conn_string = ''.join([v for v in self._params.values()])
        return ps.connect(conn_string, timeout=2, unicode_results=True, readonly=True)

    def init_params(self, **kwargs):
        self._params['DRIVER'] = '{0}={1};'.format('DRIVER', kwargs.get('DRIVER', '{PostgreSQL Unicode}'))
        self._params['UID'] = '{0}={1};'.format('UID', kwargs.get('UID', None))
        self._params['PWD'] = '{0}={1};'.format('PWD', kwargs.get('PWD', None))
        self._params['SERVER'] = '{0}={1};'.format('SERVER', kwargs.get('SERVER', None))
        self._params['PORT'] = '{0}={1};'.format('PORT', kwargs.get('PORT', None))
        self._params['DATABASE'] = '{0}={1};'.format('DATABASE', kwargs.get('DATABASE', None))
        self._params['Trusted_Connection'] = '{0}={1};'.format('Trusted_Connection',
                                                               kwargs.get('Trusted_Connection', 'yes'))

    def refresh_connection(self):
        self.conn.close()
        self.conn = self.get_conn()

    def __repr__(self):
        return '\n'.join([v for v in self._params.values()])

    def rtn_excel(self, sql_command):
        columns, data = self.get_data(sql_command)
        test = pe.Sheet()
        test.row += columns
        test.name_columns_by_row(0)
        for rows in data:
            test.row += list(rows)
        print(test)

    def rtn_dict(self, sql_command):
        columns, data = self.get_data(sql_command)
        results = []
        for row in data:
            results.append(dict(zip(columns, row)))

    def get_data(self, sql_command):
        cur = self.exc_cmd(sql_command)
        return [column[0] for column in cur.description], cur.fetchall()

    def exc_cmd(self, sql_command):
        return self.conn.cursor().execute(sql_command)

    def get_db_info(self):
        cursor1 = self.conn.cursor()
        cursor2 = self.conn.cursor()

        for i, rows in enumerate(cursor1.tables()):
            if rows['table_type'] == "TABLE":
                print('{i}: {row}'.format(i=i, row=rows['table_name']))
                for fld in cursor2.columns(rows['table_name']):
                    print(fld['table_name'], fld['column_name'])
