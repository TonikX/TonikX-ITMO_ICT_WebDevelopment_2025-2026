# Дополнительное задание

## Задание

Задание на 15 Баллов (можно реализовывать сразу): Необходимо реализовать функционал пользователя в разрабатываемом 
приложении. Функционал включает в себя:

* Авторизацию и регистрацию
* Генерацию JWT-токенов
* Аутентификацию по JWT-токену
* Хэширование паролей
* Дополнительные АПИ-методы для получения информации о пользователе, списка пользователей и смене пароля

## Установка зависимостей

Для работы с JWT-токенами и хэширования пороля были установлены библиотеки: `pyJWT`, `passlib`, `bcrypt=4.0.1`

## Логика работы с JWT

Для работы с JWT-токенами был реализован класс с методами, которые работают с токенами:

```python
import datetime

from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from sqlmodel import Session

from connection import get_session
from repos.user import UsersRepository


class AuthManager:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'ksdjbejgiwgwg'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, email):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired token')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security),
                         session: Session=Depends(get_session)):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credential'
        )
        email = self.decode_token(auth.credentials)
        if email is None:
            raise credential_exception

        user = UsersRepository(session).get_by_email(email)
        if user is None:
            raise credential_exception

        return user
```

## Изменение эндпоинтов

После реализации сервиса по работе с токенами в эндпоинты, где необходима авторизация была добавлена строка 
`user: User=Depends(auth_manager.get_current_user)`, что позволяет получать пользователя из отправленного токена,
а если его нет, то вернется 401 ошибка UNAUTHORIZED. Логика проверки, что пользователь имеет доступ к ресурсам, 
выполняется в сервисах.
