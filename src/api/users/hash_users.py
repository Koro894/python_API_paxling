# from jose import jwt
# from datetime import datetime, timedelta, timezone
# from src.config import get_auth_data
# from passlib.context import CryptContext
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
#
# #Создание JWT токена
# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(days=3)
#     to_encode.update({"exp": expire})
#     auth_data = get_auth_data()
#     encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
#     return encode_jwt
#
#
#
# #Хэширование пароля
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)
#
# #Проверка хэшированного пароля и пароля без хэширования
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)