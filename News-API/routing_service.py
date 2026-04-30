from fastapi import FastAPI
from news_api_service import NewsService
from db_connection import DatabaseConnection

routing_service = FastAPI()

@routing_service.get("/daily-headlines/{category}")
def daily_news_headlines(category):
    db_conn_obj = DatabaseConnection()
    news_service = NewsService(db_conn_obj)
    news_service.current_news_articles(category)
    db_conn_obj.commit_obj()
    db_conn_obj.connection_close()
    return "news update successful!"
