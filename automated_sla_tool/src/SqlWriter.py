import pypyodbc as ps
import sys
import traceback
from automated_sla_tool.src.QueryWriter import QueryWriter
from automated_sla_tool.src.QueryParam import QueryParam


class SqlWriter(QueryWriter):
    def __init__(self, **parameters):
        super().__init__()
        self.params = QueryParam(**parameters,
                                 spc_case=True)
        try:
            self.conn = self.get_conn()
            print('Successful connection to: {0}'.format(self.params.name))
        except Exception:
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error, flush=True)

    def get_conn(self):
        return ps.connect(self.params.connection_string())

    def refresh_connection(self):
        self.conn.close()
        self.conn = self.get_conn()