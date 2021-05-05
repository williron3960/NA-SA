from pydantic import BaseModel, Field
from typing import List, Optional
import datetime, random, uuid


class Item(BaseModel):

    value: str
