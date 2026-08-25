from datetime import datetime
from db_connection import DatabaseConnection
import pandas as pd
import json

class FileService:
    def __init__(self, db):
        self.db = db    

    def create_csv_file(self, news_category):        
        query = "SELECT art.article_title, art.contents, category.category_name FROM articles art \
                    JOIN news_categories category ON art.category_id = category.category_id \
                    WHERE category.category_name = %s"
        news_df = pd.read_sql_query(query, self.db.db, params = (news_category,))             
        file_path = "E:\\News-API\\news_csv_files\\"+news_category+".csv"
        news_df.to_csv(file_path, index=False)

    def create_json_file(self, news_response, category):
        # file_id = str(uuid.uuid3())
        with open("E:\\News-API\\news_csv_files\\"+category+"_raw"+".json", 'x') as f:
            f.write(json.dumps(news_response, indent=4))

# db_obj = DatabaseConnection()
# file_service = FileService(db_obj)
# file_service.create_csv_file("government")