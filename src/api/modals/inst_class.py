from email.policy import default

from sqlalchemy import text
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.api.texts.ruch_text import text_get
from src.database import Base, Base_Text_Rear, Base_History_Rear, Base_Grammar_Rear


class PasswodModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user: Mapped[str]
    #ТОКЕН JWT
    passwode: Mapped[str]
    email: Mapped[EmailStr | None]
    phone_number: Mapped[str | None]
    description: Mapped[str | None]

# nullable - указывает на то, что поле не может быть пустым
    _is_redovui: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    _is_researcher: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_alchemist: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_scientist: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_wandering_scientist: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_philosopher: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_doctor_of_sciences = Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_wanderer_IT: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_doctor_IT: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _is_shadow_site: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    _ban: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _right_write_text: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    _right_write_comments: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)

"""
    level_aura - уровень пользователя.
    Будет 12 уровней.
    1 - Рядовой
    2 - Исследователь
    3 - Алхимик
    4 - Учёный
    5 - Странствующий Учёный
    6 - Философ
    7 - Доктор наук
    8 - Странник IT
    9 - Доктор IT
    10 -Тень сайта
"""
"""

"""




class PasswodMod_TextRead(Base_Text_Rear):
    __tablename__ = "text_read"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str]
    title_text: Mapped[str]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    #like_post - экспериментальная. Используется для предоставления данных о поставленных лайках
    like_post: Mapped[int]

class PasswodMod_HistoryRead(Base_History_Rear):
    __tablename__ = "history_read"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str]
    title_text: Mapped[str]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    like_post: Mapped[int]

class PasswodMod_GrammarRead(Base_Grammar_Rear):
    __tablename__ = "grammar_read"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str]
    title_text: Mapped[str]
    text: Mapped[str]
    like_post: Mapped[int]
