import uvicorn
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI, Depends
import jwt

import users
from schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from token_authentication import get_current_user
from utils import JWT_SECRET

app = FastAPI()


# Cadastro de usuário
@app.post('/register/user', response_model=UserSchema)
def register_user(user_in: UserRegisterSchema, request: Request):
    return users.register_user(user_in, request)


# Fazemos o login e retornamos no corpo e cookies o token JWT a ser usado para autenticação.
@app.post('/login/user', response_model=UserSchema)
def login(user_login: UserLoginSchema, response: Response):
    user_model = users.login_user(user_login)
    token_jwt = jwt.encode({'email': user_model.email}, JWT_SECRET, algorithm='HS256')
    response.set_cookie('Authorization', f'Bearer {token_jwt.decode()}')
    return users.login_user(user_login)


@app.get('/user_data', response_model=UserSchema)
def get_user_data(user: UserSchema = Depends(get_current_user)):
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
