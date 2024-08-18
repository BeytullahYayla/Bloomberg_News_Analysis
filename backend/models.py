from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, HttpUrl
from enum import Enum
from datetime import datetime


class NewBase(BaseModel):
    id:UUID
    title:str
    description:str
    sentiment:str
    publish_date:str
