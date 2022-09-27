from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth_token, vote
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

#models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth_token.router)
app.include_router(vote.router)
