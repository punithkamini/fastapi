from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, jwt_token
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(tags=['Posts'], prefix="/posts")

@router.get("/")
def get_all_posts(db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user), limit: int =10,skip: int =0, search: Optional[str] = ""):
    #all_posts=db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Posts, func.count(models.Votes.post_id).label("vote")).join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user)):
    posts = db.query(models.Posts).filter(models.Posts.id == id)
    votes=db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()
    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if current_user.id != posts.first().owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied!")
    return votes


@router.post("/",  response_model=schemas.ShowPosts, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Posts, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user)):
    new_post=models.Posts(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schemas.Posts, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user)):
    posts=db.query(models.Posts).filter(models.Posts.id == id)
    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if current_user.id != posts.first().owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not allowed to update")
    posts.update(dict(post))
    db.commit()
    return "Updated"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user)):
    posts = db.query(models.Posts).filter(models.Posts.id == id)
    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if current_user.id != posts.first().owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not allowed to delete")
    posts.delete()
    db.commit()
    return "deleted"
