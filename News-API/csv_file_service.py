from datetime import datetime
from db_connection import DatabaseConnection
import pandas as pd

class CsvFileService:
    def __init__(self, db):
        self.db = db    

    def create_csv_file(self, news_category):        
        query = "SELECT art.article_title, art.contents, category.category_name FROM articles art \
                    JOIN news_categories category ON art.category_id = category.category_id \
                    WHERE category.category_name = %s"
        news_df = pd.read_sql_query(query, self.db.db, params = (news_category,))             
        file_path = "E:\\News-API\\news_csv_files\\"+news_category+".csv"
        news_df.to_csv(file_path, index=False)

db_obj = DatabaseConnection()
file_service = CsvFileService(db_obj)
file_service.create_csv_file("government")