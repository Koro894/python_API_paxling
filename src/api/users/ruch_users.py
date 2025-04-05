from src.api.dependences import SessionDep
from src.api.schemas.shablon import BookModel
#Нейросеть !!!
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["Добавление и удаление пользователей"]
)


#Авторизация пользователя
# @router.post('/login')
#Нейросеть !!!
# async def login(data: BookModel, session: AsyncSession = Depends(SessionDep)):
#     # 1. Поиск пользователя в базе данных
#     user = await session.execute(
#         select(User).where(User.username == data.user)
#     )
#     user = user.scalar_one_or_none()
#
#     # 2. Проверка существования пользователя
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Пользователь не найден"
#         )
# 
#     # 3. Проверка пароля с использованием bcrypt
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     if not pwd_context.verify(data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Неверный пароль"
#         )
#
#     # 4. Генерация JWT токена
#     token_data = {"sub": str(user.id), "username": user.username}
#     access_token = security.create_access_token(token_data)
#
#     return {"access_token": access_token, "token_type": "bearer"}
# async def login(data: BookModel, session: SessionDep):
#     if data.user == "test" and data.password == "test":
#         token = security.create_access_token(uid='12345')
#         return {"acces_token": token}
#     raise HTTPException(status_code=401, detail="Неправильный логин или пароль")


#Получение данных по токену пользователя
@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "TOP SECRET"}


@router.post("/passwod")
async def create_passwod(data: BookModel, session: SessionDep):
    new_book = BookModel(
        user=data.user,
        passwode=data.passwode,
    )
    session.add(new_book)
    await session.commit()
    return {'ok': True}

@router.get("/passwod")
async def read_passwod():
    pass
#
# @app.get("/password/{user_id}")
# async def read_password(user_id: int, session: MainDBSession):
#     result = await session.get(PasswordModel, user_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="User not found")
#     return result
