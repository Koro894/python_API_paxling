# from src.api.dependences import SessionDep
# from src.api.schemas.shablon import BookModel

from fastapi import APIRouter
from sqlalchemy.testing.suite.test_reflection import users

from starlette.responses import RedirectResponse, JSONResponse

from src.api.modals.inst_class import PasswodModel
from src.api.modals.shablon import BookID, BookUserRegustration, Users_ID
from src.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
# 'CryptContext' - это то, что будет использоваться для хэширования и проверки паролей.
from passlib.context import CryptContext
from src.api.db.dependences import SessionDep
from src.api.users.hash_users import create_access_token
from typing import Dict



router = APIRouter(
    prefix="/users",
    tags=["Добавление и удаление пользователей"]
)

# для получения подобной строки, выполните: $ openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
# алгоритм, используемый для подписи JWT-токена
ALGORITHM = settings.ALGORITHM
# срок действия токена JWT-токена
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES



#  функция для хэширования пароля, поступающего от пользователя.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# `oauth2_scheme` является "вызываемой" и следовательно ее можно
# использовать в зависимости `fastapi.Depends` в функции `get_current_user()`
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# создаем экземпляр приложения

@router.delete(
    "/delete_user",
    description="Удаление пользователя из БД",
    response_model=Dict
)

@router.post(
    "/sign_regustrat",
    response_model=Users_ID,
    summary="Регистрация нового пользователя"
)
async def sign_regustrat(data: BookUserRegustration, session: SessionDep):
    check_user = await session.execute(select(PasswodModel).where(PasswodModel.user == data.user))

    user_uskl = check_user.scalars().first()

    # user_uskl = check_user.scalar_one_or_none()
    if user_uskl:
        RedirectResponse('/notfind_user', status_code=status.HTTP_423_LOCKED)


    user_data = PasswodModel(**data.model_dump())
    session.add(user_data)
    await session.commit()
    await session.refresh(user_data)
    access_token = create_access_token(data={"exp": data.user})
    return {"access_token": access_token, "id": user_data.id}
    # return {'token': create_access_token({'user': data.user, 'passwode': data.passwode})
#

@router.get(
    '/notfind_user',
    status_code=status.HTTP_404_NOT_FOUND
)
async def not_find():
    return {'message': 'Пользователь отсутвует!'}

@router.get(
    '/notfind_user',
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
)
async def not_find_server():
    return {'message': "Ошибка сервера, попробуйте обратиться в поддержку или подождать некоторое время"}

@router.get(
    '/notfind_user',
    status_code=status.HTTP_423_LOCKED
)
async def not_find_():
    return {'message': "Такой пользователь уже существует, измените свой логин"}

@router.get(
    '/regustr_user',
        status_code=status.HTTP_200_OK
)
async def regustr_user():
    return {'message': "Регистрация успешна прошла!"}


@router.post(
    "/get_token",
    description="Аутентифицирование пользователя и возвращение токена.",
)
async def get_token(data: BookUserRegustration, session: Session = Depends(SessionDep)):
    result = await session.execute(select(PasswodModel).where(PasswodModel.passwode == data.passwode & PasswodModel.user == data.user))
    userDB = result.scalar()

    if not userDB:
        raise HTTPException(status_code=401, detail="Пользователь уже существует")


    return JSONResponse(
        content={"exp": create_access_token(data={'sub': data.user})},
        status_code=200
    )





#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     """Получение текущего пользователя из токена"""
#
#     # создадим исключение, которое будем возвращать, если токен недействителен
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try: # расшифруем и проверим полученный токен
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # вернем пользователя, зашитого в ключе
#         username: str = payload.get("sub")
#         if username is None:
#             # нет пользователя, отдаем HTTP-ошибку.
#             raise credentials_exception
#         # сериализуем имя пользователя моделью Pydantic
#         token_data = TokenData(username=username)
#     except JWSDecodeError:
#         # если токен недействителен, отдадим HTTP-ошибку.
#         raise credentials_exception
#     # пытаемся получить данные пользователя из базы
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         # нет пользователя, отдаем HTTP-ошибку.
#         raise credentials_exception
#     return user

#
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     """Проверяет запись пользователя по полю `disabled`"""
#
#     if current_user.disabled:
#         # если пользователь отключен, то => HTTP=ошибка
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @router.post("/token")
# async def login_for_access_token(
#     # аннотируем данные формы авторизации
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     """Функция авторизации пользователя. В случае успеха возвращает токен доступа"""
#
#     # проходим проверку подлинности
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         # не прошли проверку, отдаем HTTP-ошибку
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # устанавливаем время жизни токена
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # генерируем токен доступа
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")

#
# @router.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     """Получение своих данных (авторизированного пользователя)"""
#     return current_user
#
#
# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     """Получение какой-то записи"""
#     return [{"item_id": "Foo", "owner": current_user.username}]
#
# # система безопасности приложения
# security = HTTPBasic()

# def get_current_username(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
# ):
#     """Проверка подлинности пользователя (зависит от `security`)"""
#
#     # получаем имя пользователя из формы авторизации
#     current_username_bytes = credentials.username.encode("utf8")
#     # имя пользователя, например, полученное из базы данных
#     correct_username_bytes = b"stanleyjobson"
#     # проверяем корректность переданного имени пользователя
#     is_correct_username = secrets.compare_digest(
#         current_username_bytes, correct_username_bytes
#     )
#     # получаем пароль пользователя из формы авторизации
#     current_password_bytes = credentials.password.encode("utf8")
#     # пароль пользователя, например, полученное из базы данных
#     correct_password_bytes = b"swordfish"
#     # проверяем корректность переданного пароля пользователя
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not (is_correct_username and is_correct_password):
#         # если что-то не понравилось, отправляем ошибку авторизации
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

#
# @router.get("/users/me")
# # функции обработки пути делаем зависимыми от `get_current_username()`
# def read_current_user(username: Annotated[str, Depends(get_current_username)]):
#     return {"username": username}