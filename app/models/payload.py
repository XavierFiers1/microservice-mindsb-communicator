from typing import Optional

from pydantic import BaseModel


class PayLoad(BaseModel):
    text: str
    db_model: str
    author: Optional[str] = None


class Info(BaseModel):
    info: str
