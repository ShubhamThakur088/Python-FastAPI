from pydantic import BaseModel, ValidationError, Field, field_validator
from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated
from uuid import UUID, uuid4

class User(BaseModel):
    uid: UUID = Field(default_factory = uuid4)
    username: Annotated[str, Field(min_length = 3, max_length = 25)]
    email:str
    bio:str = ""
    age: Annotated[int, Field(gt = 13, lt = 75)]
    is_active:bool = True
    full_name:str = None
    verified_at:datetime | None = None

    @field_validator("username")
    @classmethod    
    def validate_username(cls, v:str) -> str:
        if not v.replace('_', '').isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()

class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length = 1, max_length = 200)]
    content: Annotated[str, Field(min_length = 10)]
    view_count: int = 0
    is_published: bool = False

    tags: list[str] = Field(default_factory = list)

    created_at: datetime = Field(default_factory = partial(datetime.now, tz = UTC))

    author_id: str | int

    status: Literal["draft", "published", "archived"] = "draft"

# post = BlogPost(
#     title = "Getting Started with python",
#     content = "here is how to begin",
#     author_id= 4353
# )

# print(post.model_dump_json(indent=2))

try:
    user = User(        
        username = "Skt", 
        email = "shubham.thakur908@gmail.com",
        bio = "Hey there, I am learning python's pydantic validation model",
        age = 18,
        full_name = "Shubham Thakur",
        verified_at = datetime.now()
    )
except ValidationError as e:
    print(e)


print(user.model_dump_json(indent = 2))