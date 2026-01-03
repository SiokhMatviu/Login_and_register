from fastapi import APIRouter, HTTPException, Response, Depends, status
from typing import Annotated
from repository import UserRepository
from schemas import UserSchema
from security import verify_password
from tokens import security, config


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/login")
async def login(data: Annotated[UserSchema, Depends()], response: Response,
):

    user = await UserRepository.get_by_email(data.email)


    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    token = security.create_access_token(
        uid=str(data)
    )
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, )

    return {"ok": token}