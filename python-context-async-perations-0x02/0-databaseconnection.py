import sqlite3

class DatabaseConnection:
    
    def __init__(self,db):
        self.db = db
        self.conn = None
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn
    
    def __exit__(self, exc_type, exc_val,exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)