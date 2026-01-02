from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import new_session, UserOrm
from schemas import UserSchema
from passlib.context import CryptContext
from security import hash_password
from sqlalchemy import select


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


class UserRepository:
    @classmethod
    async def register(cls, data: UserSchema) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()

            user_dict["password"] = hash_password(
                user_dict["password"]
            )


            try:
                task = UserOrm(**user_dict)
                session.add(task)
                await session.flush()
                await session.commit()
                return task.id

            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )


    @staticmethod
    async def get_by_email(email: str):
        async with new_session() as session:
            result = await session.execute(
                select(UserOrm).where(UserOrm.email == email)
            )
            return result.scalar_one_or_none()