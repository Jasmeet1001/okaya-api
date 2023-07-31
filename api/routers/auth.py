from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, oauth2, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    get_user = db.scalars(select(models.Users).where(models.Users.email == user_cred.username).limit(1)).first()

    if not (get_user and utils.validate(user_cred.password, get_user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = oauth2.create_token(data={'user_id': get_user.user_id})

    return {'token': access_token, 'token_type': 'bearer'}