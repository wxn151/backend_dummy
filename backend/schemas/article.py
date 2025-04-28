from pydantic import BaseModel
from datetime import date

class ArticleBase(BaseModel):
    article: str
    hash: str
    date: date
    copyright: str

class ArticleCreate(ArticleBase):
    pass

class ArticleOut(ArticleBase):
    id: int
    class Config:
        orm_mode = True