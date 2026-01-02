from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from database import create_tables, delete_tables
from router.login import router as login_router
from router.register import router as register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(login_router)
app.include_router(register_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# for start print in terminal "python main.py