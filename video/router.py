from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, UploadFile, File, HTTPException, status

from models.models import Video, User, VideoLike, VideoDislike

from db_initializer import get_db
from schemas.video import VideoBaseSchema, VideoLikeSchema
from services.files import save_video
from services.db import users as user_db_services

import settings

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/upload_video')
def upload(token: Annotated[str, Depends(oauth2_scheme)], payload: VideoBaseSchema = Body(),
           session: Session = Depends(get_db),
           file: UploadFile = File(...),
           ):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        file_url = save_video(file)
        payload.url = file_url
        payload.count_like = 0
        payload.user_id = data["id"]
        stmt = session.query(User).get(data["id"])
        payload.username = stmt.surname
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    return user_db_services.create_video(session, video=payload)


@router.post('/add_like')
def like(token: Annotated[str, Depends(oauth2_scheme)], payload: VideoLikeSchema = Body(),
         session: Session = Depends(get_db)):
    stmt = session.query(Video).get(int(payload.video_id))
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    like = session.query(User).filter_by(id=int(data["id"])).first()
    q = session.query(VideoLike).filter_by(user_id=data["id"], video_id=int(payload.video_id))
    d = session.query(VideoDislike).filter_by(user_id=data["id"], video_id=int(payload.video_id))
    if session.query(d.exists()).scalar():
        session.query(VideoDislike).filter_by(user_id=data["id"], video_id=int(payload.video_id)).delete()
    if session.query(q.exists()).scalar():
        session.query(VideoLike).filter_by(user_id=data["id"], video_id=int(payload.video_id)).delete()
        stmt.count_like = stmt.count_like - 1
        if stmt.count_like < 0:
            stmt.count_like = 0
        session.commit()
    else:
        stmt.like.append(like)
        session.add(stmt)
        stmt.count_like = stmt.count_like + 1
        session.commit()
    return {'Status: 200'}


@router.post('/add_dislike')
def dislike(token: Annotated[str, Depends(oauth2_scheme)], payload: VideoLikeSchema = Body(),
            session: Session = Depends(get_db)):
    stmt = session.query(Video).get(payload.video_id)
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    dislike = session.query(User).filter_by(id=int(data["id"])).first()
    q = session.query(VideoDislike).filter_by(user_id=data["id"], video_id=int(payload.video_id))
    d = session.query(VideoLike).filter_by(user_id=data["id"], video_id=int(payload.video_id))
    if session.query(d.exists()).scalar():
        session.query(VideoLike).filter_by(user_id=data["id"], video_id=int(payload.video_id)).delete()
        session.commit()
    if session.query(q.exists()).scalar():
        session.query(VideoDislike).filter_by(user_id=data["id"], video_id=int(payload.video_id)).delete()
        session.commit()
    else:
        stmt.dislike.append(dislike)
        stmt.count_like = stmt.count_like - 1
        if stmt.count_like < 0:
            stmt.count_like = 0
        session.add(stmt)
        session.commit()
    return {'200'}


@router.get('/list')
def get_video(session: Session = Depends(get_db)):
    return session.query(Video).all()


@router.get('/list_id')
def get_video_id(id: int, session: Session = Depends(get_db)):
    result = session.query(Video).filter(Video.id == id)
    return result.all()


@router.get('/my_video')
def get_my_video(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(Video).filter_by(user_id=str(data['id']))
    return stmt.all()


@router.delete('/delete_video')
def delete_my_video(token: Annotated[str, Depends(oauth2_scheme)], id_video: int,
                    session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    video = session.query(Video).filter_by(id=id_video).first()
    session.delete(video)
    session.commit()
    return {'Ok'}
