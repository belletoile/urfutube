from datetime import datetime

import bcrypt
import jwt
from sqlalchemy import (
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import  relationship

import settings
from db_initializer import Base


class VideoLike(Base):
    """Models a tags table"""
    __tablename__ = "videolike"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("video.id"))


class VideoDislike(Base):
    """Models a tags table"""
    __tablename__ = "videodislike"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("video.id"))


class Video(Base):
    """Models a videp table"""
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    count_like = Column(Integer)
    like = relationship('User', secondary="videolike", back_populates='user_like')
    dislike = relationship('User', secondary="videodislike", back_populates='user_dislike')
    url = Column(String)


class User(Base):
    """Models a user table"""
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    email = Column(String)
    hashed_password = Column(LargeBinary, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    photo_user = Column(String)
    user_like = relationship('Video', secondary="videolike", back_populates='like', cascade='all, delete')
    user_dislike = relationship('Video', secondary="videodislike", back_populates='dislike', cascade='all, delete')

    UniqueConstraint("phone", name="uq_user_phone")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {name!r}>".format(name=self.name)

    @staticmethod
    def hash_password(password) -> bytes:
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        """Confirms password validity"""
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"name": self.name, "phone": self.phone, "id": self.id},
                settings.SECRET_KEY, algorithm="HS256"
            )
        }
