import sqlite3

class DatabaseConnection:
    def __init__(self, database):
        self.database = database
        self.connection = None
