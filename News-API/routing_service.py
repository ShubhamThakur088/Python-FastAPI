from fastapi import FastAPI
from news_api_service import NewsService
from db_connection import DatabaseConnection
from csv_file_service import CsvFileService

news_api_service = FastAPI()

@news_api_service.get("/daily-headlines/{category}")
def daily_news_headlines(category):
    db_conn_obj = DatabaseConnection()
    news_service = NewsService(db_conn_obj)
    news_service.current_news_articles(category)
    db_conn_obj.commit_obj()
    db_conn_obj.connection_close()
    return "news update successful!"

@news_api_service.get("/download-csv-file/{category}")
def generate_csv_file(category):
    db_obj = DatabaseConnection()
    file_service = CsvFileService(db_obj)
    file_service.create_csv_file(category)
    db_obj.connection_close()
    return "file for category "+category+"downloaded"

