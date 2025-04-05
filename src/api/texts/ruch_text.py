from fastapi import APIRouter
from src.api.dependences import SessionDep_Text_in_Read
from src.database import passwod_engine,text_in_read_engine, history_read_engine,  grammar_read_engine, Base, Base_History_Rear, Base_Grammar_Rear, Base_Text_Rear
from src.api.modals.inst_class import PasswodMod_TextRead
from src.api.schemas.shablon import BookText, BookID
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address



limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/text",
    tags=["Добавление и получение большого текста"]
)

router.state.limiter = limiter
router.add_exception_handler(429, _rate_limit_exceeded_handler)

@router.post("/setup_database", summary="Загрузка баз данных")
#Ограничение взаимодействия с этим методом до 5 раз в минуту
@limiter.limit("5/minute")
async def setup_database():
    async with passwod_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with text_in_read_engine.begin() as conn_text_read:
        await conn_text_read.run_sync(Base_Text_Rear.metadata.create_all)

    async with history_read_engine.begin() as conn_history_read:
        await conn_history_read.run_sync(Base_History_Rear.metadata.create_all)

    async with grammar_read_engine.begin() as conn_grammar_read:
        await conn_grammar_read.run_sync(Base_Grammar_Rear.metadata.create_all)

    return {'ok' : True}

@router.post("/text_setup", response_model=BookID, summary="Добавление текста")
async def add_text(data: BookText, session: SessionDep_Text_in_Read):
    new_text = PasswodMod_TextRead(**data.model_dump())
    session.add(new_text)
    await session.commit()
    await session.refresh(new_text)


@router.get("text_get/{user_id}", summary="")
async def text_get(user_id: int, session: SessionDep_Text_in_Read):
    pass


