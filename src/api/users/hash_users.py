from datetime import timedelta

from src.config import get_auth_data
from passlib.context import CryptContext
from src.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# для получения подобной строки, выполните: $ openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
# алгоритм, используемый для подписи JWT-токена
ALGORITHM = settings.ALGORITHM
# срок действия токена JWT-токена
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_T = OAuth2PasswordBearer(tokenUrl="token")



#Создание JWT токена
def create_access_token(data: dict):
    # Настройки авторизации
    auth_data = {
        "SECRET_KEY": "your-secret-key",
        "ALGORITHM": "HS256"
    }

    # Проверка наличия ключей
    if "SECRET_KEY" not in auth_data or "ALGORITHM" not in auth_data:
        raise KeyError("Загрузка .env данных произведена неудачно")

    # Добавление времени истечения токена
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    # Создание токена
    encode_jwt = jwt.encode(to_encode, auth_data["SECRET_KEY"], algorithm=auth_data["ALGORITHM"])
    return encode_jwt



#Хэширование пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#Проверка хэшированного пароля и пароля без хэширования
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_T)):
    """!!!
        Сделать после проекта, дополнительную проверку поиска полученного
        из токена пользователя на поиск такого пользователя в БД
        !!!
    """
    try:
        decode_user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str  = decode_user.get('sub')
        if user is None:
            raise HTTPException(status_code=401, detail="Токен не существует")
        token_data = {'user': user}
    except JWTError:
        HTTPException(status_code=401, detail="Токен неверный")

    return {'user': user}

















#
# def get_user(db, username: str):
#     """Функция получения данных о пользователе из БД"""
#
#     if username in db:
#         # если в БД есть пользователь с таким именем
#         # извлекаем данные о пользователе
#         user_dict = db[username]
#         # возвращаем модель пользователя с хэшем пароля
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     """Функция для проверки подлинности и возврата пользователя"""
#
#     user = get_user(fake_db, username)
#     # проверяем, получены ли данные пользователя
#     if not user:
#         return False
#     # проверяем соответствие пароля и хэша пароля из базы данных
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     """Функция для генерации нового токена
#         timedelta - используется .env для определения ACCESS_TOKEN_EXPIRE_MINUTES,
#         а именно сколько минут будет длиться этот токен.
#         timezone - используется для определения длительности токена в определенном
#         часовом поясе.
#         :)
#     """
#
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=30)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt