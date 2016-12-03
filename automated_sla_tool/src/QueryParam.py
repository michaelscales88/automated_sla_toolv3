class QueryParam(object):
    # TODO modify how this differentiates param types between SQL Server, PG and Sqlite3 ->> spc_case
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

    @property
    def port(self):
        return self._params['port']

    @property
    def host(self):
        return self._params['host']

    @property
    def user(self):
        return self._params['user']

    @property
    # setter format = @pw.setter
    def pw(self):
        return self._params['password']

    def get_ext_db(self):
        return self._params.get('dbname', None) or self._params.get('database', None)

    def get_db_loc(self):
        return str(self._params['local_db'])

    def __getitem__(self, item):
        return self._params.get(item, None)

    def connection_string(self):
        return " ".join(["{0}='{1}'".format(key, value) for (key, value) in self._params.items() if value is not None])