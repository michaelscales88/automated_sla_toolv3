import pypyodbc as ps
from json import dumps
from automated_sla_tool.src.QueryWriter import QueryWriter
from automated_sla_tool.src.utilities import DateTimeEncoder


class SqlWriter(QueryWriter):

    def get_conn(self):
        return ps.connect(self.conn_string)

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

    def dict_command(self):
        table = self.rtn_dict(self.multi_line_cmd())
        print(table)
        print(dumps(table,
                    indent=4,
                    cls=DateTimeEncoder))
        print(type(table))

    def simple_query(self):
        # TODO Fix error: malformed results. Sample that breaks below
        # Issue seems to be with joining tables with matching field names
        '''
        Select Distinct c_call.call_id, c_event.event_id, *
        From c_event
        Inner Join c_call on c_event.call_id = c_call.call_id
        where to_char(c_call.start_time, 'YYYY-MM-DD') = '2017-03-06' and
        c_call.call_direction = 1
        Order by c_event.event_id
        '''
        rtn = super().simple_query()
        print(rtn.number_of_columns())
        print(rtn.colnames)
        print(rtn)
