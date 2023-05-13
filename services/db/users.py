from sqlalchemy.orm import Session
from sqlalchemy import select, String

from models.models import User, Video
from schemas.video import VideoBaseSchema
from schemas.users import CreateUserSchema


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_video(session: Session, video: VideoBaseSchema):
    db_video = Video(**video.dict())
    # for t in like:
    #     like = session.query(User).filter_by(id=t).first()
    #     db_video.like.append(like)
    # for d in dislike:
    #     dislike = session.query(User).filter_by(id=d).first()
    #     db_video.dislike.append(dislike)
    session.add(db_video)
    session.commit()
    # db_video.like
    # db_video.dislike
    session.refresh(db_video)
    return db_video


def get_user(session: Session, phone: str):
    return session.query(User).filter(User.phone == phone).one()


def get_user_by_id(session: Session, id: int):
    return session.query(User).filter(User.id == id).all()
