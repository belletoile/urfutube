import json

from pydantic import BaseModel


class VideoBaseSchema(BaseModel):
    name: str
    description: str
    user_id: int = None
    username: str = None
    # like: list
    # dislike: list
    url: str = None
    count_like: int = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class VideoSchema(VideoBaseSchema):
    id: int

    class Config:
        orm_mode = True


class LinkBaseSchema(BaseModel):
    pass


class LinkSchema(LinkBaseSchema):
    id: int

    class Config:
        orm_mode = True


class VideoLikeSchema(BaseModel):
    user_id: int = None
    video_id: str
