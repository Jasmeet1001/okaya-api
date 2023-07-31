from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = '0d1467ac6dc1ec97ae9da8b5b392da657934d1864e5d7621d0fc0e890efd28cd'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)