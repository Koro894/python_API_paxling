from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class BookModel(BaseModel):
    id: int
    user: str = Field(min_length=5, max_length=40)
    passwode: str = Field(min_length=5, max_length=80)
    email: EmailStr | None = None
    phone_number: str | None = None
    description: str | None = Field(min_length=0, max_length=1000)
    _
    _right_write_text: bool
    _right_write_comments: bool

    #Запрет на дополнительные параметры
    model_config = ConfigDict(extra='forbid')

class BookShema(BookModel):
    id: int

    # Запрет на дополнительные параметры
    model_config = ConfigDict(extra='forbid')

class BookText(BaseModel):
    user: str 
    text: str
    title_text: str

    # Запрет на дополнительные параметры
    model_config = ConfigDict(extra='forbid')

class  BookID(BookText):
    id: int
    created_at: datetime

    # Запрет на дополнительные параметры
    model_config = ConfigDict(extra='forbid')