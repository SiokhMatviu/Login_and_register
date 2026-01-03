from fastapi import APIRouter

from schemas import UserSchema

router = APIRouter(prefix="/", tags=["root"])

@router.get("")
def root():
    return {"status": "ok", "message": "API is running"}