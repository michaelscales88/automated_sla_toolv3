class QueryWriter(object):
    def __init__(self):
        super().__init__()
        self.conn = None

    def __del__(self):
        try:
            self.conn.close()
            print(r'Connection successfully closed.')
        except AttributeError:
            print(r'No connection to close.')