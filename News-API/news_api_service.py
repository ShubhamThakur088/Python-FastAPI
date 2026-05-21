import os
import requests as req
from dotenv import load_dotenv
from news_constants import NewsConstants
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime

class NewsService():
    def __init__(self, db):
        self.db = db    

    def date_validator(self,value):
        if datetime.fromisoformat(value).year >= 2025:
            return True
        else:
            return False    

    def current_news_articles(self, news_category):
        load_dotenv()
        api_token = os.getenv("API_KEY")        
        news_api_url = f"https://newsapi.org/v2/top-headlines?q={news_category}&apiKey={api_token}"
        api_response = req.get(news_api_url).json()['articles']       
        news_constants = [e.value for e in NewsConstants]
        articles = api_response
        cursor = self.db.cursor_obj()
               
        for i in range(len(articles)):
            published_at = articles[i]['publishedAt']
            yr = self.date_validator(published_at)
            is_title_exist = self.is_news_exists(articles[i]['title'], cursor)
            try:
                if articles[i]['source']['name'] in news_constants and yr and is_title_exist:
                    articles_url = articles[i]['url']
                    news_source = articles[i]['source']['name']
                    news_title = articles[i]['title']
                    published_date = articles[i]['publishedAt']

                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
                    request_obj = Request(articles_url,  headers = {"User-Agent":user_agent})                  

                    html_response = urlopen(request_obj, timeout=5) # Added timeout so that the 
                    html_soup = BeautifulSoup(html_response, 'html.parser')
                    paragraph_list = html_soup.find_all('p')
                    para_1 = paragraph_list[4].text
                    para_2 = paragraph_list[5].text
                    combined_para = para_1+" "+para_2
                    
                    cursor.execute("SELECT category_id FROM news_categories WHERE category_name = %s", (news_category,))
                    news_category_id = cursor.fetchone()[0]

                    cursor.execute("SELECT platform_id FROM news_platforms WHERE platform_name = %s", (news_source,))
                    news_platform_id = cursor.fetchone()[0]

                    cursor.execute("INSERT INTO articles (article_title, contents, category_id, platform_id, published_date_time, article_link)" \
                            "VALUES (%s, %s, %s, %s, %s, %s)", (news_title, combined_para, news_category_id, news_platform_id, published_date, articles_url))
                    # self.db_rw_operations(self, articles_url, news_source, news_title, published_date, combined_para, news_category)
            except Exception as e:
                print("exception occured here "+articles_url)

    def is_news_exists(self, article_title, cur):
        cur.execute("SELECT * FROM articles WHERE article_title = %s", (article_title,))
        result_set = cur.fetchone()

        if(result_set != None):
            return False
        else:
            return True
        
    

   
    # def db_rw_operations(self, articles_url, news_source, news_title, published_date, combined_para, news_category):
    #     cursor = self.db.cursor_obj()

    #     print("cursor object created")

    #     cursor.execute("SELECT category_id FROM news_categories WHERE category_name = %s", (news_category,))
    #     news_category_id = cursor.fetchone()[0]

    #     print("category fetched")
    
    #     cursor.execute("SELECT platform_id FROM news_platforms WHERE platform_name = %s", (news_source,))
    #     news_platform_id = cursor.fetchone()[0]

    #     print("news_platform_id fetched")

    #     cursor.execute("INSERT INTO articles (article_title, contents, category_id, platform_id, published_date_time, article_link)" \
    #     "VALUES (%s, %s, %s, %s, %s, %s)", (news_title, combined_para, news_category_id, news_platform_id, published_date, articles_url))

    #     print("insert executed")