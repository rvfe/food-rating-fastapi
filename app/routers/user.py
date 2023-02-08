from ..database import get_db
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils

router = APIRouter(
    prefix='/usuarios',
    tags=['Usuarios']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserCustom)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserCustom)
def  get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user