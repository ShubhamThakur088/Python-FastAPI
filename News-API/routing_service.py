from fastapi import FastAPI
from news_api_service import NewsService
from db_connection import DatabaseConnection
from file_service import FileService
import requests as req

news_api_service = FastAPI()

@news_api_service.get("/daily-headlines/{category}")
def daily_news_headlines(category):
    db_conn_obj = DatabaseConnection()
    news_service = NewsService(db_conn_obj)
    news_service.current_news_articles(category)
    db_conn_obj.commit_obj()
    db_conn_obj.connection_close()
    return "news update successful!"

@news_api_service.get("/download-file")
def generate_file(category:str, file_type_format:str):
    db_obj = DatabaseConnection()
    file_service = FileService(db_obj)

    if(file_type_format == "csv"):
        file_service.create_csv_file(category)
    elif(file_type_format == "xls"):
        pass
    elif(file_type_format == "json"):
        # news_service = NewsService()
        # response = news_service.current_news_articles(category)
        api_token = NewsService.api_access_key()        
        news_api_url = f"https://newsapi.org/v2/top-headlines?q={category}"
        api_response = req.get(news_api_url, headers={"x-api-key":api_token}).json()
        file_service.create_json_file(api_response, category)
    
    db_obj.connection_close()
    return "file for category "+category+" downloaded"