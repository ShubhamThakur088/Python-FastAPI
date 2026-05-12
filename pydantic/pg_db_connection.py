import psycopg2

class DatabaseConnection():
    def __init__(self):
        self.db = psycopg2.connect(port = "5432", database = "user-registration", 
                                   host = "localhost", password = "12345", user = "postgres")
    
    def conn_close(self):
        return self.db.close()
    
    def changes_commit(self):
        return self.db.commit()
    
    def cursor_obj(self):
        return self.db.cursor()