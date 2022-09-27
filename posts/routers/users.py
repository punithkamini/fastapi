from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, hashing, jwt_token
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(tags=['Users'])


@router.get("/users", response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    all_users=db.query(models.Users).all()
    return all_users


@router.get("/users/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    users=db.query(models.Users).filter(models.Users.id == id)
    if not users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return users.first()


@router.post("/users", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.password=hashing.Hash.bcrypt(user.password)
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
