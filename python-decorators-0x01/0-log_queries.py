import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs or args
        query = kwargs.get('query') or (args[0] if args else None)
        
        if query:
            print(f"Executing SQL Query: {query}")
        
        return func(*args, **kwargs)
    
    return wrapper
