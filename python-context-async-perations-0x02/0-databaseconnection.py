import sqlite3

class DatabaseConnection:
    def __init__(self, database):
        self.database = database
        self.connection = None

  def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
        return False

with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
