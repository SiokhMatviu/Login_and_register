from typing import Annotated
from annotated_types import  MinLen
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class UserSchemaId(UserSchema):
    id: int