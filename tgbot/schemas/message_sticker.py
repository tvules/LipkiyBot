from io import BytesIO
from typing import Optional

from pydantic import BaseModel


class MessageAuthor(BaseModel):
    first_name: str
    last_name: Optional[str]
    avatar: Optional[BytesIO]

    class Config:
        arbitrary_types_allowed = True


class MessageStickerCreate(BaseModel):
    author: MessageAuthor
    text: str
