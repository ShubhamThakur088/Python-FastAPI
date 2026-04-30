import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.db = psycopg2.connect(host = "localhost", port="5432", database="daily_news_updates", password = "32434", user = "postgres")

    def cursor_obj(self):
        return self.db.cursor()
    
    def commit_obj(self):
        return self.db.commit()
    
    def connection_close(self):
        return self.db.close()
