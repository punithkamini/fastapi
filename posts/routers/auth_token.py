from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, hashing, jwt_token
from fastapi.security import OAuth2PasswordRequestForm
from .. import jwt_token
from datetime import timedelta

router=APIRouter(tags=['Authentication'], prefix="/token")

@router.post("/", response_model=schemas.Token)
def login(users: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email == users.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not hashing.Hash.verify_password(user.password,users.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    access_token= jwt_token.create_access_token(data={"user_id":user.id, "user_email": user.email}, expires_delta=timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}