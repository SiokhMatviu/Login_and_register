from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from database import create_tables, delete_tables
from login import router as login_router
from register import router as register_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(login_router)
app.include_router(register_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)