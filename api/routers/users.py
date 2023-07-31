from .. import schemas, models, utils
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db

router = APIRouter()

@router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hased_password = utils.hash_it(user.password)
    user.password = hased_password
    new_user = models.Users(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/users/{user_id}/')
def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.Users, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} does not exist")
    
    return user