import time
import sqlite3 
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn,*args,**kwargs)
        finally:
            conn.close()          
    return wrapper

def retry_on_failure(retries=3,delay=2):
    def decorators(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            for attempt in range(retries):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    if(attempt==retries):
                        print(f"All attempts exhausted")
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorators

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)