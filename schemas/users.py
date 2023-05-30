from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    phone: str
    email: EmailStr
    name: str
    surname: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    phone: str = Field(alias="phone")
    password: str
