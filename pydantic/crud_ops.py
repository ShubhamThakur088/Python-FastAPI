from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import Annotated
from datetime import datetime
from pg_db_connection import DatabaseConnection

conn_obj = DatabaseConnection()

class CompanyDetails(BaseModel):
    company_name: Annotated[str, Field(min_length=5, max_length = 25)]
    email: EmailStr
    company_code: Annotated[str, Field(max_length=5, pattern="^[A-Z]{2}[0-9]{2}[E|N]+")]
    website : str
    created_timestamp: datetime

class CompanyService:
    def list_all_companies(self):
        cursor = conn_obj.cursor_obj()
        cursor.execute("SELECT * FROM company_details")
        result_set = cursor.fetchall()
        conn_obj.conn_close()
        print(result_set)
    
    def create_new_company_record(self, company_obj):
        try:
            cursor = conn_obj.cursor_obj()
            cursor.execute("INSERT INTO company_details (company_name, company_mail, company_code, company_website, created_timestamp)\
                           VALUES (%s, %s, %s, %s, %s)", (company_obj.company_name, company_obj.email, company_obj.company_code, company_obj.website, company_obj.created_timestamp))
            conn_obj.changes_commit()
            conn_obj.conn_close()
        except ValidationError as e:
            print(e)
    
    def get_compnay_by_id(self, company_code):
        try:
            cursor = conn_obj.cursor_obj()
            cursor.execute("SELECT * FROM company_details WHERE company_code = %s", (company_code,))
            result_set = cursor.fetchall()[0]
            print(result_set)
            conn_obj.conn_close()
        except:
            print("company with "+company_code+" not found")

intuit = CompanyDetails(company_name="Intuit", company_code="IT23E", email="intoit@intuit.com", website="intuit.co.in", created_timestamp=datetime.now())
company_service = CompanyService()
# company_service.create_new_company_record(intuit)
# company_service.list_all_companies()
# print(intuit.model_dump_json(indent=3))
company_service.get_compnay_by_id("GO23N")