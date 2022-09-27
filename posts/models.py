from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published=Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id= Column(Integer, ForeignKey('users.id'), nullable=False)

    owner=relationship("Users", back_populates="post")

class Users(Base):
    __tablename__='users'

    id = Column(Integer, primary_key=True, index= True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    post=relationship("Posts", back_populates="owner")


class Votes(Base):
    __tablename__="votes"

    user_id=Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    post_id=Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)

