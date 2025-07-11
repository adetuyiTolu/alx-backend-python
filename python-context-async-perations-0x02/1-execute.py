import sqlite3

class ExecuteQuery:
    
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.conn = None
        self.result = None
        
    def __enter__(self):
       self.conn = sqlite3.connect('users.db')
       cursor = self.conn.cursor()
       cursor.execute(self.query,self.params)
       self.result = cursor.fetchall()
       return self.result
  
    def __exit__(self, exc_type, exc_val,exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
       
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as query_result:
    print(query_result)
    