from typing import Optional, Dict, Annotated

import jwt
from fastapi import APIRouter,BackgroundTasks, UploadFile, File, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import update

import settings
from db_initializer import get_db
from models import models as user_model
from models.models import User, VideoLike, Video
from schemas.users import UserSchema, UserBaseSchema, CreateUserSchema
from services.files import save_file_user
from services.db import users as user_db_services
from tasks.tasks import send_email

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/signup', response_model=UserSchema)
def signup(
        background_tasks: BackgroundTasks,
        payload: CreateUserSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    background_tasks.add_task(send_email, payload)
    return user_db_services.create_user(session, user=payload)


@router.post('/login', response_model=Dict)
def login(payload: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_db)
          ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email,
                phone number, name

    - password:
    """
    try:
        user: user_model.User = user_db_services.get_user(
            session=session, phone=payload.username
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


@router.post('/favorite_video')
def fav_video(id_user: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    return session.query(VideoLike).filter(VideoLike.user_id == id_user).all()


@router.post('/my_video')
def my_video(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return session.query(Video).filter(Video.user_id == str(data['id'])).all()