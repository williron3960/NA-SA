from pydantic import BaseModel, Field
from typing import List, Optional
import datetime, random, uuid


# Model
class UserList(BaseModel):
    user_id          : str
    news_url         : str
    create_at        : Optional[datetime.datetime] = None
    news_result      : bool
    # block_chain_url  : str  # recover this when block chain is complete

class UserListGetid(BaseModel):
    user_id          : str
    news_url         : str


class UserEntry(BaseModel):
    user_id          : str
    news_url         : str
    news_result      : bool


class UserUpdate(BaseModel):
    user_id          : str = Field(..., example = 'enter your id')
    news_url         : str  = Field(..., example = 'enter your url')
    create_at        : Optional[datetime.datetime] = None
    news_result      : bool = Field(..., example = False)
    block_chain_url  : str  = Field(..., example = '321321314')

class UserDelete(BaseModel):
    user_id          : str = Field(..., example = 'enter your id')
    news_url         : str = Field(..., example = 'enter your url')
