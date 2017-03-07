import pypyodbc as ps
from json import dumps
from automated_sla_tool.src.QueryWriter import QueryWriter
from automated_sla_tool.src.utilities import DateTimeEncoder


class SqlWriter(QueryWriter):

    def get_conn(self):
        return ps.connect(self.conn_settings)

    def rtn_excel(self, sql_command):
        columns, data = self.get_data(sql_command)
        return data

    def rtn_dict(self, sql_command):
        columns, data = self.get_data(sql_command)
        results = []
        for row in data:
            results.append(dict(zip(columns.keys(), row)))
        return results

    def replicate_to(self, dest_conn=None, sql_commands=()):
        if dest_conn:
            for sql_command in sql_commands:
                columns, data = self.get_data(sql_command.cmd)
                data.name = sql_command.name
                dest_conn.copy_tables(columns, data)
        else:
            print('No connection to transfer to.')

    def get_db_info(self):
        cursor1 = self._conn.cursor()
        cursor2 = self._conn.cursor()

        for i, rows in enumerate(cursor1.tables()):
            if rows['table_type'] == "TABLE":
                print('{i}: {row}'.format(i=i, row=rows['table_name']))
                for fld in cursor2.columns(rows['table_name']):
                    print(fld['table_name'], fld['column_name'])

    def test_command(self):
        table = self.transform(self.exc_cmd(self.multi_line_cmd()))
        print(table)
        print(type(table))

    def dict_command(self):
        table = self.rtn_dict(self.multi_line_cmd())
        print(table)
        print(dumps(table,
                    indent=4,
                    cls=DateTimeEncoder))
        print(type(table))

