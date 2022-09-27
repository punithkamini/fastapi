from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas,models, jwt_token
from sqlalchemy.orm import Session
from ..database import get_db
router = APIRouter()

@router.post("/vote")
def create_vote(votes: schemas.Votes, db: Session =  Depends(get_db), current_user: schemas.ShowUser = Depends(jwt_token.get_current_user)):

    post=db.query(models.Posts).filter(models.Posts.id == votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {votes.post_id} not found")

    vote=db.query(models.Votes).filter(models.Votes.post_id == votes.post_id, models.Votes.user_id==current_user.id)
    if int(votes.dir) == 1:
        if vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already voted the post")
        new_vote=models.Votes(post_id=votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    else:
        if not vote.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found")

        vote.delete()
        db.commit()
        return "deleted the vote"