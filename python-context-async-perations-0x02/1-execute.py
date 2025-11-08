import sqlite3

class ExecuteQuery:
    def __init__(self, database, query, params=None):
        self.database = database
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None

  def __enter__(self):
        # Open database connection
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        
        # Fetch and store the results
        self.results = self.cursor.fetchall()
        
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
        # Return False to propagate exceptions (if any)
        return False


# Use the context manager to execute a query
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
