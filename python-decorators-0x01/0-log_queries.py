import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries
def log_queries(func):
   @functools.wraps(func)
   def wrapper(*args,**kwargs):
       timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
       query = kwargs.get('query') or (args[0] if args else None)
       if (query):
           print(f"{timestamp} [Log] Executing SQL query: {query}")
       else:
            print(f"{timestamp} [Log] NO SQL query provided")
       return func(*args,**kwargs)
   return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")