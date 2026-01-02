from fastapi import APIRouter, Depends, Response
from typing import Annotated
from repository import UserRepository
from schemas import UserSchema
from tokens import security, config


router = APIRouter(prefix="/register", tags=["register"])


@router.post("")
async def register_user(
        User: Annotated[UserSchema, Depends()], response: Response,
):
    user = await UserRepository.register(User)
    token = security.create_access_token(
        uid=str(user)
    )
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token,)

    return {"ok": token}