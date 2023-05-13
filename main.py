from datetime import datetime
from enum import Enum
from typing import Dict, Annotated, List, Optional

import fastapi
import jwt
import uvicorn
from fastapi import Body, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

# from db_initializer import get_async_session
from db_initializer import get_db
from models import models as user_model
# from models import users as link_model
# from models import video as place_model
from schemas.users import CreateUserSchema, UserSchema, UserLoginSchema
from services.db import users as user_db_services
from services.files import save_file_user
from settings import SECRET_KEY

from video.router import router as router_video
from user.router import router as router_user
from pages.router import router as router_pages

app = fastapi.FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_video)
app.include_router(router_user)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
