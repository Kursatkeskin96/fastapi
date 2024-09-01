from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional
from random import randrange
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import  engine, get_db
from typing import List
from .routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Create the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for your frontend origin
origins = [
    "http://localhost:3000",  # Your frontend URL
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
