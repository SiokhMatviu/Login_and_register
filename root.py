from fastapi import APIRouter
router = APIRouter(prefix="/", tags=["root"])

@router.get("")
def root():
    return {"status": "ok", "message": "API is running"}