import sqlite3

class ExecuteQuery:
    def __init__(self, database, query, params=None):
        self.database = database
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None
